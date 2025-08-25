#!/usr/bin/env python3
"""
Simple test script to verify MOUD data can be loaded and basic statistics calculated
"""

import csv
import os
from pathlib import Path

def test_data_loading():
    """Test loading and basic analysis of MOUD CSV files"""
    data_path = Path("moud-data-csv")
    
    if not data_path.exists():
        print(f"Error: Data directory {data_path} not found")
        return False
    
    datasets = {
        'baseline': 'Patient-Baseline-Data.csv',
        '3_month': 'Patient-3-month-Data.csv', 
        '6_month': 'Patient-6-month-Data.csv',
        '12_month': 'Patient-12-month-Data.csv',
        '18_month': 'Patient-18-month-Data.csv'
    }
    
    results = {}
    
    for timepoint, filename in datasets.items():
        filepath = data_path / filename
        
        if not filepath.exists():
            print(f"Warning: {filename} not found")
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                # Count rows and analyze key columns
                row_count = 0
                opioid_use_cols = []
                treatment_cols = []
                
                for header in headers:
                    if 'opuse' in header.lower() or 'opioid' in header.lower():
                        opioid_use_cols.append(header)
                    elif any(med in header.lower() for med in ['bup', 'mmt', 'ntx', 'methadone', 'naltrexone']):
                        treatment_cols.append(header)
                
                # Count data rows (skip header)
                for row in reader:
                    row_count += 1
                
                results[timepoint] = {
                    'file': filename,
                    'rows': row_count,
                    'columns': len(headers),
                    'opioid_vars': opioid_use_cols[:5],  # First 5 for brevity
                    'treatment_vars': treatment_cols[:5]  # First 5 for brevity
                }
                
                print(f"✓ {timepoint}: {row_count} patients, {len(headers)} variables")
                
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    return results

def analyze_key_variables(results):
    """Analyze key variables across timepoints"""
    print("\n=== Key Variable Analysis ===")
    
    for timepoint, data in results.items():
        print(f"\n{timepoint.upper()} ({data['rows']} patients):")
        print(f"  Opioid use variables: {data['opioid_vars']}")
        print(f"  Treatment variables: {data['treatment_vars']}")

if __name__ == "__main__":
    print("MOUD Data Loading Test")
    print("=====================")
    
    results = test_data_loading()
    
    if results:
        analyze_key_variables(results)
        print(f"\n✓ Successfully loaded {len(results)} datasets")
        print("Dashboard data loading verified!")
    else:
        print("❌ Data loading failed")