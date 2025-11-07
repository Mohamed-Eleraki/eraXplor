import sys
import os
from datetime import datetime, timedelta

# Add the src directory to Python path to import eraXplor modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_aws_function():
    """Simple test to verify AWS function works"""
    try:
        from eraXplor_aws.utils.cost_export_utils import monthly_account_cost_export
        
        # Test with default parameters
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"Testing AWS function with dates: {start_date} to {end_date}")
        
        cost_data = monthly_account_cost_export(
            start_date_input=start_date,
            end_date_input=end_date,
            aws_profile_name_input="default",
            cost_groupby_key_input="LINKED_ACCOUNT",
            granularity="MONTHLY"
        )
        
        print(f"✅ Success! Retrieved {len(cost_data)} cost records")
        print("Sample data:")
        for i, record in enumerate(cost_data[:3]):  # Show first 3 records
            print(f"  {i+1}. {record}")
            
        return cost_data
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    test_aws_function()