"""Create/refresh the built-in newsletter themes and wire the demo issue to them.

Run with:
  bench --site dev.localhost execute newsletter.setup_styles.create_styles
  bench --site dev.localhost execute newsletter.setup_styles.apply_to_demo

Each theme is meant to be recognisably different from every other one - not
just a colour swap but different fonts, alignment, dividers, corner rounding,
spacing and small CSS flourishes. Fonts referenced here are either bundled
with the app (/assets/newsletter/fonts) or Type-1 faces installed on the
server, each paired with its Windows/Mac metric twin as a fallback.
"""

import frappe

# Font stacks. First name = server-side/bundled face; the rest = browser fallbacks.
F_LIMELIGHT = "'Limelight', Georgia, 'Times New Roman', serif"
F_LOBSTER = "'Lobster', 'Brush Script MT', cursive"
F_RALEWAY = "'Raleway', 'Century Gothic', 'Trebuchet MS', sans-serif"
F_OPENSANS = "'Open Sans', 'Segoe UI', Helvetica, Arial, sans-serif"
F_NOTOSANS = "'Noto Sans', 'Segoe UI', Helvetica, Arial, sans-serif"
F_NOTOSERIF = "'Noto Serif', Georgia, 'Times New Roman', serif"
F_DROIDSERIF = "'Droid Serif', Georgia, 'Times New Roman', serif"
F_MONO = "'DejaVu Sans Mono', Consolas, 'Courier New', monospace"
F_LIBSANS = "'Liberation Sans', Arial, Helvetica, sans-serif"
F_SCHOOLBOOK = "'Century Schoolbook L', 'Century Schoolbook', 'New Century Schoolbook', Georgia, serif"
F_PALLADIO = "'URW Palladio L', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
F_BOOKMAN = "'URW Bookman L', 'Bookman Old Style', Bookman, Georgia, serif"


THEMES = [
	{
		"style_name": "BWH Brand Default",
		"theme_notes": "House style: white page, indigo accent, Limelight display title, Raleway headings, Open Sans body. Centred masthead, soft 14px rounding, hairline dividers.",
		"background_color": "#FFFFFF",
		"text_color": "#1C1C22",
		"accent_color": "#4F46E5",
		"muted_text_color": "#8A8A92",
		"divider_color": "#E4E4EA",
		"panel_background_color": "#F5F3FF",
		"card_background_color": "#FFFFFF",
		"display_font": F_LIMELIGHT,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_OPENSANS,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.75,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Hairline",
		"corner_radius": 14,
		"border_style": "None",
		"border_width": 0,
		"custom_css": """
.bwh-topic-title { font-family: 'Noto Serif', Georgia, serif; }
.bwh-intro { font-family: 'Noto Serif', Georgia, serif; }
""",
	},
	{
		"style_name": "Modern",
		"theme_notes": "Bold, black-on-white, oversized numerals, sharp corners, one loud red accent. Left-aligned masthead.",
		"background_color": "#FFFFFF",
		"text_color": "#0A0A0A",
		"accent_color": "#E11D48",
		"muted_text_color": "#737373",
		"divider_color": "#0A0A0A",
		"panel_background_color": "#F4F4F5",
		"card_background_color": "#FFFFFF",
		"display_font": F_RALEWAY,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_OPENSANS,
		"heading_style": "Uppercase",
		"body_font_size": 14,
		"line_height": 1.75,
		"paragraph_spacing": 12,
		"masthead_alignment": "Left",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Thick",
		"corner_radius": 0,
		"border_style": "None",
		"border_width": 0,
		"custom_css": """
.bwh-masthead h1 { font-weight: 800; text-transform: uppercase; letter-spacing: -0.02em; font-size: 44px; line-height: 1.05; }
.bwh-rule { width: 100%; height: 6px; background: #0A0A0A; }
.bwh-eyebrow .bwh-index { font-size: 40px; font-weight: 800; color: #0A0A0A; margin-right: 16px; letter-spacing: -0.03em; }
.bwh-eyebrow .bwh-dot { width: 12px; height: 12px; border-radius: 0; }
.bwh-topic-title { font-weight: 800; }
.bwh-avatar { border-radius: 0; }
.bwh-section-panel { border-radius: 0; }
""",
	},
	{
		"style_name": "Classic",
		"theme_notes": "Cream paper, burgundy ink, book-style serifs, double rules, italic titles and a drop cap on every topic.",
		"background_color": "#F8F3E7",
		"text_color": "#2C2418",
		"accent_color": "#7B2D26",
		"muted_text_color": "#8B7D6B",
		"divider_color": "#C9B99A",
		"panel_background_color": "#EFE6D2",
		"card_background_color": "#FCF8EE",
		"display_font": F_SCHOOLBOOK,
		"heading_font": F_SCHOOLBOOK,
		"label_font": F_PALLADIO,
		"font_family": F_DROIDSERIF,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.85,
		"paragraph_spacing": 14,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 1,
		"divider_style": "Double",
		"corner_radius": 3,
		"border_color": "#D8C9A8",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead h1 { font-style: italic; font-weight: 400; font-size: 38px; }
.bwh-wordmark { border-top: 1px solid #7B2D26; border-bottom: 1px solid #7B2D26; padding: 6px 0; letter-spacing: 0.4em; }
.bwh-section-title { font-style: italic; font-weight: 400; font-size: 27px; }
.bwh-eyebrow .bwh-index { font-family: Georgia, serif; font-style: italic; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-title { font-weight: 700; }
.bwh-newsletter .bwh-topic-content > p:first-child::first-letter { font-size: 2.7em; float: left; line-height: 0.85; padding: 4px 8px 0 0; color: #7B2D26; font-style: italic; }
.bwh-toc a { text-transform: none; font-style: italic; letter-spacing: 0.02em; font-size: 13px; }
""",
	},
	{
		"style_name": "Professional",
		"theme_notes": "Corporate navy and slate. Clean sans-serif, numbered chips, hairline dividers, restrained rounding. For client-facing issues.",
		"background_color": "#FFFFFF",
		"text_color": "#1F2937",
		"accent_color": "#1E3A8A",
		"muted_text_color": "#64748B",
		"divider_color": "#E2E8F0",
		"panel_background_color": "#F1F5F9",
		"card_background_color": "#FFFFFF",
		"display_font": F_LIBSANS,
		"heading_font": F_NOTOSANS,
		"label_font": F_NOTOSANS,
		"font_family": F_OPENSANS,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.7,
		"paragraph_spacing": 12,
		"masthead_alignment": "Left",
		"show_section_numbers": 1,
		"accent_headings": 1,
		"divider_style": "Hairline",
		"corner_radius": 6,
		"border_color": "#E2E8F0",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead { border-bottom: 3px solid #1E3A8A; padding-bottom: 30px; }
.bwh-masthead h1 { font-weight: 700; font-size: 32px; letter-spacing: -0.01em; }
.bwh-rule { display: none; }
.bwh-eyebrow .bwh-index { background: #1E3A8A; color: #FFFFFF; padding: 4px 9px; border-radius: 3px; font-weight: 700; font-size: 11px; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-title { font-weight: 700; }
.bwh-avatar { border-radius: 4px; }
""",
	},
	{
		"style_name": "Creative",
		"theme_notes": "Playful. Lobster script titles, a rotating rainbow of section accents, big rounded corners, dotted rules and a slightly tilted masthead.",
		"background_color": "#FFFBF2",
		"text_color": "#2B1D4A",
		"accent_color": "#FF6B6B",
		"muted_text_color": "#7A6F8F",
		"divider_color": "#F1E4CF",
		"section_accent_palette": "#FF6B6B,#4ECDC4,#FFBE0B,#8338EC,#FB5607,#3A86FF,#06D6A0,#EF476F",
		"display_font": F_LOBSTER,
		"heading_font": F_LOBSTER,
		"label_font": F_RALEWAY,
		"font_family": F_OPENSANS,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.8,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 1,
		"divider_style": "Dotted",
		"corner_radius": 26,
		"border_color": "#FFD6A5",
		"border_style": "Dashed",
		"border_width": 2,
		"custom_css": """
.bwh-masthead h1 { font-size: 48px; font-weight: 400; transform: rotate(-2deg); }
.bwh-wordmark { letter-spacing: 0.25em; }
.bwh-section-title { font-size: 32px; font-weight: 400; letter-spacing: 0.01em; }
.bwh-eyebrow .bwh-dot { width: 16px; height: 16px; }
.bwh-topic-title { font-size: 22px; font-weight: 400; }
.bwh-rule { height: 4px; width: 90px; border-radius: 2px; }
""",
	},
	{
		"style_name": "Stylish",
		"theme_notes": "Fashion-editorial: pure black on white with a gold accent, Limelight display type, ultra-light letter-spaced uppercase headings, no rounding.",
		"background_color": "#FFFFFF",
		"text_color": "#000000",
		"accent_color": "#B8962E",
		"muted_text_color": "#777777",
		"divider_color": "#000000",
		"panel_background_color": "#F7F5F0",
		"card_background_color": "#FFFFFF",
		"display_font": F_LIMELIGHT,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_NOTOSERIF,
		"heading_style": "Uppercase",
		"body_font_size": 14,
		"line_height": 1.8,
		"paragraph_spacing": 14,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Hairline",
		"corner_radius": 0,
		"border_color": "#000000",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead h1 { font-size: 40px; letter-spacing: 0.06em; }
.bwh-wordmark { letter-spacing: 0.6em; font-weight: 500; }
.bwh-rule { width: 100%; height: 1px; background: #000000; }
.bwh-section-title { font-weight: 300; letter-spacing: 0.32em; font-size: 17px; }
.bwh-eyebrow .bwh-index { font-family: 'Limelight', Georgia, serif; color: #B8962E; font-size: 18px; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-title { font-family: 'Raleway', 'Century Gothic', sans-serif; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; font-size: 13px; }
.bwh-avatar { border-radius: 0; background: #000000 !important; color: #FFFFFF !important; }
""",
	},
	{
		"style_name": "Formal",
		"theme_notes": "Monochrome and restrained: serif throughout, small-caps headings, justified text, double rules, section marks. Reads like an official circular.",
		"background_color": "#FFFFFF",
		"text_color": "#111111",
		"accent_color": "#111111",
		"muted_text_color": "#555555",
		"divider_color": "#111111",
		"panel_background_color": "#FAFAFA",
		"card_background_color": "#FFFFFF",
		"display_font": F_NOTOSERIF,
		"heading_font": F_NOTOSERIF,
		"label_font": F_NOTOSERIF,
		"font_family": F_NOTOSERIF,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.8,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Double",
		"corner_radius": 0,
		"border_color": "#111111",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead h1 { font-weight: 700; font-size: 30px; letter-spacing: 0.02em; }
.bwh-wordmark { font-variant: small-caps; text-transform: none; letter-spacing: 0.3em; font-weight: 400; font-size: 15px; }
.bwh-section-title { font-variant: small-caps; font-weight: 700; font-size: 22px; letter-spacing: 0.06em; }
.bwh-eyebrow .bwh-index::before { content: '\\00a7 '; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-content { text-align: justify; }
.bwh-avatar { border-radius: 0; }
.bwh-links a::after { content: ''; }
.bwh-links a { text-decoration: underline; }
.bwh-toc a { font-variant: small-caps; text-transform: none; font-size: 13px; letter-spacing: 0.04em; }
.bwh-footer { font-variant: small-caps; text-transform: none; font-size: 12px; }
""",
	},
	{
		"style_name": "Colourful",
		"theme_notes": "Every section gets its own bright colour - title, rule, avatars, links and panel tint - on a clean white page.",
		"background_color": "#FFFFFF",
		"text_color": "#1A1A2E",
		"accent_color": "#FF2D55",
		"muted_text_color": "#6E6E80",
		"divider_color": "#ECECF1",
		"section_accent_palette": "#FF2D55,#FF9500,#FFCC00,#34C759,#00C7BE,#007AFF,#5856D6,#AF52DE",
		"display_font": F_RALEWAY,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_OPENSANS,
		"heading_style": "Uppercase",
		"body_font_size": 14,
		"line_height": 1.75,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 1,
		"divider_style": "Thick",
		"corner_radius": 18,
		"border_style": "None",
		"border_width": 0,
		"custom_css": """
.bwh-masthead h1 { font-weight: 800; font-size: 40px; letter-spacing: -0.01em; }
.bwh-eyebrow .bwh-index { color: #FFFFFF; background: #1A1A2E; border-radius: 999px; padding: 4px 11px; font-weight: 800; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-section-title { font-weight: 800; }
.bwh-avatar { border-radius: 8px; }
.bwh-rule { width: 120px; height: 6px; border-radius: 3px; }
""",
	},
	{
		"style_name": "Minimal",
		"theme_notes": "Almost nothing but type and whitespace. Thin Raleway, grey on white, no numbers, no dots, no avatars, no contents list. Generous line height.",
		"background_color": "#FFFFFF",
		"text_color": "#262626",
		"accent_color": "#262626",
		"muted_text_color": "#A3A3A3",
		"divider_color": "#EDEDED",
		"panel_background_color": "#FAFAFA",
		"card_background_color": "#FAFAFA",
		"display_font": F_RALEWAY,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_OPENSANS,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.9,
		"paragraph_spacing": 16,
		"masthead_alignment": "Left",
		"show_section_numbers": 0,
		"accent_headings": 0,
		"divider_style": "Hairline",
		"corner_radius": 0,
		"border_style": "None",
		"border_width": 0,
		"custom_css": """
.bwh-masthead h1 { font-weight: 200; font-size: 38px; letter-spacing: -0.01em; }
.bwh-wordmark { font-weight: 500; letter-spacing: 0.25em; color: #A3A3A3; }
.bwh-rule { display: none; }
.bwh-toc { display: none; }
.bwh-section { padding-top: 46px; padding-bottom: 46px; }
.bwh-section-title { font-weight: 300; font-size: 26px; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-title { font-weight: 500; font-size: 16px; }
.bwh-avatar { display: none; }
.bwh-section-panel .bwh-topic { padding-left: 0; padding-right: 0; }
""",
	},
	{
		"style_name": "Digital",
		"theme_notes": "Dark terminal aesthetic: deep navy page, neon-green accent, monospace headings with shell-style prefixes, square avatars, dotted rules.",
		"background_color": "#0B1020",
		"text_color": "#D6E2FF",
		"accent_color": "#00E5A0",
		"muted_text_color": "#7C8AA5",
		"divider_color": "#1F2A44",
		"panel_background_color": "#111A33",
		"card_background_color": "#0F172A",
		"display_font": F_MONO,
		"heading_font": F_MONO,
		"label_font": F_MONO,
		"font_family": F_NOTOSANS,
		"heading_style": "Uppercase",
		"body_font_size": 14,
		"line_height": 1.75,
		"paragraph_spacing": 12,
		"masthead_alignment": "Left",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Dotted",
		"corner_radius": 4,
		"border_color": "#1F2A44",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead h1 { font-size: 30px; font-weight: 700; letter-spacing: 0; }
.bwh-masthead h1::before { content: '> '; color: #00E5A0; }
.bwh-wordmark::before { content: '$ '; }
.bwh-wordmark { letter-spacing: 0.2em; }
.bwh-rule { width: 100%; height: 1px; background: #1F2A44; }
.bwh-section-title::before { content: '// '; color: #00E5A0; }
.bwh-section-title { font-size: 19px; letter-spacing: 0.04em; }
.bwh-eyebrow .bwh-index { color: #00E5A0; }
.bwh-eyebrow .bwh-index::before { content: '['; }
.bwh-eyebrow .bwh-index::after { content: ']'; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-topic-title { font-size: 15px; }
.bwh-avatar { border-radius: 3px; }
.bwh-links a { text-decoration: underline; }
.bwh-media-item img { border: 1px solid #1F2A44; }
""",
	},
	{
		"style_name": "Scientific & AI",
		"theme_notes": "Journal / research-paper feel: serif body, sans headings in academic blue, monospace labels, section marks, justified text and figure captions.",
		"background_color": "#FFFFFF",
		"text_color": "#1B1F24",
		"accent_color": "#1A5FB4",
		"muted_text_color": "#5C6773",
		"divider_color": "#C7D0D9",
		"panel_background_color": "#EEF3F8",
		"card_background_color": "#FFFFFF",
		"display_font": F_NOTOSERIF,
		"heading_font": F_NOTOSANS,
		"label_font": F_MONO,
		"font_family": F_NOTOSERIF,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.75,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 1,
		"divider_style": "Hairline",
		"corner_radius": 2,
		"border_color": "#C7D0D9",
		"border_style": "Solid",
		"border_width": 1,
		"custom_css": """
.bwh-masthead h1 { font-weight: 700; font-size: 28px; }
.bwh-wordmark { text-transform: none; letter-spacing: 0.12em; font-weight: 700; }
.bwh-eyebrow .bwh-index { color: #1A5FB4; }
.bwh-eyebrow .bwh-index::before { content: '\\00a7'; }
.bwh-eyebrow .bwh-dot { display: none; }
.bwh-section-title { font-weight: 700; font-size: 20px; }
.bwh-topic-title { font-weight: 700; font-size: 15px; }
.bwh-topic-content { text-align: justify; }
.bwh-media-item .bwh-caption::before { content: 'Fig. '; font-style: normal; font-weight: 700; }
.bwh-contributor-text .bwh-role { font-size: 9px; letter-spacing: 0; }
.bwh-avatar { border-radius: 2px; }
.bwh-toc { text-transform: none; letter-spacing: 0; }
""",
	},
	{
		"style_name": "Warm Brew",
		"theme_notes": "Coffee-house warmth to match Brew with Hussain: latte background, terracotta accent, italic serif display, soft rounded cards.",
		"background_color": "#FBF3EA",
		"text_color": "#3B2418",
		"accent_color": "#B4532A",
		"muted_text_color": "#8C6F5E",
		"divider_color": "#E7D5C5",
		"panel_background_color": "#F4E6D8",
		"card_background_color": "#FFFAF4",
		"display_font": F_DROIDSERIF,
		"heading_font": F_RALEWAY,
		"label_font": F_RALEWAY,
		"font_family": F_DROIDSERIF,
		"heading_style": "Normal",
		"body_font_size": 14,
		"line_height": 1.8,
		"paragraph_spacing": 12,
		"masthead_alignment": "Center",
		"show_section_numbers": 1,
		"accent_headings": 0,
		"divider_style": "Hairline",
		"corner_radius": 14,
		"border_style": "None",
		"border_width": 0,
		"custom_css": """
.bwh-masthead h1 { font-style: italic; font-weight: 400; font-size: 36px; }
.bwh-section-title { font-weight: 600; }
.bwh-eyebrow .bwh-dot { width: 10px; height: 10px; }
.bwh-topic-title { font-weight: 600; }
""",
	},
]

# Every theme field, so refreshing a theme also clears fields it no longer sets.
ALL_FIELDS = [
	"theme_notes",
	"background_color", "text_color", "accent_color", "muted_text_color", "divider_color",
	"panel_background_color", "card_background_color", "section_accent_palette",
	"display_font", "heading_font", "label_font", "font_family",
	"heading_style", "body_font_size", "line_height", "paragraph_spacing",
	"masthead_alignment", "show_section_numbers", "accent_headings", "divider_style", "corner_radius",
	"border_color", "border_width", "border_style",
	"custom_css",
]


def create_styles():
	for theme in THEMES:
		name = theme["style_name"]
		if frappe.db.exists("Newsletter Style", name):
			doc = frappe.get_doc("Newsletter Style", name)
		else:
			doc = frappe.new_doc("Newsletter Style")
			doc.style_name = name
		for field in ALL_FIELDS:
			doc.set(field, theme.get(field))
		doc.custom_css = (doc.custom_css or "").strip()
		if doc.is_new():
			doc.insert(ignore_permissions=True)
		else:
			doc.save(ignore_permissions=True)
	frappe.db.commit()
	print(f"{len(THEMES)} themes ready: " + ", ".join(t["style_name"] for t in THEMES))


def apply_to_demo(issue="BWH Technologies Newsletter - August 2026", theme="Modern"):
	"""Point the demo issue at a theme and let the theme drive section looks.

	Earlier demo data gave the Products and Brew with Hussain sections (and
	their topics) their own hard-coded Newsletter Style so they'd render as
	coloured panels. Now that a theme defines the panel look, those overrides
	are replaced by the section's "Highlight as Panel" flag so every theme
	renders coherently.
	"""
	if not frappe.db.exists("Newsletter Issue", issue):
		print(f"Issue not found: {issue}")
		return

	doc = frappe.get_doc("Newsletter Issue", issue)
	doc.style = theme
	for row in doc.sections:
		row.highlight = 1 if row.section in ("Products", "Brew with Hussain") else 0
		row.style = None
	doc.save(ignore_permissions=True)
	for content in frappe.get_all("Newsletter Content", filters={"newsletter_issue": issue}, pluck="name"):
		frappe.db.set_value("Newsletter Content", content, "style", None)

	# The two old section-only styles are superseded by the highlight flag.
	for old in ("BWH Products Highlight", "Brew with Hussain"):
		if frappe.db.exists("Newsletter Style", old) and not frappe.db.exists("Newsletter Issue", {"style": old}):
			frappe.delete_doc("Newsletter Style", old, ignore_permissions=True, force=True)

	frappe.db.commit()
	print(f"{issue}: theme = {theme}; Products & Brew with Hussain highlighted; per-section/topic overrides cleared.")


if __name__ == "__main__":
	create_styles()
	apply_to_demo()
