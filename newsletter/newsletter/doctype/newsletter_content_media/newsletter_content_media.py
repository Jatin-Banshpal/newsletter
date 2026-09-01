# Copyright (c) 2026, Company and contributors
# For license information, please see license.txt

from frappe.model.document import Document

IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "svg", "avif", "tiff", "tif", "heic"}
VIDEO_EXTENSIONS = {"mp4", "mov", "webm", "avi", "mkv", "m4v", "ogv", "3gp"}


def detect_media_type(attachment):
	if not attachment:
		return None
	ext = attachment.rsplit(".", 1)[-1].lower() if "." in attachment else ""
	if ext in IMAGE_EXTENSIONS:
		return "Photo"
	if ext in VIDEO_EXTENSIONS:
		return "Video"
	return "Document"


class NewsletterContentMedia(Document):
	pass
