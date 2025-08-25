# MOUD Study Dashboard - Enhanced Apple-Style Interface

A sophisticated, interactive data analytics dashboard for understanding Medications for Opioid Use Disorder (MOUD) study outcomes and US healthcare trends. Features a modern Apple-inspired design with comprehensive educational content.

## 📊 Dashboard Overview

This enhanced dashboard presents longitudinal data from a **CDC National Center for Injury Prevention and Control** study of **1,974 patients** with Opioid Use Disorder tracked over **18 months** (March 2018 - May 2021) across **15 US cities**. Designed with Apple-style aesthetics and sophisticated analytics for healthcare professionals, policymakers, and newcomers to the field.

## 🚀 Quick Start

### Method 1: Enhanced Dashboard (Recommended)
```bash
python3 serve_dashboard.py
```
Then open: **http://localhost:8000/enhanced_dashboard.html**

### Method 2: Original Dashboard
```bash
python3 serve_dashboard.py
```
Then open: **http://localhost:8000/index.html**

### Method 3: Direct File Access
Open `enhanced_dashboard.html` directly in any modern web browser.

## 📁 Project Structure

```
data_viz_opiods_v1/
├── enhanced_dashboard.html     # 🌟 Enhanced Apple-style dashboard (RECOMMENDED)
├── index.html                  # Original dashboard interface  
├── dashboard_data.json         # Processed study data
├── data_processor.py          # Advanced data processing utilities
├── serve_dashboard.py         # Local HTTP server
├── test_data_loading.py       # Data validation script
├── simple_demographics.html   # Standalone demographics viewer
├── debug_demographics.html    # Demographics debugging tool
├── app.py                     # Streamlit version (requires packages)
├── DASHBOARD_FEATURES.md      # Detailed feature documentation
└── moud-data-csv/            # Original CDC study data
    ├── Patient-Baseline-Data.csv
    ├── Patient-3-month-Data.csv
    ├── Patient-6-month-Data.csv
    ├── Patient-12-month-Data.csv
    └── Patient-18-month-Data.csv
```

## 🏥 Dashboard Features

### 📈 Interactive Visualizations
- **Treatment Outcomes**: Track MOUD medication adherence over time
- **Opioid Use Reduction**: Monitor treatment effectiveness
- **Healthcare Impact**: Analyze healthcare utilization patterns
- **Demographics**: Understand patient population characteristics

### 🎓 Educational Content
- **MOUD Medications**: Detailed explanations of Buprenorphine, Methadone, and Naltrexone
- **Healthcare Context**: US healthcare system background for newcomers
- **Treatment Benefits**: Evidence-based outcomes and cost savings

### 📱 Responsive Design
- Mobile-friendly interface
- Interactive charts with Chart.js
- Clean, professional styling
- Accessible navigation

## 💊 Understanding MOUD

### Three FDA-Approved Medications:

1. **Buprenorphine (Suboxone)** - 33% of patients at baseline
   - Partial opioid agonist
   - Reduces cravings and withdrawal
   - Office-based treatment

2. **Methadone** - 62% of patients at baseline
   - Full opioid agonist
   - Daily clinic-based treatment
   - Comprehensive support services

3. **Naltrexone (Vivitrol)** - 4.4% of patients at baseline
   - Opioid antagonist
   - Blocks euphoric effects
   - Monthly injection option

## 📊 Key Study Findings

- **Treatment Retention**: Medication adherence patterns across 18 months
- **Opioid Use Reduction**: From 2.5% to 0.3% reporting recent use
- **Healthcare Utilization**: Impact on emergency department visits and hospitalizations
- **Longitudinal Outcomes**: Patient progress tracked through 5 data collection points

## 🔧 Technical Details

### Data Processing
- **Python-based**: Pure Python data processing (no external dependencies)
- **JSON Output**: Clean, structured data for web visualization
- **Performance**: Optimized for handling large CSV datasets (1,600+ variables)

### Web Technology
- **HTML5**: Modern semantic markup
- **Chart.js**: Interactive, responsive charts
- **CSS Grid/Flexbox**: Responsive layout system
- **JavaScript ES6**: Modern browser compatibility

### Browser Compatibility
- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🎯 Target Audience

This dashboard is designed for:
- **Healthcare Policymakers**: Understanding treatment effectiveness
- **Healthcare Providers**: Learning about MOUD outcomes
- **Researchers**: Analyzing longitudinal treatment data
- **General Public**: Understanding the opioid crisis and treatment options
- **International Users**: Learning about US healthcare approaches

## 📚 Healthcare Context

The dashboard provides essential context about:
- US healthcare system structure
- Opioid use disorder treatment approaches
- Evidence-based treatment outcomes
- Public health impact and cost savings

## 🔄 Data Updates

To update the dashboard with new data:

1. Replace CSV files in `moud-data-csv/` directory
2. Run the data processor: `python3 data_processor.py`
3. Refresh the dashboard in your browser

## ⚡ Performance Notes

- **Data Loading**: ~2MB JSON file loads instantly
- **Chart Rendering**: Interactive charts with smooth animations
- **Mobile Performance**: Optimized for mobile devices
- **Offline Capability**: Works without internet after initial load

## 🤝 Contributing

This dashboard was built to be:
- **Extensible**: Easy to add new visualizations
- **Maintainable**: Clean, documented code
- **Educational**: Explains complex healthcare concepts clearly
- **Accessible**: Works across devices and skill levels

## 📞 Support

For questions about the data or dashboard functionality, refer to the original MOUD study documentation or healthcare policy resources.

---

**🏥 Built to advance understanding of evidence-based opioid use disorder treatment in the United States.**