# Recruitment Funnel Analytics Pipeline

![Recruitment Funnel](<screenshots/recruitment funnel.png>)
## Project Links
- **Notebook / Analysis:** [View Project](your-link-here)

## Summary
This project is an end-to-end recruitment analytics pipeline built using Azure Blob Storage, Azure Data Factory, Azure SQL Database, SQL, and Python.

It starts with messy HR recruitment data in CSV format, loads the data into Azure using Blob Storage and Data Factory, cleans it in Azure SQL using SQL, and then uses Python for exploratory data analysis and recruitment funnel insights.

## Business Problem
Recruitment data is often messy and difficult to use directly for analysis.  
This project was built to clean and structure raw hiring data so it can be used to answer practical recruitment questions such as:

- How many applicants move through each hiring stage?
- What are the conversion rates between stages?
- Which hiring sources bring the most successful candidates?
- How much time is spent at different recruitment stages?
- What is the overall hiring rate?

## Tools & Technologies
- Azure Blob Storage
- Azure Data Factory
- Azure SQL Database
- SQL (SSMS)
- Python
- Pandas
- Jupyter Notebook

## Workflow
- Uploaded raw recruitment CSV data to Azure Blob Storage
- Moved data into Azure SQL Database using Azure Data Factory
- Cleaned and standardized the raw data in SQL using SSMS
- Used the cleaned dataset in Python for EDA and funnel analysis
- Analyzed recruitment stages, hiring rates, source performance, and stage timelines

## Key Insights
- Total Applicants: **5,134**
- Total Hired Candidates: **382**
- Overall Hiring Rate: **7.44%**
- Funnel progression drops steadily from Applied to Hired
- Job Fair, LinkedIn, and Indeed were among the strongest hiring sources
- Average time increased as candidates moved deeper into the recruitment process

## Repository Structure
```text
recruitment-funnel-analytics-pipeline/
│
├── app/
│   └── analysis.py
├── notebooks/
│   └── recruitment_funnel_analysis.ipynb
├── data/
│   ├── sample_data.csv
│   └── data_dictionary.md
├── docs/
│   ├── project_summary.md
│   ├── architecture_flow.md
│   └── insights_and_recommendations.md
├── sql/
│   └── data_cleaning.sql
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md 
```

## How to View/Run Project

- Open the SQL file to review data cleaning step
- Open the notebook to see Python EDA and funnel analysis
- Check the screenshots folder for key charts
- Read the docs folder for project summary, workflow, and insights