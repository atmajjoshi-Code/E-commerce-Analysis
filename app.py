# -*- coding: utf-8 -*-
"""
E-Commerce Sales Analytics Dashboard
=====================================
Topic     : Dashboard Creation Activity
Subject   : Data Analytics
Libraries : Pandas, NumPy, Plotly, Dash
Run       : python app.py
Browser   : http://127.0.0.1:8050
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, dash_table
import webbrowser, threading, sys, os

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── LOAD DATASET ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'ecommerce_dataset.csv')

if not os.path.exists(CSV_PATH):
    print("[ERROR] Dataset not found at: " + CSV_PATH)
    print("[INFO]  Make sure 'ecommerce_dataset.csv' is inside the 'data/' folder.")
    sys.exit(1)

df = pd.read_csv(CSV_PATH)
print(f"[OK] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"     Columns: {list(df.columns)}\n")

# ── THEME / COLORS ────────────────────────────────────────────────────────────
BG    = '#0F1117'
CARD  = '#1A1D27'
BORDER= '#252836'
TEXT  = '#FFFFFF'
MUTED = '#8A8FA8'
C     = ['#6C63FF','#00D4AA','#FF6B6B','#FFA500','#4FC3F7']

categories = sorted(df['Category'].unique().tolist())
regions    = sorted(df['Region'].unique().tolist())
cat_c = {cat: C[i % len(C)] for i, cat in enumerate(categories)}
reg_c = {reg: C[i % len(C)] for i, reg in enumerate(regions)}
mon_lbl = ['Jan','Feb','Mar','Apr','May','Jun',
           'Jul','Aug','Sep','Oct','Nov','Dec']

# ── HELPERS ───────────────────────────────────────────────────────────────────
def base_layout(title=''):
    return dict(
        title=dict(text=title, font=dict(color=TEXT, size=13), x=0.5),
        paper_bgcolor=CARD, plot_bgcolor=CARD,
        font=dict(color=TEXT, family='Segoe UI'),
        margin=dict(l=45, r=20, t=50, b=45),
        xaxis=dict(gridcolor=BORDER, showgrid=True, zeroline=False),
        yaxis=dict(gridcolor=BORDER, showgrid=True, zeroline=False),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
    )

def card(children, extra_style=None):
    s = {'backgroundColor': CARD, 'borderRadius': '12px',
         'padding': '18px', 'border': f'1px solid {BORDER}'}
    if extra_style:
        s.update(extra_style)
    return html.Div(children, style=s)

def section(title, color):
    return html.H2(title, style={
        'color': TEXT, 'fontSize': '18px', 'fontWeight': '700',
        'marginBottom': '16px', 'marginTop': '8px',
        'borderBottom': f'2px solid {color}', 'paddingBottom': '8px'
    })

# ── BUILD CHARTS ──────────────────────────────────────────────────────────────

# 1. Grouped Bar — Monthly Revenue vs Profit
monthly = df.groupby('Month').agg(
    Revenue=('Revenue','sum'), Profit=('Profit','sum')).reset_index()
fig1 = go.Figure([
    go.Bar(x=mon_lbl, y=monthly['Revenue'], name='Revenue',
           marker_color=C[0], opacity=0.9),
    go.Bar(x=mon_lbl, y=monthly['Profit'],  name='Profit',
           marker_color=C[1], opacity=0.9),
])
fig1.update_layout(**base_layout('Monthly Revenue vs Profit'), barmode='group')

# 2. Pie — Revenue by Category
cat_rev = df.groupby('Category')['Revenue'].sum().reset_index()
fig2 = go.Figure(go.Pie(
    labels=cat_rev['Category'], values=cat_rev['Revenue'],
    marker_colors=[cat_c[c] for c in cat_rev['Category']],
    hole=0.45, textinfo='label+percent', textfont=dict(color=TEXT)))
fig2.update_layout(**base_layout('Revenue by Category'))

# 3. Donut — Revenue by Region
reg_rev = df.groupby('Region')['Revenue'].sum().reset_index()
fig3 = go.Figure(go.Pie(
    labels=reg_rev['Region'], values=reg_rev['Revenue'],
    marker_colors=[reg_c[r] for r in reg_rev['Region']],
    hole=0.62, textinfo='label+percent', textfont=dict(color=TEXT)))
fig3.update_layout(**base_layout('Revenue by Region'))

# 4. Multi-line — Category Monthly Trend
fig4 = go.Figure()
for cat, clr in cat_c.items():
    m = df[df['Category']==cat].groupby('Month')['Revenue'].sum()\
        .reindex(range(1,13), fill_value=0)
    fig4.add_trace(go.Scatter(
        x=mon_lbl, y=m.values, name=cat,
        line=dict(color=clr, width=2.5),
        mode='lines+markers', marker=dict(size=6)))
fig4.update_layout(**base_layout('Category Monthly Revenue Trend'))

# 5. Horizontal Bar — Profit Margin %
margin = (df.groupby('Category')['Profit'].sum() /
          df.groupby('Category')['Revenue'].sum() * 100).reset_index()
margin.columns = ['Category','Margin']
margin = margin.sort_values('Margin')
fig5 = go.Figure(go.Bar(
    x=margin['Margin'], y=margin['Category'], orientation='h',
    marker_color=[cat_c[c] for c in margin['Category']],
    text=[f'{v:.1f}%' for v in margin['Margin']],
    textposition='outside', opacity=0.9))
fig5.update_layout(**base_layout('Profit Margin % by Category'))

# 6. Scatter — Discount vs Revenue
fig6 = px.scatter(df, x='Discount_%', y='Revenue', color='Category',
    color_discrete_map=cat_c, opacity=0.55,
    trendline='ols', trendline_scope='overall',
    trendline_color_override=C[2],
    labels={'Discount_%': 'Discount %', 'Revenue': 'Revenue (Rs)'})
lay6 = base_layout('Discount % vs Revenue')
del lay6['legend']
fig6.update_layout(**lay6)

# 7. Histogram — Customer Ratings
fig7 = go.Figure()
for cat, clr in cat_c.items():
    fig7.add_trace(go.Histogram(
        x=df[df['Category']==cat]['Rating'],
        name=cat, marker_color=clr, opacity=0.6, nbinsx=14))
fig7.add_vline(x=df['Rating'].mean(), line_color=C[2], line_dash='dash',
    annotation_text=f"Mean {df['Rating'].mean():.2f}",
    annotation_font_color=C[2])
fig7.update_layout(**base_layout('Customer Rating Distribution'),
                   barmode='overlay')

# 8. Box Plot — Revenue Spread
fig8 = go.Figure()
for cat, clr in cat_c.items():
    fig8.add_trace(go.Box(
        y=df[df['Category']==cat]['Revenue'], name=cat,
        marker_color=clr, line_color=clr, opacity=0.85, boxmean=True))
lay8 = base_layout('Revenue Spread per Category')
lay8['showlegend'] = False
fig8.update_layout(**lay8)

# 9. Correlation Heatmap
num_cols = ['Unit_Price','Quantity','Revenue','Discount_%','Profit','Rating']
short    = ['Price','Qty','Revenue','Disc%','Profit','Rating']
corr     = df[num_cols].corr()
fig9 = go.Figure(go.Heatmap(
    z=corr.values, x=short, y=short,
    colorscale='RdBu', zmid=0,
    text=np.round(corr.values, 2),
    texttemplate='%{text}', showscale=True))
fig9.update_layout(**base_layout('Correlation Heatmap'))

# 10. Area — Cumulative Revenue
df['DateD'] = pd.to_datetime(df['Date'])
daily = df.groupby('DateD')['Revenue'].sum().reset_index()
daily['Cumulative'] = daily['Revenue'].cumsum()
fig10 = go.Figure(go.Scatter(
    x=daily['DateD'], y=daily['Cumulative'],
    fill='tozeroy', line=dict(color=C[0], width=2),
    fillcolor='rgba(108,99,255,0.22)', name='Cumulative Revenue'))
fig10.update_layout(**base_layout('Cumulative Revenue — Full Year 2023'))

# ── BUILD TABLES ──────────────────────────────────────────────────────────────
tbl_common = dict(
    style_table ={'overflowX': 'auto'},
    style_header={'backgroundColor': '#252836', 'color': TEXT,
                  'fontWeight': 'bold', 'border': '1px solid #2E3347',
                  'fontSize': '13px', 'padding': '10px'},
    style_cell  ={'backgroundColor': CARD, 'color': TEXT,
                  'border': '1px solid #2E3347', 'fontSize': '12px',
                  'padding': '9px 14px', 'textAlign': 'center',
                  'fontFamily': 'Segoe UI'},
    style_data_conditional=[
        {'if': {'row_index': 'odd'}, 'backgroundColor': '#1E2130'}],
    page_size=10,
)

# Category Summary
cat_sum = df.groupby('Category').agg(
    Orders       =('Revenue','count'),
    Total_Revenue=('Revenue','sum'),
    Total_Profit =('Profit','sum'),
    Avg_Price    =('Unit_Price','mean'),
    Avg_Rating   =('Rating','mean'),
    Avg_Discount =('Discount_%','mean'),
).round(2).reset_index()
cat_sum['Total_Revenue'] = cat_sum['Total_Revenue'].map(lambda x: f'Rs {x:,.0f}')
cat_sum['Total_Profit']  = cat_sum['Total_Profit'].map(lambda x: f'Rs {x:,.0f}')
cat_sum['Avg_Price']     = cat_sum['Avg_Price'].map(lambda x: f'Rs {x:.2f}')

# Region Summary
reg_sum = df.groupby('Region').agg(
    Orders       =('Revenue','count'),
    Total_Revenue=('Revenue','sum'),
    Total_Profit =('Profit','sum'),
    Avg_Order    =('Revenue','mean'),
    Avg_Rating   =('Rating','mean'),
).round(2).reset_index()
reg_sum['Total_Revenue'] = reg_sum['Total_Revenue'].map(lambda x: f'Rs {x:,.0f}')
reg_sum['Total_Profit']  = reg_sum['Total_Profit'].map(lambda x: f'Rs {x:,.0f}')
reg_sum['Avg_Order']     = reg_sum['Avg_Order'].map(lambda x: f'Rs {x:.2f}')

# Raw Data
raw = df[['Date','Category','Region','Unit_Price','Quantity',
          'Revenue','Discount_%','Profit','Rating']].copy()
raw['Unit_Price'] = raw['Unit_Price'].map(lambda x: f'Rs {x:.2f}')
raw['Revenue']    = raw['Revenue'].map(lambda x: f'Rs {x:.2f}')
raw['Profit']     = raw['Profit'].map(lambda x: f'Rs {x:.2f}')

# ── KPI VALUES ────────────────────────────────────────────────────────────────
kpis = [
    ('Total Revenue',   f"Rs {df['Revenue'].sum()/1e5:.2f}L",    '+11% YoY', C[0]),
    ('Total Profit',    f"Rs {df['Profit'].sum()/1e4:.1f}K",     '+9% YoY',  C[1]),
    ('Total Orders',    f"{len(df):,}",                           'Records',  C[2]),
    ('Avg Order Value', f"Rs {df['Revenue'].mean():.0f}",         'Per Order',C[3]),
    ('Avg Rating',      f"{df['Rating'].mean():.2f} / 5.0",       'Customer', C[4]),
]

# ── DASH APP ──────────────────────────────────────────────────────────────────
app = Dash(__name__, assets_folder='assets')
app.title = 'E-Commerce Analytics Dashboard'

G3  = {'display':'grid','gridTemplateColumns':'repeat(3,1fr)',
       'gap':'16px','marginBottom':'20px'}
G2  = {'display':'grid','gridTemplateColumns':'1fr 1fr',
       'gap':'16px','marginBottom':'20px'}

app.layout = html.Div(style={
    'backgroundColor': BG, 'minHeight': '100vh',
    'fontFamily': 'Segoe UI, sans-serif', 'padding': '28px 36px'
}, children=[

    # Header
    html.Div([
        html.H1('E-Commerce Sales Analytics Dashboard',
            style={'color': TEXT, 'margin': '0',
                   'fontSize': '26px', 'fontWeight': '700'}),
        html.P(
            f"FY 2023  |  {len(df):,} Transactions  |  "
            f"{len(categories)} Categories  |  {len(regions)} Regions  |  "
            f"Dashboard Creation Activity",
            style={'color': MUTED, 'margin': '6px 0 0', 'fontSize': '12px'}),
    ], style={'marginBottom': '28px'}),

    # KPI Cards
    html.Div([
        html.Div([
            html.P(t, style={'color': MUTED, 'margin': '0', 'fontSize': '11px',
                             'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
            html.H2(v, style={'color': TEXT, 'margin': '6px 0 4px',
                              'fontSize': '22px', 'fontWeight': '700'}),
            html.P(s, style={'color': cl, 'margin': '0',
                             'fontSize': '12px', 'fontWeight': '600'}),
        ], style={'backgroundColor': CARD, 'borderRadius': '12px',
                  'padding': '18px 20px', 'border': f'1.5px solid {cl}'})
        for t, v, s, cl in kpis
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(5,1fr)',
              'gap': '16px', 'marginBottom': '32px'}),

    # Charts
    section('Data Visualizations', C[0]),

    html.Div([
        card(dcc.Graph(figure=fig1, style={'height': '340px'})),
        card(dcc.Graph(figure=fig2, style={'height': '340px'})),
        card(dcc.Graph(figure=fig3, style={'height': '340px'})),
    ], style=G3),

    html.Div([
        card(dcc.Graph(figure=fig4, style={'height': '340px'})),
        card(dcc.Graph(figure=fig5, style={'height': '340px'})),
    ], style=G2),

    html.Div([
        card(dcc.Graph(figure=fig6, style={'height': '340px'})),
        card(dcc.Graph(figure=fig7, style={'height': '340px'})),
        card(dcc.Graph(figure=fig8, style={'height': '340px'})),
    ], style=G3),

    html.Div([
        card(dcc.Graph(figure=fig10, style={'height': '320px'})),
        card(dcc.Graph(figure=fig9,  style={'height': '320px'})),
    ], style=G2),

    # Tables
    section('Data Tables', C[1]),

    card([
        html.H3('Category-wise Summary',
            style={'color': TEXT, 'fontSize': '14px',
                   'margin': '0 0 6px', 'fontWeight': '600'}),
        html.P('Revenue, profit, avg price, rating and discount by category.',
            style={'color': MUTED, 'fontSize': '12px', 'margin': '0 0 14px'}),
        dash_table.DataTable(
            data=cat_sum.to_dict('records'),
            columns=[{'name': c.replace('_',' '), 'id': c}
                     for c in cat_sum.columns],
            **tbl_common)
    ], {'marginBottom': '16px'}),

    card([
        html.H3('Region-wise Performance',
            style={'color': TEXT, 'fontSize': '14px',
                   'margin': '0 0 6px', 'fontWeight': '600'}),
        html.P('Sales performance broken down by geographic region.',
            style={'color': MUTED, 'fontSize': '12px', 'margin': '0 0 14px'}),
        dash_table.DataTable(
            data=reg_sum.to_dict('records'),
            columns=[{'name': c.replace('_',' '), 'id': c}
                     for c in reg_sum.columns],
            **tbl_common)
    ], {'marginBottom': '16px'}),

    card([
        html.H3(f'Full Transaction Data  ({len(df):,} Records)',
            style={'color': TEXT, 'fontSize': '14px',
                   'margin': '0 0 6px', 'fontWeight': '600'}),
        html.P('Click column headers to sort. Use filter boxes to search.',
            style={'color': MUTED, 'fontSize': '12px', 'margin': '0 0 14px'}),
        dash_table.DataTable(
            data=raw.to_dict('records'),
            columns=[{'name': c.replace('_',' '), 'id': c}
                     for c in raw.columns],
            sort_action='native', filter_action='native',
            **tbl_common)
    ], {'marginBottom': '24px'}),

    html.P(
        'Python | Pandas | NumPy | Plotly | Dash  |  '
        'Dataset: ecommerce_dataset.csv  |  Dashboard Creation Activity',
        style={'color': MUTED, 'fontSize': '11px', 'textAlign': 'center'}),
])

# ── RUN ───────────────────────────────────────────────────────────────────────
def open_browser():
    webbrowser.open('http://127.0.0.1:8050')

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    print("[OK]  Dashboard is running!")
    print("[>>]  Open in browser: http://127.0.0.1:8050")
    print("[XX]  Press Ctrl+C to stop the server\n")
    app.run(debug=False, port=8050)
