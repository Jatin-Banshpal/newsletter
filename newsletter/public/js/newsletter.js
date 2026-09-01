// Let "Attach Image" fields accept camera/web formats that browsers report with
// an empty or unusual MIME type. Frappe's control restricts uploads to
// "image/*", and Chrome/Edge on Windows give .heic files an empty `type`, so
// the uploader silently skips them ("File skipped because of invalid file
// type"). Extension entries are matched by name instead, so these get through;
// the server then transcodes them to JPEG/PNG (see newsletter/files.py).
(() => {
	const EXTRA_IMAGE_EXTENSIONS = [
		".heic", ".heif", ".hif", ".avif", ".webp",
		".tif", ".tiff", ".jp2", ".j2k", ".jpx", ".psd", ".bmp", ".gif", ".png", ".jpg", ".jpeg", ".svg",
	];

	const patch = () => {
		const Control = frappe?.ui?.form?.ControlAttachImage;
		if (!Control || Control.__newsletter_formats_patched) return;

		const original = Control.prototype.set_upload_options;
		Control.prototype.set_upload_options = function () {
			original.call(this);
			const restrictions = this.upload_options.restrictions || (this.upload_options.restrictions = {});
			const types = new Set(restrictions.allowed_file_types || []);
			EXTRA_IMAGE_EXTENSIONS.forEach((ext) => types.add(ext));
			restrictions.allowed_file_types = [...types];
		};
		Control.__newsletter_formats_patched = true;
	};

	patch();
	$(document).on("app_ready", patch);
})();
