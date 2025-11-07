#!/usr/bin/env python3
"""Test script to demonstrate granularity options in the eraXplor API"""

import json
import requests
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_granularity_options():
    """Test both MONTHLY and DAILY granularity options"""
    
    # Test dates (recent 30 days to ensure data is available)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print("🧪 Testing Granularity Options in eraXplor API")
    print("=" * 60)
    
    # Test 1: Monthly Granularity (Default)
    print("\n📅 Test 1: MONTHLY Granularity")
    print("-" * 40)
    
    monthly_payload = {
        "start_date": start_date,
        "end_date": end_date,
        "profile": "default",
        "group_by": "LINKED_ACCOUNT",
        "granularity": "MONTHLY"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/aws/cost/export", json=monthly_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Monthly request successful!")
            print(f"📊 Total records: {data['total_records']}")
            print(f"🔧 Request parameters: {json.dumps(data['request_parameters'], indent=2)}")
            if data['cost_data']:
                print(f"📝 Sample record: {json.dumps(data['cost_data'][0], indent=2)}")
        else:
            print(f"❌ Monthly request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Monthly request error: {str(e)}")
    
    # Test 2: Daily Granularity
    print("\n📅 Test 2: DAILY Granularity")
    print("-" * 40)
    
    # Use shorter date range for daily to avoid too many records
    daily_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    daily_payload = {
        "start_date": daily_start,
        "end_date": end_date,
        "profile": "default", 
        "group_by": "LINKED_ACCOUNT",
        "granularity": "DAILY"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/aws/cost/export", json=daily_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Daily request successful!")
            print(f"📊 Total records: {data['total_records']}")
            print(f"🔧 Request parameters: {json.dumps(data['request_parameters'], indent=2)}")
            if data['cost_data']:
                print(f"📝 Sample record: {json.dumps(data['cost_data'][0], indent=2)}")
        else:
            print(f"❌ Daily request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Daily request error: {str(e)}")
    
    # Test 3: GET request with granularity parameter
    print("\n📅 Test 3: GET Request with Granularity")
    print("-" * 40)
    
    try:
        params = {
            "start_date": daily_start,
            "end_date": end_date,
            "profile": "default",
            "group_by": "LINKED_ACCOUNT", 
            "granularity": "DAILY"
        }
        
        response = requests.get(f"{BASE_URL}/aws/cost/export", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET request with granularity successful!")
            print(f"📊 Total records: {data['total_records']}")
            print(f"🔧 Request parameters: {json.dumps(data['request_parameters'], indent=2)}")
        else:
            print(f"❌ GET request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ GET request error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Granularity Options Summary:")
    print("• MONTHLY: Aggregates cost data by month")
    print("• DAILY: Provides daily cost breakdown") 
    print("• Both work with POST and GET requests")
    print("• Default is MONTHLY if not specified")

if __name__ == "__main__":
    test_granularity_options()