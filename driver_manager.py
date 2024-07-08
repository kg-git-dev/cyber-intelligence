from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ChromeDriverManager:
    _driver = None
    
    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls.initialize_driver()
        return cls._driver
    
    @classmethod
    def initialize_driver(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        # Initialize Chrome driver
        service = Service("/usr/bin/chromedriver")  # Update this path if necessary
        cls._driver = webdriver.Chrome(service=service, options=chrome_options)

    @classmethod
    def quit_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None
