# Copyright (c) 2026, Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class NewsletterIssue(Document):
	def validate(self):
		self.validate_layout()

	def validate_layout(self):
		"""Sections unique; every topic row under a section this issue has; topics unique."""
		sections = []
		for row in self.sections:
			if row.section in sections:
				frappe.throw(_("Sections row #{0}: {1} is listed twice.").format(row.idx, frappe.bold(row.section)))
			sections.append(row.section)

		seen_topics = set()
		for row in self.topics:
			if row.section not in sections:
				frappe.throw(
					_("Topics row #{0}: section {1} is not in this issue's Sections table.").format(
						row.idx, frappe.bold(row.section)
					)
				)
			if row.topic in seen_topics:
				frappe.throw(_("Topics row #{0}: {1} is placed twice.").format(row.idx, frappe.bold(row.topic)))
			seen_topics.add(row.topic)
