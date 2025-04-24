import boto3
from datetime import datetime, timedelta
from typing import Union, TypedDict, Dict, List

class CostRecord(TypedDict):
    """Class type annotation tool dettermining the List Schema.
    Type definition for a single cost record.
    """
    time_period: Dict[str, str]  # {'Start': str, 'End': str}
    account_id: str
    account_cost: str
    
def monthly_account_cost_export(
    start_date_input: Union[str, datetime],  # str | datetime 
    end_date_input: Union[str, datetime], 
    aws_profile_name_input: str
    ) -> List[CostRecord]:
    """Retrieves AWS account cost data for a specified time period using AWS Cost Explorer.

    Fetches the unblended costs for all linked accounts in an AWS organization for a given
    date range, grouped by account ID and returned in monthly granularity.

    Args:
        start_date_input (str): The start date of the cost report in YYYY-MM-DD format.
        end_date_input (str): The end date of the cost report in YYYY-MM-DD format.
        aws_profile_name_input (str): The name of the AWS profile to use for authentication,
            as configured in the local AWS credentials file.

    Returns:
        list: A list of dictionaries containing cost data, where each dictionary has:
            - time_period (dict): Contains 'Start' and 'End' dates for the time period
            - account_id (str): The AWS account ID
            - account_cost (str): The unblended cost amount as a string
            
    Raises:
        botocore.exceptions.ClientError: If there are AWS API authorization or parameter issues
        botocore.exceptions.ProfileNotFound: If the specified AWS profile doesn't exist
        
    Example:
        This is an illustrative example that won't actually execute AWS calls:
        >>> costs = monthly_account_cost_export('2023-01-01', '2023-01-31', 'dummy_profile')  # doctest: +SKIP
        [
            {
                'time_period': {'Start': '2023-01-01', 'End': '2023-01-31'},
                'account_id': '123456789012',
                'account_cost': '42.50'
            }
        ]
        
        For actual testing, you would need to:
        1. Have valid AWS credentials configured
        2. Use a real profile name
        3. Mark the test to run only when AWS available:
        >>> monthly_account_cost_export('2023-01-01', '2023-01-31', 'real_profile')  # doctest: +SKIP
    """
    profile_session = boto3.Session(profile_name=str(aws_profile_name_input))
    ce_client = profile_session.client('ce')

    account_cost_usage = ce_client.get_cost_and_usage(
        TimePeriod = {
            'Start': str(start_date_input),
            'End': str(end_date_input)
        },
        Granularity = 'MONTHLY',
        Metrics = ['UnblendedCost'],
        GroupBy = [  # group the result based on account ID
            {
                'Type': 'DIMENSION',
                'Key': 'LINKED_ACCOUNT'
            }
        ]
    )

    # print(json.dumps(account_cost_usage, indent=4, default=str))
    results = []
    for item in account_cost_usage['ResultsByTime']:
        time_period = item['TimePeriod']
        for group in item['Groups']:
            account_id = group['Keys'][0]
            account_cost = group['Metrics']['UnblendedCost']['Amount']
            results.append({
                'time_period': time_period,
                'account_id': account_id,
                'account_cost': account_cost
            })
            # results.append(f"Account ID: {termcolor.colored(account_id, color='yellow')}, Cost: {termcolor.colored(account_cost, color='yellow')}")
            # results.append("\n")
    return results

# help(monthly_account_cost_export)



# billing_client = profile_session.client('billing')

# response = billing_client.list_billing_views(
#     activeTimeRange={
#         'activeAfterInclusive': datetime(2025, 3, 3),
#         'activeBeforeInclusive': datetime(2025, 3, 31)
#     },
#     arns=[
#         'string',
#     ],
#     billingViewTypes=[
#         'PRIMARY'
#     ],
#     # billingViewTypes=[
#     #     'PRIMARY'|'BILLING_GROUP'|'CUSTOM',
#     # ],
#     ownerAccountId='string',
#     maxResults=123,
#     nextToken='string'
# )

# print(json.dumps(response, indent=4, default=str))