"""Small, self-contained interface icons used in the static templates."""
from html import escape

SHAPES = {
    "terminal": '<path d="m5 6 6 6-6 6m8 0h6"/>',
    "folder": '<path d="M3 8V6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v2M3 8h18l-2 11H5L3 8Z"/>',
    "folder-grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "file": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v5h4M9 12h6m-6 4h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "pin": '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 0 1 14 0Z"/><circle cx="12" cy="10" r="2.4"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "network": '<rect x="8.5" y="2.5" width="7" height="5" rx="1"/><rect x="2" y="16.5" width="7" height="5" rx="1"/><rect x="15" y="16.5" width="7" height="5" rx="1"/><path d="M12 8v4M5.5 16v-4h13v4"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx=".6"/><path d="M9 3v3m6-3v3M9 18v3m6-3v3M3 9h3m-3 6h3m12-6h3m-3 6h3"/>',
    "layers": '<path d="M2 8 12 3l10 5-10 5-10-5Zm1 5 9 4.5 9-4.5M3 17l9 4.5 9-4.5"/>',
    "server": '<rect x="3" y="3.5" width="18" height="7" rx="1.5"/><rect x="3" y="13.5" width="18" height="7" rx="1.5"/><path d="M7 7h.5m-.5 10h.5m7-10h3m-3 10h3"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "laptop": '<rect x="4" y="4" width="16" height="12" rx="1.5"/><path d="m4 16-2 4h20l-2-4M9 20l.8-1h4.4l.8 1"/>',
    "wifi": '<path d="M2 8a16 16 0 0 1 20 0M5 11.5a11 11 0 0 1 14 0M8.5 15a5.5 5.5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/>',
    "support": '<path d="M4 13v-2a8 8 0 0 1 16 0v5c0 3-2 5-5 5h-2"/><rect x="3" y="11" width="4" height="7" rx="1.5"/><rect x="17" y="11" width="4" height="7" rx="1.5"/>',
    "code": '<path d="m7 8-5 4 5 4m10-8 5 4-5 4m-3-12-4 16"/>',
    "sliders": '<path d="M3 7h9m5 0h4M3 17h3m5 0h10"/><circle cx="14.5" cy="7" r="2.5"/><circle cx="8.5" cy="17" r="2.5"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    "book": '<path d="M3 4c4-1 6 0 9 2 3-2 5-3 9-2v14c-4-1-6 0-9 2-3-2-5-3-9-2V4Zm9 2v14"/>',
    "compare": '<rect x="2" y="4" width="8" height="16" rx="1.5"/><rect x="14" y="4" width="8" height="16" rx="1.5"/>',
    "building": '<path d="M3 21h18M5 21V7l7-4 7 4v14M8 10h1m6 0h1m-8 4h1m6 0h1m-5 7v-4h2v4"/>',
    "briefcase": '<rect x="2.5" y="7" width="19" height="13" rx="2"/><path d="M8 7V4h8v3M3 12c6 4 12 4 18 0m-9 1v3"/>',
    "graduation": '<path d="m2 9 10-5 10 5-10 5L2 9Zm4 3v5c4 3 8 3 12 0v-5m4-3v7"/>',
    "github": '<path fill="currentColor" stroke="none" d="M12 .9a11.1 11.1 0 0 0-3.51 21.63c.55.1.76-.24.76-.53v-2.08c-3.09.67-3.75-1.31-3.75-1.31-.5-1.29-1.24-1.63-1.24-1.63-1.02-.7.08-.69.08-.69 1.12.08 1.7 1.14 1.7 1.14 1 1.7 2.59 1.21 3.22.92.1-.72.39-1.21.7-1.5-2.47-.28-5.07-1.23-5.07-5.49 0-1.21.43-2.2 1.14-2.98-.11-.28-.5-1.41.11-2.94 0 0 .93-.3 3.05 1.14a10.7 10.7 0 0 1 5.56 0c2.12-1.44 3.05-1.14 3.05-1.14.61 1.53.22 2.66.11 2.94a4.28 4.28 0 0 1 1.14 2.98c0 4.27-2.6 5.2-5.09 5.47.4.35.75 1.03.75 2.08V22c0 .3.2.64.77.53A11.11 11.11 0 0 0 12 .9Z"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7.5 10v7m4-7v7m0-3.5c0-4.5 5.2-4.5 5.2 0V17"/><circle cx="7.5" cy="7.2" r=".7" fill="currentColor" stroke="none"/>'
}


def icon(name, extra_class=""):
    classes = ("icon " + extra_class).strip()
    return (f'<svg class="{escape(classes)}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.65" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{SHAPES[name]}</svg>')

