import json
import termcolor
from eraXplor_az.utils.banner_utils import banner as generate_banner
from eraXplor_az.utils.parser_utils import parser
from eraXplor_az.utils.cost_export_utils import cost_export
from eraXplor_az.utils.csv_export_utils import csv_export

def main() -> None:
    """Orchestrates & Manage depends of cost export workflow."""
    
    # Banner
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")
    
    # Fetch Parsed parameters by command line
    arg_parser = parser().parse_args()
    start_date_input = arg_parser.start_date
    end_date_input = arg_parser.end_date
    subscription_id_input = arg_parser.subscription_id
    granularity_input = arg_parser.granularity
    
    # Parsing data to cost export func
    cm_client_query_results = cost_export(
        subscription_id=subscription_id_input,
        start_date=start_date_input,
        end_date=end_date_input,
        granularity=granularity_input,
    )

    print(json.dumps(cm_client_query_results, indent=4, default=str), end="\n\n\n")
    
    csv_export(cm_client_query_results)
    
if __name__ == "__main__":
    main()