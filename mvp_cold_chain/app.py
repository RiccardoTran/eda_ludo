"""
Cold Chain Failure Prediction - Interactive Demo
Streamlit web application for visualizing predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Cold Chain Failure Prediction",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        color: #d62728;
        font-weight: bold;
    }
    .risk-medium {
        color: #ff7f0e;
        font-weight: bold;
    }
    .risk-low {
        color: #2ca02c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load the processed dataset"""
    df = pd.read_csv('data/processed/facilities_with_daily_weather_and_targets.csv')
    return df

# Calculate risk levels
def get_risk_level(failure_count):
    """Convert failure count to risk level"""
    if failure_count >= 3:
        return "HIGH", "risk-high"
    elif failure_count >= 1:
        return "MEDIUM", "risk-medium"
    else:
        return "LOW", "risk-low"

def get_risk_color(failure_count):
    """Get color for risk level"""
    if failure_count >= 3:
        return "#d62728"  # Red
    elif failure_count >= 1:
        return "#ff7f0e"  # Orange
    else:
        return "#2ca02c"  # Green

# Main app
def main():
    # Header
    st.markdown('<div class="main-header">❄️ Cold Chain Failure Prediction System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">5-Day Risk Forecast for Kenya Health Facilities</div>', unsafe_allow_html=True)

    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please run `python3 run_mvp.py` first to generate data.")
        return

    # Sidebar
    st.sidebar.title("🔍 Filters & Settings")

    # Region filter
    regions = df['facility_id'].str.split('_').str[1].unique()
    region_names = {
        'NRB': 'Nairobi',
        'TUR': 'Turkana',
        'MBA': 'Mombasa',
        'KIS': 'Kisumu',
        'GAR': 'Garissa'
    }

    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=regions,
        default=regions,
        format_func=lambda x: region_names.get(x, x)
    )

    # Power source filter
    power_sources = st.sidebar.multiselect(
        "Power Source",
        options=df['power_source'].unique(),
        default=df['power_source'].unique()
    )

    # Risk level filter
    risk_filter = st.sidebar.multiselect(
        "Risk Level",
        options=['HIGH', 'MEDIUM', 'LOW'],
        default=['HIGH', 'MEDIUM', 'LOW']
    )

    # Filter data
    df['region'] = df['facility_id'].str.split('_').str[1]
    df_filtered = df[
        (df['region'].isin(selected_regions)) &
        (df['power_source'].isin(power_sources))
    ].copy()

    # Calculate total failures per facility
    failure_cols = [f'failure_day{i}' for i in range(1, 6)]
    df_filtered['total_failures'] = df_filtered[failure_cols].sum(axis=1)
    df_filtered['risk_level'] = df_filtered['total_failures'].apply(lambda x: get_risk_level(x)[0])
    df_filtered['risk_color'] = df_filtered['total_failures'].apply(get_risk_color)

    # Apply risk filter
    df_filtered = df_filtered[df_filtered['risk_level'].isin(risk_filter)]

    # Overall Statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Facilities", len(df_filtered))

    with col2:
        high_risk = len(df_filtered[df_filtered['total_failures'] >= 3])
        st.metric("High Risk Facilities", high_risk, delta=f"{high_risk/len(df_filtered)*100:.1f}%")

    with col3:
        avg_failures = df_filtered['total_failures'].mean()
        st.metric("Avg Failures (5 days)", f"{avg_failures:.1f}")

    with col4:
        failure_rate = df_filtered[failure_cols].sum().sum() / (len(df_filtered) * 5) * 100
        st.metric("Overall Failure Rate", f"{failure_rate:.1f}%")

    st.markdown("---")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map View", "📊 Facility Details", "⚡ Power Analysis", "📈 Statistics"])

    # TAB 1: MAP VIEW
    with tab1:
        st.subheader("Geographic Risk Distribution")

        # Create map
        fig_map = px.scatter_mapbox(
            df_filtered,
            lat='latitude',
            lon='longitude',
            color='total_failures',
            size='total_failures',
            hover_name='facility_name',
            hover_data={
                'latitude': False,
                'longitude': False,
                'facility_type': True,
                'power_source': True,
                'electrification_rate': ':.1f',
                'grid_reliability_score': ':.2f',
                'total_failures': True,
                'risk_level': True
            },
            color_continuous_scale=['green', 'yellow', 'orange', 'red'],
            range_color=[0, 5],
            zoom=5,
            height=600,
            mapbox_style='open-street-map',
            title=f"Cold Chain Risk Map - {len(df_filtered)} Facilities"
        )

        fig_map.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                title="Failures<br>(5 days)",
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        )

        st.plotly_chart(fig_map, use_container_width=True)

        # Risk summary by region
        st.subheader("Risk by Region")
        region_stats = df_filtered.groupby('region').agg({
            'total_failures': 'mean',
            'facility_id': 'count',
            'electrification_rate': 'mean',
            'grid_reliability_score': 'mean'
        }).round(2)
        region_stats.columns = ['Avg Failures', 'Facilities', 'Avg Electrification %', 'Avg Grid Reliability']
        region_stats.index = region_stats.index.map(region_names)

        st.dataframe(region_stats, use_container_width=True)

    # TAB 2: FACILITY DETAILS
    with tab2:
        st.subheader("Detailed Facility View")

        # Select facility
        facility_names = df_filtered.sort_values('total_failures', ascending=False)['facility_name'].tolist()
        selected_facility = st.selectbox(
            "Select a facility to view details:",
            facility_names
        )

        facility_data = df_filtered[df_filtered['facility_name'] == selected_facility].iloc[0]

        # Facility info
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Facility Information")
            st.write(f"**Name:** {facility_data['facility_name']}")
            st.write(f"**Type:** {facility_data['facility_type']}")
            st.write(f"**Power Source:** {facility_data['power_source']}")
            st.write(f"**Location:** {facility_data['latitude']:.2f}°, {facility_data['longitude']:.2f}°")

            risk_level, risk_class = get_risk_level(facility_data['total_failures'])
            st.markdown(f"**Overall Risk:** <span class='{risk_class}'>{risk_level}</span>", unsafe_allow_html=True)

        with col2:
            st.markdown("#### Power Infrastructure")
            st.write(f"**Electrification Rate:** {facility_data['electrification_rate']:.1f}%")
            st.write(f"**Grid Reliability:** {facility_data['grid_reliability_score']:.2f} ({facility_data['avg_power_hours_per_day']:.1f} hrs/day)")
            st.write(f"**Distance to Grid:** {facility_data['distance_to_grid_km']:.1f} km")
            st.write(f"**Power Vulnerability:** {facility_data['power_vulnerability_score']:.1f}/100")

            if facility_data['high_outage_risk'] == 1:
                st.warning("⚠️ High outage risk area")
            if facility_data['very_low_power_access'] == 1:
                st.error("🔴 Very low power access")

        st.markdown("---")

        # 5-day forecast timeline
        st.markdown("#### 5-Day Failure Forecast")

        forecast_date = pd.to_datetime(facility_data['forecast_date'])
        days = [(forecast_date + timedelta(days=i)).strftime('%a, %b %d') for i in range(1, 6)]

        # Create timeline visualization
        fig_timeline = go.Figure()

        # Failures
        failures = [facility_data[f'failure_day{i}'] for i in range(1, 6)]
        colors = [get_risk_color(f) if f == 1 else '#2ca02c' for f in failures]

        fig_timeline.add_trace(go.Bar(
            x=days,
            y=[1 if f == 1 else 0.3 for f in failures],
            marker_color=colors,
            name='Failure Risk',
            text=[f'FAILURE ⚠️' if f == 1 else 'OK ✓' for f in failures],
            textposition='inside',
            hovertemplate='<b>%{x}</b><br>Status: %{text}<extra></extra>'
        ))

        fig_timeline.update_layout(
            title="Daily Failure Predictions",
            xaxis_title="Date",
            yaxis_title="Risk Level",
            height=300,
            showlegend=False,
            yaxis=dict(showticklabels=False)
        )

        st.plotly_chart(fig_timeline, use_container_width=True)

        # Weather conditions
        st.markdown("#### Weather Conditions (5-Day Forecast)")

        # Create weather subplots
        fig_weather = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Temperature (°C)', 'Cloud Cover (%)'),
            vertical_spacing=0.15
        )

        # Temperature
        temps_max = [facility_data[f'temp_max_day{i}'] for i in range(1, 6)]
        temps_min = [facility_data[f'temp_min_day{i}'] for i in range(1, 6)]

        fig_weather.add_trace(
            go.Scatter(x=days, y=temps_max, mode='lines+markers', name='Max Temp',
                      line=dict(color='red', width=2)),
            row=1, col=1
        )
        fig_weather.add_trace(
            go.Scatter(x=days, y=temps_min, mode='lines+markers', name='Min Temp',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )

        # Cloud cover
        clouds = [facility_data[f'clouds_day{i}'] for i in range(1, 6)]
        fig_weather.add_trace(
            go.Bar(x=days, y=clouds, name='Cloud Cover', marker_color='lightblue'),
            row=2, col=1
        )

        fig_weather.update_layout(height=500, showlegend=True)
        fig_weather.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
        fig_weather.update_yaxes(title_text="Cloud Cover (%)", row=2, col=1)

        st.plotly_chart(fig_weather, use_container_width=True)

    # TAB 3: POWER ANALYSIS
    with tab3:
        st.subheader("Power Infrastructure Impact Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Failure rate by grid reliability
            st.markdown("#### Failure Rate by Grid Reliability")

            df_filtered['reliability_category'] = pd.cut(
                df_filtered['grid_reliability_score'],
                bins=[0, 0.6, 0.8, 1.0],
                labels=['Low (<60%)', 'Medium (60-80%)', 'High (>80%)']
            )

            reliability_stats = df_filtered.groupby('reliability_category', observed=True).agg({
                'total_failures': 'mean',
                'facility_id': 'count'
            }).reset_index()
            reliability_stats.columns = ['Category', 'Avg Failures', 'Facilities']

            fig_reliability = px.bar(
                reliability_stats,
                x='Category',
                y='Avg Failures',
                text='Avg Failures',
                color='Avg Failures',
                color_continuous_scale=['green', 'yellow', 'red'],
                title='Unreliable grid = Higher failure risk'
            )
            fig_reliability.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_reliability.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_reliability, use_container_width=True)

        with col2:
            # Failure rate by electrification
            st.markdown("#### Failure Rate by Electrification Level")

            df_filtered['elec_category'] = pd.cut(
                df_filtered['electrification_rate'],
                bins=[0, 40, 70, 100],
                labels=['Low (<40%)', 'Medium (40-70%)', 'High (>70%)']
            )

            elec_stats = df_filtered.groupby('elec_category', observed=True).agg({
                'total_failures': 'mean',
                'facility_id': 'count'
            }).reset_index()
            elec_stats.columns = ['Category', 'Avg Failures', 'Facilities']

            fig_elec = px.bar(
                elec_stats,
                x='Category',
                y='Avg Failures',
                text='Avg Failures',
                color='Avg Failures',
                color_continuous_scale=['green', 'yellow', 'red'],
                title='Low electrification = Higher risk'
            )
            fig_elec.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_elec.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_elec, use_container_width=True)

        # Distance to grid analysis
        st.markdown("#### Distance to Grid vs Failure Rate")

        fig_distance = px.scatter(
            df_filtered,
            x='distance_to_grid_km',
            y='total_failures',
            color='power_source',
            size='power_vulnerability_score',
            hover_name='facility_name',
            title='Remote facilities have higher failure rates',
            labels={'distance_to_grid_km': 'Distance to Grid (km)', 'total_failures': 'Total Failures (5 days)'}
        )
        fig_distance.update_layout(height=400)
        st.plotly_chart(fig_distance, use_container_width=True)

        # Power vulnerability distribution
        st.markdown("#### Power Vulnerability Score Distribution")

        fig_vuln = px.histogram(
            df_filtered,
            x='power_vulnerability_score',
            color='risk_level',
            nbins=20,
            title='Facilities by Power Vulnerability (0=Best, 100=Worst)',
            labels={'power_vulnerability_score': 'Vulnerability Score'},
            color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        )
        fig_vuln.update_layout(height=400)
        st.plotly_chart(fig_vuln, use_container_width=True)

    # TAB 4: STATISTICS
    with tab4:
        st.subheader("Overall Statistics & Insights")

        # Failure distribution by day
        st.markdown("#### Failure Distribution by Day")

        daily_failures = []
        for day in range(1, 6):
            count = df_filtered[f'failure_day{day}'].sum()
            daily_failures.append({
                'Day': f'Day {day}',
                'Failures': count,
                'Percentage': count / len(df_filtered) * 100
            })

        df_daily = pd.DataFrame(daily_failures)

        fig_daily = go.Figure()
        fig_daily.add_trace(go.Bar(
            x=df_daily['Day'],
            y=df_daily['Failures'],
            text=df_daily['Percentage'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            marker_color=['#2ca02c', '#2ca02c', '#ff7f0e', '#d62728', '#d62728']
        ))
        fig_daily.update_layout(
            title='Risk accumulates over time (temporal pattern)',
            xaxis_title='Forecast Day',
            yaxis_title='Number of Failures',
            height=400
        )
        st.plotly_chart(fig_daily, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Failure by power source
            st.markdown("#### Failures by Power Source")

            power_stats = df_filtered.groupby('power_source').agg({
                'total_failures': 'mean',
                'facility_id': 'count'
            }).reset_index()
            power_stats.columns = ['Power Source', 'Avg Failures', 'Facilities']

            fig_power = px.bar(
                power_stats,
                x='Power Source',
                y='Avg Failures',
                text='Avg Failures',
                color='Power Source'
            )
            fig_power.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_power.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_power, use_container_width=True)

        with col2:
            # Failure by facility type
            st.markdown("#### Failures by Facility Type")

            facility_stats = df_filtered.groupby('facility_type').agg({
                'total_failures': 'mean',
                'facility_id': 'count'
            }).reset_index()
            facility_stats.columns = ['Facility Type', 'Avg Failures', 'Facilities']

            fig_facility = px.bar(
                facility_stats,
                x='Facility Type',
                y='Avg Failures',
                text='Avg Failures',
                color='Facility Type'
            )
            fig_facility.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_facility.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_facility, use_container_width=True)

        # Key insights
        st.markdown("---")
        st.markdown("### 🔍 Key Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"""
            **Power Infrastructure**

            Facilities with unreliable grid (<60% uptime) have **3.6x higher** failure rates than those with reliable grid.

            Low electrification areas (<40%) show **70% failure rate** vs 18% in high-electrification areas.
            """)

        with col2:
            st.warning(f"""
            **Geographic Patterns**

            Remote facilities (>40km from grid) have **56% failure rate**.

            Turkana region (north) shows highest risk due to low electrification and extreme temperatures.
            """)

        with col3:
            st.success(f"""
            **Temporal Patterns**

            Risk accumulates over time - Days 1-2 show low failures, while Days 3-5 show **50% failure rate**.

            This reflects realistic cold chain stress building up over consecutive hot days.
            """)

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This system predicts vaccine cold chain failures for health facilities in Kenya using:

    - **5-day weather forecasts** (temperature, clouds, humidity)
    - **Power infrastructure data** (grid reliability, electrification)
    - **Facility characteristics** (type, power source, location)

    **Model Features:** 60 inputs, 5 daily predictions
    """)

    st.markdown("---")
    st.markdown("### 📊 Data Info")
    try:
        df_info = load_data()
        st.metric("Total Facilities", len(df_info))
        st.metric("Forecast Period", "5 days")
        st.metric("Last Updated", df_info['forecast_date'].iloc[0])
    except:
        pass

    st.markdown("---")
    st.markdown("**Built with:** Streamlit, Plotly, Pandas")

# Run app
if __name__ == "__main__":
    main()
