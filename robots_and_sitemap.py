from driver_manager import ChromeDriverManager
from links_manager import LinksManager
from bs4 import BeautifulSoup
import re

def validate_url(website_url):
    pattern = re.compile(
        r'^(http://|https://)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z]+)+(/)?$'
    )
    return pattern.match(website_url)


def format_url(url, protocol_choice):
    if protocol_choice == '1':
        return 'https://' + url
    elif protocol_choice == '2':
        return 'http://' + url


def get_protocol_choice():
    while True:
        choice = input("Choose protocol (1 for HTTPS, 2 for HTTP, Enter for HTTPS): ").strip()
        if choice == '1' or choice == '2':
            return choice
        elif choice == '':
            return '1'
        else:
            print("Invalid choice. Please choose 1, 2, or leave empty for default HTTPS.")


def extract_links_from_sitemap_xml(sitemap_url, driver):
    print(sitemap_url, "here")

def get_robots_txt(website_url):
    driver = ChromeDriverManager.get_driver()
    website_url = website_url.rstrip('/')

    try:
        robots_url = website_url + '/robots.txt'
        print(f"Fetching {robots_url}...")
        
        driver.get(robots_url)
        robots_content = driver.page_source
        
        soup = BeautifulSoup(robots_content, 'html.parser')
        robotsTxt = soup.get_text()
        
        if not robots_content:
            print(f"Failed to fetch {robots_url}.")
            return None

        print(f"Content of {robots_url}:")
        print(robotsTxt)
        
        sitemap_urls = re.findall(r'^Sitemap:\s*(.*)$', robotsTxt, re.MULTILINE)
        if sitemap_urls:
            print("Sitemap URLs found in robots.txt:")
            for sitemap_url in sitemap_urls:
                LinksManager.add_sitemap_urls(sitemap_url)
                print(sitemap_url)
                extract_links_from_sitemap_xml(sitemap_url, driver)

            return sitemap_urls
        else:
            print("No Sitemap URLs found in robots.txt.")
            return None
            
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")
        return None
    finally:
        ChromeDriverManager.quit_driver()


if __name__ == "__main__":
    while True:
        website_url = input("Enter the website URL to scan (or 'exit' to quit): ").strip()
        
        if website_url.lower() == 'exit':
            print("Exiting program.")
            break
        
        if not validate_url(website_url):
            print("Invalid URL format. Please enter a valid web address.")
            continue
        
        # Check if the URL has a protocol; if not, prompt for choice
        if not website_url.startswith('http://') and not website_url.startswith('https://'):
            protocol_choice = get_protocol_choice()
            website_url = format_url(website_url, protocol_choice)
        
        get_robots_txt(website_url)
        break


