
import io
import urllib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine


st.set_page_config(page_title="HR Recruitment Funnel Analysis", layout="wide")


def format_pct(value: float) -> str:
    return f"{value:.2f}%"


def clean_source(series: pd.Series) -> pd.Series:
    source_map = {
        "EMPLOYEEREFERRAL": "Employee Referral",
        "EMPLOYEE REFERRAL": "Employee Referral",
        "JOBFAIR": "Job Fair",
        "JOB FAIR": "Job Fair",
        "COMPANYWEBSITE": "Company Website",
        "COMPANY WEBSITE": "Company Website",
        "LINKEDIN": "LinkedIn",
        "INDEED": "Indeed",
        "GLASSDOOR": "Glassdoor",
        "NAUKRI": "Naukri",
        "MONSTER": "Monster",
    }
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    return cleaned.map(source_map).fillna(cleaned.str.title())


def clean_stage(series: pd.Series) -> pd.Series:
    stage_map = {
        "APPLIED": "Applied",
        "SCREENED": "Screened",
        "INTERVIEW1": "Interview 1",
        "INTERVIEW 1": "Interview 1",
        "INTERVIEW2": "Interview 2",
        "INTERVIEW 2": "Interview 2",
        "OFFER": "Offer",
        "HIRED": "Hired",
        "REJECTED": "Rejected",
        "UNKNOWN": "Unknown",
    }
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    return cleaned.map(stage_map).fillna(cleaned.str.title())


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Source"] = clean_source(df["Source"])
    df["Stage"] = clean_stage(df["Stage"])
    df["ApplicationDate"] = pd.to_datetime(df["ApplicationDate"], errors="coerce")
    df["DateatStage"] = pd.to_datetime(df["DateatStage"], errors="coerce")
    df["TimeToStage"] = (df["DateatStage"] - df["ApplicationDate"]).dt.days
    return df


@st.cache_resource
def get_engine():
    username = st.secrets["database"]["username"]
    password = st.secrets["database"]["password"]
    server = st.secrets["database"]["server"]
    database = st.secrets["database"]["database_name"]

    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=90;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


@st.cache_data
def load_data():
    engine = get_engine()
    query = "SELECT * FROM HR_Recruitment"
    raw_df = pd.read_sql(query, engine)
    return preprocess_data(raw_df)


st.title("HR Recruitment Funnel Analysis")

st.markdown("""
### Project Overview
This project analyzes the recruitment pipeline using HR candidate-stage data stored in Azure SQL Database.

The goal is to understand:
- how candidates move through each hiring stage
- which recruitment sources generate the most hires
- how long candidates take to move across stages
- where the biggest drop-offs happen in the funnel

*Note: This app follows the same project logic used in the notebook and reads the data directly from Azure SQL for analysis and visualization.*
""")

st.markdown("---")

st.markdown("""
### Business Questions
1. How many total applicants entered the recruitment pipeline?
2. How many candidates were finally hired?
3. What is the overall hiring rate?
4. Where are the biggest candidate drop-offs in the recruitment funnel?
5. Which recruitment sources generate the most successful hires?
6. How much time do candidates spend at each stage?
""")

st.markdown("---")

st.markdown("""
### Dataset Overview
Each row in the dataset represents a candidate record at a particular stage of the recruitment process.

**Column Descriptions:**
- **CandidateID**: Unique candidate identifier
- **PositionID**: Job position identifier
- **JobTitle**: Role applied for
- **ApplicationDate**: Candidate application date
- **Source**: Recruitment source
- **Stage**: Recruitment stage reached by the candidate
- **DateatStage**: Date when the candidate reached that stage
""")

st.markdown("---")

st.subheader("Connect Python to Azure SQL")

try:
    df = load_data()
    st.success("Data loaded successfully from Azure SQL.")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.info("""
Add your database credentials in `.streamlit/secrets.toml` like this:

[database]
username = "your-username"
password = "your-password"
server = "your-server-name.database.windows.net"
database_name = "your-database-name"
""")
    st.stop()

st.subheader("Data Loading and Initial Validation")

st.write("Preview data")
st.dataframe(df.head(10), use_container_width=True)

st.write("Count of rows and columns of the dataset:")
st.write(df.shape)

st.write("Structure of the data and non-null counts in each column")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

st.write("Total number of missing values:")
missing_df = (
    df.isna()
    .sum()
    .reset_index()
    .rename(columns={"index": "column", 0: "missing_values"})
)
st.dataframe(missing_df, use_container_width=True)

st.markdown("---")

st.subheader("Data Standardization and Feature Engineering")
st.write("The recruitment source and stage values are standardized and date fields are converted to datetime format.")
st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")

st.header("Recruitment KPI Overview")

valid_df = df[~df["Stage"].isin(["Unknown", "Rejected"])].copy()
total_applicants = valid_df["CandidateID"].nunique()
total_hired = df.loc[df["Stage"] == "Hired", "CandidateID"].nunique()
hiring_rate = (total_hired / total_applicants * 100) if total_applicants else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Applicants", f"{total_applicants:,}")
col2.metric("Total Hired Candidates", f"{total_hired:,}")
col3.metric("Hiring Rate", format_pct(hiring_rate))

st.markdown("---")

st.header("Recruitment Funnel Analysis")

stage_order = ["Applied", "Screened", "Interview 1", "Interview 2", "Offer", "Hired"]

funnel_counts = (
    df[df["Stage"].isin(stage_order)]
    .groupby("Stage")["CandidateID"]
    .nunique()
    .reindex(stage_order)
    .fillna(0)
    .astype(int)
)

fig = px.funnel(
    x=funnel_counts.values,
    y=funnel_counts.index,
    title="Recruitment Funnel",
    labels={"x": "Number of Candidates", "y": "Stage"},
    color_discrete_sequence=px.colors.sequential.Blues_r,
)
fig.update_traces(textinfo="value+percent initial", marker_line_width=2, marker_line_color="white")
fig.update_layout(title_x=0.5, template="plotly_white", yaxis_title=None)
st.plotly_chart(fig, use_container_width=True)

biggest_drop_stage = None
if len(funnel_counts) > 1:
    drop_off = funnel_counts.diff().abs().iloc[1:]
    if not drop_off.empty:
        biggest_drop_stage = drop_off.idxmax()

offer_count = int(funnel_counts.get("Offer", 0))
hired_count = int(funnel_counts.get("Hired", 0))
offer_to_hired_rate = (hired_count / offer_count * 100) if offer_count else 0.0

st.markdown("**Data Insights**")
if biggest_drop_stage:
    previous_stage = stage_order[stage_order.index(biggest_drop_stage) - 1]
    st.markdown(
        f"- The biggest drop-off happens between **{previous_stage}** and **{biggest_drop_stage}**, so this is the main stage where candidate numbers reduce the most."
    )
st.markdown(
    f"- The **Offer to Hired** conversion is **{offer_to_hired_rate:.2f}%**, which shows strong final-stage candidate acceptance."
)
st.markdown(
    f"- The funnel starts with **{int(funnel_counts.get('Applied', 0)):,}** applicants and ends with **{hired_count:,}** hired candidates."
)

st.markdown("---")

st.header("Source Effectiveness Analysis")

hired_df = df[df["Stage"] == "Hired"].copy()
source_hired = (
    hired_df.groupby("Source")["CandidateID"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Hired Candidates")
)

st.dataframe(source_hired, use_container_width=True)

fig = px.bar(
    source_hired,
    x="Hired Candidates",
    y="Source",
    orientation="h",
    title="Hiring Effectiveness by Recruitment Source",
    text="Hired Candidates",
    color="Hired Candidates",
    color_continuous_scale=px.colors.sequential.Teal,
)
fig.update_layout(title_x=0.5, yaxis_title=None, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

if not source_hired.empty:
    top_source = source_hired.iloc[0]["Source"]
    top_source_hires = int(source_hired.iloc[0]["Hired Candidates"])
    st.markdown("**Data Insights**")
    st.markdown(f"- **{top_source}** is the top-performing recruitment source with **{top_source_hires}** hires.")
    st.markdown("- Recruitment sources with consistently higher hires should receive more focus in future hiring campaigns.")
    st.markdown("- Comparing source performance helps the HR team decide where hiring budget and effort should go.")

st.markdown("---")

st.header("Time to Hire Analysis")

avg_time_stage = (
    df.groupby("Stage")["TimeToStage"]
    .mean()
    .round(1)
    .reset_index()
)
avg_time_stage = avg_time_stage[~avg_time_stage["Stage"].isin(["Applied", "Unknown"])]
avg_time_stage["stage_sort"] = avg_time_stage["Stage"].map({
    "Rejected": 1,
    "Screened": 2,
    "Interview 1": 3,
    "Interview 2": 4,
    "Offer": 5,
    "Hired": 6,
})
avg_time_stage = avg_time_stage.sort_values(["stage_sort", "TimeToStage"]).drop(columns="stage_sort")

st.dataframe(avg_time_stage, use_container_width=True)

fig = px.bar(
    avg_time_stage,
    x="Stage",
    y="TimeToStage",
    color="TimeToStage",
    text="TimeToStage",
    title="Average Time Taken at Each Hiring Stage",
    color_continuous_scale=px.colors.sequential.Teal,
    labels={"TimeToStage": "Average Time (Days)"},
)
fig.update_layout(title_x=0.5, xaxis_title=None, yaxis_title=None, template="plotly_white")
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
st.plotly_chart(fig, use_container_width=True)

if not avg_time_stage.empty:
    slowest_stage = avg_time_stage.sort_values("TimeToStage", ascending=False).iloc[0]
    fastest_stage = avg_time_stage.sort_values("TimeToStage", ascending=True).iloc[0]
    st.markdown("**Data Insights**")
    st.markdown(
        f"- The slowest stage is **{slowest_stage['Stage']}** with an average of **{slowest_stage['TimeToStage']:.1f} days**."
    )
    st.markdown(
        f"- The fastest stage is **{fastest_stage['Stage']}** with an average of **{fastest_stage['TimeToStage']:.1f} days**."
    )
    st.markdown("- Longer stage duration can indicate scheduling, approval, or documentation delays.")

st.markdown("---")

st.header("Stage-to-Stage Conversion Rate Analysis")

stage_conversion = (funnel_counts / funnel_counts.shift(1) * 100).iloc[1:].round(2)

conversion_df = pd.DataFrame({
    "From Stage": stage_order[:-1],
    "To Stage": stage_order[1:],
    "Conversion Rate (%)": stage_conversion.values,
})

st.dataframe(conversion_df, use_container_width=True)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=conversion_df["To Stage"],
        y=conversion_df["Conversion Rate (%)"],
        text=conversion_df["Conversion Rate (%)"].round(2),
        textposition="auto",
    )
)
fig.update_layout(
    title="Stage-to-Stage Conversion Rate (%)",
    xaxis_title="Recruitment Stage",
    yaxis_title="Conversion Rate (%)",
    template="plotly_white",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

if not conversion_df.empty:
    lowest_conversion_row = conversion_df.sort_values("Conversion Rate (%)").iloc[0]
    highest_conversion_row = conversion_df.sort_values("Conversion Rate (%)", ascending=False).iloc[0]
    st.markdown(
        f"- The weakest stage transition is from **{lowest_conversion_row['From Stage']}** to **{lowest_conversion_row['To Stage']}** with a conversion rate of **{lowest_conversion_row['Conversion Rate (%)']:.2f}%**."
    )
    st.markdown(
        f"- The strongest stage transition is from **{highest_conversion_row['From Stage']}** to **{highest_conversion_row['To Stage']}** with a conversion rate of **{highest_conversion_row['Conversion Rate (%)']:.2f}%**."
    )

st.markdown("---")

st.header("Strategic Business Recommendations")

recommendation_source = source_hired.iloc[0]["Source"] if not source_hired.empty else "top-performing sources"

st.markdown(f"""
- Since **{recommendation_source}** is performing strongly, the HR team should prioritize budget and hiring effort toward high-performing recruitment channels.
- The biggest funnel drop-off should be reviewed carefully so the team can improve job descriptions, screening criteria, or candidate matching.
- Stages with higher average processing time should be streamlined to reduce delays in hiring decisions.
- Strong final-stage conversion suggests that candidates who reach the offer stage are generally well-matched for the role.
- Regular funnel monitoring can help the team identify hiring bottlenecks early and improve recruitment efficiency.
""")
