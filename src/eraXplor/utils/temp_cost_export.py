import boto3
import json

profile_session = boto3.Session(profile_name="eraki")
ce_client = profile_session.client('ce')
account_cost_usage = ce_client.get_cost_and_usage(
    TimePeriod = {
        'Start': '2025-01-01',
        'End': '2025-03-30'
    },
    Granularity = 'MONTHLY',
    Metrics = ['UnblendedCost'],
    # GroupBy = [  # group the result based on account ID
    #     {
    #         'Type': 'DIMENSION',
    #         'Key': 'LINKED_ACCOUNT'
    #     }
    # ]
)    
print(json.dumps(account_cost_usage, indent=4, default=str))  # print all