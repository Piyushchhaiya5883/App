import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import re

#PAGE CONFIGURATION
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

#CUSTOM CSS STYLING
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Rajdhani', sans-serif;
        }

        /* Background */
        .stApp {
            background: linear-gradient(135deg, #050f05 0%, #0a1f0a 50%, #050f05 100%);
            color: #e0e0e0;
        }

        /* Main Title */
        .main-title {
            font-family: 'Orbitron', monospace;
            font-size: 2.8rem;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(90deg, #00c853, #b2ff59, #00c853);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
            letter-spacing: 2px;
        }

        .sub-title {
            text-align: center;
            color: #aab4be;
            font-size: 1rem;
            margin-bottom: 2rem;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(178,255,89,0.05));
            border: 1px solid rgba(0,200,83,0.4);
            border-radius: 12px;
            padding: 0.5rem;
            text-align: center;
            margin: 0.5rem 0;
        }

        .metric-card h2 {
            font-family: 'Orbitron', monospace;
            color: #b2ff59;
            font-size: 2rem;
            margin: 0;
        }

        .metric-card p {
            color: #aab4be;
            margin: 0;
            font-size: 0.85rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* Section Headers */
        .section-header {
            font-family: 'Orbitron', monospace;
            color: #00c853;
            font-size: 1.1rem;
            border-left: 4px solid #b2ff59;
            padding-left: 12px;
            margin: 1.5rem 0 1rem 0;
            letter-spacing: 1px;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #00c853, #b2ff59);
            color: #050f05;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            font-size: 0.9rem;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 200, 83, 0.5);

        }

        /* Input Fields */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(0,200,83,0.3) !important;
            border-radius: 8px !important;
            color: #e0e0e0 !important;
            font-family: 'Rajdhani', sans-serif !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a1f0a, #050f05) !important;
            border-right: 1px solid rgba(0,200,83,0.2);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            gap: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 1px;
            color: #aab4be;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, rgba(0,200,83,0.2), rgba(178,255,89,0.1));
            color: #b2ff59 !important;
            border-radius: 8px;
        }

        /* Dataframe */
        .stDataFrame {
            border: 1px solid rgba(0,200,83,0.2);
            border-radius: 10px;
        }

        /* Welcome banner */
        .welcome-banner {
            background: linear-gradient(90deg, rgba(0,200,83,0.2), rgba(178,255,89,0.1), rgba(0,200,83,0.2));
            border: 1px solid rgba(178,255,89,0.3);
            border-radius: 12px;
            padding: 1rem 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .welcome-banner h3 {
            font-family: 'Orbitron', monospace;
            color: #b2ff59;
            margin: 0;
            font-size: 1.1rem;
        }

        /* Selectbox */
        .stSelectbox > div > div {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(0,200,83,0.3) !important;
            border-radius: 8px !important;
            color: #e0e0e0 !important;
        }

        /* Multiselect */
        .stMultiSelect > div > div {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(0,200,83,0.3) !important;
            border-radius: 8px !important;
        }

        /* hide streamlit default menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)



#USER DATA SETUP

FILE_NAME = "users.csv"

REQUIRED_COLS = ["First Name", "Last Name", "Email", "Phone", "Username", "Password"]

def _init_users_file():
    
    needs_reset = False
    if not os.path.exists(FILE_NAME):
        needs_reset = True
    else:
        try:
            existing = pd.read_csv(FILE_NAME)
            if not all(col in existing.columns for col in REQUIRED_COLS):
                needs_reset = True
        except Exception:
            needs_reset = True

    if needs_reset:
        demo = pd.DataFrame([{
            "First Name": "Admin", "Last Name": "User",
            "Email": "admin@supermart.com", "Phone": "9999999999",
            "Username": "admin", "Password": "Admin@123"
        }])
        demo.to_csv(FILE_NAME, index=False)

_init_users_file()

# ── SESSION STATE ──
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "firstname" not in st.session_state:
    st.session_state.firstname = ""

# ── QUERY PARAMS RESTORE (persist login on rerun) ──
if "logged_in" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.username  = st.query_params.get("user", "")
    st.session_state.firstname = st.query_params.get("name", "")


#LOAD & PREPARE DATA
@st.cache_data(show_spinner="Loading Supermart data …")
def load_data():
    df = pd.read_csv("Supermart Grocery Sales.csv")

    # Parse dates (dayfirst for DD-MM-YYYY format)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Order Date"])

    # Derived columns
    df["Year"]            = df["Order Date"].dt.year.astype(int)
    df["Month"]           = df["Order Date"].dt.month
    df["Month Name"]      = df["Order Date"].dt.strftime("%b")
    df["Month_dt"]        = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Quarter"]         = "Q" + df["Order Date"].dt.quarter.astype(str) + " " + df["Year"].astype(str)
    df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
    df["Discount %"]      = (df["Discount"] * 100).round(1)

    return df

df = load_data()

# ── Plotly dark theme helper ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0.2)",
    font=dict(color="#c0d0c0", family="Rajdhani, sans-serif", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
)
GREEN_SCALE  = ["#0a1f0a", "#00c853", "#b2ff59"]
GREEN_SCALE2 = ["#0a1f0a", "#b2ff59", "#00c853"]

def theme(fig, xangle=0):
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(gridcolor="#1a3a1a", zerolinecolor="#1a3a1a", tickangle=xangle)
    fig.update_yaxes(gridcolor="#1a3a1a", zerolinecolor="#1a3a1a")
    return fig


#AUTH PAGES
def signup_page():
    df_users = pd.read_csv(FILE_NAME)
    st.markdown('<div class="section-header">📝 CREATE YOUR ACCOUNT</div>', unsafe_allow_html=True)

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            firstname = st.text_input("First Name", placeholder="Enter first name")
            email     = st.text_input("Email", placeholder="Enter email")
            username  = st.text_input("Username", placeholder="Choose username")
        with col2:
            lastname  = st.text_input("Last Name", placeholder="Enter last name")
            phone     = st.text_input("Phone Number", placeholder="10-digit phone")
            password  = st.text_input("Password", type="password", placeholder="Min 8 chars")

        re_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        submit = st.form_submit_button("🛒 REGISTER NOW")

        if submit:
            if not all([firstname, lastname, email, phone, username, password, re_password]):
                st.error("⚠️ All fields are mandatory!")
            elif password != re_password:
                st.error("⚠️ Passwords do not match!")
            elif len(password) < 8:
                st.error("⚠️ Password must be at least 8 characters!")
            elif not re.search(r"[A-Z]", password):
                st.error("⚠️ Password must have at least one capital letter!")
            elif not re.search(r"[!@#$%*&]", password):
                st.error("⚠️ Password must have at least one special character (!@#$%*&)!")
            elif not re.search(r"[0-9]", password):
                st.error("⚠️ Password must have at least one digit!")
            elif not re.match(r"^\d{10}$", phone):
                st.error("⚠️ Phone must be exactly 10 digits!")
            elif email in df_users["Email"].values:
                st.warning("⚠️ Email already registered. Please login!")
            elif username in df_users["Username"].values:
                st.warning("⚠️ Username already taken. Choose another!")
            else:
                new_user = {
                    "First Name": firstname, "Last Name": lastname,
                    "Email": email, "Phone": phone,
                    "Username": username, "Password": password
                }
                df_users = pd.concat([df_users, pd.DataFrame([new_user])], ignore_index=True)
                df_users.to_csv(FILE_NAME, index=False)
                st.success(f"✅ Welcome {firstname}! Registration successful! Please login.")
                st.balloons()


def login_page():
    df_users = pd.read_csv(FILE_NAME)
    st.markdown('<div class="section-header">🔐 LOGIN TO YOUR ACCOUNT</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit   = st.form_submit_button("🛒 LOGIN")

        if submit:
            if not username or not password:
                st.error("⚠️ Please enter username and password!")
            else:
                user = df_users[
                    (df_users["Username"] == username) &
                    (df_users["Password"] == password)
                ]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.username  = username
                    st.session_state.firstname = user.iloc[0]["First Name"]
                    st.query_params["logged_in"] = "true"
                    st.query_params["user"]       = username
                    st.query_params["name"]       = user.iloc[0]["First Name"]
                    st.success("✅ Login Successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password!")


#MAIN DASHBOARD
def dashboard():

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center; padding:1rem 0;'>
                <div style='font-family:Orbitron,monospace; color:#b2ff59; font-size:1.4rem;'>🛒 SUPERMART</div>
                <div style='color:#aab4be; font-size:0.8rem; letter-spacing:2px;'>SALES ANALYTICS</div>
            </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=["Overview", "Category Analysis", "Region & State",
                     "Customer Insights", "Comparison", "Insights & Export"],
            icons=["speedometer2", "bar-chart-fill", "globe2",
                   "people-fill", "arrow-left-right", "lightbulb-fill"],
            menu_icon="cart3",
            default_index=0,
            styles={
                "container":        {"background-color": "transparent"},
                "icon":             {"color": "#00c853", "font-size": "16px"},
                "nav-link":         {"color": "#aab4be", "font-size": "13px",
                                     "font-family": "Rajdhani, sans-serif",
                                     "font-weight": "600", "letter-spacing": "1px"},
                "nav-link-selected":{"background": "linear-gradient(90deg, rgba(0,200,83,0.3), rgba(178,255,89,0.1))",
                                     "color": "#b2ff59", "border-left": "3px solid #00c853"},
            }
        )

        st.markdown("---")

        # ── Sidebar Filters ──
        st.markdown("<div style='color:#b2ff59; font-family:Orbitron,monospace; font-size:0.75rem; letter-spacing:1px;'>🔍 GLOBAL FILTERS</div>", unsafe_allow_html=True)
        st.markdown("")

        all_years = sorted(df["Year"].dropna().unique().astype(int))
        sel_years = st.multiselect("📅 Year", all_years, default=all_years)

        all_regions = sorted(df["Region"].dropna().unique())
        sel_regions = st.multiselect("🌍 Region", all_regions, default=all_regions)

        all_cats = sorted(df["Category"].dropna().unique())
        sel_cats = st.multiselect("🏷️ Category", all_cats, default=all_cats)

        st.markdown("---")
        st.markdown(f"""
            <div style='text-align:center;'>
                <div style='color:#b2ff59; font-family:Orbitron,monospace; font-size:0.8rem;'>LOGGED IN AS</div>
                <div style='color:#00c853; font-weight:700; font-size:1rem;'>{st.session_state.firstname}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")

        if st.button("LOGOUT"):
            st.session_state.logged_in  = False
            st.session_state.username   = ""
            st.session_state.firstname  = ""
            st.query_params.clear()
            st.rerun()

    # ── Apply filters ──
    dff = df[
        df["Year"].isin(sel_years) &
        df["Region"].isin(sel_regions) &
        df["Category"].isin(sel_cats)
    ].copy()

    # ── PAGE HEADER ──
    st.markdown('<div class="main-title">🛒 SUPERMART ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Grocery Sales — Performance Intelligence</div>', unsafe_allow_html=True)


    if dff.empty:
        st.warning("⚠️ No data for selected filters. Adjust the sidebar filters.")
        return

    #PAGE 1 — OVERVIEW
    if selected == "Overview":

        # KPI Metrics Row
        total_sales    = dff["Sales"].sum()
        total_profit   = dff["Profit"].sum()
        total_orders   = dff["Order ID"].nunique()
        avg_margin     = dff["Profit Margin %"].mean()
        total_customers= dff["Customer Name"].nunique()
        avg_discount   = dff["Discount %"].mean()

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(f'<div class="metric-card"><h2>₹{total_sales/1e6:.1f}M</h2><p>Total Sales</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><h2>₹{total_profit/1e6:.1f}M</h2><p>Total Profit</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><h2>{total_orders:,}</h2><p>Total Orders</p></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><h2>{avg_margin:.1f}%</h2><p>Avg Margin</p></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="metric-card"><h2>{total_customers}</h2><p>Customers</p></div>', unsafe_allow_html=True)
        with c6:
            st.markdown(f'<div class="metric-card"><h2>{avg_discount:.1f}%</h2><p>Avg Discount</p></div>', unsafe_allow_html=True)

        st.markdown("")

        # Sales Over Time (Monthly line chart)
        st.markdown('<div class="section-header">📈 Sales & Profit Over Time (Monthly)</div>', unsafe_allow_html=True)
        monthly = (
            dff.groupby("Month_dt")[["Sales", "Profit"]]
            .sum().reset_index().sort_values("Month_dt")
        )
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=monthly["Month_dt"], y=monthly["Sales"],
            name="Sales", mode="lines+markers",
            line=dict(color="#00c853", width=2.5),
            fill="tozeroy", fillcolor="rgba(0,200,83,0.08)",
            marker=dict(size=7)
        ))
        fig_line.add_trace(go.Scatter(
            x=monthly["Month_dt"], y=monthly["Profit"],
            name="Profit", mode="lines+markers",
            line=dict(color="#b2ff59", width=2.5),
            fill="tozeroy", fillcolor="rgba(178,255,89,0.05)",
            marker=dict(size=7)
        ))
        fig_line.update_layout(
            height=340,
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
            xaxis_title="Month", yaxis_title="Amount (₹)",
            **PLOT_LAYOUT
        )
        theme(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

        # Year-wise summary table
        st.markdown('<div class="section-header">📊 Year-Wise Performance Summary</div>', unsafe_allow_html=True)
        yearly = (
            dff.groupby("Year")
            .agg(Total_Sales=("Sales","sum"), Total_Profit=("Profit","sum"),
                 Orders=("Order ID","count"), Avg_Margin=("Profit Margin %","mean"))
            .reset_index().sort_values("Year", ascending=False)
        )
        yearly["Total_Sales"]  = yearly["Total_Sales"].map("₹{:,.0f}".format)
        yearly["Total_Profit"] = yearly["Total_Profit"].map("₹{:,.0f}".format)
        yearly["Avg_Margin"]   = yearly["Avg_Margin"].map("{:.2f}%".format)
        yearly.columns = ["Year", "Total Sales", "Total Profit", "Orders", "Avg Margin"]
        st.dataframe(yearly, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">🏷️ Sales Share by Category</div>', unsafe_allow_html=True)
            cat_sales = dff.groupby("Category")["Sales"].sum().reset_index()
            fig_pie = px.pie(
                cat_sales, names="Category", values="Sales", hole=0.45,
                color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6","#00e5ff","#76ff03","#ccff90"],
                template="plotly_dark"
            )
            fig_pie.update_traces(textposition="outside", textinfo="percent+label", pull=[0.04]*len(cat_sales))
            fig_pie.update_layout(height=380, showlegend=False, **PLOT_LAYOUT)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">🌍 Sales by Region</div>', unsafe_allow_html=True)
            reg_sales = dff.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
            fig_reg = px.bar(
                reg_sales, x="Region", y="Sales",
                color="Sales", color_continuous_scale=GREEN_SCALE,
                text="Sales", template="plotly_dark"
            )
            fig_reg.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig_reg.update_layout(height=380, showlegend=False, coloraxis_showscale=False,
                                  xaxis_title="", yaxis_title="Sales (₹)", **PLOT_LAYOUT)
            theme(fig_reg)
            st.plotly_chart(fig_reg, use_container_width=True)

    #PAGE 2 — CATEGORY ANALYSIS
    elif selected == "Category Analysis":
        st.markdown('<div class="section-header">🏷️ CATEGORY PERFORMANCE</div>', unsafe_allow_html=True)

        # Category selector
        cat_choice = st.selectbox("Select Category to Drill Down", ["All"] + sorted(dff["Category"].unique()))
        drill = dff if cat_choice == "All" else dff[dff["Category"] == cat_choice]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">🏆 Top Sub-Categories by Sales</div>', unsafe_allow_html=True)
            top_sub = drill.groupby("Sub Category")["Sales"].sum().nlargest(10).reset_index().sort_values("Sales")
            fig = px.bar(top_sub, x="Sales", y="Sub Category", orientation="h",
                         color="Sales", color_continuous_scale=GREEN_SCALE, text="Sales",
                         template="plotly_dark")
            fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig.update_layout(height=420, coloraxis_showscale=False,
                              xaxis_title="Sales (₹)", yaxis_title="", **PLOT_LAYOUT)
            theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">💰 Top Sub-Categories by Profit</div>', unsafe_allow_html=True)
            top_profit = drill.groupby("Sub Category")["Profit"].sum().nlargest(10).reset_index().sort_values("Profit")
            fig2 = px.bar(top_profit, x="Profit", y="Sub Category", orientation="h",
                          color="Profit", color_continuous_scale=GREEN_SCALE2, text="Profit",
                          template="plotly_dark")
            fig2.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig2.update_layout(height=420, coloraxis_showscale=False,
                               xaxis_title="Profit (₹)", yaxis_title="", **PLOT_LAYOUT)
            theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        # Treemap
        st.markdown('<div class="section-header">🌳 Sales Treemap — Category → Sub-Category</div>', unsafe_allow_html=True)
        tree_data = dff.groupby(["Category","Sub Category"])["Sales"].sum().reset_index()
        fig_tree = px.treemap(
            tree_data, path=["Category","Sub Category"], values="Sales",
            color="Sales", color_continuous_scale=GREEN_SCALE,
            template="plotly_dark"
        )
        fig_tree.update_layout(height=420, **PLOT_LAYOUT)
        st.plotly_chart(fig_tree, use_container_width=True)

        # Monthly trend by category
        st.markdown('<div class="section-header">📈 Monthly Sales Trend by Category</div>', unsafe_allow_html=True)
        cat_monthly = dff.groupby(["Month_dt","Category"])["Sales"].sum().reset_index()
        fig_cat_line = px.line(
            cat_monthly, x="Month_dt", y="Sales", color="Category",
            markers=True, template="plotly_dark",
            color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6","#00e5ff","#76ff03","#ccff90"]
        )
        fig_cat_line.update_traces(line_width=2, marker_size=6)
        fig_cat_line.update_layout(height=360, xaxis_title="Month", yaxis_title="Sales (₹)", **PLOT_LAYOUT)
        theme(fig_cat_line)
        st.plotly_chart(fig_cat_line, use_container_width=True)

        # Discount vs Margin grouped bar
        st.markdown('<div class="section-header">🔖 Discount vs Avg Profit Margin by Category</div>', unsafe_allow_html=True)
        disc_cat = dff.groupby("Category").agg(
            Avg_Discount=("Discount %","mean"),
            Avg_Margin=("Profit Margin %","mean")
        ).reset_index()
        fig_disc = go.Figure()
        fig_disc.add_trace(go.Bar(x=disc_cat["Category"], y=disc_cat["Avg_Discount"],
                                  name="Avg Discount %", marker_color="#00c853"))
        fig_disc.add_trace(go.Bar(x=disc_cat["Category"], y=disc_cat["Avg_Margin"],
                                  name="Avg Margin %",   marker_color="#b2ff59"))
        fig_disc.update_layout(barmode="group", height=340,
                               xaxis_title="", yaxis_title="%",
                               legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                               **PLOT_LAYOUT)
        theme(fig_disc, xangle=-20)
        st.plotly_chart(fig_disc, use_container_width=True)

    #PAGE 3 — REGION & STATE
    elif selected == "Region & State":
        # st.markdown('<div class="section-header">🌍 REGION & STATE PERFORMANCE</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # Region-wise Sales Pie
            st.markdown('<div class="section-header">🥧 Region-Wise Sales Share</div>', unsafe_allow_html=True)
            reg_sales = dff.groupby("Region")["Sales"].sum().reset_index()
            fig_pie = px.pie(reg_sales, names="Region", values="Sales", hole=0.45,
                             color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6","#00e5ff"],
                             template="plotly_dark")
            fig_pie.update_traces(textposition="outside", textinfo="percent+label", pull=[0.04]*5)
            fig_pie.update_layout(height=380, showlegend=True, **PLOT_LAYOUT)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Region-wise Profit Donut
            st.markdown('<div class="section-header">🍩 Region-Wise Profit Share</div>', unsafe_allow_html=True)
            reg_profit = dff.groupby("Region")["Profit"].sum().reset_index()
            fig_donut = px.pie(reg_profit, names="Region", values="Profit", hole=0.55,
                               color_discrete_sequence=["#b2ff59","#00c853","#69f0ae","#1de9b6","#76ff03"],
                               template="plotly_dark")
            fig_donut.update_traces(textposition="outside", textinfo="percent+label", pull=[0.04]*5)
            fig_donut.update_layout(height=380, showlegend=True, **PLOT_LAYOUT)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Region × Category heatmap-style grouped bar
        st.markdown('<div class="section-header">📊 Sales by Region & Category</div>', unsafe_allow_html=True)
        reg_cat = dff.groupby(["Region","Category"])["Sales"].sum().reset_index()
        fig_rc = px.bar(reg_cat, x="Region", y="Sales", color="Category", barmode="group",
                        color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6","#00e5ff","#76ff03","#ccff90"],
                        template="plotly_dark")
        fig_rc.update_layout(height=360, xaxis_title="", yaxis_title="Sales (₹)",
                             legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                             **PLOT_LAYOUT)
        theme(fig_rc)
        st.plotly_chart(fig_rc, use_container_width=True)

        # Region monthly trend
        st.markdown('<div class="section-header">📈 Region-Wise Monthly Sales Trend</div>', unsafe_allow_html=True)
        reg_monthly = dff.groupby(["Month_dt","Region"])["Sales"].sum().reset_index()
        fig_rl = px.line(reg_monthly, x="Month_dt", y="Sales", color="Region",
                         markers=True, template="plotly_dark",
                         color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6","#00e5ff"])
        fig_rl.update_traces(line_width=2.5, marker_size=7)
        fig_rl.update_layout(height=360, xaxis_title="Month", yaxis_title="Sales (₹)",
                              legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                              **PLOT_LAYOUT)
        theme(fig_rl)
        st.plotly_chart(fig_rl, use_container_width=True)

        # Win % style win/loss → high/low profit margin regions
        st.markdown('<div class="section-header">📉 Profit Margin vs Discount by Region</div>', unsafe_allow_html=True)
        reg_disc = dff.groupby("Region").agg(
            Avg_Discount=("Discount %","mean"),
            Avg_Margin=("Profit Margin %","mean")
        ).reset_index()
        melt = reg_disc.melt(id_vars="Region", var_name="Metric", value_name="Value")
        fig_rd = px.bar(melt, x="Region", y="Value", color="Metric", barmode="group",
                        color_discrete_map={"Avg_Discount":"#00c853","Avg_Margin":"#b2ff59"},
                        template="plotly_dark")
        fig_rd.update_layout(height=340, xaxis_title="", yaxis_title="%",
                              legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                              **PLOT_LAYOUT)
        theme(fig_rd)
        st.plotly_chart(fig_rd, use_container_width=True)

    #PAGE 4 — CUSTOMER INSIGHTS
    elif selected == "Customer Insights":
        st.markdown('<div class="section-header">👤 CUSTOMER PERFORMANCE</div>', unsafe_allow_html=True)

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            region_f = st.multiselect("Filter by Region", dff["Region"].unique(), default=list(dff["Region"].unique()))
        with col2:
            cat_f = st.multiselect("Filter by Category", dff["Category"].unique(), default=list(dff["Category"].unique()))

        cust_df = dff[dff["Region"].isin(region_f) & dff["Category"].isin(cat_f)]

        # Customer summary table
        cust_summary = (
            cust_df.groupby("Customer Name")
            .agg(Total_Sales=("Sales","sum"), Total_Profit=("Profit","sum"),
                 Orders=("Order ID","count"), Avg_Margin=("Profit Margin %","mean"))
            .reset_index().sort_values("Total_Sales", ascending=False)
        )
        st.dataframe(cust_summary.style.format({
            "Total_Sales": "₹{:,.0f}", "Total_Profit": "₹{:,.0f}", "Avg_Margin": "{:.1f}%"
        }), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">🏅 Top 10 Customers by Sales</div>', unsafe_allow_html=True)
            top_cust = cust_summary.nlargest(10, "Total_Sales").sort_values("Total_Sales")
            fig = px.bar(top_cust, x="Total_Sales", y="Customer Name", orientation="h",
                         color="Total_Sales", color_continuous_scale=GREEN_SCALE,
                         text="Total_Sales", template="plotly_dark")
            fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig.update_layout(height=420, coloraxis_showscale=False,
                              xaxis_title="Sales (₹)", yaxis_title="", **PLOT_LAYOUT)
            theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">💎 Top 10 Customers by Profit</div>', unsafe_allow_html=True)
            top_prof = cust_summary.nlargest(10, "Total_Profit").sort_values("Total_Profit")
            fig2 = px.bar(top_prof, x="Total_Profit", y="Customer Name", orientation="h",
                          color="Total_Profit", color_continuous_scale=GREEN_SCALE2,
                          text="Total_Profit", template="plotly_dark")
            fig2.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig2.update_layout(height=420, coloraxis_showscale=False,
                               xaxis_title="Profit (₹)", yaxis_title="", **PLOT_LAYOUT)
            theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        # Sales vs Profit scatter per customer
        st.markdown('<div class="section-header">🔬 Sales vs Profit Scatter (per Customer)</div>', unsafe_allow_html=True)
        fig_sc = px.scatter(
            cust_summary, x="Total_Sales", y="Total_Profit",
            size="Orders", color="Avg_Margin",
            hover_name="Customer Name",
            color_continuous_scale=GREEN_SCALE,
            template="plotly_dark", opacity=0.85
        )
        fig_sc.update_layout(height=400, xaxis_title="Total Sales (₹)",
                              yaxis_title="Total Profit (₹)", **PLOT_LAYOUT)
        theme(fig_sc)
        st.plotly_chart(fig_sc, use_container_width=True)

    #PAGE 5 — COMPARISON (Category vs Category)
    elif selected == "Comparison":
        st.markdown('<div class="section-header">⚔️ CATEGORY VS CATEGORY COMPARISON</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        all_cats_list = sorted(dff["Category"].unique())
        with col1:
            cat1 = st.selectbox("Select Category 1", all_cats_list, index=0, key="c1")
        with col2:
            cat2 = st.selectbox("Select Category 2", all_cats_list, index=1, key="c2")

        if cat1 != cat2:
            d1 = dff[dff["Category"] == cat1]
            d2 = dff[dff["Category"] == cat2]

            def cat_stats(d):
                return {
                    "Total Sales (₹)":  d["Sales"].sum(),
                    "Total Profit (₹)": d["Profit"].sum(),
                    "Orders":           d["Order ID"].count(),
                    "Avg Margin (%)":   d["Profit Margin %"].mean(),
                    "Avg Discount (%)": d["Discount %"].mean(),
                    "Unique Sub-Cats":  d["Sub Category"].nunique(),
                }

            s1, s2 = cat_stats(d1), cat_stats(d2)

            # Side-by-side cards
            col1c, col2c = st.columns(2)
            with col1c:
                st.markdown(f'<div class="metric-card"><h2 style="font-size:1.4rem;">{cat1}</h2><p>Category 1</p></div>', unsafe_allow_html=True)
                st.markdown("")
                for k, v in s1.items():
                    val = f"₹{v:,.0f}" if "₹" in k else (f"{v:.1f}%" if "%" in k else f"{int(v):,}")
                    st.markdown(f'<div class="metric-card" style="margin:4px 0;"><h2 style="font-size:1.3rem;">{val}</h2><p>{k}</p></div>', unsafe_allow_html=True)

            with col2c:
                st.markdown(f'<div class="metric-card"><h2 style="font-size:1.4rem;">{cat2}</h2><p>Category 2</p></div>', unsafe_allow_html=True)
                st.markdown("")
                for k, v in s2.items():
                    val = f"₹{v:,.0f}" if "₹" in k else (f"{v:.1f}%" if "%" in k else f"{int(v):,}")
                    st.markdown(f'<div class="metric-card" style="margin:4px 0;"><h2 style="font-size:1.3rem;">{val}</h2><p>{k}</p></div>', unsafe_allow_html=True)

            st.markdown("")

            # Comparison grouped bar
            st.markdown('<div class="section-header">📊 Side-by-Side Stats Comparison</div>', unsafe_allow_html=True)
            compare_df = pd.DataFrame({
                "Metric": list(s1.keys()),
                cat1:     list(s1.values()),
                cat2:     list(s2.values()),
            })
            melted = compare_df.melt(id_vars="Metric", var_name="Category", value_name="Value")
            fig_bar = px.bar(melted, x="Metric", y="Value", color="Category", barmode="group",
                             color_discrete_map={cat1: "#00c853", cat2: "#b2ff59"},
                             template="plotly_dark",
                             title=f"{cat1}  vs  {cat2} — Stats Comparison")
            fig_bar.update_layout(height=400, xaxis_title="", yaxis_title="",
                                  legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                                  **PLOT_LAYOUT)
            theme(fig_bar, xangle=-15)
            st.plotly_chart(fig_bar, use_container_width=True)


            # Monthly trend comparison
            st.markdown('<div class="section-header">📈 Monthly Sales Trend Comparison</div>', unsafe_allow_html=True)
            m1 = d1.groupby("Month_dt")["Sales"].sum().reset_index().rename(columns={"Sales": cat1})
            m2 = d2.groupby("Month_dt")["Sales"].sum().reset_index().rename(columns={"Sales": cat2})
            merged = pd.merge(m1, m2, on="Month_dt", how="outer").sort_values("Month_dt").fillna(0)
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=merged["Month_dt"], y=merged[cat1], name=cat1,
                                            mode="lines+markers", line=dict(color="#00c853", width=2.5), marker=dict(size=7)))
            fig_trend.add_trace(go.Scatter(x=merged["Month_dt"], y=merged[cat2], name=cat2,
                                            mode="lines+markers", line=dict(color="#b2ff59", width=2.5), marker=dict(size=7)))
            fig_trend.update_layout(height=360, xaxis_title="Month", yaxis_title="Sales (₹)",
                                     legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
                                     **PLOT_LAYOUT)
            theme(fig_trend)
            st.plotly_chart(fig_trend, use_container_width=True)

        else:
            st.warning("⚠️ Please select two different categories to compare!")

    #PAGE 6 — INSIGHTS & EXPORT
    elif selected == "Insights & Export":
        st.markdown('<div class="section-header">💡 KEY SALES INSIGHTS</div>', unsafe_allow_html=True)

        # Auto-derived insight cards (top row)
        top_cat     = dff.groupby("Category")["Sales"].sum().idxmax()
        top_subcat  = dff.groupby("Sub Category")["Sales"].sum().idxmax()
        top_cust    = dff.groupby("Customer Name")["Sales"].sum().idxmax()
        top_region  = dff.groupby("Region")["Sales"].sum().idxmax()
        best_margin = dff.groupby("Category")["Profit Margin %"].mean().idxmax()
        worst_disc  = dff.groupby("Category")["Discount %"].mean().idxmax()

        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{top_cat}</h2><p>🏆 Top Category (Sales)</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{top_subcat}</h2><p>🥇 Top Sub-Category</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{top_cust}</h2><p>👑 Top Customer</p></div>', unsafe_allow_html=True)

        st.markdown("")
        c4,c5,c6 = st.columns(3)
        with c4:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{top_region}</h2><p>🌍 Best Region</p></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{best_margin}</h2><p>📈 Best Profit Margin</p></div>', unsafe_allow_html=True)
        with c6:
            st.markdown(f'<div class="metric-card"><h2 style="font-size:1.1rem;">{worst_disc}</h2><p>🔖 Highest Avg Discount</p></div>', unsafe_allow_html=True)

        st.markdown("")

        # Year-wise Sales Trend line
        st.markdown('<div class="section-header">📊 Year-Wise Sales Trend</div>', unsafe_allow_html=True)
        yearly_trend = dff.groupby("Year")["Sales"].sum().reset_index()
        fig_yt = px.line(yearly_trend, x="Year", y="Sales", markers=True,
                         template="plotly_dark", color_discrete_sequence=["#00c853"])
        fig_yt.update_traces(line_width=3, marker_size=10)
        fig_yt.update_layout(height=300, xaxis_title="Year", yaxis_title="Sales (₹)", **PLOT_LAYOUT)
        theme(fig_yt)
        st.plotly_chart(fig_yt, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            # Sales by Discount band
            st.markdown('<div class="section-header">🔖 Sales by Discount Band</div>', unsafe_allow_html=True)
            dff["Discount Band"] = pd.cut(
                dff["Discount %"],
                bins=[0,12,20,27,35],
                labels=["10–12%","13–20%","21–27%","28–35%"]
            )
            disc_band = dff.groupby("Discount Band", observed=True)["Sales"].sum().reset_index()
            fig_db = px.pie(disc_band, names="Discount Band", values="Sales", hole=0.5,
                            color_discrete_sequence=["#00c853","#b2ff59","#69f0ae","#1de9b6"],
                            template="plotly_dark")
            fig_db.update_layout(height=360, **PLOT_LAYOUT)
            st.plotly_chart(fig_db, use_container_width=True)

        with col2:
            # Quarterly profit trend
            st.markdown('<div class="section-header">📅 Quarterly Profit Trend</div>', unsafe_allow_html=True)
            qtr = dff.groupby("Quarter")["Profit"].sum().reset_index().sort_values("Quarter")
            fig_qtr = px.bar(qtr, x="Quarter", y="Profit",
                             color="Profit", color_continuous_scale=GREEN_SCALE,
                             text="Profit", template="plotly_dark")
            fig_qtr.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig_qtr.update_layout(height=360, coloraxis_showscale=False,
                                   xaxis_title="", yaxis_title="Profit (₹)", **PLOT_LAYOUT)
            theme(fig_qtr, xangle=-20)
            st.plotly_chart(fig_qtr, use_container_width=True)

        # Profit Margin heatmap (Category x Year)
        st.markdown('<div class="section-header">🌡️ Profit Margin Heatmap — Category × Year</div>', unsafe_allow_html=True)
        heat_data = dff.groupby(["Category","Year"])["Profit Margin %"].mean().reset_index()
        heat_pivot = heat_data.pivot(index="Category", columns="Year", values="Profit Margin %")
        fig_heat = px.imshow(
            heat_pivot, color_continuous_scale=GREEN_SCALE,
            text_auto=".1f", aspect="auto",
            template="plotly_dark"
        )
        fig_heat.update_layout(height=340, **PLOT_LAYOUT)
        st.plotly_chart(fig_heat, use_container_width=True)

        # ── EXPORT ──
        st.markdown('<div class="section-header">📥 EXPORT DATA</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            csv_full = dff.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Filtered Data", csv_full,
                               "supermart_filtered.csv", "text/csv", use_container_width=True)


#MAIN APP ROUTER
if st.session_state.logged_in:
    dashboard()
else:
    st.markdown('<div class="main-title">🛒 Intelligent Sales Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sign in to access the Sales Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["📝  SIGNUP", "🔐  LOGIN"])
        with tab1:
            signup_page()
        with tab2:
            login_page()
