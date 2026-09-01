"""Universal image-format support for uploads.

Why this exists
---------------
Frappe happily *stores* any file extension (System Settings' allow-list is
blank on this site), but two things still break for modern camera/web
formats:

1. Browsers (Chrome/Edge/Firefox) and wkhtmltopdf cannot display HEIC/HEIF
   (iPhone default), TIFF, JPEG-2000 or PSD at all; wkhtmltopdf additionally
   cannot render WebP or AVIF, so those vanish from the newsletter PDF.
2. Frappe's own image pipeline (Pillow) cannot even open HEIC without the
   pillow-heif plugin, so thumbnails/optimisation fail.

Fix: register the extra Pillow codecs, and transcode hostile formats to JPEG
(or PNG when the image has transparency) at upload time, via Frappe's
`write_file` hook - which runs after all validation but *before* the bytes are
written to disk, so the File record, the returned file_url and the attached
field all simply see a .jpg/.png. Nothing else in the system has to know.
"""

import io
import os

import frappe
from frappe import _

# Extensions that get transcoded on upload. BMP/GIF/PNG/JPEG/SVG are left alone
# (every renderer handles them). Remove an entry here to keep that format as-is.
CONVERT_EXTENSIONS = {"heic", "heif", "hif", "avif", "webp", "tif", "tiff", "jp2", "j2k", "jpx", "psd"}

JPEG_QUALITY = 90


def register_openers():
	"""Teach Pillow to open HEIC/HEIF (and AVIF on Pillow builds without it). Idempotent."""
	try:
		import pillow_heif

		pillow_heif.register_heif_opener()
		if hasattr(pillow_heif, "register_avif_opener"):
			from PIL import features

			if not features.check("avif"):
				pillow_heif.register_avif_opener()
	except ImportError:
		pass


def _extension(file_name):
	return file_name.rsplit(".", 1)[-1].lower() if file_name and "." in file_name else ""


def transcode_image(content: bytes, file_name: str):
	"""Return (bytes, new_file_name, content_type) for a hostile-format image, else None."""
	if _extension(file_name) not in CONVERT_EXTENSIONS or not content:
		return None

	register_openers()
	from PIL import Image, ImageOps

	try:
		image = Image.open(io.BytesIO(content))
		image.load()
	except Exception:
		# Not a decodable image (or a codec we still lack) - store untouched.
		return None

	# Apply camera orientation so the pixels are upright without relying on EXIF.
	image = ImageOps.exif_transpose(image) or image

	has_alpha = image.mode in ("RGBA", "LA", "PA") or (image.mode == "P" and "transparency" in image.info)
	stem = file_name.rsplit(".", 1)[0]
	out = io.BytesIO()
	if has_alpha:
		image.convert("RGBA").save(out, "PNG", optimize=True)
		return out.getvalue(), f"{stem}.png", "image/png"

	image.convert("RGB").save(out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
	return out.getvalue(), f"{stem}.jpg", "image/jpeg"


def write_file(file):
	"""Frappe `write_file` hook (see frappe/core/doctype/file/file.py::save_file)."""
	from frappe.core.doctype.file.utils import get_content_hash

	if not file.is_remote_file and file._content and not file.flags.skip_image_transcode:
		result = transcode_image(file._content, file.file_name)
		if result:
			content, new_name, content_type = result
			original_name = file.file_name
			file._content = content
			file.file_name = new_name
			file.content_type = content_type
			file.file_size = len(content)
			file.content_hash = get_content_hash(content)
			if hasattr(file, "set_file_type"):
				file.set_file_type()
			file.flags.transcoded_from = original_name
			frappe.msgprint(
				_("{0} was converted to {1} so it displays in browsers and PDFs.").format(
					frappe.bold(original_name), _extension(new_name).upper()
				),
				alert=True,
				indicator="blue",
			)

	return file.save_file_on_filesystem()


def convert_existing_files(dry_run=False):
	"""One-off: transcode already-uploaded hostile-format images in place.

	Run with: bench --site <site> execute newsletter.files.convert_existing_files
	Updates the File record (name/url/hash/size), rewrites the field on the
	document it is attached to (if any), and removes the old file from disk.
	"""
	from frappe.core.doctype.file.utils import get_content_hash

	pattern = "|".join(sorted(CONVERT_EXTENSIONS))
	files = frappe.db.sql(
		f"""select name from tabFile where is_folder=0 and lower(file_name) regexp '\\\\.({pattern})$'""",
		pluck="name",
	)
	converted = 0
	for name in files:
		doc = frappe.get_doc("File", name)
		if doc.is_remote_file or not doc.exists_on_disk():
			continue
		result = transcode_image(doc.get_content(), doc.file_name)
		if not result:
			continue
		content, new_name, content_type = result
		old_path, old_url = doc.get_full_path(), doc.file_url
		print(f"{'would convert' if dry_run else 'converting'} {doc.file_name} -> {new_name}")
		if dry_run:
			continue

		new_path = os.path.join(os.path.dirname(old_path), new_name)
		with open(new_path, "wb") as f:
			f.write(content)
		new_url = old_url.rsplit("/", 1)[0] + "/" + new_name

		frappe.db.set_value(
			"File",
			name,
			{
				"file_name": new_name,
				"file_url": new_url,
				"content_hash": get_content_hash(content),
				"file_size": len(content),
				"content_type": content_type,
			},
			update_modified=False,
		)
		if doc.attached_to_doctype and doc.attached_to_name and doc.attached_to_field:
			if frappe.db.get_value(doc.attached_to_doctype, doc.attached_to_name, doc.attached_to_field) == old_url:
				frappe.db.set_value(doc.attached_to_doctype, doc.attached_to_name, doc.attached_to_field, new_url)
		# Child-table references (e.g. Newsletter Topic Media.attachment) don't carry attached_to_field.
		for row in frappe.get_all("Newsletter Topic Media", filters={"attachment": old_url}, pluck="name"):
			frappe.db.set_value("Newsletter Topic Media", row, "attachment", new_url, update_modified=False)

		if os.path.exists(old_path) and old_path != new_path:
			os.remove(old_path)
		converted += 1

	frappe.db.commit()
	print(f"{converted} file(s) converted out of {len(files)} candidate(s).")
