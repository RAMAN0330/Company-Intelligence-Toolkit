import streamlit as st
from MainOrchestrator import MultiAgentOrchestrator
import pandas as pd
import os

# Streamlit app configuration
st.set_page_config(page_title="AI Use Case Generator", layout="wide")

# Title of the app
st.title("AI Use Case Generator for Companies")

# Input section for company name
company_name = st.text_input("Enter the Company Name:", "Tesla")

# Button to run the analysis
if st.button("Generate Use Cases and Solutions"):
    with st.spinner("Processing..."):
        # Initialize the orchestrator
        orchestrator = MultiAgentOrchestrator(company_name)
        file_name = f"{company_name}_research.xlsx"
        
        # Run the workflow and obtain results directly
        results = orchestrator.run_workflow()
        orchestrator.close()

        # Unpack results if available
        use_cases = results.get("use_cases")
        genai_solutions = results.get("genai_solutions")
        research_data = results.get("research_data")

        # Display use cases as Markdown if available
        if use_cases:
            st.subheader("Generated Use Cases")
            # Assuming the 'use_cases' is a file path or a string of markdown content
            if isinstance(use_cases, str) and os.path.exists(use_cases):
                with open(use_cases, "r") as file:
                    st.markdown(file.read())
            else:
                st.markdown(use_cases)
        else:
            st.warning("No use cases generated. Please try again.")

        # Display GenAI solutions as Markdown if available
        if genai_solutions:
            st.subheader("Suggested GenAI Solutions")
            # Assuming 'genai_solutions' is a file path or string of markdown content
            if isinstance(genai_solutions, str) and os.path.exists(genai_solutions):
                with open(genai_solutions, "r") as file:
                    st.markdown(file.read())
            else:
                st.markdown(genai_solutions)
        else:
            st.warning("No GenAI solutions generated. Please try again.")

        # Display research data if available
        if os.path.exists(file_name):
            try:
                # Read the Excel file
                xls = pd.ExcelFile(file_name)

                # Display sheet names
                sheet_names = xls.sheet_names
                st.write(f"Sheet Names: {sheet_names}")

                # Display data for each sheet
                for sheet_name in sheet_names:
                    st.write(f"### {sheet_name}")
                    sheet_data = pd.read_excel(xls, sheet_name=sheet_name)
                    st.dataframe(sheet_data)

            except Exception as e:
                st.error(f"Error reading the file {file_name}: {e}")
        else:
            st.warning(f"The file '{file_name}' was not found in the current directory.")
# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")