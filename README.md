# Recruitment Funnel Analytics Pipeline

![Recruitment Funnel](<screenshots/recruitment funnel.png>)
## Project Links
- **Notebook / Analysis:** [View EDA Notebook](https://recruitment-funnel-analysis.streamlit.app/)

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
- The funnel processed 5,134 applicants and resulted in 382 hires, for an overall hiring rate of 7.44%
- The largest drop-off happened early, with about 64% moving from Applied to Screened
- Conversion improved in later stages, showing stronger candidate quality among shortlisted applicants
- Offer-to-hire conversion was about 97.45%, indicating very strong final-stage acceptance
- Job Fair, LinkedIn, and Indeed were the strongest sources by final hires
- Time-to-hire increased across stages, from about 4 days at screening to around 20 days by final hiring

## Business Recommendations
- Re-evaluate early-stage screening criteria to reduce unnecessary candidate drop-offs
- Allocate more hiring budget and effort to high-performing sources like LinkedIn and Job Fairs
- Monitor stage-wise conversion rates to identify weak transitions in the funnel
- Reduce delays in later hiring stages by improving scheduling and approval processes
- Track funnel performance regularly to improve hiring efficiency over time

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