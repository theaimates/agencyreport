"""
ReportFlow — Freelancer Portfolio PDF
Clean white case-study format for Upwork / LinkedIn.
One section per page, consistent header/footer on every inner page.
Outputs: .tmp/ReportFlow_Portfolio.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '.tmp')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'ReportFlow_Portfolio.pdf')

# ── Colours (clean light theme) ───────────────────────────────────
C_BG       = colors.HexColor('#FFFFFF')
C_INK      = colors.HexColor('#0F172A')   # near-black text
C_MUTED    = colors.HexColor('#64748B')   # slate-500
C_SUBTLE   = colors.HexColor('#94A3B8')   # slate-400
C_RULE     = colors.HexColor('#E2E8F0')   # slate-200
C_CARD     = colors.HexColor('#F8FAFC')   # slate-50
C_INDIGO   = colors.HexColor('#6366F1')   # indigo-500
C_VIOLET   = colors.HexColor('#8B5CF6')   # violet-500
C_GREEN    = colors.HexColor('#10B981')   # emerald-500
C_AMBER    = colors.HexColor('#F59E0B')   # amber-500
C_RED      = colors.HexColor('#EF4444')   # red-500
C_IND_BG   = colors.HexColor('#EEF2FF')   # indigo-50
C_GRN_BG   = colors.HexColor('#ECFDF5')   # emerald-50
C_RED_BG   = colors.HexColor('#FEF2F2')   # red-50

W, H = A4  # 595 × 842 pts

# ── Page-level constants ──────────────────────────────────────────
MARGIN_L = 0.75 * inch
MARGIN_R = 0.75 * inch
MARGIN_T = 0.75 * inch
MARGIN_B = 0.75 * inch

# Section metadata — (header_label, accent_color) per page (0-indexed, page 0 = cover)
PAGES = [
    ('CASE STUDY  ·  AI Automation  ·  n8n  ·  Airtable', C_INDIGO),   # cover
    ('01 — THE PROBLEM',                                    C_RED),
    ('02 — WHAT I BUILT',                                   C_INDIGO),
    ('03 — HOW I BUILT IT',                                 C_GREEN),
    ('04 — TECHNICAL DEPTH',                                C_VIOLET),
    ('05 — TECH STACK',                                     C_AMBER),
    ('06 — RESULTS & IMPACT',                               C_GREEN),
]
DOC_LABEL = 'ReportFlow  ·  Portfolio'
AUTHOR    = 'Johyandi Lukmana'
ROLE      = 'AI Automation Architect'
EMAIL     = 'youraimates@gmail.com'
LINKEDIN  = 'linkedin.com/in/johyandi-lukmana-932073337'
UPWORK    = 'upwork.com/freelancers/~01d1a59155f46bc949'
TOTAL_PGS = len(PAGES)

# ── Document ──────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT_PATH,
    pagesize=A4,
    leftMargin=MARGIN_L,
    rightMargin=MARGIN_R,
    topMargin=0.9 * inch,
    bottomMargin=0.75 * inch,
    title='ReportFlow — Portfolio',
    author=AUTHOR,
)
USABLE_W = W - MARGIN_L - MARGIN_R

# ── Styles ────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def s(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    # Cover
    'cover_label':  s('cv_lbl',  fontSize=8.5, textColor=C_MUTED,   fontName='Helvetica',
                                  spaceAfter=2, leading=13, letterSpacing=1.8),
    'cover_title':  s('cv_ttl',  fontSize=46, textColor=C_INK,      fontName='Helvetica-Bold',
                                  spaceAfter=0, leading=52),
    'cover_accent': s('cv_acc',  fontSize=46, textColor=C_INDIGO,   fontName='Helvetica-Bold',
                                  spaceAfter=0, leading=52),
    'cover_sub':    s('cv_sub',  fontSize=14, textColor=C_MUTED,    fontName='Helvetica',
                                  spaceAfter=0, leading=21),

    # Section heading (large, on each page)
    'page_title':   s('pg_ttl',  fontSize=28, textColor=C_INK,      fontName='Helvetica-Bold',
                                  spaceBefore=0, spaceAfter=4, leading=34),
    'page_accent':  s('pg_acc',  fontSize=28, textColor=C_INDIGO,   fontName='Helvetica-Bold',
                                  spaceBefore=0, spaceAfter=4, leading=34),
    'page_intro':   s('pg_int',  fontSize=11, textColor=C_MUTED,    fontName='Helvetica',
                                  spaceAfter=12, leading=17),

    # Sub-labels (small caps style)
    'label':        s('lbl',     fontSize=8,  textColor=C_MUTED,    fontName='Helvetica-Bold',
                                  spaceBefore=14, spaceAfter=6, leading=12, letterSpacing=1.6),

    # Body
    'body':         s('body',    fontSize=10.5, textColor=C_INK,    fontName='Helvetica',
                                  spaceAfter=5, leading=16.5),
    'muted':        s('muted',   fontSize=10,   textColor=C_MUTED,  fontName='Helvetica',
                                  spaceAfter=4, leading=15),
    'bullet':       s('bul',     fontSize=10.5, textColor=C_INK,    fontName='Helvetica',
                                  spaceAfter=4, leading=16, leftIndent=14, firstLineIndent=-10),
    'bullet_m':     s('bul_m',   fontSize=10,   textColor=C_MUTED,  fontName='Helvetica',
                                  spaceAfter=3, leading=15, leftIndent=14, firstLineIndent=-10),
    'bullet_g':     s('bul_g',   fontSize=10.5, textColor=C_GREEN,  fontName='Helvetica',
                                  spaceAfter=4, leading=16, leftIndent=14, firstLineIndent=-10),

    # Cards
    'card_title':   s('cd_t',    fontSize=11,  textColor=C_INK,     fontName='Helvetica-Bold',
                                  spaceAfter=3, leading=16),
    'card_body':    s('cd_b',    fontSize=9.5, textColor=C_MUTED,   fontName='Helvetica',
                                  spaceAfter=0, leading=14),

    # Table
    'th':           s('th',      fontSize=9,   textColor=C_MUTED,   fontName='Helvetica-Bold',
                                  spaceAfter=0, leading=13, letterSpacing=1.2),
    'td':           s('td',      fontSize=10,  textColor=C_INK,     fontName='Helvetica',
                                  spaceAfter=0, leading=15),
    'td_m':         s('td_m',    fontSize=10,  textColor=C_MUTED,   fontName='Helvetica',
                                  spaceAfter=0, leading=15),

    # Stats
    'stat_big':     s('st_big',  fontSize=30, textColor=C_INDIGO,  fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, leading=34),
    'stat_lbl':     s('st_lbl',  fontSize=9,  textColor=C_MUTED,   fontName='Helvetica',
                                  alignment=TA_CENTER, leading=13),

    # Stack pills (cover)
    'stack_lbl':    s('stk_lbl', fontSize=8,  textColor=C_MUTED,   fontName='Helvetica-Bold',
                                  spaceAfter=6, leading=12, letterSpacing=1.5),

    # Quote / callout
    'quote':        s('qt',      fontSize=12, textColor=C_INK,      fontName='Helvetica-Oblique',
                                  spaceAfter=0, leading=19, leftIndent=16),

    # Results numbered takeaway
    'takeaway_n':   s('tk_n',    fontSize=10.5, textColor=C_INDIGO, fontName='Helvetica-Bold',
                                  spaceAfter=2, leading=15),
    'takeaway_t':   s('tk_t',    fontSize=11,   textColor=C_INK,    fontName='Helvetica-Bold',
                                  spaceAfter=3, leading=16),
    'takeaway_b':   s('tk_b',    fontSize=10,   textColor=C_MUTED,  fontName='Helvetica',
                                  spaceAfter=0, leading=15),

    # CTA box
    'cta_h':        s('cta_h',   fontSize=16, textColor=C_BG,      fontName='Helvetica-Bold',
                                  spaceAfter=6, leading=22),
    'cta_b':        s('cta_b',   fontSize=10, textColor=colors.HexColor('#C7D2FE'),
                                  fontName='Helvetica', spaceAfter=4, leading=15),
    'cta_link':     s('cta_lnk', fontSize=10, textColor=C_BG,      fontName='Helvetica',
                                  alignment=TA_RIGHT, spaceAfter=3, leading=15),
}


# ── Canvas callbacks — header + footer on every page ─────────────

def _draw_header(canvas, page_num):
    """Small-caps breadcrumb top of page."""
    if page_num >= len(PAGES):
        page_num = len(PAGES) - 1
    label, accent = PAGES[page_num]
    y = H - 0.48 * inch

    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.setFillColor(C_MUTED)
    # Left: section label
    canvas.drawString(MARGIN_L, y, label)
    # Right: doc label
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(W - MARGIN_R, y, DOC_LABEL)
    # Rule below
    canvas.setStrokeColor(C_RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, y - 6, W - MARGIN_R, y - 6)


def _draw_footer(canvas, page_num, total):
    """Name + role left, links right, page number far right."""
    y = 0.42 * inch
    # Rule above
    canvas.setStrokeColor(C_RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, y + 14, W - MARGIN_R, y + 14)

    # Left: name + role
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(C_INK)
    canvas.drawString(MARGIN_L, y + 3, AUTHOR)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(MARGIN_L, y - 8, ROLE)

    # Right: contact
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(C_MUTED)
    canvas.drawRightString(W - MARGIN_R, y + 3,  EMAIL)
    canvas.drawRightString(W - MARGIN_R, y - 8,  LINKEDIN)

    # Page number (far right, above rule)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(C_SUBTLE)
    canvas.drawRightString(W - MARGIN_R, y + 20, f'{page_num} / {total}')


# State for tracking logical page number across pages
_page_counter = [0]

def on_page(canvas, doc):
    canvas.saveState()
    _page_counter[0] += 1
    n = _page_counter[0]
    if n > 1:  # cover has no header
        _draw_header(canvas, n - 1)
    _draw_footer(canvas, n, TOTAL_PGS)
    canvas.restoreState()


# ── Custom Flowables ──────────────────────────────────────────────

class HRule(Flowable):
    def __init__(self, color=C_RULE, height=0.5, space_before=0, space_after=8):
        super().__init__()
        self.color = color
        self._h = height
        self.spaceBefore = space_before
        self.spaceAfter  = space_after
    def wrap(self, w, h):
        self.width = w
        return w, self._h
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self._h, fill=1, stroke=0)


class AccentRule(Flowable):
    """Short colored accent bar — used under page titles."""
    def __init__(self, color=C_INDIGO, width=0.4 * inch, height=3):
        super().__init__()
        self._w = width
        self._h = height
        self.color = color
        self.spaceAfter = 10
    def wrap(self, w, h):
        return self._w, self._h
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self._w, self._h, fill=1, stroke=0)


class StackPills(Flowable):
    """Renders a row of rounded pill-shaped tags — light style."""
    def __init__(self, tags, tag_colors=None, height=0.3 * inch):
        super().__init__()
        self.tags        = tags
        self.tag_colors  = tag_colors or {}   # {tag: (bg_color, text_color)}
        self._height     = height
        self.spaceAfter  = 6
    def wrap(self, w, h):
        self.width = w
        return w, self._height
    def draw(self):
        c   = self.canv
        x   = 0
        pad = 10
        for tag in self.tags:
            c.setFont('Helvetica-Bold', 8.5)
            tw = c.stringWidth(tag, 'Helvetica-Bold', 8.5)
            pw = tw + pad * 2
            if x + pw > self.width:
                break
            bg, fg = self.tag_colors.get(tag, (C_IND_BG, C_INDIGO))
            c.setFillColor(bg)
            c.roundRect(x, 1, pw, self._height - 2, 4, fill=1, stroke=0)
            c.setFillColor(fg)
            c.drawString(x + pad, 5, tag)
            x += pw + 5


class StatCard(Flowable):
    """Single stat card — value + label, with top accent bar."""
    def __init__(self, value, label, color=C_INDIGO, width=None, height=0.85 * inch):
        super().__init__()
        self.value   = value
        self.label   = label
        self.color   = color
        self._width  = width
        self._height = height
    def wrap(self, w, h):
        self.width = self._width or w
        return self.width, self._height
    def draw(self):
        c  = self.canv
        w  = self.width
        h  = self._height
        # Card background
        c.setFillColor(C_CARD)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=1)
        # Top color bar
        c.setFillColor(self.color)
        c.roundRect(0, h - 5, w, 5, 3, fill=1, stroke=0)
        # Value
        c.setFillColor(self.color)
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(w / 2, h - 34, self.value)
        # Label (multi-line support)
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica', 8)
        lines = self.label.split('\n')
        for i, line in enumerate(lines):
            c.drawCentredString(w / 2, h - 50 - i * 11, line)


class LeftBorderCard(Flowable):
    """Card with a colored left border — like the pain-point cards in the reference PDF."""
    def __init__(self, title, body, color=C_RED, width=None, height=None):
        super().__init__()
        self.title   = title
        self.body    = body
        self.color   = color
        self._width  = width
        self._height = height or (0.95 * inch)
        self.spaceAfter = 6
    def wrap(self, w, h):
        self.width = self._width or w
        return self.width, self._height
    def draw(self):
        c = self.canv
        w = self.width
        h = self._height
        # Background
        c.setFillColor(C_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=1)
        # Left color border
        c.setFillColor(self.color)
        c.rect(0, 0, 3.5, h, fill=1, stroke=0)
        # Title
        c.setFillColor(C_INK)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(14, h - 20, self.title)
        # Body (wrap manually)
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica', 9)
        words  = self.body.split()
        line   = ''
        y_off  = h - 34
        max_w  = w - 20
        for word in words:
            test = (line + ' ' + word).strip()
            if c.stringWidth(test, 'Helvetica', 9) < max_w:
                line = test
            else:
                c.drawString(14, y_off, line)
                y_off -= 12
                line   = word
        if line:
            c.drawString(14, y_off, line)


class TakeawayBlock(Flowable):
    """Numbered takeaway row — number badge + bold title + body text."""
    def __init__(self, number, title, body, color=C_INDIGO, height=0.75 * inch):
        super().__init__()
        self.number  = number
        self.title   = title
        self.body    = body
        self.color   = color
        self._height = height
        self.spaceAfter = 6
    def wrap(self, w, h):
        self.width = w
        return w, self._height
    def draw(self):
        c = self.canv
        w = self.width
        h = self._height
        # Card bg
        c.setFillColor(C_CARD)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=1)
        # Number badge
        badge_x = 14
        badge_y = h / 2 - 10
        c.setFillColor(self.color)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(badge_x, badge_y + 4, self.number)
        # Title
        c.setFillColor(C_INK)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(50, h - 22, self.title)
        # Body
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica', 9)
        words  = self.body.split()
        line   = ''
        y_off  = h - 36
        max_w  = w - 60
        for word in words:
            test = (line + ' ' + word).strip()
            if c.stringWidth(test, 'Helvetica', 9) < max_w:
                line = test
            else:
                c.drawString(50, y_off, line)
                y_off -= 12
                line   = word
        if line:
            c.drawString(50, y_off, line)


# ── Helper: section page header block (inside story) ─────────────

def section_heading(title_plain, title_accent, subtitle, accent_color=C_INDIGO):
    """Returns a list of flowables for the top of a section page."""
    items = []
    # Two-part title: plain + colored accent word
    title_tbl = Table(
        [[Paragraph(title_plain, S['page_title']),
          Paragraph(title_accent, ParagraphStyle(
              'pg_acc_dyn', fontSize=28, textColor=accent_color,
              fontName='Helvetica-Bold', spaceBefore=0, spaceAfter=4, leading=34))]],
        colWidths=None, hAlign='LEFT',
    )
    title_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    items.append(title_tbl)
    items.append(Spacer(1, 6))
    items.append(Paragraph(subtitle, S['page_intro']))
    items.append(HRule(C_RULE, space_before=2, space_after=14))
    return items


def clean_table(header_row, data_rows, col_widths=None, accent_col=C_INDIGO):
    """Returns a clean light-background table."""
    all_rows = [header_row] + data_rows
    t = Table(all_rows, colWidths=col_widths, hAlign='LEFT', repeatRows=1)
    style = [
        ('BACKGROUND',    (0, 0), (-1, 0),  C_IND_BG),
        ('BACKGROUND',    (0, 1), (-1, -1), C_BG),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_BG, C_CARD]),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  accent_col),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9.5),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 9),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 9),
        ('GRID',          (0, 0), (-1, -1), 0.5, C_RULE),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]
    t.setStyle(TableStyle(style))
    return t


# ════════════════════════════════════════════════════════════════
# STORY
# ════════════════════════════════════════════════════════════════
story = []
SW = USABLE_W   # shorthand


# ────────────────────────────────────────────────────────────────
# PAGE 1 — COVER
# ────────────────────────────────────────────────────────────────

# Case study label
story.append(Paragraph('CASE STUDY  ·  AI Automation  ·  n8n  ·  Airtable  ·  GPT-4o', S['cover_label']))
story.append(Spacer(1, 18))

# Large title
story.append(Paragraph('ReportFlow', S['cover_title']))
story.append(Paragraph('Agency Reporting, Automated.', ParagraphStyle(
    'cv_sub2', fontSize=28, textColor=C_INDIGO, fontName='Helvetica-Bold', leading=34, spaceAfter=12)))
story.append(Spacer(1, 4))
story.append(Paragraph(
    'How I built an end-to-end automation system that pulls live data from 5 marketing '
    'platforms, generates AI-written client summaries with GPT-4o, and delivers branded '
    'reports on a fully automatic weekly schedule — with zero manual steps after setup.',
    S['cover_sub']
))
story.append(Spacer(1, 24))

# Stats row
stat_w = (SW - 12) / 4
stat_row = Table(
    [[StatCard('5',      'data sources\nintegrated',     C_INDIGO, width=stat_w),
      StatCard('6',      'n8n workflows\nproduction-ready', C_VIOLET, width=stat_w),
      StatCard('50 hrs', 'saved per\n10-client agency',  C_GREEN,  width=stat_w),
      StatCard('<$0.10', 'AI cost per\nclient per week', C_AMBER,  width=stat_w)]],
    colWidths=[stat_w + 4] * 4,
    hAlign='LEFT',
)
stat_row.setStyle(TableStyle([
    ('LEFTPADDING',  (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING',   (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING',(0, 0), (-1, -1), 0),
    ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
]))
story.append(stat_row)
story.append(Spacer(1, 24))

# Stack label + pills
story.append(Paragraph('STACK', S['stack_lbl']))
tag_colors = {
    'n8n':               (C_IND_BG, C_INDIGO),
    'GPT-4o':            (C_IND_BG, C_INDIGO),
    'Airtable':          (C_IND_BG, C_INDIGO),
    'Google Analytics':  (colors.HexColor('#F0FDF4'), C_GREEN),
    'Meta Ads API':      (colors.HexColor('#F0FDF4'), C_GREEN),
    'Google Ads API':    (colors.HexColor('#F0FDF4'), C_GREEN),
    'Stripe API':        (colors.HexColor('#FFFBEB'), C_AMBER),
    'Mailchimp API':     (colors.HexColor('#FFFBEB'), C_AMBER),
    'Vanilla JS':        (C_CARD, C_MUTED),
    'Python':            (C_CARD, C_MUTED),
    'WAT Framework':     (C_CARD, C_MUTED),
    'Gmail OAuth2':      (C_CARD, C_MUTED),
}
story.append(StackPills(
    ['n8n', 'GPT-4o', 'Airtable', 'Google Analytics', 'Meta Ads API',
     'Google Ads API', 'Stripe API', 'Mailchimp API'],
    tag_colors, height=0.3 * inch))
story.append(StackPills(
    ['Vanilla JS', 'Python', 'WAT Framework', 'Gmail OAuth2'],
    tag_colors, height=0.3 * inch))

story.append(PageBreak())


# ────────────────────────────────────────────────────────────────
# PAGE 2 — THE PROBLEM
# ────────────────────────────────────────────────────────────────

for fl in section_heading(
    'Marketing agencies waste ',
    '4–6 hours per client',
    'every month on manual reporting — pulling from 5 platforms, calculating trends by hand, '
    'writing the same analysis from scratch. ReportFlow eliminates that entirely.',
    C_RED
):
    story.append(fl)

story.append(Paragraph('PAIN POINTS', S['label']))
story.append(Spacer(1, 6))

pain_data = [
    ('Time sink per client',          C_RED,
     'Manually adapting data from GA4, Meta, Google Ads, Stripe, and Mailchimp into a '
     'single report takes 4–6 hours per client, per month — blocking billable strategy work.'),
    ('Inconsistent output quality',   C_AMBER,
     'Writing quality varies with energy and time pressure. Rushed reports perform worse, '
     'but there is no reliable way to maintain analysis standards at speed.'),
    ('Repetitive, low-leverage work', C_MUTED,
     'The same process — export, paste, calculate, write, format, send — repeated identically '
     'every week. A textbook automation opportunity being ignored.'),
    ('No live view between cycles',   C_INDIGO,
     'Clients have no visibility between monthly PDFs. Every question becomes an email thread '
     'and another hour of an account manager\'s time.'),
]

# 2-column pain cards
for i in range(0, len(pain_data), 2):
    left  = pain_data[i]
    right = pain_data[i + 1] if i + 1 < len(pain_data) else None
    card_h = 0.95 * inch
    card_w = (SW - 6) / 2
    row_items = [LeftBorderCard(left[0], left[2], color=left[1], width=card_w, height=card_h)]
    if right:
        row_items.append(LeftBorderCard(right[0], right[2], color=right[1], width=card_w, height=card_h))
    row_t = Table([row_items], colWidths=[card_w + 3, card_w + 3], hAlign='LEFT')
    row_t.setStyle(TableStyle([
        ('LEFTPADDING',  (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING',   (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(row_t)

story.append(Spacer(1, 12))
story.append(Paragraph('BEFORE  VS.  AFTER', S['label']))
story.append(Spacer(1, 6))

before_items = [
    'Pull data from 5 separate platform dashboards (45–60 min)',
    'Manually calculate week-over-week changes and trends (30 min)',
    'Write narrative analysis and insights from scratch (45 min)',
    'Format into Google Slides / Docs (30 min)',
    'Send and follow up when the client has questions (15 min)',
    'Repeat identically next month',
]
after_items = [
    'Activate six n8n workflows — runs fully automatically',
    'Live data pulled every morning at 6 AM from all 5 platforms',
    'GPT-4o writes a personalised analysis for each client',
    'Branded email report delivered every Monday at 9 AM',
    'Client opens the live dashboard any time — no follow-up needed',
    'Zero manual steps after initial setup',
]

b_paras = [[Paragraph(f'• {t}', S['bullet_m'])] for t in before_items]
a_paras = [[Paragraph(f'• {t}', S['bullet_g'])] for t in after_items]

ba_tbl = Table(
    [[
        Paragraph('BEFORE — MANUAL PROCESS', ParagraphStyle('bh', fontSize=8, textColor=C_RED,
                                              fontName='Helvetica-Bold', leading=12, letterSpacing=1.2)),
        Paragraph('AFTER — REPORTFLOW', ParagraphStyle('ah', fontSize=8, textColor=C_GREEN,
                                         fontName='Helvetica-Bold', leading=12, letterSpacing=1.2)),
    ]] + [[b[0], a[0]] for b, a in zip(b_paras, a_paras)],
    colWidths=[SW / 2 - 3, SW / 2 - 3],
    hAlign='LEFT',
)
ba_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0, 0), (0, 0), C_RED_BG),
    ('BACKGROUND',    (1, 0), (1, 0), C_GRN_BG),
    ('BACKGROUND',    (0, 1), (0, -1), C_BG),
    ('BACKGROUND',    (1, 1), (1, -1), C_BG),
    ('ROWBACKGROUNDS',(0, 1), (0, -1), [C_BG, C_CARD]),
    ('ROWBACKGROUNDS',(1, 1), (1, -1), [C_BG, C_CARD]),
    ('FONTSIZE',      (0, 0), (-1, -1), 9.5),
    ('TOPPADDING',    (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING',   (0, 0), (-1, -1), 10),
    ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ('GRID',          (0, 0), (-1, -1), 0.5, C_RULE),
    ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
]))
story.append(ba_tbl)

story.append(PageBreak())


# ────────────────────────────────────────────────────────────────
# PAGE 3 — WHAT I BUILT
# ────────────────────────────────────────────────────────────────

for fl in section_heading(
    'Built on the ',
    'WAT Framework',
    'AI for thinking, code for doing. '
    'n8n handles deterministic orchestration, GPT-4o handles intelligent analysis, '
    'and a vanilla JS dashboard abstracts all complexity behind a live client view.',
    C_INDIGO
):
    story.append(fl)

story.append(Paragraph('SYSTEM ARCHITECTURE', S['label']))
story.append(Spacer(1, 6))

arch_header = [Paragraph(t, S['th']) for t in ['LAYER', 'TECHNOLOGY', 'WHAT IT DOES']]
arch_rows   = [
    [Paragraph('Data Collection', S['td']),
     Paragraph('n8n + 5 APIs', S['td']),
     Paragraph('Pulls GA4, Meta Ads, Google Ads, Stripe, and Mailchimp every morning at 6 AM', S['td_m'])],
    [Paragraph('Aggregation', S['td']),
     Paragraph('n8n scheduled WFs', S['td']),
     Paragraph('Calculates weekly and monthly channel performance, KPI snapshots, and ROAS', S['td_m'])],
    [Paragraph('AI Analysis', S['td']),
     Paragraph('GPT-4o (OpenAI)', S['td']),
     Paragraph('Writes personalised narrative summaries per client — biggest win, watch, next move', S['td_m'])],
    [Paragraph('Data Storage', S['td']),
     Paragraph('Airtable (6 tables)', S['td']),
     Paragraph('Clients · Campaigns · Revenue · KPI Snapshots · Channel Performance · AI Summaries', S['td_m'])],
    [Paragraph('Delivery', S['td']),
     Paragraph('n8n + Gmail OAuth2', S['td']),
     Paragraph('Branded HTML email sent automatically every Monday at 9 AM', S['td_m'])],
    [Paragraph('Dashboard API', S['td']),
     Paragraph('n8n Webhook REST', S['td']),
     Paragraph('Paginated, CORS-protected read endpoint — serves live data to the frontend', S['td_m'])],
    [Paragraph('Frontend', S['td']),
     Paragraph('Vanilla JS / HTML5', S['td']),
     Paragraph('Zero-dependency live dashboard — charts, campaign table, AI panel, date filters', S['td_m'])],
]
story.append(clean_table(arch_header, arch_rows,
             col_widths=[SW * 0.20, SW * 0.22, SW * 0.58], accent_col=C_INDIGO))
story.append(Spacer(1, 16))

story.append(Paragraph('WAT FRAMEWORK ROLES', S['label']))
story.append(Spacer(1, 6))

wat_w    = (SW - 8) / 3
wat_data = [
    ('W  —  Workflows', C_INDIGO,
     'Markdown SOPs in workflows/ define the objective, required inputs, tool sequence, '
     'and edge case handling. These are the instructions.'),
    ('A  —  Agent', C_VIOLET,
     'I (or Claude) read the workflow, sequence tool calls, handle failures, and update '
     'the workflow when a better method is discovered.'),
    ('T  —  Tools', C_GREEN,
     'Deterministic Python and JS scripts handle execution. Testable, fast, consistent. '
     'AI never does what a script can do reliably.'),
]
wat_cells = []
for title, col, body in wat_data:
    wat_cells.append(
        Table(
            [[Paragraph(title, ParagraphStyle('wt', fontSize=11, textColor=col,
                                               fontName='Helvetica-Bold', leading=15, spaceAfter=6))],
             [Paragraph(body, S['card_body'])]],
            colWidths=[wat_w - 16],
            hAlign='LEFT',
        )
    )

wat_row = Table([wat_cells], colWidths=[wat_w + 4] * 3, hAlign='LEFT')
wat_row.setStyle(TableStyle([
    ('BACKGROUND',   (0, 0), (-1, -1), C_CARD),
    ('GRID',         (0, 0), (-1, -1), 0.5, C_RULE),
    ('TOPPADDING',   (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING',(0, 0), (-1, -1), 10),
    ('LEFTPADDING',  (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
    ('LINEABOVE',    (0, 0), (0, 0), 3, C_INDIGO),
    ('LINEABOVE',    (1, 0), (1, 0), 3, C_VIOLET),
    ('LINEABOVE',    (2, 0), (2, 0), 3, C_GREEN),
]))
story.append(wat_row)

story.append(PageBreak())


# ────────────────────────────────────────────────────────────────
# PAGE 4 — HOW I BUILT IT  (Technical Deep Dive)
# ────────────────────────────────────────────────────────────────

for fl in section_heading(
    '6 workflows. ',
    'Every design decision intentional.',
    'The build was sequenced to de-risk each layer: data model first, read API before writers, '
    'demo mode before live integrations. Here is the full node-by-node breakdown.',
    C_GREEN
):
    story.append(fl)

story.append(Paragraph('N8N WORKFLOW — NODE BREAKDOWN', S['label']))
story.append(Spacer(1, 6))

wf_header = [Paragraph(t, S['th']) for t in ['WF', 'WORKFLOW', 'SCHEDULE', 'WHAT IT DOES']]
wf_rows   = [
    [Paragraph('WF1', S['td']), Paragraph('Daily Data Collection', S['td']),
     Paragraph('6 AM daily', S['td_m']),
     Paragraph('Pulls yesterday\'s data from GA4, Meta, Google Ads, Stripe & Mailchimp → Airtable', S['td_m'])],
    [Paragraph('WF2', S['td']), Paragraph('Weekly Aggregation', S['td']),
     Paragraph('Mon 7 AM', S['td_m']),
     Paragraph('Aggregates last 7 days into Channel Performance table with ROAS and trend', S['td_m'])],
    [Paragraph('WF3', S['td']), Paragraph('Monthly Aggregation', S['td']),
     Paragraph('1st of month', S['td_m']),
     Paragraph('Aggregates last month into Channel Performance — same schema as WF2', S['td_m'])],
    [Paragraph('WF4', S['td']), Paragraph('AI Report Generation', S['td']),
     Paragraph('Mon 8 AM', S['td_m']),
     Paragraph('GPT-4o reads KPI data per client and writes a structured 3-insight summary to Airtable', S['td_m'])],
    [Paragraph('WF5', S['td']), Paragraph('Report Delivery', S['td']),
     Paragraph('Mon 9 AM', S['td_m']),
     Paragraph('Sends AI summary as a branded HTML email to each active client via Gmail OAuth2', S['td_m'])],
    [Paragraph('WF6', S['td']), Paragraph('Dashboard API', S['td']),
     Paragraph('On demand', S['td_m']),
     Paragraph('Webhook endpoint: reads Airtable, returns paginated JSON to the live dashboard', S['td_m'])],
]
story.append(clean_table(wf_header, wf_rows,
             col_widths=[SW * 0.07, SW * 0.22, SW * 0.14, SW * 0.57], accent_col=C_GREEN))
story.append(Spacer(1, 16))

story.append(Paragraph('KEY DESIGN DECISIONS', S['label']))
story.append(Spacer(1, 6))

dd_data = [
    ('WF6 built before WF1–5',
     C_INDIGO,
     'The read API (WF6) was built first so the frontend could run on demo data from day one. '
     'No blocking dependency between backend and UI development.'),
    ('Idempotent data pulls',
     C_GREEN,
     'WF1 always requests only yesterday\'s data. Re-running any workflow never creates duplicate '
     'Airtable rows — safe to retry after any failure.'),
    ('Structured GPT-4o prompting',
     C_VIOLET,
     'The AI prompt is a JSON template, not free text. Each field (insight type, title, body) '
     'maps directly to an Airtable column and a dashboard UI component.'),
    ('Zero-dependency frontend',
     C_AMBER,
     'No React, no bundler, no build step. A single HTML file runs offline with built-in mock '
     'data. Deployable to any static host in seconds — or just opened locally.'),
]

dd_w = (SW - 6) / 2
for i in range(0, len(dd_data), 2):
    l = dd_data[i]
    r = dd_data[i + 1] if i + 1 < len(dd_data) else None
    lc = LeftBorderCard(l[0], l[2], color=l[1], width=dd_w, height=0.9 * inch)
    row_cells = [lc]
    if r:
        row_cells.append(LeftBorderCard(r[0], r[2], color=r[1], width=dd_w, height=0.9 * inch))
    rrow = Table([row_cells], colWidths=[dd_w + 3, dd_w + 3], hAlign='LEFT')
    rrow.setStyle(TableStyle([
        ('LEFTPADDING',  (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING',   (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(rrow)

story.append(PageBreak())


# ────────────────────────────────────────────────────────────────
# PAGE 5 — TECH STACK
# ────────────────────────────────────────────────────────────────

for fl in section_heading(
    'Built on ',
    'proven infrastructure.',
    'No custom servers to maintain. No vendor lock-in. Every tool was chosen for a specific '
    'reason — here is the full stack and the rationale behind each choice.',
    C_AMBER
):
    story.append(fl)

story.append(Paragraph('FULL TECH STACK', S['label']))
story.append(Spacer(1, 6))

st_header = [Paragraph(t, S['th']) for t in ['TOOL', 'ROLE', 'WHY I CHOSE IT']]
st_rows   = [
    [Paragraph('n8n (self-hosted)', S['td']),   Paragraph('Workflow engine',     S['td']),
     Paragraph('Full API access, runs on-prem, no per-execution pricing at scale', S['td_m'])],
    [Paragraph('Airtable',          S['td']),   Paragraph('Data warehouse',      S['td']),
     Paragraph('Structured storage with a visual UI clients can inspect; fast API', S['td_m'])],
    [Paragraph('OpenAI GPT-4o',     S['td']),   Paragraph('AI narrative engine', S['td']),
     Paragraph('Best structured-output accuracy; JSON mode maps cleanly to DB fields', S['td_m'])],
    [Paragraph('Google Analytics 4',S['td']),   Paragraph('Web traffic',         S['td']),
     Paragraph('GA4 Data API v1 — sessions, conversions, revenue by channel', S['td_m'])],
    [Paragraph('Meta Graph API',    S['td']),   Paragraph('Paid social',         S['td']),
     Paragraph('Ad account insights: spend, impressions, CPM, ROAS per campaign', S['td_m'])],
    [Paragraph('Google Ads API',    S['td']),   Paragraph('Search / PMax',       S['td']),
     Paragraph('GAQL queries for clicks, conversions, CPA, and quality score', S['td_m'])],
    [Paragraph('Stripe API',        S['td']),   Paragraph('Revenue data',        S['td']),
     Paragraph('Charges and payment intents with metadata for revenue attribution', S['td_m'])],
    [Paragraph('Mailchimp API v3',  S['td']),   Paragraph('Email performance',   S['td']),
     Paragraph('Campaign reports: open rate, CTR, unsubscribe, revenue per send', S['td_m'])],
    [Paragraph('Vanilla JS / HTML5',S['td']),   Paragraph('Frontend dashboard',  S['td']),
     Paragraph('Zero build overhead; deployable to any static host in seconds', S['td_m'])],
    [Paragraph('Python + reportlab',S['td']),   Paragraph('Doc generation',      S['td']),
     Paragraph('PDF and PPTX outputs are code — version-controlled, not design files', S['td_m'])],
    [Paragraph('Gmail OAuth2',      S['td']),   Paragraph('Email delivery',      S['td']),
     Paragraph('Native Google auth; no third-party mail service dependency', S['td_m'])],
]
story.append(clean_table(st_header, st_rows,
             col_widths=[SW * 0.23, SW * 0.20, SW * 0.57], accent_col=C_AMBER))
story.append(Spacer(1, 14))

story.append(Paragraph('CORE SKILLS DEMONSTRATED', S['label']))
story.append(Spacer(1, 6))

all_tags = {
    'n8n Automation': (C_IND_BG, C_INDIGO), 'API Integration': (C_IND_BG, C_INDIGO),
    'OpenAI / GPT-4o': (C_IND_BG, C_INDIGO), 'Prompt Engineering': (C_IND_BG, C_INDIGO),
    'REST APIs': (C_IND_BG, C_INDIGO), 'Webhook Design': (C_IND_BG, C_INDIGO),
    'Airtable': (colors.HexColor('#F0FDF4'), C_GREEN), 'Data Pipelines': (colors.HexColor('#F0FDF4'), C_GREEN),
    'System Design': (colors.HexColor('#F0FDF4'), C_GREEN), 'OAuth2': (colors.HexColor('#F0FDF4'), C_GREEN),
    'JavaScript (ES6+)': (colors.HexColor('#FFFBEB'), C_AMBER), 'HTML5 / CSS3': (colors.HexColor('#FFFBEB'), C_AMBER),
    'Python': (colors.HexColor('#FFFBEB'), C_AMBER), 'WAT Framework': (C_CARD, C_MUTED),
}
story.append(StackPills(
    ['n8n Automation', 'API Integration', 'OpenAI / GPT-4o', 'Prompt Engineering',
     'REST APIs', 'Webhook Design'],
    all_tags, height=0.3 * inch))
story.append(StackPills(
    ['Airtable', 'Data Pipelines', 'System Design', 'OAuth2',
     'JavaScript (ES6+)', 'HTML5 / CSS3', 'Python', 'WAT Framework'],
    all_tags, height=0.3 * inch))

story.append(PageBreak())


# ────────────────────────────────────────────────────────────────
# PAGE 6 — RESULTS & IMPACT  (last page)
# ────────────────────────────────────────────────────────────────

for fl in section_heading(
    'The system works. ',
    'Every time.',
    'Here is what it proved — and what I can build for you.',
    C_GREEN
):
    story.append(fl)

story.append(Paragraph('MEASURED OUTCOMES', S['label']))
story.append(Spacer(1, 6))

# 3-wide stat row with more breathing room
res_w = (SW - 8) / 3
res_row = Table(
    [[StatCard('50 hrs/mo', 'saved per\n10-client agency', C_INDIGO, width=res_w, height=0.9*inch),
      StatCard('×10 faster', 'report generation\nvs. manual',  C_GREEN,  width=res_w, height=0.9*inch),
      StatCard('100%',        'on-time delivery\nevery week',   C_AMBER,  width=res_w, height=0.9*inch)]],
    colWidths=[res_w + 4] * 3,
    hAlign='LEFT',
)
res_row.setStyle(TableStyle([
    ('LEFTPADDING',  (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING',   (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING',(0, 0), (-1, -1), 0),
]))
story.append(res_row)
story.append(Spacer(1, 16))

# Quote callout
quote_tbl = Table(
    [[Paragraph(
        '"Real scenario: 10 clients × 5 hrs/month = 50 hrs of manual work. '
        'With ReportFlow: those 50 hours become 0. '
        'At $150/hr that\'s $7,500/month in recovered billable capacity — without hiring."',
        S['quote']
    )]],
    colWidths=[SW],
    hAlign='LEFT',
)
quote_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0, 0), (-1, -1), C_IND_BG),
    ('TOPPADDING',   (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING',(0, 0), (-1, -1), 12),
    ('LEFTPADDING',  (0, 0), (-1, -1), 14),
    ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ('LINEBEFORE',   (0, 0), (0, -1), 4, C_INDIGO),
]))
story.append(quote_tbl)
story.append(Spacer(1, 14))

story.append(Paragraph('KEY TAKEAWAYS', S['label']))
story.append(Spacer(1, 6))

takeaways = [
    ('01', 'Separation of concerns is what makes automation reliable',
     'GPT-4o handles content generation (high-variance, creative). n8n and scripts handle '
     'routing, storage, and delivery (zero-variance, testable). Mixing these is how systems become brittle.'),
    ('02', 'Build the read path before the write path',
     'WF6 (the dashboard API) was built first. The frontend ran on demo data from day one. '
     'This removes the most common bottleneck in automation projects: waiting for data before building UI.'),
    ('03', 'Demo mode is a business asset',
     'Three realistic mock clients let you demonstrate the full system to prospects before any live '
     'API is connected. The pitch is live before the product is.'),
    ('04', 'Automation compounds — the first run pays for itself',
     'At $150/hr, one setup eliminates $7,500/month in manual labor for a 10-client agency. '
     'Every subsequent run is pure leverage.'),
]
for num, title, body in takeaways:
    story.append(TakeawayBlock(num, title, body, color=C_INDIGO, height=0.72 * inch))

story.append(Spacer(1, 16))

# CTA box
cta_inner = Table(
    [[
        [
            Paragraph('Want a system like this built\nfor your workflow?', S['cta_h']),
            Spacer(1, 4),
            Paragraph(
                'I design and build AI automation systems that replace hours of '
                'manual work with a single click. n8n · GPT-4o · Custom tools · '
                'Full handoff with documentation.',
                S['cta_b']
            ),
        ],
        [
            Paragraph(EMAIL,    S['cta_link']),
            Paragraph(LINKEDIN, S['cta_link']),
            Paragraph(UPWORK,   S['cta_link']),
        ],
    ]],
    colWidths=[SW * 0.56, SW * 0.44],
    hAlign='LEFT',
)
cta_inner.setStyle(TableStyle([
    ('BACKGROUND',   (0, 0), (-1, -1), C_INDIGO),
    ('TOPPADDING',   (0, 0), (-1, -1), 16),
    ('BOTTOMPADDING',(0, 0), (-1, -1), 16),
    ('LEFTPADDING',  (0, 0), (-1, -1), 16),
    ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
    ('ROUNDEDCORNERS', [6]),
]))
story.append(cta_inner)


# ── Render ────────────────────────────────────────────────────────
_page_counter[0] = 0   # reset before build

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'Saved: {OUT_PATH}')
