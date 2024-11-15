# MainOrchestrator.py
from ResearchAgent import ResearchAgent
from MultiAgentSystem import IndustryAgent, UseCaseAgent, GenAISolutionsAgent
import json

class MultiAgentOrchestrator:
    def __init__(self, company_name):
        self.company_name = company_name
        self.research_agent = ResearchAgent()
        self.industry_agent = IndustryAgent()
        self.use_case_agent = UseCaseAgent()
        self.genai_solutions_agent = GenAISolutionsAgent()

    def run_workflow(self):
        # Step 1: Gather industry info and key offerings
        research_data = self.research_agent.gather_company_info(self.company_name, "industry segment")
        key_offerings_info = self.research_agent.gather_company_info(self.company_name, "key offerings")
        dataset_info = self.research_agent.gather_datasets(self.company_name)
        self.research_agent.save_to_csv(research_data, key_offerings_info, dataset_info, f"{self.company_name}_research.xlsx")

        # Step 2: Analyze industry using IndustryAgent
        print(self.company_name)
        industry_analysis = self.industry_agent.analyze_industry(self.company_name) 

        # Step 3: Generate use cases based on industry analysis
        use_cases = self.use_case_agent.generate_use_cases(industry_analysis) 

        # Step 4: Suggest GenAI solutions based on use cases
        genai_solutions = self.genai_solutions_agent.suggest_genai_solutions(use_cases)

        return {
        "use_cases": use_cases,
        "genai_solutions": genai_solutions,
        "research_data": research_data  # Assume this is a dict of sheet names with data
        }

    def close(self):
        self.research_agent.close()

# Example usage
if __name__ == "__main__":
    company_name = "Tesla"
    orchestrator = MultiAgentOrchestrator(company_name)
    orchestrator.run_workflow()
    orchestrator.close()