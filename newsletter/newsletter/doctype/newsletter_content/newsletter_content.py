# Copyright (c) 2026, Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from newsletter.newsletter.doctype.newsletter_content_media.newsletter_content_media import (
	detect_media_type,
)


class NewsletterContent(Document):
	def validate(self):
		for row in self.media:
			row.media_type = detect_media_type(row.attachment)
		self.set_section_from_issue()
		self.resolve_sort_order()

	def resolve_sort_order(self):
		"""Keep Sort Order unique among contents of the same issue + topic.

		Blank gets the next free number. Picking a number another content holds
		swaps the two: the other content takes this one's previous number. A new
		content (nothing to give back) is bumped to the next free number instead.
		"""
		if not (self.newsletter_issue and self.topic):
			return

		siblings = frappe.get_all(
			"Newsletter Content",
			filters={
				"newsletter_issue": self.newsletter_issue,
				"topic": self.topic,
				"name": ["!=", self.name or ""],
			},
			fields=["name", "title", "sort_order"],
		)
		used = {s.sort_order for s in siblings}
		next_free = 1
		while next_free in used:
			next_free += 1

		self.sort_order = frappe.utils.cint(self.sort_order)
		if self.sort_order < 1:
			self.sort_order = next_free
			return

		clash = next((s for s in siblings if s.sort_order == self.sort_order), None)
		if not clash:
			return

		before = self.get_doc_before_save()
		previous = 0
		if (
			before
			and before.newsletter_issue == self.newsletter_issue
			and before.topic == self.topic
		):
			previous = frappe.utils.cint(before.sort_order)

		if previous >= 1 and previous != self.sort_order and previous not in used:
			frappe.db.set_value("Newsletter Content", clash.name, "sort_order", previous)
			frappe.msgprint(
				_("Sort Orders swapped: {0} moved to {1}.").format(
					frappe.bold(clash.title), frappe.bold(previous)
				),
				title=_("Sort Order Swapped"),
				indicator="green",
			)
		else:
			taken = self.sort_order
			self.sort_order = next_free
			frappe.msgprint(
				_("Sort Order {0} is already taken by {1} in this topic. Assigned {2} instead.").format(
					frappe.bold(taken), frappe.bold(clash.title), frappe.bold(next_free)
				),
				title=_("Sort Order Adjusted"),
				indicator="orange",
			)

	def set_section_from_issue(self):
		"""The section is wherever this topic sits in this issue's layout."""
		if not (self.newsletter_issue and self.topic):
			self.section = None
			return
		section = frappe.db.get_value(
			"Newsletter Issue Topic", {"parent": self.newsletter_issue, "topic": self.topic}, "section"
		)
		if not section:
			frappe.throw(
				_("Topic {0} is not placed in {1}. Add it to the issue's Topics table first.").format(
					frappe.bold(self.topic), frappe.bold(self.newsletter_issue)
				),
				title=_("Topic not in this issue"),
			)
		self.section = section


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def topics_for_issue(doctype, txt, searchfield, start, page_len, filters):
	"""Link-field query: only topics placed in the given issue, in layout order, with their section."""
	issue = (filters or {}).get("newsletter_issue")
	if not issue:
		return []
	return frappe.db.sql(
		"""
		select t.topic, t.section
		from `tabNewsletter Issue Topic` t
		where t.parent = %(issue)s and t.topic like %(txt)s
		order by t.idx
		limit %(page_len)s offset %(start)s
		""",
		{"issue": issue, "txt": f"%{txt}%", "page_len": page_len, "start": start},
	)


@frappe.whitelist()
def get_default_issue():
	"""Most recent issue still being assembled - the sensible default for new content."""
	rows = frappe.get_all(
		"Newsletter Issue",
		filters={"status": ["!=", "Published"]},
		order_by="publish_date desc, creation desc",
		limit=1,
		pluck="name",
	)
	return rows[0] if rows else None
