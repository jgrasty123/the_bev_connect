#!/usr/bin/env python3
"""
SUPERSEDED — DO NOT RUN.  (2026-08-24)

The single-page ReportLab rate sheet this script builds was replaced by a
designed two-page PDF covering both programs:

    assets/downloads/the-bev-connect-pricing-and-programs.pdf

That file is now the source of truth and is NOT generated from this repo.
Running this script writes to a path nothing links to any more; if the OUT
path is ever pointed back at the live PDF it will silently clobber the
designed file with stale single-program pricing.

Kept for the layout geometry only. To change published pricing, update the
designed PDF and re-drop it, then update the teaser figures in index.html
and rate-sheet.html to match.

--- original docstring below ---

Regenerates assets/downloads/the-bev-connect-rate-sheet.pdf

The original PDF was produced with ReportLab but its source script was never
committed, so this rebuild reproduces the original layout (Letter, Helvetica,
brand palette) from the geometry of that file and is now the source of truth.
Edit the RATE TABLE / ADDONS / COVERAGE blocks below and re-run:

    python3 tools/build_rate_sheet.py

Owner: James Grasty (Go-To Gifting LLC)
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import os

# ---------------------------------------------------------------- palette
INK        = HexColor('#0E0D0D')
ACCENT     = HexColor('#E23B22')
PAPER      = HexColor('#F4F1EA')
WHITE      = HexColor('#FFFFFF')
MUTED      = HexColor('#A8A299')
BODY       = HexColor('#2B2B2B')
RULE       = HexColor('#E8E4DA')

W, H = letter                      # 612 x 792
L, R = 43.2, 568.8                 # content margins

OUT = os.path.join(os.path.dirname(__file__), '..',
                   'assets', 'downloads', '_legacy-rate-sheet-DO-NOT-PUBLISH.pdf')

# ---------------------------------------------------------------- content
# Per-category rate rows: (label, wine, spirits, beer)
ROWS = [
    ('Storage',                 '$5/case/mo',        '$6/case/mo',        '$4/case/mo'),
    ('Receiving',               '$5/case',           '$5/case',           '$5/case'),
    ('Pick & Pack (Singles)',   '$4.00 first bottle\n$0.90 each add\u2019l',
                                '$4.75 first bottle\n$1.25 each add\u2019l',
                                '$3.50 first pack\n$0.75 each add\u2019l'),
    ('Full Case Pick',          '$3.00 (12 btl)',    '$3.50 (12 btl)',    '$2.50 (12-24)'),
    ('Customization & Kitting', '$2.50/item or $60/hr', '$2.50/item or $60/hr', '$2.50/item or $60/hr'),
    ('Engraving',               '$15/item',          '$15/item',          '$15 + $5 blank glass'),
]

# Rows that span the full width (label, value)
FULLROWS = [
    ('Pallet Receiving',        '$40 per pallet - one-time fee'),
    ('Pallet Storage',          '$25 per pallet / month'),
    ('Packaging Materials',     'Pass-through cost + 12% admin fee'),
    ('Shipping Charges',        'Carrier pass-through (UPS & GLS) + 8% admin fee - no markup'),
    ('Returns & Reverse Logistics', '$10/order + shipping'),
    ('Account & Compliance',    '$150/month minimum + $0.50/order - includes age verification, '
                                'excise reporting & compliance filing'),
]

ADDONS = [
    ('Greeting cards',   'from $1.99'),
    ('Engraving',        'from $15/item'),
    ('Pallet storage',   '$25/pallet/mo'),
    ('Gift boxes & crates', 'custom quote'),
    ('Custom kitting',   '$2.50/item or $60/hr'),
]

COVERAGE = [
    'Alcohol: Broad compliant coverage across most of the U.S.',
    'Non-alcohol: all 50 states, APO/FPO, Canada & Mexico.',
    'Pallet-in / pallet-out receiving and bulk storage.',
    'Carriers: UPS & GLS - overnight, 2-day, 3-day, ground.',
    'Packing Mon-Fri, plus Saturdays in Nov-Dec peak.',
]


def wrapped(c, text, font, size, maxw):
    return simpleSplit(text, font, size, maxw)


def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle('The Bev Connect - Alcohol Fulfillment Rate Sheet')
    c.setAuthor('The Bev Connect')
    c.setSubject('Alcohol Fulfillment Rate Sheet')

    # ---------------- masthead
    c.setFillColor(INK)
    c.rect(0, H - 110, W, 110, stroke=0, fill=1)

    # bottle mark
    c.setFillColor(ACCENT)
    c.roundRect(L + 20, H - 92, 26, 46, 4, stroke=0, fill=1)
    c.setFillColor(INK)
    c.rect(L + 29, H - 52, 8, 10, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(107, H - 80, 'The Bev')
    c.setFillColor(ACCENT)
    c.drawString(161, H - 80, 'Connect')

    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawString(107, H - 96, 'ALCOHOL-READY 3PL FULFILLMENT')
    c.setFont('Helvetica', 8.5)
    c.drawRightString(R, H - 76, 'hello@thebevconnect.com')
    c.drawRightString(R, H - 88, '(805) 413-4141 - Ventura')

    # ---------------- title block
    y = H - 138
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawString(L, y, 'ALCOHOL FULFILLMENT RATE SHEET')

    y -= 28
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 26)
    c.drawString(L, y, 'Transparent pricing, by product')
    y -= 26
    c.drawString(L, y, 'category.')

    y -= 22
    c.setFillColor(BODY)
    c.setFont('Helvetica', 10.5)
    lede = ('Compliant 3PL fulfillment for beer, wine & spirits brands shipping DTC to 42+ '
            'destinations from our licensed warehouse in Ventura. One partner, one '
            'invoice, no markup games.')
    for ln in wrapped(c, lede, 'Helvetica', 10.5, R - L):
        c.drawString(L, y, ln)
        y -= 14

    # ---------------- rate table
    y -= 14
    col = [L + 10, 232, 350, 468]     # label, wine, spirits, beer (centred cols)
    head_h = 23
    c.setFillColor(INK)
    c.rect(L, y - head_h, R - L, head_h, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(col[0], y - 16, 'Service')
    for x, t in ((col[1], 'Wine'), (col[2], 'Spirits'), (col[3], 'Beer / RTD')):
        c.drawCentredString(x + 45, y - 16, t)
    y -= head_h

    c.setFont('Helvetica', 8.7)
    for i, (label, *vals) in enumerate(ROWS):
        lines = max(len(v.split('\n')) for v in vals)
        h = 22 if lines == 1 else 32
        c.setFillColor(PAPER if i % 2 == 0 else WHITE)
        c.rect(L, y - h, R - L, h, stroke=0, fill=1)

        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 8.7)
        c.drawString(col[0], y - (h / 2) - 3, label)

        c.setFillColor(BODY)
        c.setFont('Helvetica', 8.7)
        for x, v in zip(col[1:], vals):
            parts = v.split('\n')
            if len(parts) == 1:
                c.drawCentredString(x + 45, y - (h / 2) - 3, parts[0])
            else:
                c.drawCentredString(x + 45, y - 14, parts[0])
                c.drawCentredString(x + 45, y - 26, parts[1])
        y -= h

    # ---------------- full-width rows
    y -= 4
    for i, (label, val) in enumerate(FULLROWS):
        vlines = wrapped(c, val, 'Helvetica', 8.7, R - 232 - 12)
        h = 21 if len(vlines) == 1 else 30
        c.setFillColor(WHITE if i % 2 == 0 else PAPER)
        c.rect(L, y - h, R - L, h, stroke=0, fill=1)

        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 8.7)
        c.drawString(col[0], y - (h / 2) - 3, label)

        c.setFillColor(BODY)
        c.setFont('Helvetica', 8.7)
        if len(vlines) == 1:
            c.drawString(232, y - (h / 2) - 3, vlines[0])
        else:
            yy = y - 13
            for ln in vlines:
                c.drawString(232, yy, ln)
                yy -= 11
        y -= h

    # ---------------- CTA band (directly under the rate table)
    # Order is: table -> CTA band -> two-up (add-ons | coverage) -> fine print.
    # Everything is measured and flowed, never pinned to a magic number, so the
    # sections cannot overrun each other.
    BAND_H   = 48
    FINE_Y   = 30                     # baseline of last fine-print line
    FINE_TOP = FINE_Y + 20            # fine print block occupies roughly 30..50

    LEFT_X0, LEFT_X1 = L, 262         # add-ons: name at X0, price right-aligned at X1
    RIGHT_X0 = 292                    # coverage: starts after a 30pt gutter

    y -= 14
    band_y = y - BAND_H
    c.setFillColor(INK)
    c.rect(L, band_y, R - L, BAND_H, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 11.5)
    c.drawString(L + 18, band_y + 32, 'Ready to hand off fulfillment?')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 9.5)
    c.drawString(L + 18, band_y + 16,
                 "Book a discovery call - we'll send pricing, timing and a tailored plan "
                 "within one business day.")
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 10)
    c.drawRightString(R - 18, band_y + 24, 'thebevconnect.com')

    # ---------------- two-up: add-ons | coverage
    head_y = band_y - 24

    # Measure both columns first.
    cov_lines = [wrapped(c, item, 'Helvetica', 9, R - RIGHT_X0) for item in COVERAGE]
    addon_h = len(ADDONS) * 14
    cov_h   = sum(len(ls) * 11 + 3 for ls in cov_lines)
    need    = 24 + max(addon_h, cov_h)          # 24 = header + rule

    # Hard guarantee: the block must fit between head_y and the fine print.
    avail = head_y - FINE_TOP
    if need > avail:
        raise SystemExit(
            f'Two-up block needs {need:.0f}pt but only {avail:.0f}pt is available '
            f'above the fine print. Trim ADDONS/COVERAGE or shorten the table.')

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(LEFT_X0, head_y, 'Popular add-ons & upsells')
    c.drawString(RIGHT_X0, head_y, 'Coverage & carriers')

    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(LEFT_X0, head_y - 8, LEFT_X1, head_y - 8)
    c.line(RIGHT_X0, head_y - 8, R, head_y - 8)

    ay = head_y - 24
    c.setFont('Helvetica', 9)
    for name, price in ADDONS:
        c.setFillColor(BODY)
        c.drawString(LEFT_X0, ay, name)
        c.setFillColor(ACCENT)
        c.drawRightString(LEFT_X1, ay, price)
        ay -= 14

    cy = head_y - 24
    c.setFillColor(BODY)
    c.setFont('Helvetica', 9)
    for lines in cov_lines:
        for ln in lines:
            c.drawString(RIGHT_X0, cy, ln)
            cy -= 11
        cy -= 3

    # ---------------- fine print
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawCentredString(W / 2, FINE_Y + 12,
                        'Pricing is indicative and subject to a written services agreement. '
                        'Volume and custom-program rates available on request.')
    c.drawCentredString(W / 2, FINE_Y,
                        '(c) 2026 The Bev Connect - Ventura - '
                        'hello@thebevconnect.com - (805) 413-4141')

    c.showPage()
    c.save()
    print('wrote', os.path.normpath(OUT))


if __name__ == '__main__':
    build()
