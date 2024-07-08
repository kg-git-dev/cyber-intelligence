import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

# Predefined possible sitemap file paths
predefined_sitemap_paths = [
    "/sitemap-index.xml", "/sitemap.php", "/sitemap.txt",
    "/sitemap.xml.gz", "/sitemap/sitemap.xml",
    "/sitemapindex.xml", "/sitemap/index.xml", "/sitemap1.xml",
    "/rss/", "/rss.xml", "/atom.xml"
]

# Function to validate the URL
def validate_url(url):
    pattern = re.compile(
        r'^(http://|https://)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z]+)+(/)?$'
    )
    return pattern.match(url)

# Function to validate sitemap path
def validate_sitemap_path(path):
    pattern = re.compile(
        r'^(/[\w-]+)+(\.[a-zA-Z]+)?$'
    )
    return pattern.match(path)

# Function to fetch and return the content of a URL
def fetch_url_content(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        return driver.page_source
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to fetch robots.txt content and sitemap URLs
def fetch_robots_txt(driver, url):
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        robots_url = url.rstrip('/') + '/robots.txt'
        print(f"Fetching {robots_url}...")
        
        robots_content = fetch_url_content(driver, robots_url)
        if not robots_content:
            print(f"Failed to fetch {robots_url}.")
            return None
        
        print(f"Content of {robots_url}:")
        print(robots_content)
        
        sitemap_urls = re.findall(r'^Sitemap:\s*(.*)$', robots_content, re.MULTILINE)
        if sitemap_urls:
            print("Sitemap URLs found in robots.txt:")
            for sitemap_url in sitemap_urls:
                print(sitemap_url)
            return sitemap_urls
        else:
            print("No Sitemap URLs found in robots.txt.")
            return None
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")
        return None

# Function to check predefined sitemap paths
def check_predefined_sitemaps(driver, base_url):
    for path in predefined_sitemap_paths:
        sitemap_url = urljoin(base_url, path)
        print(f"Checking {sitemap_url}...")
        
        sitemap_content = fetch_url_content(driver, sitemap_url)
        if sitemap_content:
            print(f"Sitemap found at {sitemap_url}")
            print(sitemap_content)
            return sitemap_url
    return None

# Function to parse and print XML content
def parse_xml_content(xml_content):
    try:
        root = ET.fromstring(xml_content)
        # Example: Print all URLs from sitemap XML
        urls = root.findall(".//url/loc")
        if urls:
            print("URLs found in sitemap:")
            for url in urls:
                print(url.text)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <website>")
        sys.exit(1)
    
    website = sys.argv[1]
    if not validate_url(website):
        print("Invalid URL format. Please enter a valid web address.")
        sys.exit(1)

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Initialize Chrome driver
    service = Service("/usr/bin/chromedriver")  # Update this path if necessary
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Fetch robots.txt and check for sitemaps
        sitemap_urls = fetch_robots_txt(driver, website)
        if sitemap_urls:
            # Redirect to the first sitemap URL found in robots.txt
            sitemap_url = sitemap_urls[0]  # Assuming we choose the first sitemap URL
            print(f"Redirecting to {sitemap_url}...")
            sitemap_content = fetch_url_content(driver, sitemap_url)
            
            if sitemap_content:
                print(f"Sitemap content from {sitemap_url}:")
                print(sitemap_content)
                parse_xml_content(sitemap_content)
            else:
                print(f"Failed to fetch sitemap from {sitemap_url}.")
        else:
            # If no sitemaps found in robots.txt, check predefined paths
            base_url = 'https://' + website if not website.startswith(('http://', 'https://')) else website
            sitemap_url = check_predefined_sitemaps(driver, base_url)
            
            if not sitemap_url:
                print("No predefined sitemaps found. Enter a custom sitemap path or type 'quit' to exit.")
                
                while True:
                    custom_path = input("Enter sitemap path: ")
                    if custom_path.lower() == 'quit':
                        print("Exiting.")
                        break
                    if not validate_sitemap_path(custom_path):
                        print("Invalid sitemap format. Please enter a valid sitemap path.")
                        continue
                    if not custom_path.startswith('/'):
                        custom_path = '/' + custom_path
                    if '.' not in custom_path:
                        custom_path += '.xml'
                    sitemap_url = urljoin(base_url, custom_path)
                    print(f"Checking {sitemap_url}...")
                    
                    sitemap_content = fetch_url_content(driver, sitemap_url)
                    if sitemap_content:
                        print(f"Sitemap content from {sitemap_url}:")
                        print(sitemap_content)
                        parse_xml_content(sitemap_content)
                        break
                    else:
                        print(f"Sitemap not found at {sitemap_url}. Try again or type 'quit' to exit.")
    finally:
        driver.quit()
    
if __name__ == "__main__":
    main()
