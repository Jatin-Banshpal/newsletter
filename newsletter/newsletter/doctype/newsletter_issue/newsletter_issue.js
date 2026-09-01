// Copyright (c) 2026, Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("Newsletter Issue", {
	setup(frm) {
		// A topic row may only use a section this issue actually has.
		frm.set_query("section", "topics", () => ({
			filters: { name: ["in", (frm.doc.sections || []).map((r) => r.section)] },
		}));
	},

	refresh(frm) {
		frm.add_custom_button(__("Copy Layout From..."), () => copy_layout_from(frm));
	},
});

function copy_layout_from(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __("Copy Layout From Another Issue"),
		fields: [
			{
				fieldname: "source",
				fieldtype: "Link",
				label: __("Issue"),
				options: "Newsletter Issue",
				reqd: 1,
				get_query: () => ({ filters: { name: ["!=", frm.doc.name || ""] } }),
			},
			{
				fieldname: "note",
				fieldtype: "HTML",
				options: `<p class="text-muted small">${__(
					"Adds that issue's sections and topic placements (order, highlight, style overrides) after any you already have. Written content is never copied."
				)}</p>`,
			},
		],
		primary_action_label: __("Copy"),
		primary_action({ source }) {
			frappe.db.get_doc("Newsletter Issue", source).then((doc) => {
				const have_sections = new Set((frm.doc.sections || []).map((r) => r.section));
				const have_topics = new Set((frm.doc.topics || []).map((r) => r.topic));
				let sections = 0;
				let topics = 0;
				(doc.sections || []).forEach((row) => {
					if (have_sections.has(row.section)) return;
					frm.add_child("sections", { section: row.section, highlight: row.highlight, style: row.style });
					have_sections.add(row.section);
					sections += 1;
				});
				(doc.topics || []).forEach((row) => {
					if (have_topics.has(row.topic)) return;
					frm.add_child("topics", { topic: row.topic, section: row.section });
					have_topics.add(row.topic);
					topics += 1;
				});
				frm.refresh_field("sections");
				frm.refresh_field("topics");
				frm.dirty();
				dialog.hide();
				frappe.show_alert({
					message: __("{0} section(s) and {1} topic(s) added from {2}", [sections, topics, source]),
					indicator: sections + topics ? "green" : "orange",
				});
			});
		},
	});
	dialog.show();
}
