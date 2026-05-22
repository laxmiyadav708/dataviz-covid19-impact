import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 Global Impact Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

    /* ── Sidebar branding ── */
    .sidebar-brand {
        text-align: center;
        padding: 16px 0 8px 0;
    }
    .sidebar-brand .logo { font-size: 40px; line-height: 1; }
    .sidebar-brand .app-name {
        font-size: 15px; font-weight: 700; color: #e0e0e0;
        margin-top: 6px; letter-spacing: 0.5px;
    }
    .sidebar-brand .app-sub { font-size: 11px; color: #888; margin-top: 2px; }

    /* ── Fix selectbox red border on focus ── */
    div[data-baseweb="select"] > div:focus-within {
        border-color: #9b59b6 !important;
        box-shadow: 0 0 0 1px #9b59b6 !important;
    }

    /* ── KPI Cards ── */
    .kpi-row { display: flex; gap: 16px; margin-bottom: 8px; }
    .kpi-card {
        flex: 1;
        background: linear-gradient(145deg, #1a1a2e, #22223a);
        border-radius: 14px;
        padding: 22px 18px 18px 18px;
        border-left: 5px solid #e74c3c;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        text-align: center;
        min-width: 0;
    }
    .kpi-card.blue   { border-left-color: #3498db; }
    .kpi-card.green  { border-left-color: #2ecc71; }
    .kpi-card.orange { border-left-color: #f39c12; }
    .kpi-icon  { font-size: 22px; margin-bottom: 4px; }
    .kpi-label { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; }
    .kpi-value { font-size: 26px; font-weight: 800; color: #ffffff; font-family: monospace; }
    .kpi-sub   { font-size: 11px; color: #777; margin-top: 5px; }

    /* ── Section title ── */
    .section-title {
        font-size: 20px; font-weight: 700; color: #ddd;
        border-bottom: 2px solid #2e2e4a;
        padding-bottom: 8px; margin: 32px 0 10px 0;
        display: flex; align-items: center; gap: 10px;
    }

    /* ── Insight box ── */
    .insight-box {
        background: #14142a;
        border-left: 4px solid #9b59b6;
        padding: 11px 16px;
        border-radius: 6px;
        color: #bbb;
        font-size: 13.5px;
        margin-bottom: 14px;
        line-height: 1.6;
    }

    /* ── Sidebar tag pills ── */
    .tag-pill {
        display: inline-block;
        background: #2a2a3e;
        color: #aaa;
        font-size: 11px;
        border-radius: 20px;
        padding: 3px 10px;
        margin: 3px 2px;
        border: 1px solid #3d3d5c;
    }

    /* ── Author card ── */
    .author-card {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        margin-top: 8px;
    }
    .author-name { font-size: 14px; font-weight: 700; color: #e0e0e0; }
    .author-sub  { font-size: 12px; color: #888; margin-top: 3px; }
    .author-links { margin-top: 10px; display: flex; justify-content: center; gap: 8px; }
    .author-link {
        background: #2a2a3e; color: #9b59b6 !important;
        padding: 4px 14px; border-radius: 20px; font-size: 12px;
        text-decoration: none; border: 1px solid #9b59b6;
    }
    .author-link:hover { background: #9b59b6; color: white !important; }
</style>
""", unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('country_wise_latest.csv')
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("❌ 'country_wise_latest.csv' not found. Place it in the same folder as app.py.")
        return None

df = load_data()
if df is None:
    st.stop()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Branding
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">🦠</div>
        <div class="app-name">COVID-19 Dashboard</div>
        <div class="app-sub">Global Impact Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Filter
    st.markdown("**Filter by WHO Region**")
    region_options = sorted(df['WHO Region'].dropna().unique().tolist())
    selected_region = st.selectbox(
        label="WHO Region",
        options=['All Regions'] + region_options,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # About
    st.markdown("**About this Dashboard**")
    st.markdown("""
    <div style="font-size:13px; color:#aaa; line-height:1.7;">
    Visualizes the global spread and severity of COVID-19 across 180+ countries using WHO country-wise data.
    </div>
    <div style="margin-top:10px;">
        <span class="tag-pill">Python</span>
        <span class="tag-pill">Pandas</span>
        <span class="tag-pill">Streamlit</span>
        <span class="tag-pill">Plotly</span>
        <span class="tag-pill">Seaborn</span>
    </div>
    <div style="font-size:12px; color:#777; margin-top:10px;">
        <b>Data Source:</b> WHO / Kaggle COVID-19 Dataset
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Author
    st.markdown("""
    <div class="author-card">
        <div class="author-name">👩‍💻 Laxmi</div>
        <div class="author-sub">B.Tech CSE (AI &amp; Analytics)<br>GLA University</div>
        <div class="author-links">
            <a class="author-link" href="https://github.com/laxmiyadav708" target="_blank">GitHub</a>
            <a class="author-link" href="https://www.linkedin.com/in/laxmi-b38100309/" target="_blank">LinkedIn</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Filter Data ───────────────────────────────────────────────────────────────
if selected_region == 'All Regions':
    df_filtered = df.copy()
    region_label = "Global"
else:
    df_filtered = df[df['WHO Region'] == selected_region].copy()
    region_label = selected_region


# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("## 🦠 COVID-19 Global Impact Dashboard")
st.markdown(
    f"<span style='color:#888; font-size:14px;'>Showing data for: </span>"
    f"<span style='color:#9b59b6; font-weight:700; font-size:14px;'>{region_label}</span>",
    unsafe_allow_html=True
)
st.markdown("---")


# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_confirmed = int(df_filtered['Confirmed'].sum())
total_deaths    = int(df_filtered['Deaths'].sum())
total_recovered = int(df_filtered['Recovered'].sum())
total_active    = int(df_filtered['Active'].sum())
global_cfr      = round(total_deaths / total_confirmed * 100, 2) if total_confirmed else 0
global_rr       = round(total_recovered / total_confirmed * 100, 2) if total_confirmed else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-icon">🔵</div>
        <div class="kpi-label">Total Confirmed</div>
        <div class="kpi-value">{total_confirmed:,}</div>
        <div class="kpi-sub">{region_label}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💀</div>
        <div class="kpi-label">Total Deaths</div>
        <div class="kpi-value">{total_deaths:,}</div>
        <div class="kpi-sub">CFR: {global_cfr}%</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-icon">💚</div>
        <div class="kpi-label">Total Recovered</div>
        <div class="kpi-value">{total_recovered:,}</div>
        <div class="kpi-sub">Recovery Rate: {global_rr}%</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">Active Cases</div>
        <div class="kpi-value">{total_active:,}</div>
        <div class="kpi-sub">{region_label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


# ── CHART 1: World Map ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🗺️ 1. Global Case Distribution — World Map</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> The Americas and South-East Asia were the most severely affected by total confirmed cases. <b>Hover over any country</b> to see full stats.</div>', unsafe_allow_html=True)

fig_map = px.choropleth(
    df_filtered,
    locations="Country/Region",
    locationmode="country names",
    color="Confirmed",
    hover_name="Country/Region",
    hover_data={"Confirmed": ":,", "Deaths": ":,", "Recovered": ":,", "Active": ":,"},
    color_continuous_scale="Reds",
    title=f"COVID-19 Confirmed Cases — {region_label}",
)
fig_map.update_layout(
    paper_bgcolor='rgba(14,14,26,1)',
    plot_bgcolor='rgba(14,14,26,1)',
    geo=dict(
        bgcolor='rgba(14,14,26,1)',
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#555",
        showland=True,
        landcolor='rgba(30,30,50,1)',
        showocean=True,
        oceancolor='rgba(10,10,22,1)',
        showlakes=False,
        showcountries=True,
        countrycolor='rgba(80,80,100,0.5)',
    ),
    font=dict(color='white'),
    title_font_size=15,
    height=480,
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_colorbar=dict(
        title=dict(text="Confirmed", font=dict(color='white', size=12)),
        tickfont=dict(color='white', size=10),
        bgcolor='rgba(20,20,40,0.8)',
        bordercolor='#444',
    ),
)
st.plotly_chart(fig_map, use_container_width=True)


# ── CHART 2 & 3: Side by Side ─────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-title">📊 2. Top 10 by Confirmed Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">💡 US, Brazil, and India had the highest absolute case counts globally.</div>', unsafe_allow_html=True)

    df_top10 = df_filtered.nlargest(10, 'Confirmed').sort_values('Confirmed', ascending=True)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    fig2.patch.set_facecolor('#0e0e1a')
    ax2.set_facecolor('#0e0e1a')
    n = max(len(df_top10), 1)
    colors2 = plt.cm.Reds([0.3 + 0.7 * i / n for i in range(1, n + 1)])
    ax2.barh(df_top10['Country/Region'], df_top10['Confirmed'], color=colors2, edgecolor='none')
    ax2.set_xlabel('Confirmed Cases', color='#aaa', fontsize=10)
    ax2.set_title(f'Top 10 — Confirmed ({region_label})', color='white', fontsize=12, pad=10)
    ax2.tick_params(colors='#ccc', labelsize=9)
    for spine in ax2.spines.values():
        spine.set_edgecolor('#2a2a3e')
    ax2.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax2.xaxis.label.set_color('#aaa')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

with col_right:
    st.markdown('<div class="section-title">💚 3. Top 10 by Recovery Rate</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">💡 Countries with >1000 confirmed cases shown. Higher % = better healthcare response.</div>', unsafe_allow_html=True)

    df_rec = df_filtered[df_filtered['Confirmed'] > 1000].copy()
    df_rec['Recovery Rate (%)'] = (df_rec['Recovered'] / df_rec['Confirmed'] * 100).round(2)
    df_top_rec = df_rec.nlargest(10, 'Recovery Rate (%)').sort_values('Recovery Rate (%)', ascending=True)

    fig3, ax3 = plt.subplots(figsize=(7, 5))
    fig3.patch.set_facecolor('#0e0e1a')
    ax3.set_facecolor('#0e0e1a')
    n3 = max(len(df_top_rec), 1)
    colors3 = plt.cm.Greens([0.3 + 0.7 * i / n3 for i in range(1, n3 + 1)])
    ax3.barh(df_top_rec['Country/Region'], df_top_rec['Recovery Rate (%)'], color=colors3, edgecolor='none')
    ax3.set_xlabel('Recovery Rate (%)', color='#aaa', fontsize=10)
    ax3.set_title(f'Top 10 — Recovery Rate ({region_label})', color='white', fontsize=12, pad=10)
    ax3.tick_params(colors='#ccc', labelsize=9)
    for spine in ax3.spines.values():
        spine.set_edgecolor('#2a2a3e')
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)


# ── CHART 4: CFR Box Plot ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">⚠️ 4. Case Fatality Rate by WHO Region</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> Europe had the highest median CFR. The wide spread shows that healthcare capacity, demographics, and reporting practices vary greatly within each region.</div>', unsafe_allow_html=True)

fig4, ax4 = plt.subplots(figsize=(13, 5))
fig4.patch.set_facecolor('#0e0e1a')
ax4.set_facecolor('#0e0e1a')
palette4 = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
sns.boxplot(
    ax=ax4, x='WHO Region', y='Deaths / 100 Cases', data=df,
    palette=palette4, linewidth=1.5,
    flierprops=dict(marker='o', color='#777', markersize=3, alpha=0.6)
)
ax4.set_title('Case Fatality Rate (Deaths per 100 Cases) by WHO Region', color='white', fontsize=13, pad=12)
ax4.set_xlabel('WHO Region', color='#aaa', fontsize=11)
ax4.set_ylabel('Deaths / 100 Cases (%)', color='#aaa', fontsize=11)
ax4.tick_params(colors='#ccc', axis='both', labelsize=9)
ax4.tick_params(axis='x', rotation=12)
for spine in ax4.spines.values():
    spine.set_edgecolor('#2a2a3e')
ax4.yaxis.grid(True, color='#2a2a3e', linestyle='--', alpha=0.6)
ax4.set_axisbelow(True)
plt.tight_layout()
st.pyplot(fig4)
plt.close(fig4)


# ── CHART 5: Deaths vs Recovered Scatter ──────────────────────────────────────
st.markdown('<div class="section-title">🔵 5. Deaths vs Recovered — Country Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> Countries bottom-right = high recovery, low deaths = better outcomes. Bubble size = total confirmed cases. Hover for details.</div>', unsafe_allow_html=True)

df_scatter = df_filtered[df_filtered['Confirmed'] > 500].copy()
fig5 = px.scatter(
    df_scatter, x='Recovered', y='Deaths', size='Confirmed',
    color='WHO Region', hover_name='Country/Region',
    hover_data={'Confirmed': ':,', 'Deaths': ':,', 'Recovered': ':,'},
    title=f'Deaths vs Recovered ({region_label})',
    size_max=55,
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig5.update_layout(
    paper_bgcolor='rgba(14,14,26,1)',
    plot_bgcolor='rgba(18,18,30,1)',
    font=dict(color='white'),
    title_font_size=14,
    height=460,
    xaxis=dict(gridcolor='#2a2a3e', color='#aaa', title_font=dict(color='#aaa')),
    yaxis=dict(gridcolor='#2a2a3e', color='#aaa', title_font=dict(color='#aaa')),
    legend=dict(bgcolor='rgba(20,20,40,0.85)', font=dict(color='white'), bordercolor='#3d3d5c', borderwidth=1),
    margin=dict(l=0, r=0, t=40, b=0),
)
st.plotly_chart(fig5, use_container_width=True)


# ── CHART 6: Acceleration Bar ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 6. Fastest-Growing Countries (1-Week % Increase)</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> These countries showed the sharpest week-over-week case spikes — early signals of emerging outbreaks or new waves.</div>', unsafe_allow_html=True)

df_accel = df_filtered.nlargest(15, '1 week % increase').sort_values('1 week % increase', ascending=True)
fig6, ax6 = plt.subplots(figsize=(13, 6))
fig6.patch.set_facecolor('#0e0e1a')
ax6.set_facecolor('#0e0e1a')
n6 = max(len(df_accel), 1)
colors6 = plt.cm.plasma([0.2 + 0.7 * i / n6 for i in range(1, n6 + 1)])
ax6.barh(df_accel['Country/Region'], df_accel['1 week % increase'], color=colors6, edgecolor='none')
ax6.set_xlabel('1-Week % Increase in Cases', color='#aaa', fontsize=11)
ax6.set_title(f'Top 15 — Fastest Case Growth ({region_label})', color='white', fontsize=13, pad=12)
ax6.tick_params(colors='#ccc', labelsize=9)
for spine in ax6.spines.values():
    spine.set_edgecolor('#2a2a3e')
ax6.xaxis.grid(True, color='#2a2a3e', linestyle='--', alpha=0.5)
ax6.set_axisbelow(True)
plt.tight_layout()
st.pyplot(fig6)
plt.close(fig6)


# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🗃️ Data Explorer</div>', unsafe_allow_html=True)

search_col, count_col = st.columns([3, 1])
with search_col:
    search_country = st.text_input("", placeholder="🔍 Search by country name (e.g. India, Brazil...)", label_visibility="collapsed")
with count_col:
    st.markdown("<div style='padding-top:8px; color:#888; font-size:13px;'>Rows shown:</div>", unsafe_allow_html=True)

df_display = df_filtered.copy()
if search_country:
    df_display = df_display[df_display['Country/Region'].str.contains(search_country, case=False, na=False)]

st.markdown(f"<span style='color:#9b59b6; font-weight:600;'>{len(df_display)}</span> <span style='color:#888; font-size:13px;'>countries</span>", unsafe_allow_html=True)

fmt = {
    'Confirmed': '{:,.0f}', 'Deaths': '{:,.0f}',
    'Recovered': '{:,.0f}', 'Active': '{:,.0f}',
    'Deaths / 100 Cases': '{:.2f}', 'Recovered / 100 Cases': '{:.2f}',
    '1 week % increase': '{:.2f}',
}
st.dataframe(df_display.style.format(fmt), use_container_width=True, height=400)

csv_data = df_display.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name=f'covid19_{region_label.replace(" ", "_").lower()}.csv',
    mime='text/csv',
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding: 8px 0;'>
    <span style='color:#555; font-size:12px;'>Built by </span>
    <span style='color:#9b59b6; font-weight:700; font-size:13px;'>Laxmi</span>
    <span style='color:#555; font-size:12px;'> · B.Tech CSE (AI & Analytics) · GLA University · </span>
    <a href='https://github.com/laxmiyadav708' style='color:#9b59b6; font-size:12px; text-decoration:none;'>GitHub</a>
    <span style='color:#555; font-size:12px;'> · </span>
    <a href='https://www.linkedin.com/in/laxmi-b38100309/' style='color:#9b59b6; font-size:12px; text-decoration:none;'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
