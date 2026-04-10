"""
ReportFlow — Setup Guide PDF Generator
Outputs: .tmp/ReportFlow_Setup_Guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '.tmp')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'ReportFlow_Setup_Guide.pdf')

# ── Colours ──────────────────────────────────────────────────────
C_BG       = colors.HexColor('#0E0D0B')
C_ACCENT   = colors.HexColor('#D4A843')
C_WHITE    = colors.HexColor('#FFFFFF')
C_MUTED    = colors.HexColor('#9A9690')
C_CARD     = colors.HexColor('#1A1815')
C_INDIGO   = colors.HexColor('#6366F1')
C_GREEN    = colors.HexColor('#3ECF8E')
C_RED      = colors.HexColor('#EF4444')
C_BORDER   = colors.HexColor('#2A2824')

W, H = A4  # 595 x 842 pts

# ── Doc setup ────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT_PATH,
    pagesize=A4,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch,
    topMargin=0.9*inch,
    bottomMargin=0.75*inch,
    title='ReportFlow Setup Guide',
    author='ReportFlow',
)

# ── Styles ───────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent='Normal', **kw):
    s = ParagraphStyle(name, parent=base[parent], **kw)
    return s

S = {
    'cover_title': style('cover_title', fontSize=38, textColor=C_WHITE,
                         fontName='Helvetica-Bold', spaceAfter=6, leading=44),
    'cover_sub':   style('cover_sub', fontSize=16, textColor=C_ACCENT,
                         fontName='Helvetica', spaceAfter=4, leading=22),
    'cover_meta':  style('cover_meta', fontSize=12, textColor=C_MUTED,
                         fontName='Helvetica', spaceAfter=0),
    'h1':          style('h1', fontSize=22, textColor=C_WHITE,
                         fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=6, leading=28),
    'h2':          style('h2', fontSize=15, textColor=C_ACCENT,
                         fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=4, leading=20),
    'h3':          style('h3', fontSize=12, textColor=C_GREEN,
                         fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=3, leading=16),
    'body':        style('body', fontSize=10.5, textColor=C_WHITE,
                         fontName='Helvetica', spaceAfter=6, leading=16),
    'muted':       style('muted', fontSize=10, textColor=C_MUTED,
                         fontName='Helvetica', spaceAfter=4, leading=15),
    'bullet':      style('bullet', fontSize=10.5, textColor=C_WHITE,
                         fontName='Helvetica', spaceAfter=3, leading=15,
                         leftIndent=14, firstLineIndent=-14),
    'code':        style('code', fontSize=9.5, textColor=C_GREEN,
                         fontName='Courier', spaceAfter=3, leading=14,
                         leftIndent=10, backColor=C_CARD),
    'warning':     style('warning', fontSize=10, textColor=C_ACCENT,
                         fontName='Helvetica-Bold', spaceAfter=3, leading=14, leftIndent=8),
    'note':        style('note', fontSize=10, textColor=C_MUTED,
                         fontName='Helvetica-Oblique', spaceAfter=3, leading=14, leftIndent=8),
    'toc_item':    style('toc_item', fontSize=11, textColor=C_WHITE,
                         fontName='Helvetica', spaceAfter=5, leading=16),
    'toc_num':     style('toc_num', fontSize=11, textColor=C_ACCENT,
                         fontName='Helvetica-Bold', spaceAfter=5, leading=16),
    'step':        style('step', fontSize=13, textColor=C_WHITE,
                         fontName='Helvetica-Bold', spaceAfter=4, leading=18),
}

# ── Custom Flowables ─────────────────────────────────────────────

class AccentBar(Flowable):
    """Full-width gold accent bar."""
    def __init__(self, height=3):
        Flowable.__init__(self)
        self.height = height
    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height
    def draw(self):
        self.canv.setFillColor(C_ACCENT)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

class SectionDivider(Flowable):
    """Thin muted line."""
    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, 1
    def draw(self):
        self.canv.setFillColor(C_BORDER)
        self.canv.rect(0, 0, self.width, 1, fill=1, stroke=0)

def info_box(text, color=C_ACCENT, icon='ℹ'):
    data = [[Paragraph(f'<b>{icon}  {text}</b>',
                       ParagraphStyle('ib', fontSize=10, textColor=color,
                                      fontName='Helvetica-Bold', leading=14))]]
    t = Table(data, colWidths=[W - 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('BOX',        (0,0), (-1,-1), 0.75, color),
        ('LEFTPADDING',(0,0), (-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ]))
    return t

def step_box(number, title, body_paragraphs):
    """Numbered step card."""
    header = Table(
        [[Paragraph(f'<b>Step {number}</b>',
                    ParagraphStyle('sn', fontSize=10, textColor=C_BG,
                                   fontName='Helvetica-Bold', leading=13)),
          Paragraph(f'<b>{title}</b>',
                    ParagraphStyle('st', fontSize=13, textColor=C_WHITE,
                                   fontName='Helvetica-Bold', leading=16))]],
        colWidths=[55, W - 1.5*inch - 55]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_ACCENT),
        ('BACKGROUND', (1,0), (1,0), C_CARD),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0,0), (-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING',(0,0),(-1,-1), 9),
    ]))

    body_data = [[p] for p in body_paragraphs]
    body_table = Table([[p] for p in [Spacer(1,4)] + body_paragraphs + [Spacer(1,4)]],
                       colWidths=[W - 1.5*inch])
    body_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('LEFTPADDING',(0,0), (-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
        ('BOX',        (0,0), (-1,-1), 0.5, C_BORDER),
    ]))

    return KeepTogether([header, body_table, Spacer(1, 10)])

def code_block(lines):
    """Monospaced code block."""
    data = [[Paragraph(line,
                       ParagraphStyle('cb', fontSize=9, textColor=C_GREEN,
                                      fontName='Courier', leading=14,
                                      leftIndent=0))]
            for line in lines]
    t = Table(data, colWidths=[W - 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('BOX',        (0,0), (-1,-1), 0.5, C_BORDER),
        ('LEFTPADDING',(0,0), (-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    return t

def b(text): return f'<b>{text}</b>'
def acc(text): return f'<font color="#D4A843"><b>{text}</b></font>'
def grn(text): return f'<font color="#3ECF8E">{text}</font>'
def mut(text): return f'<font color="#9A9690">{text}</font>'

def P(text, s='body'): return Paragraph(text, S[s])
def SP(n=6):           return Spacer(1, n)

# ── Background page callback ──────────────────────────────────────
def dark_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Top accent bar
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, H-4, W, 4, fill=1, stroke=0)
    # Bottom bar
    canvas.setFillColor(C_BORDER)
    canvas.rect(0, 0, W, 2, fill=1, stroke=0)
    # Page number (skip cover)
    if doc.page > 1:
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(C_MUTED)
        canvas.drawRightString(W - 0.75*inch, 0.45*inch, f'ReportFlow Setup Guide  ·  {doc.page}')
        canvas.drawString(0.75*inch, 0.45*inch, 'reportflow.io')
    canvas.restoreState()

# ════════════════════════════════════════════════════════════════
# CONTENT
# ════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────
story += [
    SP(80),
    AccentBar(4),
    SP(24),
    Paragraph('<b>ReportFlow</b>', S['cover_title']),
    Paragraph('Setup & User Guide', S['cover_sub']),
    SP(8),
    SectionDivider(),
    SP(12),
    Paragraph('Everything you need to go from zero to fully automated agency reporting.', S['body']),
    SP(6),
    Paragraph(mut('Version 1.0  ·  April 2026  ·  For internal agency use'), S['muted']),
    SP(280),
    SectionDivider(),
    SP(8),
    Paragraph(mut('Confidential. For authorised users only.'), S['muted']),
    PageBreak(),
]

# ── TABLE OF CONTENTS ─────────────────────────────────────────────
story += [
    P(b('Contents'), 'h1'),
    AccentBar(2),
    SP(12),
]

toc = [
    ('1', 'Overview & Architecture',         'What ReportFlow is and how the pieces fit together'),
    ('2', 'Prerequisites',                    'Accounts and API keys you need before starting'),
    ('3', 'Airtable Setup',                   'Creating the database schema'),
    ('4', 'n8n Setup',                        'Installing and importing the 6 workflows'),
    ('5', 'Connecting Your Credentials',      'Linking Airtable, Google, Meta, Stripe, Mailchimp, OpenAI'),
    ('6', 'Dashboard Deployment',             'Hosting the frontend and connecting it to n8n'),
    ('7', 'Adding Your First Client',         'Step-by-step: onboarding a real client'),
    ('8', 'Testing the System',               'Verifying each workflow works correctly'),
    ('9', 'Going Live',                       'Activating all workflows on schedule'),
    ('10','Day-to-Day Usage',                 'What happens automatically, what needs manual attention'),
    ('11','Troubleshooting',                  'Common issues and how to fix them'),
    ('12','Security Checklist',               'Before you share the dashboard with clients'),
]
for num, title, desc in toc:
    row = Table(
        [[Paragraph(acc(num), S['toc_num']),
          Paragraph(b(title), S['toc_item']),
          Paragraph(mut(desc), S['muted'])]],
        colWidths=[30, 175, W - 1.5*inch - 205]
    )
    row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ]))
    story.append(row)
    story.append(SectionDivider())

story.append(PageBreak())

# ── SECTION 1: Overview ───────────────────────────────────────────
story += [
    P('1. Overview & Architecture', 'h1'),
    AccentBar(2), SP(10),
    P('ReportFlow is a fully automated agency reporting system. Once set up, it runs itself — collecting data every morning, aggregating it weekly, generating AI-written analysis, emailing reports to clients, and serving a live dashboard. You never touch a spreadsheet again.'),
    SP(6),
    P(b('The WAT Architecture'), 'h2'),
    P('ReportFlow is built on three layers:'),
    SP(4),
]

arch = [
    ['Layer', 'Component', 'What It Does'],
    ['Workflows', 'n8n (6 JSON files)', 'Orchestration — pulls data, transforms it, triggers AI, sends emails'],
    ['Agents', 'GPT-4o via OpenAI API', 'Reads weekly KPI data and writes personalised client analysis'],
    ['Tools', 'Python scripts', 'Testing, validation, and utility scripts in the tools/ directory'],
]
arch_table = Table(arch, colWidths=[80, 130, W - 1.5*inch - 210])
arch_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0), C_ACCENT),
    ('TEXTCOLOR',    (0,0), (-1,0), C_BG),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 10),
    ('BACKGROUND',   (0,1), (-1,-1), C_CARD),
    ('TEXTCOLOR',    (0,1), (-1,-1), C_WHITE),
    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, colors.HexColor('#201E1A')]),
    ('GRID',         (0,0), (-1,-1), 0.5, C_BORDER),
    ('LEFTPADDING',  (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING',   (0,0), (-1,-1), 7),
    ('BOTTOMPADDING',(0,0), (-1,-1), 7),
    ('VALIGN',       (0,0), (-1,-1), 'TOP'),
]))
story.append(arch_table)
story.append(SP(12))

story += [
    P(b('The 6 Workflows'), 'h2'),
]
wfs = [
    ('WF1', 'Daily Data Collection',       '6:00 AM daily',     'Pulls GA4, Meta, Google Ads, Stripe, Mailchimp → Airtable'),
    ('WF2', 'Weekly Aggregation',          '7:00 AM Monday',    'Aggregates 7 days of data into Channel Performance records'),
    ('WF3', 'Monthly Channel Performance', '8:00 AM 1st of month','Builds monthly channel comparison records'),
    ('WF4', 'AI Report Generation',        '7:00 AM Monday',    'Fetches KPIs + channels → GPT-4o → AI Summary in Airtable'),
    ('WF5', 'Report Delivery',             '10:00 AM Monday',   'Fetches Draft summaries → sends branded email → marks Sent'),
    ('WF6', 'Dashboard API',               'On webhook request', 'Serves live data to the frontend dashboard on demand'),
]
wf_table = Table(
    [['ID', 'Name', 'Schedule', 'Purpose']] + [[a,b,c,d] for a,b,c,d in wfs],
    colWidths=[35, 140, 110, W - 1.5*inch - 285]
)
wf_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), C_INDIGO),
    ('TEXTCOLOR',     (0,0), (-1,0), C_WHITE),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [C_CARD, colors.HexColor('#201E1A')]),
    ('TEXTCOLOR',     (0,1), (-1,-1), C_WHITE),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('GRID',          (0,0), (-1,-1), 0.5, C_BORDER),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story += [wf_table, SP(6),
          info_box('WF4 and WF5 run on Mondays. WF4 generates at 7 AM, WF5 delivers at 10 AM — giving a 3-hour window for AI generation across all clients.'),
          PageBreak()]

# ── SECTION 2: Prerequisites ──────────────────────────────────────
story += [
    P('2. Prerequisites', 'h1'),
    AccentBar(2), SP(10),
    P('You need accounts and API keys for each data source before importing any workflows. Get these set up first — it will save you time later.'),
    SP(8),
]

prereqs = [
    (C_GREEN,  '✓ Required', [
        ('n8n', 'Self-hosted (Docker recommended) or n8n Cloud account', 'n8n.io'),
        ('Airtable', 'Free plan is sufficient for most agencies', 'airtable.com'),
        ('OpenAI', 'API key with GPT-4o access — pay-as-you-go', 'platform.openai.com'),
    ]),
    (C_ACCENT, '✓ Per-client (add as you onboard clients)', [
        ('Google Analytics 4', 'GA4 property + Google Cloud project with Analytics API enabled', 'console.cloud.google.com'),
        ('Meta Business Suite', 'Meta App with ads_read permission + long-lived access token', 'developers.facebook.com'),
        ('Google Ads', 'Google Ads Manager account + Developer Token', 'ads.google.com'),
        ('Stripe', 'API key (restricted read-only key recommended)', 'dashboard.stripe.com/apikeys'),
        ('Mailchimp', 'API key — found under Account → Extras → API Keys', 'mailchimp.com'),
    ]),
]

for color, label, items in prereqs:
    story.append(P(f'<font color="#{color.hexval()[2:]}">{label}</font>', 'h3'))
    for name, desc, url in items:
        row = Table(
            [[Paragraph(f'<b>{name}</b>', ParagraphStyle('pn', fontSize=10, textColor=C_WHITE, fontName='Helvetica-Bold', leading=14)),
              Paragraph(desc, ParagraphStyle('pd', fontSize=10, textColor=C_MUTED, fontName='Helvetica', leading=14)),
              Paragraph(mut(url), ParagraphStyle('pu', fontSize=9, textColor=C_MUTED, fontName='Helvetica-Oblique', leading=13))]],
            colWidths=[110, 230, W - 1.5*inch - 340]
        )
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CARD),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story += [row, SP(4)]

story.append(PageBreak())

# ── SECTION 3: Airtable Setup ─────────────────────────────────────
story += [
    P('3. Airtable Setup', 'h1'),
    AccentBar(2), SP(10),
    P('ReportFlow uses 6 Airtable tables. Create them in a new base. The field names must match exactly — the n8n workflows reference them by name.'),
    SP(8),
]

tables_spec = [
    ('Clients', C_GREEN, [
        ('client_id',     'Single line text', 'Unique ID e.g. brightedge — used in all other tables as the FK'),
        ('company_name',  'Single line text', 'Display name shown on dashboard'),
        ('status',        'Single select',    'Values: Active, Paused, Churned'),
        ('niche',         'Single line text', 'E.g. E-commerce, SaaS, Coaching'),
        ('brand_color',   'Single line text', 'Hex colour for dashboard avatar e.g. #6366F1'),
        ('mailchimp_dc',  'Single line text', 'Datacenter prefix from API key e.g. us14 (after the dash)'),
        ('google_ads_id', 'Single line text', 'Google Ads customer ID without dashes'),
        ('meta_account_id','Single line text','Meta Ad Account ID e.g. act_123456789'),
        ('ga4_property_id','Single line text','GA4 property ID e.g. 123456789'),
        ('stripe_key',    'Single line text', 'Optional: per-client Stripe key if different from default'),
    ]),
    ('KPI Snapshots', C_INDIGO, [
        ('client',         'Single line text', 'client_id value'),
        ('snapshot_date',  'Date',             'Format: YYYY-MM-DD'),
        ('total_revenue',  'Number',           'Decimal'),
        ('ad_spend',       'Number',           'Decimal'),
        ('total_orders',   'Number',           'Integer'),
        ('total_sessions', 'Number',           'Integer'),
        ('source',         'Single line text', 'e.g. ga4, meta, google_ads'),
    ]),
    ('Campaigns', C_ACCENT, [
        ('campaign_id',   'Single line text', 'Platform campaign ID'),
        ('client',        'Single line text', 'client_id value'),
        ('campaign_name', 'Single line text', 'Campaign display name'),
        ('platform',      'Single select',    'meta / google / email / organic'),
        ('status',        'Single select',    'Active / Paused / Ended'),
        ('spend',         'Number',           'Decimal'),
        ('revenue',       'Number',           'Decimal'),
        ('impressions',   'Number',           'Integer'),
        ('clicks',        'Number',           'Integer'),
        ('ctr',           'Number',           'Decimal — percentage'),
        ('cpc',           'Number',           'Decimal'),
        ('roas',          'Number',           'Decimal'),
        ('last_synced',   'Date',             'Date of last data update'),
    ]),
    ('Revenue', C_GREEN, [
        ('client',      'Single line text', 'client_id value'),
        ('week_start',  'Date',             'Monday of the week'),
        ('week_label',  'Single line text', 'e.g. Wk 1, Wk 2'),
        ('revenue',     'Number',           'Total revenue for the week'),
        ('channel',     'Single line text', 'e.g. Stripe, Meta, Google'),
    ]),
    ('Channel Performance', C_INDIGO, [
        ('client',        'Single line text', 'client_id value'),
        ('channel',       'Single line text', 'e.g. Meta Ads, Google Ads, Email'),
        ('period_start',  'Date',             'Start of the aggregation period'),
        ('period_end',    'Date',             'End of the aggregation period'),
        ('total_revenue', 'Number',           'Decimal'),
        ('total_spend',   'Number',           'Decimal'),
        ('roas',          'Number',           'Decimal'),
        ('avg_conv_rate', 'Number',           'Decimal — percentage'),
        ('bar_width_pct', 'Number',           'Integer 0–100, for dashboard bar chart'),
    ]),
    ('AI Summaries', C_ACCENT, [
        ('client',          'Single line text', 'client_id value'),
        ('period_start',    'Date',             'Start of the report period'),
        ('period_end',      'Date',             'End of the report period'),
        ('status',          'Single select',    'Draft / Sent'),
        ('generated_at',    'Date',             'When the AI generated this summary'),
        ('body_html',       'Long text',        'Full HTML body of the AI summary'),
        ('insight_1_title', 'Single line text', 'Biggest Win title'),
        ('insight_1_text',  'Long text',        'Biggest Win body text'),
        ('insight_2_title', 'Single line text', 'Watch Closely title'),
        ('insight_2_text',  'Long text',        'Watch Closely body text'),
        ('insight_3_title', 'Single line text', 'Next Steps title'),
        ('insight_3_text',  'Long text',        'Next Steps body text'),
    ]),
]

for table_name, color, fields in tables_spec:
    story.append(P(f'<font color="#{color.hexval()[2:]}">{table_name}</font>', 'h2'))
    rows = [['Field Name', 'Field Type', 'Notes']]
    for fname, ftype, note in fields:
        rows.append([
            Paragraph(f'<font face="Courier" size="9">{fname}</font>', ParagraphStyle('fn', fontSize=9, fontName='Courier', textColor=C_GREEN, leading=13)),
            Paragraph(ftype, ParagraphStyle('ft', fontSize=9.5, fontName='Helvetica', textColor=C_MUTED, leading=13)),
            Paragraph(note, ParagraphStyle('fn2', fontSize=9.5, fontName='Helvetica', textColor=C_WHITE, leading=13)),
        ])
    t = Table(rows, colWidths=[120, 100, W - 1.5*inch - 220])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), color),
        ('TEXTCOLOR',     (0,0), (-1,0), C_BG),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,0), 10),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, colors.HexColor('#201E1A')]),
        ('GRID',          (0,0), (-1,-1), 0.5, C_BORDER),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    story += [t, SP(10)]

story.append(info_box('After creating all 6 tables, copy the Base ID from the Airtable URL. It starts with "app" — e.g. appXXXXXXXXXXXXXX. You will need it for every n8n workflow.', C_ACCENT, '★'))
story.append(PageBreak())

# ── SECTION 4: n8n Setup ──────────────────────────────────────────
story += [
    P('4. n8n Setup', 'h1'),
    AccentBar(2), SP(10),
    P('Import all 6 workflow files into your n8n instance. Each file is self-contained — no additional nodes or plugins required beyond what n8n ships with.'),
    SP(8),
    step_box('4.1', 'Install n8n', [
        P('The recommended method is Docker:'),
        code_block([
            'docker run -it --rm --name n8n \\',
            '  -p 5678:5678 \\',
            '  -v ~/.n8n:/home/node/.n8n \\',
            '  n8nio/n8n',
        ]),
        P('Or install globally with npm:'),
        code_block(['npm install -g n8n', 'n8n start']),
        P(mut('Then open http://localhost:5678 in your browser.')),
    ]),
    SP(6),
    step_box('4.2', 'Import the Workflows', [
        P('In n8n, go to ' + b('Workflows → New → Import from file') + ' and import each of these files in order:'),
        SP(4),
        *[P(f'  {grn("→")}  {f}', 'bullet') for f in [
            'workflow_1_daily_data_collection.json',
            'workflow_2_weekly_aggregation.json',
            'workflow_3_monthly_channel_performance.json',
            'workflow_4_ai_report_generation.json',
            'workflow_5_report_delivery.json',
            'workflow_6_dashboard_api.json',
        ]],
        SP(4),
        P(mut('Tip: import them all before configuring credentials — you can set credentials once and they apply to all workflows.')),
    ]),
    SP(6),
    step_box('4.3', 'Replace Placeholder Values', [
        P('Search every workflow for these placeholders and replace with your actual values:'),
        SP(4),
    ] + [
        P(f'  {grn("→")}  <font face="Courier" size="9" color="#D4A843">{ph}</font>  {mut("→")}  {desc}', 'bullet')
        for ph, desc in [
            ('YOUR_AIRTABLE_BASE_ID',        'Your Airtable base ID (starts with "app")'),
            ('YOUR_GOOGLE_ADS_DEVELOPER_TOKEN','Your Google Ads Developer Token'),
            ('YOUR_DASHBOARD_DOMAIN',        'The domain where you host the dashboard frontend'),
            ('YOUR_WEBHOOK_SECRET',          'A random secret string you create (e.g. a UUID)'),
        ]
    ]),
    PageBreak(),
]

# ── SECTION 5: Credentials ────────────────────────────────────────
story += [
    P('5. Connecting Your Credentials', 'h1'),
    AccentBar(2), SP(10),
    P('In n8n, go to ' + b('Settings → Credentials') + ' and create one credential for each service. These are shared across all workflows.'),
    SP(8),
]

creds = [
    ('Airtable', C_GREEN, [
        'Go to airtable.com/account → API section',
        'Create a Personal Access Token with scopes: data.records:read, data.records:write, schema.bases:read',
        'In n8n: create an "Airtable Token API" credential and paste the token',
    ]),
    ('OpenAI', C_INDIGO, [
        'Go to platform.openai.com/api-keys',
        'Create a new secret key',
        'In n8n: create an "OpenAI API" credential and paste the key',
        'Ensure your account has GPT-4o access (requires billing set up)',
    ]),
    ('Google (GA4 + Google Ads)', C_ACCENT, [
        'Go to console.cloud.google.com → Create a new project',
        'Enable: Google Analytics Data API, Google Ads API',
        'Create OAuth 2.0 credentials (Web Application type)',
        'In n8n: create a "Google OAuth2 API" credential and complete the OAuth flow',
        'For Google Ads: also add your Developer Token in the workflow HTTP headers',
    ]),
    ('Meta / Facebook', C_RED, [
        'Go to developers.facebook.com → My Apps → Create App',
        'Add the Marketing API product',
        'Generate a long-lived User Access Token with ads_read permission',
        'In n8n: create an "HTTP Header Auth" credential with the token as a Bearer header',
        'Note: Meta tokens expire — set a calendar reminder to refresh every 60 days',
    ]),
    ('Stripe', C_GREEN, [
        'Go to dashboard.stripe.com/apikeys',
        'Create a Restricted Key with: charges:read permission only',
        'In n8n: create an "HTTP Bearer Auth" credential and paste the key',
    ]),
    ('Mailchimp', C_ACCENT, [
        'Go to Mailchimp → Account → Extras → API Keys',
        'Create a new API key',
        'Note the datacenter prefix (e.g. us14) from after the dash in the key',
        'Add mailchimp_dc field to each client record in Airtable (e.g. "us14")',
        'In n8n: create an "HTTP Basic Auth" credential (username: anystring, password: your API key)',
    ]),
    ('Gmail (for WF5 delivery)', C_INDIGO, [
        'In n8n: create a "Gmail OAuth2 API" credential',
        'Complete the Google OAuth flow using the same Google project as GA4',
        'Grant mail sending permissions when prompted',
    ]),
]

for service, color, steps in creds:
    story.append(P(f'<font color="#{color.hexval()[2:]}">{service}</font>', 'h2'))
    for i, step in enumerate(steps):
        story.append(P(f'  {i+1}.  {step}', 'bullet'))
    story.append(SP(6))

story.append(PageBreak())

# ── SECTION 6: Dashboard Deployment ──────────────────────────────
story += [
    P('6. Dashboard Deployment', 'h1'),
    AccentBar(2), SP(10),
    P('The dashboard is a static HTML/JS/CSS site. It has no build step and no server requirements. Deploy it anywhere that serves static files.'),
    SP(8),
    step_box('Option A', 'Netlify (Recommended — free)', [
        P('1.  Drag and drop the ' + b('frontend/') + ' folder onto netlify.com/drop'),
        P('2.  Netlify gives you a URL like ' + mut('https://your-site.netlify.app')),
        P('3.  Update ' + b('YOUR_DASHBOARD_DOMAIN') + ' in WF6 to this URL'),
        P('4.  (Optional) Add a custom domain in Netlify settings'),
    ]),
    SP(6),
    step_box('Option B', 'GitHub Pages (free)', [
        P('1.  Push the ' + b('frontend/') + ' folder contents to a GitHub repo'),
        P('2.  Go to Settings → Pages → Deploy from main branch'),
        P('3.  Your URL will be ' + mut('https://yourusername.github.io/repo-name')),
    ]),
    SP(6),
    step_box('Option C', 'Your own server / VPS', [
        P('Copy the ' + b('frontend/') + ' folder to your web root (e.g. /var/www/html)'),
        P('Any web server works: nginx, Apache, Caddy, or even Python\'s built-in server:'),
        code_block(['cd frontend', 'python -m http.server 8080']),
    ]),
    SP(10),
    P(b('After deploying — connect the dashboard to n8n:'), 'h2'),
    P('1.  Open the dashboard in your browser'),
    P('2.  Click ' + b('Settings') + ' in the left sidebar'),
    P('3.  Enter your n8n base URL (e.g. https://your-n8n.com)'),
    P('4.  Enter your webhook secret (the same value as YOUR_WEBHOOK_SECRET in WF6)'),
    P('5.  Click ' + b('Connect') + ' — the dashboard will switch from demo to live mode'),
    SP(8),
    info_box('The dashboard works in demo mode with no n8n connection. Safe to share the URL with clients before live data is connected.', C_GREEN, '✓'),
    PageBreak(),
]

# ── SECTION 7: Adding Your First Client ──────────────────────────
story += [
    P('7. Adding Your First Client', 'h1'),
    AccentBar(2), SP(10),
    P('Every client needs a record in Airtable and their API credentials in n8n before WF1 can collect their data.'),
    SP(8),
    step_box('7.1', 'Create the Client Record in Airtable', [
        P('Open your Airtable base → Clients table → Add a new record:'),
        SP(4),
        *[P(f'  {grn("→")}  Set {b(f)} to {mut(v)}', 'bullet') for f, v in [
            ('client_id',      'A short unique slug, lowercase, no spaces — e.g. brightedge'),
            ('company_name',   'The client\'s business name'),
            ('status',         'Active'),
            ('niche',          'Their industry — E-commerce, SaaS, etc.'),
            ('brand_color',    'A hex colour for their dashboard avatar — e.g. #6366F1'),
            ('mailchimp_dc',   'The datacenter from their Mailchimp API key — e.g. us14'),
            ('google_ads_id',  'Their Google Ads customer ID (no dashes)'),
            ('meta_account_id','Their Meta Ad Account ID — starts with act_'),
            ('ga4_property_id','Their GA4 property ID — numbers only'),
        ]],
    ]),
    SP(6),
    step_box('7.2', 'Add Their API Credentials to n8n', [
        P('For each of the client\'s platforms, create new credentials in n8n (or update existing ones if you\'re using a shared agency account):'),
        P('Go to ' + b('n8n → Settings → Credentials → New') + ' and follow the steps in Section 5 for each platform.'),
        SP(4),
        info_box('If your agency has one shared Google Ads MCC, one shared Meta Business Manager, and one Stripe account — you only create these credentials once and they work for all clients.', C_INDIGO, '★'),
    ]),
    SP(6),
    step_box('7.3', 'Run WF1 Manually to Test', [
        P('Open WF1 in n8n → click ' + b('Test Workflow') + '.'),
        P('Watch the execution. For each node, check the Output tab shows data.'),
        P('After it completes, open Airtable and verify:'),
        P(f'  {grn("→")}  KPI Snapshots: should have today\'s entry for the client', 'bullet'),
        P(f'  {grn("→")}  Campaigns: should have updated records', 'bullet'),
        P(f'  {grn("→")}  Revenue: should have new weekly records', 'bullet'),
    ]),
    PageBreak(),
]

# ── SECTION 8: Testing ────────────────────────────────────────────
story += [
    P('8. Testing the System', 'h1'),
    AccentBar(2), SP(10),
    P('Run each workflow manually in sequence before activating the schedules. This confirms every credential and API connection works.'),
    SP(8),
]

test_steps = [
    ('WF1', 'Daily Data Collection',
     'Click Test Workflow. Verify KPI Snapshots and Campaigns rows appear in Airtable for your test client.'),
    ('WF2', 'Weekly Aggregation',
     'Click Test Workflow. Verify Channel Performance rows appear in Airtable.'),
    ('WF3', 'Monthly Channel Performance',
     'Click Test Workflow. Verify monthly Channel Performance records appear.'),
    ('WF4', 'AI Report Generation',
     'Click Test Workflow. Verify an AI Summaries row appears in Airtable with status = Draft and body_html populated.'),
    ('WF5', 'Report Delivery',
     'Click Test Workflow. Check your Gmail Sent folder — a branded email should have been delivered to the client address.'),
    ('WF6', 'Dashboard API',
     'Open the dashboard in your browser, enter your n8n URL in Settings, and verify the client selector shows live data.'),
]

for wf, name, check in test_steps:
    row = Table(
        [[Paragraph(f'<b>{wf}</b>', ParagraphStyle('wn', fontSize=11, textColor=C_BG, fontName='Helvetica-Bold', leading=14)),
          Paragraph(f'<b>{name}</b>', ParagraphStyle('wt', fontSize=11, textColor=C_ACCENT, fontName='Helvetica-Bold', leading=14)),
          Paragraph(check, ParagraphStyle('wc', fontSize=10, textColor=C_WHITE, fontName='Helvetica', leading=14))]],
        colWidths=[40, 145, W - 1.5*inch - 185]
    )
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_ACCENT),
        ('BACKGROUND', (1,0), (-1,-1), C_CARD),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story += [row, SP(5)]

story += [SP(8), info_box('Run the Python test script for a faster automated check: python tools/test_wf6.py', C_GREEN, '→'), PageBreak()]

# ── SECTION 9: Going Live ─────────────────────────────────────────
story += [
    P('9. Going Live', 'h1'),
    AccentBar(2), SP(10),
    P('Once all tests pass, activate each workflow on its schedule.'),
    SP(8),
    P('In n8n, open each workflow and click the ' + b('Inactive') + ' toggle to switch it to ' + b('Active') + '. Do this in order:'),
    SP(6),
]

activate_order = [
    ('1st', 'WF6', 'Dashboard API — activate this first so the dashboard works immediately'),
    ('2nd', 'WF1', 'Daily Data Collection — starts running at 6 AM the next morning'),
    ('3rd', 'WF2', 'Weekly Aggregation — runs next Monday at 7 AM'),
    ('4th', 'WF3', 'Monthly Channel Performance — runs on the 1st of next month'),
    ('5th', 'WF4', 'AI Report Generation — runs next Monday at 7 AM'),
    ('6th', 'WF5', 'Report Delivery — runs next Monday at 10 AM'),
]
for order, wf, desc in activate_order:
    story.append(P(f'  {acc(order)}  {b(wf)}  {mut("—")}  {desc}', 'bullet'))
    story.append(SP(3))

story += [
    SP(10),
    info_box('After activating WF1, wait until 6 AM the next morning and check the n8n execution history to confirm it ran successfully. This is the most important workflow — if it fails, no data is collected.', C_ACCENT, '⚠'),
    PageBreak(),
]

# ── SECTION 10: Day-to-Day ────────────────────────────────────────
story += [
    P('10. Day-to-Day Usage', 'h1'),
    AccentBar(2), SP(10),
    P('Once live, almost nothing requires manual action. Here is what happens automatically vs. what you manage.'),
    SP(8),
]

auto = [
    'Data collected every morning at 6 AM from all active clients\' platforms',
    'KPI Snapshots, Campaigns, and Revenue records updated in Airtable daily',
    'Channel Performance aggregated every Monday at 7 AM',
    'AI analysis written for each client every Monday at 7 AM',
    'Branded email reports delivered to clients every Monday at 10 AM',
    'Dashboard updated in real time whenever a client opens it',
]
manual = [
    'Onboarding new clients — add their Airtable record and n8n credentials',
    'Refreshing Meta access tokens — they expire every 60 days',
    'Reviewing AI summaries before delivery — optional but recommended in early weeks',
    'Updating Google Ads API version — versions deprecate every ~12–18 months',
    'Monitoring n8n execution history weekly for any failed runs',
]

row = Table(
    [[Paragraph(grn('Happens Automatically'), ParagraphStyle('ah', fontSize=12, textColor=C_GREEN, fontName='Helvetica-Bold', leading=16)),
      Paragraph(acc('Requires Your Attention'), ParagraphStyle('mh', fontSize=12, textColor=C_ACCENT, fontName='Helvetica-Bold', leading=16))]],
    colWidths=[(W - 1.5*inch)/2, (W - 1.5*inch)/2]
)
row.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), colors.HexColor('#0E1810')),
    ('BACKGROUND', (1,0), (1,0), colors.HexColor('#181408')),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(row)

body_rows = []
max_rows = max(len(auto), len(manual))
for i in range(max_rows):
    left  = auto[i]   if i < len(auto)   else ''
    right = manual[i] if i < len(manual) else ''
    body_rows.append([
        Paragraph(f'✓  {left}'  if left  else '', ParagraphStyle('al', fontSize=10, textColor=C_WHITE, fontName='Helvetica', leading=14)),
        Paragraph(f'→  {right}' if right else '', ParagraphStyle('ml', fontSize=10, textColor=C_MUTED, fontName='Helvetica', leading=14)),
    ])

body = Table(body_rows, colWidths=[(W - 1.5*inch)/2, (W - 1.5*inch)/2])
body.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (0,-1), colors.HexColor('#0E1810')),
    ('BACKGROUND',    (1,0), (1,-1), colors.HexColor('#181408')),
    ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LINEBEFORE',    (1,0), (1,-1), 0.5, C_BORDER),
    ('BOX',           (0,0), (-1,-1), 0.5, C_BORDER),
]))
story += [body, PageBreak()]

# ── SECTION 11: Troubleshooting ───────────────────────────────────
story += [
    P('11. Troubleshooting', 'h1'),
    AccentBar(2), SP(10),
]

issues = [
    ('WF1 fails on GA4 node',
     ['OAuth token has expired — re-authenticate the Google credential in n8n',
      'GA4 property ID is wrong — verify it in Google Analytics → Admin → Property Settings',
      'Analytics Data API not enabled — check Google Cloud Console']),
    ('WF1 fails on Meta node',
     ['Access token expired (60-day limit) — generate a new long-lived token',
      'Ad account ID is wrong — it must start with act_ and match exactly',
      'App permissions changed — re-authorise in Meta App Dashboard']),
    ('WF1 fails on Mailchimp node',
     ['The mailchimp_dc field in Airtable is wrong or missing — check the datacenter prefix',
      'API key has been revoked — generate a new one in Mailchimp account settings']),
    ('WF4 generates empty AI summaries',
     ['No KPI Snapshot data for the period — check WF1 ran successfully first',
      'OpenAI API key has no credit — add billing at platform.openai.com',
      'GPT-4o rate limit hit — WF4 adds a delay between clients but large agencies may need a longer pause']),
    ('WF5 sends no emails',
     ['No AI Summaries with status = Draft — check WF4 ran and wrote records',
      'Gmail credential expired — re-authenticate in n8n',
      'WF5 fired before WF4 finished — the 3-hour gap should prevent this, but check execution history']),
    ('Dashboard shows no data',
     ['n8n URL in Settings is wrong — include the protocol (https://) and no trailing slash',
      'Webhook secret mismatch — must match YOUR_WEBHOOK_SECRET in WF6 exactly',
      'CORS error in browser console — confirm Access-Control-Allow-Origin in WF6 matches your dashboard domain',
      'WF6 not active — activate it in n8n']),
    ('Stripe pagination loop does not stop',
     ['The safety cap limits to 10 pages (1,000 charges) — this is intentional',
      'If you need more than 1,000 charges per day, increase the cap in the Collect Stripe Page Code node']),
]

for problem, solutions in issues:
    story.append(P(acc('⚠  ' + problem), 'h3'))
    for sol in solutions:
        story.append(P(f'  →  {sol}', 'bullet'))
    story.append(SP(6))

story.append(PageBreak())

# ── SECTION 12: Security Checklist ───────────────────────────────
story += [
    P('12. Security Checklist', 'h1'),
    AccentBar(2), SP(10),
    P('Before sharing the dashboard URL with any client, confirm every item below.'),
    SP(8),
]

checklist = [
    (C_GREEN,  'Webhook secret set',         'YOUR_WEBHOOK_SECRET replaced with a real secret in WF6. Same value entered in dashboard Settings.'),
    (C_GREEN,  'CORS domain locked',         'Access-Control-Allow-Origin in WF6 set to your actual dashboard domain, not *.'),
    (C_GREEN,  'Dashboard domain set',       'YOUR_DASHBOARD_DOMAIN replaced in WF6 Respond nodes.'),
    (C_GREEN,  'Airtable base ID set',       'YOUR_AIRTABLE_BASE_ID replaced in all Airtable nodes across all 6 workflows.'),
    (C_GREEN,  'Stripe key is restricted',   'Using a restricted Stripe key with charges:read only — not a full secret key.'),
    (C_ACCENT, 'Meta token rotation',        'Calendar reminder set to refresh Meta access tokens every 60 days.'),
    (C_ACCENT, 'n8n not publicly exposed',   'n8n is behind authentication or only accessible on your internal network / VPN.'),
    (C_ACCENT, '.env not committed',         'API keys are in .env — confirm .env is in .gitignore and never committed.'),
    (C_RED,    'OpenAI spend limit',         'Set a monthly spend limit in OpenAI billing settings to prevent runaway costs.'),
    (C_RED,    'Airtable access scoped',     'Airtable Personal Access Token has minimum required scopes — not full account access.'),
]

for color, title, desc in checklist:
    row = Table(
        [[Paragraph(f'<font color="#{color.hexval()[2:]}">[ ]</font>  <b>{title}</b>', ParagraphStyle('ct', fontSize=11, textColor=C_WHITE, fontName='Helvetica-Bold', leading=15)),
          Paragraph(desc, ParagraphStyle('cd', fontSize=10, textColor=C_MUTED, fontName='Helvetica', leading=14))]],
        colWidths=[160, W - 1.5*inch - 160]
    )
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('BOX', (0,0), (-1,-1), 0.5, color),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    story += [row, SP(5)]

# ── Final page ────────────────────────────────────────────────────
story += [
    PageBreak(),
    SP(120),
    AccentBar(3),
    SP(20),
    Paragraph('<b>ReportFlow</b>', ParagraphStyle('fp', fontSize=28, textColor=C_WHITE, fontName='Helvetica-Bold', leading=34, alignment=TA_CENTER)),
    Paragraph('Set up once. Report forever.', ParagraphStyle('fs', fontSize=16, textColor=C_ACCENT, fontName='Helvetica-Oblique', leading=22, alignment=TA_CENTER)),
    SP(16),
    Paragraph(mut('For support or questions, refer to the workflow documentation in workflows/ or the n8n community forum.'), ParagraphStyle('fm', fontSize=11, textColor=C_MUTED, fontName='Helvetica', leading=16, alignment=TA_CENTER)),
]

# ── Build ─────────────────────────────────────────────────────────
doc.build(story, onFirstPage=dark_page, onLaterPages=dark_page)
print(f'Saved: {OUT_PATH}')
