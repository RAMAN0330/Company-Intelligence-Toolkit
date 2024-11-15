import google.generativeai as genai
import logging
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Setup logging
logging.basicConfig(level=logging.INFO)

# Industry Agent
class IndustryAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_industry(self, company_name):
        prompt_text = f"Provide a brief overview of the industry for {company_name}."
        
        try:
            response = self.model.generate_content(prompt_text)
            logging.info(f"IndustryAgent response: {response}")

            if not response or not response.text.strip():
                raise ValueError("Received empty response from IndustryAgent.")
            
            return response.text
        
        except Exception as e:
            logging.error(f"Error in IndustryAgent: {e}")
            time.sleep(5)  # Adding delay in case of rate-limiting issues
            return "Error: Unable to fetch valid industry data."


# Use Case Agent
class UseCaseAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_use_cases(self, industry_info):
        prompt_text = (
            f"Based on the following industry information: {industry_info}, propose detailed AI and ML use cases for the company. "
            f"Each use case should include:\n\n"
            f"1. Objective/Use Case: Describe the main goal of the AI solution.\n"
            f"2. AI Application: Explain the specific AI technology and methods to be used.\n"
            f"3. Cross-Functional Benefits: List benefits for various departments like Operations, "
            f"Finance, and Quality Assurance.\n\n"
            f"Please follow this format for each use case, providing relevant, industry-specific examples."
        )
        
        try:
            response = self.model.generate_content(prompt_text)
            logging.info(f"UseCaseAgent response: {response}")

            if not response or not response.text.strip():
                raise ValueError("Received empty response from UseCaseAgent.")
            
            return response.text
        
        except Exception as e:
            logging.error(f"Error in UseCaseAgent: {e}")
            return "Error: Unable to generate use cases."


# GenAI Solutions Agent
class GenAISolutionsAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def suggest_genai_solutions(self, use_cases):
        prompt_text = (
            f"For the following use cases: {use_cases}, propose GenAI solutions such as document search, automated reporting, and chat systems."
        )

        try:
            response = self.model.generate_content(prompt_text)
            logging.info(f"GenAISolutionsAgent response: {response}")

            if not response or not response.text.strip():
                raise ValueError("Received empty response from GenAISolutionsAgent.")
            
            return response.text
        
        except Exception as e:
            logging.error(f"Error in GenAISolutionsAgent: {e}")
            return "Error: Unable to suggest GenAI solutions."
