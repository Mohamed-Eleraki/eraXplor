#!/usr/bin/env python3
"""
Simple test to demonstrate granularity options
Run this when your FastAPI server is running on localhost:8000
"""

import json

def show_granularity_examples():
    """Show examples of using granularity in API requests"""
    
    print("🎯 eraXplor API - Granularity Feature")
    print("=" * 50)
    
    print("\n📅 Available Granularity Options:")
    print("• MONTHLY (default) - Groups costs by month")
    print("• DAILY - Provides daily cost breakdown")
    
    print("\n🔧 Example POST Request with DAILY granularity:")
    monthly_example = {
        "start_date": "2025-08-01",
        "end_date": "2025-10-30", 
        "profile": "default",
        "group_by": "LINKED_ACCOUNT-With-SERVICE",
        "granularity": "DAILY"  # 👈 This is the key parameter!
    }
    
    print("curl -X POST 'http://localhost:8000/aws/cost/export' \\")
    print("  -H 'Content-Type: application/json' \\")
    print(f"  -d '{json.dumps(monthly_example, indent=2)}'")
    
    print("\n🔧 Example GET Request with MONTHLY granularity:")
    print("curl 'http://localhost:8000/aws/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=MONTHLY'")
    
    print("\n📊 Expected Response with granularity info:")
    response_example = {
        "success": True,
        "message": "AWS cost data exported successfully",
        "total_records": 31,
        "request_parameters": {
            "start_date": "2025-08-01",
            "end_date": "2025-10-30",
            "profile": "default", 
            "group_by": "LINKED_ACCOUNT-With-SERVICE",
            "granularity": "DAILY"  # 👈 Confirms granularity used
        }
    }
    
    print(json.dumps(response_example, indent=2))
    
    print("\n💡 Key Differences:")
    print("📅 MONTHLY: TIME_PERIOD spans entire months")
    print("   Example: {'Start': '2025-08-01', 'End': '2025-09-01'}")
    print("📅 DAILY: TIME_PERIOD shows single days")  
    print("   Example: {'Start': '2025-08-01', 'End': '2025-08-02'}")
    
    print("\n✅ Your API already supports granularity!")
    print("🚀 Both endpoints (POST and GET) accept the 'granularity' parameter")

if __name__ == "__main__":
    show_granularity_examples()