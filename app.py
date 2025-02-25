
########################################################################
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Caching the data load so it doesn't reload on every interaction
@st.cache_data
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="Data")
    return df


# Load the dataset
file_path = "MOR-EV_Stats_Page_Data_Download.xlsx"
df = load_data(file_path)

# Data Cleaning and Introduction
st.title("Massachusetts Electric Vehicle Data Analysis")

st.write(
    "The MOR-EV data comes from Massachusetts' rebate program for electric vehicles. This program gives cash back to people who buy or lease EVs. The data shows where these rebates have been issued—organized by zip code and county—and covers information from June 2014 onward.")

st.write("**What It Shows:**")
st.write("- Number of EV rebates by zip code.")
st.write("- Trends in EV adoption across regions.")
st.write("- Areas with higher EV interest.")

st.write("**How It’s Collected:**")
st.write("- The state tracks rebates given to EV buyers or leasers.")
st.write("- The data is compiled into an Excel file for public analysis.")
st.write("- It only includes those who applied for and received a rebate.")

st.write("**Limitations:**")
st.write("- Not every EV owner applies for a rebate.")
st.write("- Some regions may appear to have lower EV counts than they really do.")
st.write("- It does not capture the full count of all electric vehicles on the road.")

st.write("---")
st.write("### Data Cleaning and Preparation")
st.write("The dataset contains the following columns:")
st.write(df.columns)

# Keep only relevant columns and drop rows with missing values
columns_to_keep = ['Applicant: County', 'Applicant: Postal Code', 'Vehicle Category', 'Total Amount']
df = df[columns_to_keep].dropna()

# Remove entries with invalid or unknown counties
df = df[df['Applicant: County'].str.lower() != 'unknown']

st.write("Data has been cleaned by removing irrelevant and missing values.")

st.write("---")
st.write("### Data Source and Relevance")
st.write(
    "This dataset comes from the MOR-EV rebate program. It is essential for understanding how and where EV adoption is occurring in Massachusetts, and it helps guide policymaking for sustainable transportation.")

st.write("---")
st.write("### Visualization: Top 10 Counties and ZIP Codes by Vehicle Category")

vehicle_categories = df['Vehicle Category'].unique()

# Top 10 Counties Visualization per Category
st.write("#### Top 10 Counties with Most Electric Vehicles by Category")
for category in vehicle_categories:
    st.write(f"**Category: {category}**")
    top_counties = (df[df['Vehicle Category'] == category]
                    .groupby('Applicant: County')
                    .size()
                    .reset_index(name='EV Applications')
                    .sort_values(by='EV Applications', ascending=False)
                    .head(10))
    st.write(top_counties)

    fig, ax = plt.subplots()
    sns.barplot(y=top_counties['Applicant: County'], x=top_counties['EV Applications'], ax=ax)
    ax.set_title(f"Top 10 Counties for {category}")
    st.pyplot(fig)
    st.write("---")  # Divider between visualizations

# Top 10 ZIP Codes Visualization per Category
st.write("#### Top 10 ZIP Codes with Most Electric Vehicles by Category")
for category in vehicle_categories:
    st.write(f"**Category: {category}**")
    top_zipcodes = (df[df['Vehicle Category'] == category]
                    .groupby('Applicant: Postal Code')
                    .size()
                    .reset_index(name='EV Applications')
                    .sort_values(by='EV Applications', ascending=False)
                    .head(10))
    st.write(top_zipcodes)

    fig, ax = plt.subplots()
    sns.barplot(y=top_zipcodes['Applicant: Postal Code'].astype(str), x=top_zipcodes['EV Applications'], ax=ax)
    ax.set_title(f"Top 10 ZIP Codes for {category}")
    st.pyplot(fig)
    st.write("---")  # Divider between visualizations

st.write("### Key Insights")
st.write("- Certain counties and ZIP codes show much higher numbers of EV rebates.")
st.write("- The rebate program appears effective in boosting EV adoption, particularly in urban/suburban areas.")
st.write("- These insights can help tailor policies and incentives to further promote clean transportation.")

st.write("### Conclusion")
st.write(
    "The MOR-EV dataset provides a valuable snapshot of EV distribution in Massachusetts. These insights are critical for policymakers, businesses, and consumers aiming to advance sustainable transportation.")

st.write("---")
st.write("### Predictive Analysis for Missing EV Counts")
st.write(
    "Since the dataset includes only the vehicles that received rebates, it does not capture the entire EV market. To estimate the total EV count, we use a scaling factor. Here’s why we use a **30% scaling factor**:")

st.write("### Why Use a 30% Scaling Factor? Detailed Explanation")
st.write("""
**Calculation Details:**
- **Observed Data:**  
  The MOR-EV Report shows 12,854 rebate applications out of 19,290 EV registrations.  
  If we assume a uniform 66% participation rate, the estimated total EVs would be:

      Estimated EVs = 12,854 / 0.66 ≈ 19,484

- **Conservative Approach:**  
  However, many regions may have lower participation rates due to differences in awareness or access.  
  To be cautious, analysts sometimes assume only 30% of EV owners apply for rebates.

- **Scaling Factor Calculation:**  
  With a 30% participation rate, the scaling factor is:

      Scaling Factor = 1 / 0.30 ≈ 3.33

  Therefore, for every rebate application, we estimate there are about 3.33 total EVs.

      Example: For 1,000 rebate applications,
      Estimated Total EVs = 1,000 / 0.30 ≈ 3,333
""")
st.write(
    "Sources: [MOR-EV Annual Report](https://malegislature.gov/Bills/193/SD3519.pdf?utm_source=chatgpt.com), Alternative Fuels Data Center")

# Filter only Battery Electric Vehicles (BEVs)
df_bev = df[df["Vehicle Category"] == "BEV"].copy()
df_bev["Applicant: Postal Code"] = df_bev["Applicant: Postal Code"].astype(str)

# Group by Postal Code to count BEV rebates
bev_by_zip = (df_bev.groupby("Applicant: Postal Code")["Applicant: Postal Code"]
              .count()
              .reset_index(name="BEV Rebates Count"))

# Apply scaling to estimate total BEVs per ZIP code
scaling_factor = 1 / 0.30  # Approximately 3.33 multiplier
bev_by_zip["Estimated Total BEVs"] = (bev_by_zip["BEV Rebates Count"] * scaling_factor).round().astype(int)

st.write("### Methodology for Predictive Analysis")
st.write("1. **Data Selection:** We filter the dataset to include only Battery Electric Vehicles (BEVs).")
st.write("2. **Grouping by ZIP Code:** We count the number of rebate applications per ZIP code.")
st.write(
    "3. **Scaling Factor:** Assuming that rebate applications represent roughly 30% of all EVs, we multiply by 3.33 (1/0.30) to estimate the total number of BEVs.")
st.write(
    "4. **Result Interpretation:** This is an estimate and not an exact count, but it provides a useful indication of EV adoption levels by region.")

# Get the top 10 ZIP codes with the highest estimated BEVs
top_10_zip_codes = bev_by_zip.nlargest(10, "Estimated Total BEVs")
st.write("### Top 10 ZIP Codes with Highest Estimated EV Adoption")
st.write(top_10_zip_codes)

fig, ax = plt.subplots()
sns.barplot(y=top_10_zip_codes["Applicant: Postal Code"].astype(str),
            x=top_10_zip_codes["Estimated Total BEVs"], ax=ax)
ax.set_title("Top 10 ZIP Codes for Estimated BEV Adoption")
ax.set_xlabel("Estimated Total BEVs")
ax.set_ylabel("ZIP Code")
st.pyplot(fig)
st.write("---")
