import csv
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Define acceptable thresholds (in milliseconds)
THRESHOLDS = {
    "50th Percentile Response Time": 1000,  # in ms
    "95th Percentile Response Time": 2000,  # in ms
}

# List of CSV files to validate
csv_files = [
    "reports/metrics/collections_stats.csv",
    "reports/metrics/shipments_stats.csv"
]

def print_divider():
    print(Fore.CYAN + "-" * 80)  # Cyan divider for separation

def validate_metrics(file_path):
    print_divider()
    print(Fore.YELLOW + f"Validating metrics for {file_path}")
    print_divider()

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        all_passed = True
        
        for row in reader:
            # Skip empty or aggregated rows if desired
            if not row['Name'] or row['Name'] == 'Aggregated':
                continue
            
            request_type = row['Type']
            endpoint = row['Name']
            median_response_time = float(row['50%'])
            p95_response_time = float(row['95%'])
            
            # Validate thresholds
            if median_response_time > THRESHOLDS["50th Percentile Response Time"]:
                print(Fore.RED + f"FAIL: {request_type} {endpoint} has high median response time ({median_response_time}ms)")
                all_passed = False
            else:
                print(Fore.GREEN + f"PASS: {request_type} {endpoint} - Median Response Time: {median_response_time}ms")
            
            if p95_response_time > THRESHOLDS["95th Percentile Response Time"]:
                print(Fore.RED + f"FAIL: {request_type} {endpoint} has high p95 response time ({p95_response_time}ms)")
                all_passed = False
            else:
                print(Fore.GREEN + f"PASS: {request_type} {endpoint} - p95 Response Time: {p95_response_time}ms")
        
        print_divider()
        return all_passed

# Validate each CSV file
all_files_passed = True
for csv_file in csv_files:
    if not validate_metrics(csv_file):
        all_files_passed = False

if not all_files_passed:
    print(Fore.RED + "Some metrics failed validation.")
    sys.exit(1)  # Exit with error if any validation fails

print(Fore.GREEN + "All metrics passed validation.")
print_divider()
