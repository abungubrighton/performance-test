import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os

# Define the list of tests to run with the appropriate flags
tests = [
    {
        "file": "./tests/load_tests/endpoints/collections_tests.py", 
        "csv_report": "reports/metrics/collections", 
        "html_report": "reports/summaries/collections.html"
    },
    {
        "file": "./tests/load_tests/endpoints/shipments_tests.py", 
        "csv_report": "reports/metrics/shipments", 
        "html_report": "reports/summaries/shipments.html"
    }
]

# Create the reports directory if it doesn't exist
os.makedirs("reports/metrics", exist_ok=True)
os.makedirs("reports/summaries", exist_ok=True)

# Loop through each test and run it using os.system
for test in tests:
    command = f"locust -f {test['file']} --headless --csv {test['csv_report']} --html {test['html_report']}"
    os.system(command)
    print(f"Test completed for {test['file']}, CSV saved to {test['csv_report']} and HTML saved to {test['html_report']}")
