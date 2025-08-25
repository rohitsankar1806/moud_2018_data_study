import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="MOUD Study Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache MOUD study data"""
    data_path = Path("moud-data-csv")
    
    datasets = {
        'baseline': 'Patient-Baseline-Data.csv',
        '3_month': 'Patient-3-month-Data.csv', 
        '6_month': 'Patient-6-month-Data.csv',
        '12_month': 'Patient-12-month-Data.csv',
        '18_month': 'Patient-18-month-Data.csv'
    }
    
    loaded_data = {}
    for period, filename in datasets.items():
        try:
            df = pd.read_csv(data_path / filename)
            # Add time period column
            df['time_period'] = period
            loaded_data[period] = df
        except FileNotFoundError:
            st.error(f"Could not find {filename}")
            return None
    
    return loaded_data

@st.cache_data
def process_longitudinal_data(data_dict):
    """Process data for longitudinal analysis"""
    if not data_dict:
        return None
    
    # Key variables for analysis
    key_vars = [
        'CID', 'time_period', 'responded', 'opuse30', 'opabst90', 
        'opoverdose', 'suoverdose', 'currentbup', 'currentmmt', 
        'currentntx', 'edvisit', 'hospstay', 'pcp90', 'mentalillness',
        'insurance', 'employed', 'fnuse30', 'hruse30', 'diversionuse90'
    ]
    
    # Combine all periods
    combined_data = []
    for period, df in data_dict.items():
        # Select available columns
        available_vars = [var for var in key_vars if var in df.columns]
        period_data = df[available_vars].copy()
        combined_data.append(period_data)
    
    return pd.concat(combined_data, ignore_index=True)

def create_overview_section():
    """Create the overview section explaining MOUD"""
    st.markdown('<div class="main-header">MOUD Study Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Understanding Medications for Opioid Use Disorder Treatment Outcomes</div>', unsafe_allow_html=True)
    
    # What is MOUD explanation
    st.markdown("""
    <div class="info-box">
    <h3>🏥 What is MOUD?</h3>
    <p><strong>Medications for Opioid Use Disorder (MOUD)</strong> is an evidence-based treatment approach that combines medication with counseling and behavioral therapies. This study tracks patient outcomes across multiple sites in the United States over 18 months.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key medications explanation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-box">
        <h4>💊 Buprenorphine</h4>
        <p>A partial opioid agonist that reduces cravings and withdrawal symptoms while having a "ceiling effect" for respiratory depression.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h4>💊 Methadone</h4>
        <p>A full opioid agonist administered in specialized clinics. Effective for severe opioid addiction but requires daily supervised dosing.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
        <h4>💊 Naltrexone</h4>
        <p>An opioid antagonist that blocks the effects of opioids. Available as daily oral medication or monthly injection.</p>
        </div>
        """, unsafe_allow_html=True)

def create_treatment_outcomes_viz(df):
    """Create treatment outcomes visualization"""
    st.header("📈 Treatment Outcomes Over Time")
    
    if df is None or df.empty:
        st.warning("No data available for treatment outcomes analysis.")
        return
    
    # Calculate abstinence rates by time period
    abstinence_data = []
    medication_data = []
    
    time_periods = ['baseline', '3_month', '6_month', '12_month', '18_month']
    time_labels = ['Baseline', '3 Months', '6 Months', '12 Months', '18 Months']
    
    for period, label in zip(time_periods, time_labels):
        period_df = df[df['time_period'] == period]
        if not period_df.empty and 'opabst90' in period_df.columns:
            # Calculate abstinence rate (assuming 1 = abstinent)
            abstinence_rate = (period_df['opabst90'] == 1).mean() * 100
            abstinence_data.append({'Time': label, 'Abstinence_Rate': abstinence_rate})
        
        # Calculate medication usage
        if not period_df.empty:
            bup_rate = (period_df.get('currentbup', 0) == 1).mean() * 100
            mmt_rate = (period_df.get('currentmmt', 0) == 1).mean() * 100  
            ntx_rate = (period_df.get('currentntx', 0) == 1).mean() * 100
            
            medication_data.append({
                'Time': label,
                'Buprenorphine': bup_rate,
                'Methadone': mmt_rate,
                'Naltrexone': ntx_rate
            })
    
    col1, col2 = st.columns(2)
    
    with col1:
        if abstinence_data:
            abstinence_df = pd.DataFrame(abstinence_data)
            fig_abs = px.line(abstinence_df, x='Time', y='Abstinence_Rate',
                            title='Opioid Abstinence Rates Over Time',
                            labels={'Abstinence_Rate': 'Abstinence Rate (%)'})
            fig_abs.update_traces(line=dict(width=3), marker=dict(size=8))
            fig_abs.update_layout(height=400)
            st.plotly_chart(fig_abs, use_container_width=True)
    
    with col2:
        if medication_data:
            med_df = pd.DataFrame(medication_data)
            fig_med = go.Figure()
            
            medications = ['Buprenorphine', 'Methadone', 'Naltrexone']
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
            
            for med, color in zip(medications, colors):
                fig_med.add_trace(go.Scatter(
                    x=med_df['Time'], y=med_df[med],
                    mode='lines+markers',
                    name=med,
                    line=dict(width=3, color=color),
                    marker=dict(size=8)
                ))
            
            fig_med.update_layout(
                title='Medication Usage Over Time',
                xaxis_title='Time Period',
                yaxis_title='Usage Rate (%)',
                height=400
            )
            st.plotly_chart(fig_med, use_container_width=True)

def create_drug_use_patterns_viz(df):
    """Create drug use patterns visualization"""
    st.header("⚠️ Drug Use Patterns and Risk Indicators")
    
    if df is None or df.empty:
        st.warning("No data available for drug use patterns analysis.")
        return
    
    # Overdose incidents over time
    col1, col2 = st.columns(2)
    
    with col1:
        overdose_data = []
        time_periods = ['baseline', '3_month', '6_month', '12_month', '18_month']
        time_labels = ['Baseline', '3 Months', '6 Months', '12 Months', '18 Months']
        
        for period, label in zip(time_periods, time_labels):
            period_df = df[df['time_period'] == period]
            if not period_df.empty:
                opioid_od = (period_df.get('opoverdose', 0) == 1).sum()
                substance_od = (period_df.get('suoverdose', 0) == 1).sum()
                
                overdose_data.append({
                    'Time': label,
                    'Opioid Overdose': opioid_od,
                    'Substance Overdose': substance_od
                })
        
        if overdose_data:
            od_df = pd.DataFrame(overdose_data)
            fig_od = go.Figure()
            
            fig_od.add_trace(go.Bar(
                x=od_df['Time'],
                y=od_df['Opioid Overdose'],
                name='Opioid Overdose',
                marker_color='#d62728'
            ))
            
            fig_od.add_trace(go.Bar(
                x=od_df['Time'],
                y=od_df['Substance Overdose'], 
                name='Substance Overdose',
                marker_color='#ff7f0e'
            ))
            
            fig_od.update_layout(
                title='Overdose Incidents Over Time',
                xaxis_title='Time Period',
                yaxis_title='Number of Incidents',
                height=400,
                barmode='group'
            )
            st.plotly_chart(fig_od, use_container_width=True)
    
    with col2:
        # Drug type usage comparison
        drug_use_data = []
        
        for period, label in zip(time_periods, time_labels):
            period_df = df[df['time_period'] == period]
            if not period_df.empty:
                opioid_use = (period_df.get('opuse30', 0) == 1).mean() * 100
                fentanyl_use = (period_df.get('fnuse30', 0) == 1).mean() * 100
                heroin_use = (period_df.get('hruse30', 0) == 1).mean() * 100
                
                drug_use_data.append({
                    'Time': label,
                    'Any Opioid': opioid_use,
                    'Fentanyl': fentanyl_use,
                    'Heroin': heroin_use
                })
        
        if drug_use_data:
            drug_df = pd.DataFrame(drug_use_data)
            fig_drug = go.Figure()
            
            drugs = ['Any Opioid', 'Fentanyl', 'Heroin']
            colors = ['#1f77b4', '#d62728', '#9467bd']
            
            for drug, color in zip(drugs, colors):
                fig_drug.add_trace(go.Scatter(
                    x=drug_df['Time'],
                    y=drug_df[drug],
                    mode='lines+markers',
                    name=drug,
                    line=dict(width=3, color=color),
                    marker=dict(size=8)
                ))
            
            fig_drug.update_layout(
                title='Drug Use Patterns (Past 30 Days)',
                xaxis_title='Time Period', 
                yaxis_title='Usage Rate (%)',
                height=400
            )
            st.plotly_chart(fig_drug, use_container_width=True)

def create_healthcare_utilization_viz(df):
    """Create healthcare utilization visualization"""
    st.header("🏥 Healthcare System Impact")
    
    if df is None or df.empty:
        st.warning("No data available for healthcare utilization analysis.")
        return
    
    # Healthcare utilization metrics
    col1, col2, col3 = st.columns(3)
    
    time_periods = ['baseline', '3_month', '6_month', '12_month', '18_month']
    time_labels = ['Baseline', '3 Months', '6 Months', '12 Months', '18 Months']
    
    healthcare_data = []
    
    for period, label in zip(time_periods, time_labels):
        period_df = df[df['time_period'] == period]
        if not period_df.empty:
            ed_visits = (period_df.get('edvisit', 0) == 1).mean() * 100
            hospital_stays = (period_df.get('hospstay', 0) == 1).mean() * 100
            pcp_visits = (period_df.get('pcp90', 0) == 1).mean() * 100
            
            healthcare_data.append({
                'Time': label,
                'ED Visits': ed_visits,
                'Hospital Stays': hospital_stays, 
                'Primary Care': pcp_visits
            })
    
    if healthcare_data:
        hc_df = pd.DataFrame(healthcare_data)
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Emergency Department Visits', 'Hospital Stays', 'Primary Care Visits'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Scatter(x=hc_df['Time'], y=hc_df['ED Visits'], 
                      mode='lines+markers', name='ED Visits',
                      line=dict(color='#d62728', width=3)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=hc_df['Time'], y=hc_df['Hospital Stays'],
                      mode='lines+markers', name='Hospital Stays', 
                      line=dict(color='#ff7f0e', width=3)),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=hc_df['Time'], y=hc_df['Primary Care'],
                      mode='lines+markers', name='Primary Care',
                      line=dict(color='#2ca02c', width=3)),
            row=1, col=3
        )
        
        fig.update_layout(
            height=400,
            title_text="Healthcare Utilization Patterns",
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Utilization Rate (%)")
        
        st.plotly_chart(fig, use_container_width=True)

def create_demographics_viz(df):
    """Create demographics and social factors visualization"""
    st.header("👥 Patient Demographics & Social Factors")
    
    if df is None or df.empty:
        st.warning("No data available for demographics analysis.")
        return
    
    # Use baseline data for demographics
    baseline_df = df[df['time_period'] == 'baseline']
    
    if baseline_df.empty:
        st.warning("No baseline data available for demographics.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Employment status
        if 'employed' in baseline_df.columns:
            employment_counts = baseline_df['employed'].value_counts()
            fig_emp = px.pie(
                values=employment_counts.values,
                names=['Unemployed', 'Employed'] if len(employment_counts) == 2 else employment_counts.index,
                title='Employment Status at Baseline'
            )
            fig_emp.update_layout(height=300)
            st.plotly_chart(fig_emp, use_container_width=True)
    
    with col2:
        # Insurance status
        if 'insurance' in baseline_df.columns:
            insurance_counts = baseline_df['insurance'].value_counts()
            fig_ins = px.pie(
                values=insurance_counts.values,
                names=['No Insurance', 'Has Insurance'] if len(insurance_counts) == 2 else insurance_counts.index,
                title='Insurance Coverage at Baseline'
            )
            fig_ins.update_layout(height=300)
            st.plotly_chart(fig_ins, use_container_width=True)
    
    # Mental health comorbidity
    if 'mentalillness' in baseline_df.columns:
        mental_health_rate = (baseline_df['mentalillness'] == 1).mean() * 100
        
        st.markdown(f"""
        <div class="metric-card">
        <h4>🧠 Mental Health Comorbidity</h4>
        <h2>{mental_health_rate:.1f}%</h2>
        <p>of patients have co-occurring mental health conditions</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Sidebar navigation
    st.sidebar.title("📊 Dashboard Navigation")
    
    # Load data
    with st.spinner("Loading MOUD study data..."):
        raw_data = load_data()
        processed_data = process_longitudinal_data(raw_data) if raw_data else None
    
    if raw_data is None:
        st.error("❌ Failed to load data. Please check that CSV files are in the moud-data-csv directory.")
        return
    
    # Navigation options
    sections = [
        "🏥 Study Overview",
        "📈 Treatment Outcomes", 
        "⚠️ Drug Use Patterns",
        "🏥 Healthcare Impact",
        "👥 Demographics"
    ]
    
    selected_section = st.sidebar.radio("Select Section:", sections)
    
    # Display selected section
    if selected_section == "🏥 Study Overview":
        create_overview_section()
        
        # Show study statistics
        if processed_data is not None:
            st.subheader("📊 Study Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_patients = processed_data['CID'].nunique()
                st.metric("Total Patients", f"{total_patients:,}")
            
            with col2:
                response_rate = (processed_data['responded'] == 1).mean() * 100
                st.metric("Response Rate", f"{response_rate:.1f}%")
            
            with col3:
                time_points = processed_data['time_period'].nunique()
                st.metric("Follow-up Periods", time_points)
                
            with col4:
                study_sites = processed_data['pufsite_ID'].nunique() if 'pufsite_ID' in processed_data.columns else 0
                st.metric("Study Sites", study_sites)
    
    elif selected_section == "📈 Treatment Outcomes":
        create_treatment_outcomes_viz(processed_data)
    
    elif selected_section == "⚠️ Drug Use Patterns":
        create_drug_use_patterns_viz(processed_data)
    
    elif selected_section == "🏥 Healthcare Impact":
        create_healthcare_utilization_viz(processed_data)
    
    elif selected_section == "👥 Demographics":
        create_demographics_viz(processed_data)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>MOUD Study Dashboard</p>
    <p>Understanding Opioid Treatment Outcomes</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()