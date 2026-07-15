#!/usr/bin/env python3
"""
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
                   'assets', 'downloads', 'the-bev-connect-rate-sheet.pdf')

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
    'Alcohol: ships to every U.S. state except Utah & Alabama (42+ states).',
    'Non-alcoholic: all U.S. states, Armed Services addresses, Canada & Mexico.',
    'Pallet-in / pallet-out receiving and bulk storage available at our Ventura warehouse.',
    'Carriers: UPS & GLS, with overnight, 2-day, 3-day & ground options.',
    'Operations: packing Mon-Fri, plus Saturdays in the Nov-Dec peak.',
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
    c.drawRightString(R, H - 88, '(805) 413-4141 - Ventura, CA')

    # ---------------- title block
    y = H - 150
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawString(L, y, 'ALCOHOL FULFILLMENT RATE SHEET')

    y -= 34
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 26)
    c.drawString(L, y, 'Transparent pricing, by product')
    y -= 28
    c.drawString(L, y, 'category.')

    y -= 26
    c.setFillColor(BODY)
    c.setFont('Helvetica', 10.5)
    lede = ('Compliant 3PL fulfillment for beer, wine & spirits brands shipping DTC to 42+ '
            'states from our licensed warehouse in Ventura, California. One partner, one '
            'invoice, no markup games.')
    for ln in wrapped(c, lede, 'Helvetica', 10.5, R - L):
        c.drawString(L, y, ln)
        y -= 14

    # ---------------- rate table
    y -= 18
    col = [L + 10, 232, 350, 468]     # label, wine, spirits, beer (centred cols)
    head_h = 25
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
        h = 25 if lines == 1 else 36
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
        h = 23 if len(vlines) == 1 else 34
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

    # ---------------- two-up: add-ons | coverage
    y -= 30
    # Two independent columns with a real gutter between them.
    LEFT_X0, LEFT_X1 = L, 300          # add-ons: name at X0, price right-aligned at X1
    RIGHT_X0 = 330                     # coverage: starts after a 30pt gutter
    mid = LEFT_X1
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(L, y, 'Popular add-ons & upsells')
    c.drawString(RIGHT_X0, y, 'Coverage & carriers')

    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(LEFT_X0, y - 8, LEFT_X1, y - 8)
    c.line(RIGHT_X0, y - 8, R, y - 8)

    ay = y - 24
    c.setFont('Helvetica', 9)
    for name, price in ADDONS:
        c.setFillColor(BODY)
        c.drawString(L, ay, name)
        c.setFillColor(ACCENT)
        c.drawRightString(LEFT_X1, ay, price)
        ay -= 15

    cy = y - 24
    c.setFillColor(BODY)
    c.setFont('Helvetica', 9)
    for item in COVERAGE:
        for ln in wrapped(c, item, 'Helvetica', 9, R - RIGHT_X0):
            c.drawString(RIGHT_X0, cy, ln)
            cy -= 11
        cy -= 4

    # ---------------- CTA band
    band_y = 96
    c.setFillColor(INK)
    c.rect(L, band_y, R - L, 52, stroke=0, fill=1)
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

    # ---------------- fine print
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawCentredString(W / 2, 50,
                        'Pricing is indicative and subject to a written services agreement. '
                        'Volume and custom-program rates available on request.')
    c.drawCentredString(W / 2, 38,
                        '(c) 2026 The Bev Connect - Ventura, California - '
                        'hello@thebevconnect.com - (805) 413-4141')

    c.showPage()
    c.save()
    print('wrote', os.path.normpath(OUT))


if __name__ == '__main__':
    build()
