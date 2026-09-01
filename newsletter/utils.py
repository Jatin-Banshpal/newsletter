"""Small Jinja helpers for the newsletter print format.

Kept deliberately dependency-free (plain hex math) since the print format
must also render correctly through wkhtmltopdf, which does not understand
modern CSS like color-mix() or custom properties (var()) - only plain
rgba()/hex, which these helpers produce.
"""


def _to_rgb(hex_color):
	h = (hex_color or "").lstrip("#")
	if len(h) == 3:
		h = "".join(c * 2 for c in h)
	if len(h) != 6:
		return (0, 0, 0)
	try:
		return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
	except ValueError:
		return (0, 0, 0)


def hex_to_rgba(hex_color, alpha=1.0):
	"""Return e.g. 'rgba(79,70,229,0.14)' for a hex color and alpha (0-1)."""
	if not hex_color:
		return f"rgba(0,0,0,{alpha})"
	r, g, b = _to_rgb(hex_color)
	return f"rgba({r},{g},{b},{alpha})"


def file_url(path):
	"""URL-encode an attached file's path, keeping it site-relative.

	Two different renderers read this print format, and they need two
	different kinds of URL:

	- The live browser Print Preview loads the print page itself at
	  whatever host/port/proxy the user's browser actually used (which is
	  often NOT the server's own internal site URL, e.g. when the bench is
	  reached through a tunnel or port-forward). A *relative* "/files/..."
	  path resolves correctly against that real origin; a hardcoded
	  internal absolute URL (http://dev.localhost:8000/...) does not, and
	  silently fails as a broken-image icon.
	- The "Get PDF" download runs wkhtmltopdf server-side, which has no
	  browser origin to resolve a relative path against. Frappe's own
	  get_pdf() already handles this: it calls scrub_urls() on the HTML
	  first, which expands any "/..." path to an absolute URL using the
	  server's own internal site URL - the same address that works from
	  inside this bench.

	So the only thing this helper needs to do is percent-encode the path
	(a filename with spaces, e.g. "Screenshot 2026-08-30 032003.png",
	otherwise breaks wkhtmltopdf's own HTTP fetch) while leaving it
	relative; everything else is handled by the two renderers themselves.
	"""
	import urllib.parse

	if not path:
		return path
	if path.startswith("http"):
		scheme_sep = "://"
		if scheme_sep in path:
			scheme, rest = path.split(scheme_sep, 1)
			return f"{scheme}{scheme_sep}{urllib.parse.quote(rest, safe='/:')}"
		return path
	return urllib.parse.quote(path, safe="/:")
