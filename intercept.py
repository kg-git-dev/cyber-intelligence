import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse, parse_qs

def extract_request_details(log_entry):
    log_data = json.loads(log_entry)
    message = log_data.get('message', {})
    params = message.get('params', {})
    request = params.get('request', {})
    
    if not request:
        print("Unexpected log entry format:", json.dumps(log_data, indent=2))
        return None

    url = request['url']
    method = request['method']
    headers = request.get('headers', {})

    parsed_url = urlparse(url)
    path = parsed_url.path
    query_params = parse_qs(parsed_url.query)
    
    return {
        'method': method,
        'url': url,
        'path': path,
        'headers': headers,
        'query_params': query_params
    }

def format_request_details(details):
    if not details:
        return "Invalid request details."

    formatted_details = []
    formatted_details.append(f"Method: {details['method']}")
    formatted_details.append(f"URL: {details['url']}")
    formatted_details.append(f"Path: {details['path']}")
    
    if details['query_params']:
        formatted_details.append("Query Parameters:")
        for param, values in details['query_params'].items():
            formatted_details.append(f"  {param}: {', '.join(values)}")
    
    if details['headers']:
        formatted_details.append("Headers:")
        for header, value in details['headers'].items():
            formatted_details.append(f"  {header}: {value}")
    
    return "\n".join(formatted_details)

def intercept_requests(url):
    print("started intercept")
    # Validate and format the URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url

    # Path to the ChromeDriver executable
    CHROMEDRIVER_PATH = "./chromedriver/chromedriver"

    # Enable request interception in Chrome
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Initialize Chrome WebDriver
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.capabilities.update(capabilities)

    driver = webdriver.Chrome(service=service, options=options)

    # Open the URL
    driver.get(url)

    # Wait for some time to allow for requests to be logged
    time.sleep(5)

    # Fetch performance logs from the browser
    logs = driver.get_log('performance')

    # Filter and print network requests
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Network.requestWillBeSent' in log['method']:
            request_details = extract_request_details(entry['message'])
            formatted_details = format_request_details(request_details)
            print(formatted_details)
            print("\n" + "="*80 + "\n")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python intercept.py <URL>")
    else:
        intercept_requests(sys.argv[1])
