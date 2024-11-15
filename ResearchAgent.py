# ResearchAgent.py
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import pandas as pd
import time

# Load environment variables from the .env file
load_dotenv()

class ResearchAgent:
    """
    A web-scraping agent that automates the process of gathering industry information,
    key offerings, strategic areas, and relevant datasets about a specified company.
    
    Attributes:
        driver_path (str): Path to the Chrome WebDriver.
        driver (webdriver.Chrome): An instance of Chrome WebDriver with specified options.
    """
    
    def __init__(self):
        """
        Initializes the ResearchAgent with Chrome WebDriver settings.
        """
        # Load ChromeDriver path from environment variable
        driver_path = os.getenv("CHROMEDRIVER_PATH")
        self.filename = ''
        
        # Initialize Chrome options for running in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without GUI
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Set up the WebDriver with specified path and options
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_page_load_timeout(240)  # Set page load timeout to 240 seconds
    
    def search_info(self, query):
        """
        Performs a Google search and returns the top search result links and titles.
        
        Parameters:
            query (str): The search query.
        
        Returns:
            list of dict: A list of dictionaries containing titles and links to the top search results.
        """
        self.driver.get("https://www.google.com")
        try:
            # Explicit wait for the search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            # Explicit wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='g']//a"))
            )

            results = self.driver.find_elements(By.XPATH, "//div[@class='g']//a")
            links = []
            for result in results[:10]:  # Collect information from the top 10 results
                title = result.find_element(By.XPATH, ".//h3").text
                link = result.get_attribute("href")
                links.append({"title": title, "link": link})

            return links

        except TimeoutException:
            print("Timeout occurred during Google search.")
            return []

    def fetch_details_from_link(self, link):
        """
        Fetches and returns relevant content from a provided link, extracting key information.
        
        Parameters:
            link (str): The URL of the webpage to extract content from.
        
        Returns:
            str: A snippet of relevant content from the webpage.
        """
        try:
            self.driver.get(link)
            # Explicit wait to ensure the page loads
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
            page_content = [para.text for para in paragraphs[:5]]  # Limit to top 5 paragraphs
            
            return " ".join(page_content)
        
        except TimeoutException:
            print(f"Timeout occurred while loading {link}. Skipping this link.")
            return None

    def gather_company_info(self, company_name, query_type):
        """
        Gathers information about the company based on the specified query type.
        
        Parameters:
            company_name (str): The name of the company to research.
            query_type (str): The type of information to gather (e.g., "industry segment", "key offerings").
        
        Returns:
            dict: A dictionary containing information aggregated across multiple sources.
        """
        query = f"{company_name} {query_type}"
        links = self.search_info(query)
        info = {
            "company": company_name,
            "industry_info" if query_type == "industry segment" else "key_offerings": []
        }
        
        for item in links:
            try:
                content = self.fetch_details_from_link(item["link"])
                info["industry_info" if query_type == "industry segment" else "key_offerings"].append({
                    "title": item["title"],
                    "link": item["link"],
                    "content_snippet": content
                })
            except Exception as e:
                print(f"Error fetching details from {item['link']}: {e}")
        
        print(f"Gathered info for {query_type}: {info}")  # Debugging line
        return info

    def gather_datasets(self, company_name):
        """
        Searches for relevant datasets for the company's industry or key offerings.
        
        Parameters:
            company_name (str): The name of the company to research.
        
        Returns:
            dict: A dictionary containing dataset links and titles.
        """
        query = f"{company_name} datasets AI machine learning"
        links = self.search_info(query)
        dataset_info = {"company": company_name, "datasets": []}
        
        for item in links:
            try:
                content = self.fetch_details_from_link(item["link"])
                dataset_info["datasets"].append({
                    "title": item["title"],
                    "link": item["link"],
                    "content_snippet": content
                })
            except Exception as e:
                print(f"Error fetching dataset details from {item['link']}: {e}")
        
        return dataset_info

    def save_to_csv(self, industry_info, key_offerings_info, dataset_info, filename):
        """
        Saves the gathered industry, key offerings, and dataset information to a single CSV file.
        
        Parameters:
            industry_info (dict): The research information about industry segment.
            key_offerings_info (dict): The research information about key offerings.
            dataset_info (dict): The information about relevant datasets.
            filename (str): The name of the CSV file to save the data.
        """
        # Combine industry, key offerings, and dataset information
        industry_df = pd.DataFrame(industry_info["industry_info"])
        key_offerings_df = pd.DataFrame(key_offerings_info["key_offerings"])
        datasets_df = pd.DataFrame(dataset_info["datasets"])
        
        # Save each to a separate sheet in the same Excel file
        with pd.ExcelWriter(filename) as writer:
            industry_df.to_excel(writer, sheet_name="Industry_Info", index=False)
            key_offerings_df.to_excel(writer, sheet_name="Key_Offerings", index=False)
            datasets_df.to_excel(writer, sheet_name="Datasets", index=False)
        
        print(f"Research completed. Data saved to {filename}.")

    def close(self):
        """Closes the WebDriver to free up system resources."""
        self.driver.quit()
