import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="Aegis Sovereign Logistics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark military industrial theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0f1a;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    /* Headers */
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #10b981 !important;
        font-family: 'JetBrains Mono', monospace;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    /* Text */
    p, span, label {
        color: #cbd5e1;
    }

    /* Selectbox and inputs */
    .stSelectbox > div > div {
        background-color: #1e293b;
        border-color: #334155;
        color: #f1f5f9;
    }

    /* Tables */
    .stDataFrame {
        background-color: #0f172a;
    }

    /* Custom classes */
    .status-safe {
        background-color: rgba(16, 185, 129, 0.1);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 4px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        font-size: 12px;
    }

    .status-warning {
        background-color: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 4px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        font-size: 12px;
    }

    .status-danger {
        background-color: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        padding: 4px 12px;
        border-radius: 4px;
        border: 1px solid rgba(244, 63, 94, 0.2);
        font-size: 12px;
    }

    .sovereignty-badge {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }

    .sovereignty-score {
        font-size: 48px;
        font-weight: bold;
        color: #10b981;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }

    .card {
        background-color: rgba(15, 23, 42, 0.8);
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .mono {
        font-family: 'JetBrains Mono', monospace;
        color: #10b981;
    }

    .timeline-step {
        padding: 12px;
        border-left: 2px solid #334155;
        margin-left: 12px;
    }

    .timeline-step-complete {
        border-left-color: #10b981;
    }

    .timeline-step-active {
        border-left-color: #f59e0b;
    }

    .restricted-zone {
        background-color: rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.2);
        padding: 4px 8px;
        border-radius: 4px;
        margin: 2px;
        display: inline-block;
        font-family: monospace;
        font-size: 11px;
        color: #f43f5e;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .classification-banner {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 12px;
        border-radius: 4px;
        text-align: center;
        font-size: 10px;
        letter-spacing: 2px;
        color: #f59e0b;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============ MOCK DATA ============

SHIPMENTS = [
    {
        'id': 'US-MIL-8842X',
        'cargo': 'Guidance Chips (Class 3)',
        'classification': 'ITAR',
        'origin': 'Los Angeles, CA',
        'destination': 'Yokosuka, Japan',
        'status': 'In Transit',
        'progress': 65,
        'vessel': 'USNS Comfort',
        'vessel_flag': 'US',
        'eta': datetime.now() + timedelta(days=5),
        'weight': '2,400 kg',
        'sovereignty_score': 100,
        'lat': 21.3069,
        'lng': -157.8583,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'Raytheon Tucson, AZ', 'time': '2025-01-18 06:00'},
            {'step': 'Customs Cleared (US)', 'status': 'complete', 'location': 'Port of Los Angeles', 'time': '2025-01-18 07:30'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'complete', 'location': 'USNS Comfort', 'time': '2025-01-18 08:00'},
            {'step': 'Transit (International Waters)', 'status': 'active', 'location': 'Pacific Ocean', 'time': '2025-01-23 16:45'},
            {'step': 'Arrival (Allied Port)', 'status': 'pending', 'location': 'Yokosuka Naval Base', 'time': 'ETA 2025-01-28'},
        ]
    },
    {
        'id': 'US-MIL-7721A',
        'cargo': 'Thermal Optics Array',
        'classification': 'ITAR',
        'origin': 'San Diego, CA',
        'destination': 'Tokyo, Japan',
        'status': 'In Transit',
        'progress': 45,
        'vessel': 'MV Alliance',
        'vessel_flag': 'US',
        'eta': datetime.now() + timedelta(days=7),
        'weight': '890 kg',
        'sovereignty_score': 100,
        'lat': 25.7617,
        'lng': -140.1918,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'L3Harris San Diego', 'time': '2025-01-20 10:00'},
            {'step': 'Customs Cleared (US)', 'status': 'complete', 'location': 'Port of San Diego', 'time': '2025-01-20 11:30'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'complete', 'location': 'MV Alliance', 'time': '2025-01-20 12:00'},
            {'step': 'Transit (International Waters)', 'status': 'active', 'location': 'Pacific Ocean', 'time': '2025-01-23 14:20'},
            {'step': 'Arrival (Allied Port)', 'status': 'pending', 'location': 'Port of Tokyo', 'time': 'ETA 2025-01-30'},
        ]
    },
    {
        'id': 'US-MIL-9034B',
        'cargo': 'F-35 Spare Components',
        'classification': 'ITAR/EAR99',
        'origin': 'Fort Worth, TX',
        'destination': 'Iwakuni, Japan',
        'status': 'In Transit',
        'progress': 82,
        'vessel': 'USS Theodore Roosevelt',
        'vessel_flag': 'US',
        'eta': datetime.now() + timedelta(days=2),
        'weight': '5,200 kg',
        'sovereignty_score': 100,
        'lat': 28.4177,
        'lng': 145.7731,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'Lockheed Martin Fort Worth', 'time': '2025-01-15 12:00'},
            {'step': 'Customs Cleared (US)', 'status': 'complete', 'location': 'DFW Air Cargo', 'time': '2025-01-15 13:30'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'complete', 'location': 'USS Theodore Roosevelt', 'time': '2025-01-15 14:00'},
            {'step': 'Transit (International Waters)', 'status': 'complete', 'location': 'Pacific Ocean', 'time': '2025-01-22 08:00'},
            {'step': 'Arrival (Allied Port)', 'status': 'active', 'location': 'MCAS Iwakuni', 'time': 'ETA 2025-01-25'},
        ]
    },
    {
        'id': 'US-MIL-6655C',
        'cargo': 'Encrypted Comm Modules',
        'classification': 'ITAR',
        'origin': 'Seattle, WA',
        'destination': 'Seoul, South Korea',
        'status': 'Loading',
        'progress': 15,
        'vessel': 'USNS Bob Hope',
        'vessel_flag': 'US',
        'eta': datetime.now() + timedelta(days=13),
        'weight': '340 kg',
        'sovereignty_score': 100,
        'lat': 47.6062,
        'lng': -122.3321,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'Boeing Seattle', 'time': '2025-01-23 08:00'},
            {'step': 'Customs Cleared (US)', 'status': 'active', 'location': 'Port of Seattle', 'time': '2025-01-23 10:00'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'pending', 'location': 'USNS Bob Hope', 'time': 'Pending'},
            {'step': 'Transit (International Waters)', 'status': 'pending', 'location': 'TBD', 'time': 'Pending'},
            {'step': 'Arrival (Allied Port)', 'status': 'pending', 'location': 'Busan Naval Base', 'time': 'ETA 2025-02-05'},
        ]
    },
    {
        'id': 'US-MIL-3398D',
        'cargo': 'Radar Components (AN/APG-81)',
        'classification': 'ITAR',
        'origin': 'Baltimore, MD',
        'destination': 'Ramstein, Germany',
        'status': 'Delivered',
        'progress': 100,
        'vessel': 'MV Cape Race',
        'vessel_flag': 'US',
        'eta': datetime.now() - timedelta(days=3),
        'weight': '1,800 kg',
        'sovereignty_score': 100,
        'lat': 49.4401,
        'lng': 7.6009,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'Northrop Grumman Baltimore', 'time': '2025-01-10 04:00'},
            {'step': 'Customs Cleared (US)', 'status': 'complete', 'location': 'Port of Baltimore', 'time': '2025-01-10 05:30'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'complete', 'location': 'MV Cape Race', 'time': '2025-01-10 06:00'},
            {'step': 'Transit (International Waters)', 'status': 'complete', 'location': 'Atlantic Ocean', 'time': '2025-01-18 12:00'},
            {'step': 'Arrival (Allied Port)', 'status': 'complete', 'location': 'Ramstein Air Base', 'time': '2025-01-20 08:00'},
        ]
    },
    {
        'id': 'US-MIL-2287E',
        'cargo': 'UAV Control Systems',
        'classification': 'ITAR',
        'origin': 'Phoenix, AZ',
        'destination': 'Darwin, Australia',
        'status': 'In Transit',
        'progress': 55,
        'vessel': 'USNS Watkins',
        'vessel_flag': 'US',
        'eta': datetime.now() + timedelta(days=9),
        'weight': '670 kg',
        'sovereignty_score': 100,
        'lat': 13.4443,
        'lng': 144.7937,
        'custody_chain': [
            {'step': 'Pickup (Secure Facility)', 'status': 'complete', 'location': 'General Atomics Phoenix', 'time': '2025-01-19 08:00'},
            {'step': 'Customs Cleared (US)', 'status': 'complete', 'location': 'Port of Los Angeles', 'time': '2025-01-19 09:30'},
            {'step': 'Loaded (US Flag Vessel)', 'status': 'complete', 'location': 'USNS Watkins', 'time': '2025-01-19 10:00'},
            {'step': 'Transit (International Waters)', 'status': 'active', 'location': 'Western Pacific', 'time': '2025-01-23 12:30'},
            {'step': 'Arrival (Allied Port)', 'status': 'pending', 'location': 'Port of Darwin', 'time': 'ETA 2025-02-01'},
        ]
    },
]

RESTRICTED_JURISDICTIONS = [
    {'code': 'CN', 'name': 'China', 'category': 'Primary Adversary'},
    {'code': 'RU', 'name': 'Russia', 'category': 'Primary Adversary'},
    {'code': 'IR', 'name': 'Iran', 'category': 'ITAR 126.1'},
    {'code': 'KP', 'name': 'North Korea', 'category': 'ITAR 126.1'},
    {'code': 'SY', 'name': 'Syria', 'category': 'ITAR 126.1'},
    {'code': 'CU', 'name': 'Cuba', 'category': 'ITAR 126.1'},
    {'code': 'BY', 'name': 'Belarus', 'category': 'Sanctions'},
    {'code': 'VE', 'name': 'Venezuela', 'category': 'Sanctions'},
]

ORIGINS = ['Los Angeles, CA', 'San Francisco, CA', 'Seattle, WA', 'San Diego, CA', 'Norfolk, VA', 'Charleston, SC']
DESTINATIONS = [
    {'name': 'Yokosuka, Japan', 'alliance': 'US-Japan Treaty'},
    {'name': 'Tokyo, Japan', 'alliance': 'US-Japan Treaty'},
    {'name': 'Busan, South Korea', 'alliance': 'US-ROK Alliance'},
    {'name': 'Darwin, Australia', 'alliance': 'AUKUS'},
    {'name': 'Ramstein, Germany', 'alliance': 'NATO'},
    {'name': 'Rota, Spain', 'alliance': 'NATO'},
]
WAYPOINTS = ['Pearl Harbor, HI', 'Guam', 'Anchorage, AK', 'Diego Garcia']

# ============ SIDEBAR ============

with st.sidebar:
    # Logo and title
    st.markdown("### 🛡️ AEGIS")
    st.markdown("<p style='font-size: 10px; color: #64748b; letter-spacing: 3px;'>SOVEREIGN LOGISTICS</p>", unsafe_allow_html=True)

    st.markdown("---")

    # System status
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 8px;'>
        <div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite;'></div>
        <span style='color: #10b981; font-size: 12px; font-weight: 500;'>SYSTEM OPERATIONAL</span>
    </div>
    <p style='font-size: 10px; color: #64748b; margin-top: 8px;'>🔒 AES-256 • FIPS 140-2</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    page = st.radio(
        "Navigation",
        ["Dashboard", "Active Shipments", "Route Planner", "Compliance & Risk"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Live feed
    st.markdown("<p style='font-size: 10px; color: #64748b; letter-spacing: 1px;'>📡 LIVE FEED</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 11px; color: #94a3b8;'>
        <p><span style='color: #10b981; font-family: monospace;'>US-MIL-8842X</span> • Hawaii checkpoint</p>
        <p><span style='color: #10b981; font-family: monospace;'>US-MIL-9034B</span> • Japan waters</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Classification
    st.markdown("""
    <div class='classification-banner'>
        UNCLASSIFIED // FOUO
    </div>
    """, unsafe_allow_html=True)

# ============ MAIN CONTENT ============

# Classification banner at top
st.markdown("""
<div class='classification-banner'>
    UNCLASSIFIED // FOR OFFICIAL USE ONLY
</div>
""", unsafe_allow_html=True)

if page == "Dashboard":
    st.title("Command Center")
    st.caption("Real-time sovereign logistics overview")

    # Top stats row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Shipments", "5", "+2 this week")
    with col2:
        st.metric("Compliance Score", "100%", "Perfect record")
    with col3:
        st.metric("Avg Transit Time", "8.4 days", "-0.6 vs last month")
    with col4:
        st.metric("Cargo Value (MTD)", "$847M", "+12% YoY")

    # Sovereignty badge
    st.markdown("""
    <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2);
                border-radius: 8px; padding: 12px; margin: 20px 0; display: flex; align-items: center; gap: 12px;'>
        <span style='font-size: 20px;'>🛡️</span>
        <span style='color: #10b981; font-weight: 500;'>All Routes Clean</span>
        <span style='color: rgba(16, 185, 129, 0.6); font-family: monospace; font-size: 12px;'>0 adversary contacts</span>
    </div>
    """, unsafe_allow_html=True)

    # Map and shipments
    col_map, col_list = st.columns([2, 1])

    with col_map:
        st.subheader("🗺️ God View")

        # Create Pacific-centered map with routes
        fig = go.Figure()

        # Add red zones for adversary territories
        # China approximate area
        fig.add_trace(go.Scattergeo(
            lon=[105, 135, 135, 105, 105],
            lat=[20, 20, 45, 45, 20],
            mode='lines',
            fill='toself',
            fillcolor='rgba(239, 68, 68, 0.15)',
            line=dict(color='rgba(239, 68, 68, 0.4)', width=1, dash='dash'),
            name='Restricted Zone',
            hoverinfo='name'
        ))

        # Add route lines (LA -> Pearl Harbor -> Japan)
        fig.add_trace(go.Scattergeo(
            lon=[-118.4, -157.9, 139.7],
            lat=[33.9, 21.4, 35.7],
            mode='lines',
            line=dict(color='#10b981', width=3),
            name='Clean Route',
            hoverinfo='name'
        ))

        # Add shipment markers
        for ship in SHIPMENTS:
            if ship['status'] != 'Delivered':
                color = '#10b981' if ship['status'] == 'In Transit' else '#f59e0b'
                fig.add_trace(go.Scattergeo(
                    lon=[ship['lng']],
                    lat=[ship['lat']],
                    mode='markers+text',
                    marker=dict(size=12, color=color, symbol='circle'),
                    text=ship['id'][-5:],
                    textposition='bottom center',
                    textfont=dict(size=10, color='#94a3b8'),
                    name=ship['id'],
                    hovertemplate=f"<b>{ship['id']}</b><br>{ship['cargo']}<br>Progress: {ship['progress']}%<extra></extra>"
                ))

        # Add port markers
        ports = [
            {'name': 'LAX', 'lat': 33.9, 'lon': -118.4},
            {'name': 'PRL', 'lat': 21.4, 'lon': -157.9},
            {'name': 'GUA', 'lat': 13.4, 'lon': 144.8},
            {'name': 'TOK', 'lat': 35.7, 'lon': 139.7},
        ]
        for port in ports:
            fig.add_trace(go.Scattergeo(
                lon=[port['lon']],
                lat=[port['lat']],
                mode='markers+text',
                marker=dict(size=8, color='#1e293b', line=dict(color='#10b981', width=2)),
                text=port['name'],
                textposition='top center',
                textfont=dict(size=9, color='#64748b'),
                showlegend=False,
                hoverinfo='text'
            ))

        fig.update_geos(
            projection_type="natural earth",
            showland=True,
            landcolor='#1e293b',
            showocean=True,
            oceancolor='#0a0f1a',
            showcoastlines=True,
            coastlinecolor='#334155',
            showframe=False,
            bgcolor='#0a0f1a',
            center=dict(lat=25, lon=-160),
            projection_scale=2.5,
        )

        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#0a0f1a',
            geo=dict(bgcolor='#0a0f1a'),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_list:
        st.subheader("Active Assets")

        for ship in SHIPMENTS[:4]:
            if ship['status'] != 'Delivered':
                status_color = '#10b981' if ship['status'] == 'In Transit' else '#f59e0b'
                st.markdown(f"""
                <div class='card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='mono'>{ship['id']}</span>
                        <span style='background: rgba(16, 185, 129, 0.1); color: {status_color};
                                     padding: 2px 8px; border-radius: 4px; font-size: 10px;'>
                            {ship['status']}
                        </span>
                    </div>
                    <p style='font-size: 12px; color: #94a3b8; margin: 8px 0 4px 0;'>{ship['cargo']}</p>
                    <div style='background: #1e293b; height: 4px; border-radius: 2px; overflow: hidden;'>
                        <div style='background: #10b981; height: 100%; width: {ship['progress']}%;'></div>
                    </div>
                    <p style='font-size: 10px; color: #64748b; text-align: right; margin-top: 4px;'>{ship['progress']}%</p>
                </div>
                """, unsafe_allow_html=True)

elif page == "Active Shipments":
    st.title("Active Shipments")
    st.caption("Manage and track all sovereign logistics operations")

    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by ID, cargo, or destination...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "In Transit", "Loading", "Delivered"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: #10b981; font-family: monospace;'>{len(SHIPMENTS)}</span> shipments", unsafe_allow_html=True)

    # Shipments table and detail panel
    col_table, col_detail = st.columns([2, 1])

    with col_table:
        # Filter shipments
        filtered = SHIPMENTS
        if status_filter != "All":
            filtered = [s for s in filtered if s['status'] == status_filter]
        if search:
            search_lower = search.lower()
            filtered = [s for s in filtered if search_lower in s['id'].lower() or
                       search_lower in s['cargo'].lower() or search_lower in s['destination'].lower()]

        # Display as dataframe
        df_data = []
        for s in filtered:
            df_data.append({
                'Container ID': s['id'],
                'Cargo': s['cargo'],
                'Origin': s['origin'].split(',')[0],
                'Destination': s['destination'].split(',')[0],
                'Status': s['status'],
                'Progress': f"{s['progress']}%",
                'Sovereignty': f"{s['sovereignty_score']}%"
            })

        if df_data:
            df = pd.DataFrame(df_data)

            # Let user select a shipment
            selected_id = st.selectbox("Select shipment for details:",
                                       [s['id'] for s in filtered],
                                       label_visibility="collapsed")

            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No shipments match your filters")
            selected_id = None

    with col_detail:
        st.subheader("Chain of Custody")

        if selected_id:
            ship = next((s for s in SHIPMENTS if s['id'] == selected_id), None)
            if ship:
                # Sovereignty badge
                st.markdown(f"""
                <div class='sovereignty-badge'>
                    <p style='font-size: 12px; color: #10b981; margin-bottom: 8px;'>🛡️ SOVEREIGNTY CHECK</p>
                    <p class='sovereignty-score'>{ship['sovereignty_score']}%</p>
                    <p style='font-size: 10px; color: rgba(16, 185, 129, 0.7); margin-top: 8px;'>
                        CLEAN / NO ADVERSARY CONTACT
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Shipment details
                st.markdown(f"""
                <div class='card'>
                    <p style='font-size: 10px; color: #64748b;'>CONTAINER</p>
                    <p class='mono' style='font-size: 14px;'>{ship['id']}</p>
                    <p style='font-size: 12px; color: #cbd5e1; margin-top: 4px;'>{ship['cargo']}</p>
                    <p style='font-size: 10px; color: #64748b; margin-top: 4px;'>{ship['classification']}</p>
                </div>
                """, unsafe_allow_html=True)

                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    st.markdown(f"<p style='font-size: 10px; color: #64748b;'>VESSEL</p><p style='font-size: 12px; font-family: monospace;'>{ship['vessel']}</p>", unsafe_allow_html=True)
                with col_v2:
                    st.markdown(f"<p style='font-size: 10px; color: #64748b;'>FLAG</p><p style='font-size: 12px;'>🇺🇸 <span style='color: #10b981;'>{ship['vessel_flag']}</span></p>", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 10px; color: #64748b; letter-spacing: 1px;'>CUSTODY TIMELINE</p>", unsafe_allow_html=True)

                # Timeline
                for step in ship['custody_chain']:
                    if step['status'] == 'complete':
                        icon = "✅"
                        color = "#10b981"
                    elif step['status'] == 'active':
                        icon = "🔄"
                        color = "#f59e0b"
                    else:
                        icon = "⏳"
                        color = "#64748b"

                    st.markdown(f"""
                    <div style='border-left: 2px solid {color}; padding-left: 12px; margin: 8px 0;'>
                        <p style='font-size: 12px; color: {color}; margin: 0;'>{icon} {step['step']}</p>
                        <p style='font-size: 10px; color: #64748b; margin: 2px 0;'>📍 {step['location']}</p>
                        <p style='font-size: 10px; color: #475569; font-family: monospace;'>{step['time']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Select a shipment to view details")

elif page == "Route Planner":
    st.title("Route Planner")
    st.caption("Plan sovereign-compliant logistics routes with automated ITAR/EAR validation")

    col_config, col_result = st.columns([1, 1])

    with col_config:
        st.subheader("Route Configuration")

        origin = st.selectbox("📍 Origin Port", [""] + ORIGINS)
        waypoint = st.selectbox("🔗 Waypoint (Optional)", ["None"] + WAYPOINTS)
        dest_names = [d['name'] for d in DESTINATIONS]
        destination = st.selectbox("⚓ Destination", [""] + dest_names)

        if destination:
            dest_info = next((d for d in DESTINATIONS if d['name'] == destination), None)
            if dest_info:
                st.markdown(f"<p style='font-size: 11px; color: #64748b;'>Alliance: <span style='color: #10b981;'>{dest_info['alliance']}</span></p>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Compliance Controls")

        exclude_126 = st.toggle("🛡️ Exclude 126.1 Countries", value=True)

        if not exclude_126:
            st.warning("⚠️ **Compliance Risk**: Routes may pass through restricted jurisdictions. ITAR violations can result in severe penalties.")

        st.markdown("<p style='font-size: 10px; color: #64748b; margin-top: 16px;'>EXCLUDED JURISDICTIONS</p>", unsafe_allow_html=True)

        restricted_html = ""
        for j in RESTRICTED_JURISDICTIONS:
            color = "#f43f5e" if exclude_126 else "#64748b"
            restricted_html += f"<span class='restricted-zone' style='color: {color}; border-color: {color};'>{j['code']}</span> "
        st.markdown(restricted_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        calculate = st.button("⚡ Calculate Route", type="primary", use_container_width=True)

    with col_result:
        st.subheader("Route Analysis")

        if calculate and origin and destination:
            # Mock route calculation
            distance = random.randint(4000, 7000)
            transit_days = round(distance / 400)
            cost = random.randint(200, 700)
            sovereignty_score = 100 if exclude_126 else random.randint(50, 80)

            # Status badge
            if sovereignty_score == 100:
                st.markdown("""
                <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3);
                            padding: 8px 16px; border-radius: 4px; display: inline-block;'>
                    <span style='color: #10b981; font-weight: 500;'>✅ CLEAN ROUTE</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3);
                            padding: 8px 16px; border-radius: 4px; display: inline-block;'>
                    <span style='color: #f43f5e; font-weight: 500;'>⚠️ HIGH RISK</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Route summary
            route_text = f"{origin} → "
            if waypoint != "None":
                route_text += f"{waypoint} → "
            route_text += destination

            st.markdown(f"""
            <div class='card'>
                <p style='font-size: 12px; color: #94a3b8;'>📍 {route_text}</p>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Distance", f"{distance:,} nm")
            with col_m2:
                st.metric("Transit Time", f"{transit_days} days")
            with col_m3:
                st.metric("Est. Cost", f"${cost}K")

            # Sovereignty score
            score_color = "#10b981" if sovereignty_score == 100 else "#f43f5e"
            st.markdown(f"""
            <div style='background: rgba(16, 185, 129, 0.05); border: 1px solid {score_color}33;
                        border-radius: 8px; padding: 20px; margin-top: 16px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='color: #cbd5e1;'>🛡️ Sovereignty Score</span>
                    <span style='font-size: 32px; font-weight: bold; color: {score_color};
                                font-family: monospace; text-shadow: 0 0 20px {score_color}50;'>
                        {sovereignty_score}%
                    </span>
                </div>
                <div style='margin-top: 16px; font-size: 12px;'>
                    <p style='color: {"#10b981" if sovereignty_score == 100 else "#f43f5e"}; margin: 4px 0;'>
                        {"✓" if sovereignty_score == 100 else "✗"} {"No adversary jurisdiction contact" if sovereignty_score == 100 else "Route passes through restricted zones"}
                    </p>
                    <p style='color: #10b981; margin: 4px 0;'>✓ US-Flag vessel required</p>
                    <p style='color: #10b981; margin: 4px 0;'>✓ Allied port destination confirmed</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Vessel recommendation
            st.markdown("""
            <div class='card'>
                <p style='font-size: 10px; color: #64748b;'>RECOMMENDED VESSEL TYPE</p>
                <p style='font-size: 14px; color: #cbd5e1;'>🚢 US-Flag Container</p>
                <p style='font-size: 12px; color: #10b981; font-family: monospace;'>🇺🇸 US Flag</p>
            </div>
            """, unsafe_allow_html=True)

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.button("✅ Approve Route", type="primary", use_container_width=True)
            with col_b2:
                st.button("💾 Save Draft", use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 60px 20px; color: #64748b;'>
                <p style='font-size: 48px; margin-bottom: 16px;'>🌍</p>
                <p>Configure route parameters</p>
                <p style='font-size: 12px;'>Select origin, destination, and calculate</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "Compliance & Risk":
    st.title("Compliance & Risk")
    st.caption("ITAR/EAR compliance dashboard and jurisdiction risk management")

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='sovereignty-badge'>
            <p style='font-size: 10px; color: #64748b;'>COMPLIANCE SCORE</p>
            <p class='sovereignty-score'>100%</p>
            <p style='font-size: 10px; color: #10b981;'>All shipments clean</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("Active Licenses", "24", "ITAR/EAR authorizations")
    with col3:
        st.metric("Days Since Incident", "847", "Perfect record")
    with col4:
        st.metric("Audits (YTD)", "12", "100% passed")

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart, col_status = st.columns([2, 1])

    with col_chart:
        st.subheader("📈 Monthly Compliance Trend")

        months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
        scores = [100, 100, 98, 100, 100, 100]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months,
            y=scores,
            marker_color='#10b981',
            text=scores,
            textposition='outside',
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='#0a0f1a',
            plot_bgcolor='#0a0f1a',
            yaxis=dict(range=[90, 102], gridcolor='#1e293b', tickfont=dict(color='#64748b')),
            xaxis=dict(tickfont=dict(color='#64748b')),
            font=dict(color='#cbd5e1'),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Recent audits
        st.subheader("Recent Audits")
        audits = [
            {'id': 'AUD-2025-0123', 'type': 'ITAR Review', 'status': 'Passed', 'date': '2025-01-23', 'findings': 0},
            {'id': 'AUD-2025-0115', 'type': 'EAR Classification', 'status': 'Passed', 'date': '2025-01-15', 'findings': 0},
            {'id': 'AUD-2025-0108', 'type': 'Quarterly DDTC', 'status': 'Passed', 'date': '2025-01-08', 'findings': 0},
        ]

        for audit in audits:
            st.markdown(f"""
            <div class='card' style='display: flex; align-items: center; gap: 16px;'>
                <span style='font-size: 20px;'>✅</span>
                <div style='flex: 1;'>
                    <p style='font-family: monospace; color: #cbd5e1; margin: 0;'>{audit['id']}</p>
                    <p style='font-size: 12px; color: #64748b; margin: 4px 0 0 0;'>{audit['type']}</p>
                </div>
                <div style='text-align: right;'>
                    <p style='font-size: 12px; font-family: monospace; color: #94a3b8;'>{audit['date']}</p>
                    <p style='font-size: 10px; color: #64748b;'>{audit['findings']} findings</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_status:
        st.subheader("🔒 Sovereignty Status")

        # Pie chart
        fig = go.Figure(go.Pie(
            values=[6, 0],
            labels=['Clean', 'At Risk'],
            hole=0.7,
            marker_colors=['#10b981', '#f43f5e'],
            textinfo='none',
        ))
        fig.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            annotations=[dict(text='6/6<br>CLEAN', x=0.5, y=0.5, font_size=16,
                            font_color='#10b981', showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div style='font-size: 12px;'>
            <p style='color: #10b981; margin: 8px 0;'>✓ Zero adversary contact</p>
            <p style='color: #10b981; margin: 8px 0;'>✓ US-flag vessels only</p>
            <p style='color: #10b981; margin: 8px 0;'>✓ Allied destinations only</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🚫 Restricted Jurisdictions")

        for j in RESTRICTED_JURISDICTIONS:
            st.markdown(f"""
            <div style='background: rgba(244, 63, 94, 0.05); border: 1px solid rgba(244, 63, 94, 0.1);
                        padding: 8px 12px; border-radius: 4px; margin: 4px 0; display: flex;
                        justify-content: space-between; align-items: center;'>
                <span style='font-size: 12px; color: #cbd5e1;'>❌ {j['name']}</span>
                <span style='font-size: 10px; font-family: monospace; color: #f43f5e;'>{j['code']}</span>
            </div>
            """, unsafe_allow_html=True)
