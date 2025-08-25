#!/usr/bin/env python3
"""
Data processing utilities for MOUD study dashboard
Generates JSON data for web-based visualizations
"""

import csv
import json
from pathlib import Path
from collections import defaultdict, Counter

class MOUDDataProcessor:
    def __init__(self, data_path="moud-data-csv"):
        self.data_path = Path(data_path)
        self.datasets = {
            'baseline': 'Patient-Baseline-Data.csv',
            '3_month': 'Patient-3-month-Data.csv', 
            '6_month': 'Patient-6-month-Data.csv',
            '12_month': 'Patient-12-month-Data.csv',
            '18_month': 'Patient-18-month-Data.csv'
        }
        self.raw_data = {}
        
    def load_all_data(self):
        """Load all CSV files into memory"""
        for timepoint, filename in self.datasets.items():
            filepath = self.data_path / filename
            if filepath.exists():
                self.raw_data[timepoint] = self._load_csv(filepath)
                print(f"Loaded {timepoint}: {len(self.raw_data[timepoint])} records")
        
    def _load_csv(self, filepath):
        """Load a single CSV file"""
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    
    def get_treatment_outcomes(self):
        """Analyze treatment outcomes over time"""
        outcomes = {}
        
        for timepoint, data in self.raw_data.items():
            if not data:
                continue
                
            # Count current treatments
            bup_count = sum(1 for row in data if row.get('currentbup') == '1')
            mmt_count = sum(1 for row in data if row.get('currentmmt') == '1')
            ntx_count = sum(1 for row in data if row.get('currentntx') == '1')
            
            # Count opioid use
            opioid_use = sum(1 for row in data if row.get('opuse30') == '1')
            
            total_patients = len(data)
            
            outcomes[timepoint] = {
                'timepoint': timepoint,
                'total_patients': total_patients,
                'buprenorphine': bup_count,
                'methadone': mmt_count,
                'naltrexone': ntx_count,
                'opioid_use_30_days': opioid_use,
                'bup_rate': round(bup_count / total_patients * 100, 1) if total_patients > 0 else 0,
                'mmt_rate': round(mmt_count / total_patients * 100, 1) if total_patients > 0 else 0,
                'ntx_rate': round(ntx_count / total_patients * 100, 1) if total_patients > 0 else 0,
                'opioid_rate': round(opioid_use / total_patients * 100, 1) if total_patients > 0 else 0
            }
            
        return outcomes
    
    def get_demographic_summary(self):
        """Get demographic summary from baseline data"""
        baseline = self.raw_data.get('baseline', [])
        if not baseline:
            return {}
            
        demographics = {
            'total_patients': len(baseline),
            'sex': Counter(),
            'age_categories': Counter(), 
            'race_ethnicity': Counter(),
            'education': Counter(),
            'employment': Counter()
        }
        
        for row in baseline:
            # Gender/Sex
            sex = row.get('sex', '').strip()
            if sex == '1':
                demographics['sex']['Male'] += 1
            elif sex == '2':
                demographics['sex']['Female'] += 1
            elif sex:
                demographics['sex'][f'Other ({sex})'] += 1
            
            # Age categories
            agecat = row.get('agecat', '').strip()
            age_mapping = {
                '1': '18-25',
                '2': '26-35', 
                '3': '36-45',
                '4': '46-55',
                '5': '56-65',
                '6': '65+'
            }
            if agecat in age_mapping:
                demographics['age_categories'][age_mapping[agecat]] += 1
            elif agecat:
                demographics['age_categories'][f'Category {agecat}'] += 1
            
            # Race/ethnicity
            raceth = row.get('raceth', '').strip()
            race_mapping = {
                '1': 'White',
                '2': 'Black/African American',
                '3': 'Hispanic/Latino', 
                '4': 'Asian',
                '5': 'Native American',
                '6': 'Mixed Race',
                '7': 'Other'
            }
            if raceth in race_mapping:
                demographics['race_ethnicity'][race_mapping[raceth]] += 1
            elif raceth:
                demographics['race_ethnicity'][f'Category {raceth}'] += 1
            
            # Education
            educat = row.get('educat', '').strip() or row.get('education', '').strip()
            education_mapping = {
                '1': 'Less than High School',
                '2': 'High School/GED',
                '3': 'Some College',
                '4': 'College Graduate',
                '5': 'Graduate Degree',
                '6': 'Post-Graduate'
            }
            if educat in education_mapping:
                demographics['education'][education_mapping[educat]] += 1
            elif educat:
                demographics['education'][f'Level {educat}'] += 1
            
            # Employment
            employed = row.get('employed', '').strip()
            employment_mapping = {
                '1': 'Full-time',
                '2': 'Part-time', 
                '3': 'Unemployed',
                '4': 'Disabled',
                '5': 'Retired',
                '6': 'Student'
            }
            if employed in employment_mapping:
                demographics['employment'][employment_mapping[employed]] += 1
            elif employed:
                demographics['employment'][f'Status {employed}'] += 1
        
        return demographics
    
    def get_healthcare_utilization(self):
        """Analyze healthcare utilization patterns"""
        utilization = {}
        
        for timepoint, data in self.raw_data.items():
            if not data:
                continue
                
            # Look for healthcare utilization variables
            ed_visits = []
            hospital_stays = []
            
            for row in data:
                # Emergency department visits
                for key, value in row.items():
                    if 'ed' in key.lower() and 'visit' in key.lower():
                        if value and value.isdigit():
                            ed_visits.append(int(value))
                    elif 'hospital' in key.lower() and ('stay' in key.lower() or 'admit' in key.lower()):
                        if value and value.isdigit():
                            hospital_stays.append(int(value))
            
            utilization[timepoint] = {
                'timepoint': timepoint,
                'total_patients': len(data),
                'avg_ed_visits': round(sum(ed_visits) / len(ed_visits), 2) if ed_visits else 0,
                'avg_hospital_stays': round(sum(hospital_stays) / len(hospital_stays), 2) if hospital_stays else 0,
                'patients_with_ed_visits': len([x for x in ed_visits if x > 0]),
                'patients_with_hospital_stays': len([x for x in hospital_stays if x > 0])
            }
        
        return utilization
    
    def generate_dashboard_data(self):
        """Generate all data needed for dashboard"""
        self.load_all_data()
        
        dashboard_data = {
            'study_overview': {
                'title': 'Medications for Opioid Use Disorder (MOUD) Study',
                'description': 'CDC National Center for Injury Prevention and Control longitudinal study tracking treatment outcomes for opioid use disorder across the United States',
                'total_patients': len(self.raw_data.get('baseline', [])),
                'study_period': {
                    'start_date': 'March 2018',
                    'end_date': 'May 2021',
                    'duration': '3+ years',
                    'follow_up_period': '18 months per patient'
                },
                'timepoints': {
                    'baseline': {'label': 'Baseline', 'description': 'Treatment initiation (March 2018 onwards)'},
                    '3_month': {'label': '3-Month Follow-up', 'description': '3 months post-baseline'},
                    '6_month': {'label': '6-Month Follow-up', 'description': '6 months post-baseline'},
                    '12_month': {'label': '12-Month Follow-up', 'description': '12 months post-baseline'},
                    '18_month': {'label': '18-Month Follow-up', 'description': '18 months post-baseline (May 2021)'}
                },
                'study_locations': [
                    'Birmingham, AL', 'Boston, MA', 'Chicago, IL', 'Cincinnati, OH',
                    'Dallas, TX', 'Denver, CO', 'Huntington, WV', 'Los Angeles, CA',
                    'New York, NY', 'Phoenix, AZ', 'Raleigh-Durham, NC', 
                    'Salt Lake City, UT', 'San Francisco, CA', 'Seattle, WA', 
                    'Washington, DC Metro Area'
                ],
                'data_collection_period': '18 months per patient',
                'response_rates': {
                    'baseline': '100% (1,974 patients)',
                    '3_month': '72%',
                    '6_month': '68%', 
                    '12_month': '52%',
                    '18_month': '53%'
                }
            },
            'treatment_outcomes': self.get_treatment_outcomes(),
            'demographics': self.get_demographic_summary(),
            'healthcare_utilization': self.get_healthcare_utilization(),
            'moud_medications': {
                'buprenorphine': {
                    'name': 'Buprenorphine',
                    'description': 'Partial opioid agonist that reduces cravings and withdrawal symptoms',
                    'brand_names': ['Suboxone', 'Subutex', 'Zubsolv']
                },
                'methadone': {
                    'name': 'Methadone',
                    'description': 'Full opioid agonist administered in specialized clinics',
                    'brand_names': ['Dolophine', 'Methadose']
                },
                'naltrexone': {
                    'name': 'Naltrexone',
                    'description': 'Opioid antagonist that blocks the effects of opioids',
                    'brand_names': ['Vivitrol', 'ReVia', 'Depade']
                }
            }
        }
        
        return dashboard_data
    
    def save_dashboard_data(self, output_file='dashboard_data.json'):
        """Save processed data to JSON file"""
        data = self.generate_dashboard_data()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Dashboard data saved to {output_file}")
        return data

if __name__ == "__main__":
    processor = MOUDDataProcessor()
    data = processor.save_dashboard_data()
    
    print("\nDashboard Data Summary:")
    print(f"- Study includes {data['study_overview']['total_patients']} patients")
    print(f"- Tracked over {len(data['treatment_outcomes'])} timepoints")
    print(f"- Treatment outcomes calculated for all medications")