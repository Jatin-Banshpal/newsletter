// Copyright (c) 2026, Company and contributors
// For license information, please see license.txt

const CONTENT_API = "newsletter.newsletter.doctype.newsletter_content.newsletter_content";

frappe.ui.form.on("Newsletter Content", {
	setup(frm) {
		// Offer only the topics that the chosen issue has placed in its layout.
		frm.set_query("topic", () => ({
			query: `${CONTENT_API}.topics_for_issue`,
			filters: { newsletter_issue: frm.doc.newsletter_issue },
		}));
	},

	onload(frm) {
		if (frm.is_new() && !frm.doc.newsletter_issue) {
			frappe.xcall(`${CONTENT_API}.get_default_issue`).then((issue) => {
				if (issue) frm.set_value("newsletter_issue", issue);
			});
		}
	},

	newsletter_issue(frm) {
		if (frm.doc.topic) frm.set_value("topic", null);
		frm.set_value("section", null);
	},

	topic(frm) {
		// Show the section straight away; the server re-derives it on save anyway.
		if (!(frm.doc.newsletter_issue && frm.doc.topic)) {
			frm.set_value("section", null);
			return;
		}
		frappe.db
			.get_value("Newsletter Issue Topic", { parent: frm.doc.newsletter_issue, topic: frm.doc.topic }, "section")
			.then((r) => frm.set_value("section", (r.message && r.message.section) || null));
	},
});
