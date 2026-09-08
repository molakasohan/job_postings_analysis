"""
Job Postings Analysis - Data Analyst Roles
--------------------------------------------
Install pandas + matplotlib first if you don't have them:
    pip install pandas matplotlib
    (or: conda install pandas matplotlib -y)

This script:
1. Generates a small fake job postings dataset (so you can run it immediately)
2. Loads it into pandas
3. Finds top hiring companies, most in-demand skills, top locations, salary trends
4. Draws simple charts

To use REAL data instead: export job search results from Naukri/LinkedIn as CSV
(or copy-paste postings into a spreadsheet) with similar columns, then skip Step 1
and load your file directly in Step 2.
"""

import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

# ----------------------------------------------------
# STEP 1: Create a sample dataset (skip this if you have your own CSV)
# ----------------------------------------------------
random.seed(42)

companies = ["TCS", "Accenture", "Infosys", "Wipro", "Cognizant", "Google",
             "Amazon", "Deloitte", "EXL", "Fractal Analytics", "ZS Associates",
             "IBM", "LatentView Analytics"]

locations = ["Bangalore", "Hyderabad", "Pune", "Gurgaon", "Chennai", "Mumbai"]

all_skills = ["SQL", "Excel", "Python", "Power BI", "Tableau", "Statistics",
              "AWS", "Snowflake", "R"]

experience_levels = ["Fresher", "0-2 years", "2-4 years"]

rows = []
start_date = datetime(2026, 6, 1)

for i in range(150):
    posting_date = start_date + timedelta(days=random.randint(0, 90))
    company = random.choice(companies)
    location = random.choice(locations)
    experience = random.choice(experience_levels)
    # each posting asks for 3-5 random skills
    required_skills = random.sample(all_skills, random.randint(3, 5))
    salary_lpa = round(random.uniform(3.5, 12), 1) if experience == "Fresher" \
        else round(random.uniform(6, 20), 1)

    rows.append({
        "PostingID": i + 1,
        "Date": posting_date,
        "Company": company,
        "Location": location,
        "Experience": experience,
        "Skills": ", ".join(required_skills),
        "SalaryLPA": salary_lpa
    })

df = pd.DataFrame(rows)
df.to_csv("sample_job_postings.csv", index=False)
print("Sample dataset created: sample_job_postings.csv\n")

# ----------------------------------------------------
# STEP 2: Load data (this is where you'd start if using your own CSV)
# ----------------------------------------------------
# df = pd.read_csv("sample_job_postings.csv", parse_dates=["Date"])

print("---- Basic Info ----")
print(df.info())

# ----------------------------------------------------
# STEP 3: Core analysis
# ----------------------------------------------------

# Top hiring companies (by number of postings)
top_companies = df["Company"].value_counts().head(10)
print("\n---- Top Hiring Companies ----")
print(top_companies)

# Most in-demand skills
# "Skills" column has comma-separated values, so we split and count each one
skill_counts = df["Skills"].str.split(", ").explode().value_counts()
print("\n---- Most In-Demand Skills ----")
print(skill_counts)

# Top hiring locations
top_locations = df["Location"].value_counts()
print("\n---- Top Hiring Locations ----")
print(top_locations)

# Average salary by experience level
avg_salary = df.groupby("Experience")["SalaryLPA"].mean().sort_values(ascending=False)
print("\n---- Average Salary by Experience (LPA) ----")
print(avg_salary)

# Fresher-specific salary range
fresher_df = df[df["Experience"] == "Fresher"]
print(f"\nFresher salary range: ₹{fresher_df['SalaryLPA'].min()} - "
      f"₹{fresher_df['SalaryLPA'].max()} LPA")
print(f"Fresher average salary: ₹{fresher_df['SalaryLPA'].mean():.1f} LPA")

# Postings trend over time (weekly)
df["Week"] = df["Date"].dt.to_period("W")
weekly_postings = df.groupby("Week").size()
print("\n---- Postings per Week ----")
print(weekly_postings)

# ----------------------------------------------------
# STEP 4: Simple charts
# ----------------------------------------------------

# Bar chart - top hiring companies
plt.figure(figsize=(9, 5))
top_companies.plot(kind="bar", color="steelblue")
plt.title("Top Hiring Companies (by number of postings)")
plt.ylabel("Number of Postings")
plt.xlabel("Company")
plt.tight_layout()
plt.savefig("top_hiring_companies.png")
print("\nSaved chart: top_hiring_companies.png")

# Bar chart - most in-demand skills
plt.figure(figsize=(9, 5))
skill_counts.plot(kind="bar", color="darkorange")
plt.title("Most In-Demand Skills")
plt.ylabel("Number of Postings Mentioning Skill")
plt.xlabel("Skill")
plt.tight_layout()
plt.savefig("in_demand_skills.png")
print("Saved chart: in_demand_skills.png")

# Line chart - postings trend
plt.figure(figsize=(9, 5))
weekly_postings.plot(kind="line", marker="o", color="green")
plt.title("Job Postings Trend (Weekly)")
plt.ylabel("Number of Postings")
plt.xlabel("Week")
plt.tight_layout()
plt.savefig("postings_trend.png")
print("Saved chart: postings_trend.png")

# ----------------------------------------------------
# STEP 5: Export a summary report
# ----------------------------------------------------
summary = pd.DataFrame({
    "Metric": ["Top Hiring Company", "Most In-Demand Skill", "Top Location",
               "Average Fresher Salary (LPA)", "Total Postings Analyzed"],
    "Value": [
        top_companies.index[0],
        skill_counts.index[0],
        top_locations.index[0],
        f"{fresher_df['SalaryLPA'].mean():.1f}",
        len(df)
    ]
})
summary.to_csv("job_postings_summary.csv", index=False)
print("\nSaved summary report: job_postings_summary.csv")
print("\nDone! Check the generated CSV and PNG files in this folder.")
