# AI Use Case Generator for Companies

A Streamlit-based web application that generates AI/ML use cases and GenAI solutions for companies. Given a company name, the app fetches relevant data and displays AI/ML use cases, suggested GenAI solutions, and additional research insights if available.

---

## Features

- **AI/ML Use Case Generation**: Provides AI/ML-based use cases tailored to a specified company.
- **GenAI Solution Suggestions**: Lists potential Generative AI solutions that can enhance the company’s operations.
- **Research Data Display**: Automatically displays relevant research data from an `.xlsx` file in the directory named as `{company_name}_research.xlsx`.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.9 installed. Then, install the necessary dependencies using:

```bash
pip install -r requirements.txt
```
## Directory Structure
-  app.py: Main Streamlit app file.
-  MainOrchestrator.py: Contains the orchestration logic for AI/ML use case generation.
-  company_name}_research.xlsx: Excel file in the current directory, containing research data related to the specified company.

## Installation
Clone this repository and install the dependencies:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```
## Usage
- Run the Streamlit app:
  ```bash
  streamlit run app.py
  ```
- Enter a company name in the input field. Ensure there’s an .xlsx file in the directory named {company_name}_research.xlsx (e.g., Tesla_research.xlsx).
- Click on Generate Use Cases and Solutions to fetch and display data.

The project includes the following components:

	•	MultiAgentOrchestrator: Main orchestrator to handle workflow execution for use case and GenAI solution generation.
	•	Streamlit App: UI setup with inputs and display sections for use cases, GenAI solutions, and research data.

## Example
- Suppose you enter Tesla as the company name:
	- The app fetches or generates:
	- Use Cases: AI/ML use cases specific to Tesla’s domain.
	- GenAI Solutions: Suggested solutions using Generative AI.
	- Research Data from Tesla_research.xlsx displays each sheet in a table format.

## Dependencies
See requirements.txt for the full list.
