import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse, parse_qs

# Define the relevant HTTP methods for penetration testing
RELEVANT_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

def extract_request_details(log_entry):
    log_data = json.loads(log_entry)
    message = log_data.get('message', {})
    params = message.get('params', {})
    request = params.get('request', {})
    
    if not request:
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
    print("Started intercept")

    # Validate and format the URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url

    # Enable request interception in Chrome
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Initialize Chrome WebDriver
    service = Service('/usr/bin/chromedriver')  
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = "/usr/bin/chromium-browser" 
    options.capabilities.update(capabilities)

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        return

    # Open the URL
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error loading URL {url}: {e}")
        driver.quit()
        return

    # Wait for some time to allow for requests to be logged
    time.sleep(5)

    # Fetch performance logs from the browser
    try:
        logs = driver.get_log('performance')
    except Exception as e:
        print(f"Error fetching performance logs: {e}")
        driver.quit()
        return

    # Filter and print relevant network requests
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Network.requestWillBeSent' in log['method']:
            request_details = extract_request_details(entry['message'])
            if request_details and request_details['method'] in RELEVANT_METHODS:
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
