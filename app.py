# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import folium
# from streamlit_folium import folium_static
# from pgeocode import Nominatim
#
# # Load the dataset
# file_path = "MOR-EV_Stats_Page_Data_Download.xlsx"
# xls = pd.ExcelFile(file_path)
# df = pd.read_excel(xls, sheet_name="Data")
#
# # Function to get city from ZIP code and coordinates
# def get_location(zip_code):
#     nomi = Nominatim("us")
#     location = nomi.query_postal_code(zip_code)
#     if location is not None:
#         return location.place_name, location.latitude, location.longitude
#     return "Unknown", None, None
#
#
# # Streamlit app
# def main():
#     st.title("Exploratory Data Analysis (EDA) - EV Dataset")
#
#     # Display basic info
#     st.subheader("Dataset Information")
#     st.write("Shape of the Dataset",df.shape)
#     st.write("Total number of records :",df.shape[0])
#     st.write("Total number of Col :",df.shape[1])
#
#     #buffer = df.info(buf=None)
#     #st.text(buffer)
#
#     # Missing values
#     st.subheader("Missing Values")
#     st.write(df.isnull().sum())
#
#     # Summary statistics
#     st.subheader("Summary Statistics")
#     st.write(df.describe())
#
#     # Count of applications by vehicle category
#     st.subheader("EV Applications by Vehicle Category")
#     fig, ax = plt.subplots()
#     sns.countplot(y=df['Vehicle Category'], order=df['Vehicle Category'].value_counts().index, ax=ax)
#     ax.set_title("EV Applications by Vehicle Category")
#     st.pyplot(fig)
#
#     # Count of applications by year
#     if 'Date of Purchase' in df.columns:
#         df['Year'] = pd.to_datetime(df['Date of Purchase'], errors='coerce').dt.year
#         st.subheader("EV Adoption Trend by Year")
#         fig, ax = plt.subplots()
#         sns.countplot(x=df['Year'].dropna().astype(int), order=df['Year'].dropna().astype(int).value_counts().index,
#                       ax=ax)
#         ax.set_title("EV Applications by Year")
#         plt.xticks(rotation=45)
#         st.pyplot(fig)
#
#     # Rebate Amount Distribution
#     if 'Total Amount' in df.columns:
#         st.subheader("Rebate Amount Distribution")
#         fig, ax = plt.subplots()
#         sns.histplot(df['Total Amount'].dropna(), bins=20, kde=True, ax=ax)
#         ax.set_title("Distribution of Rebate Amounts")
#         st.pyplot(fig)
#
#     # Leasing vs Purchasing Patterns
#     if 'Purchase or Lease?' in df.columns:
#         st.subheader("Leasing vs Purchasing")
#         fig, ax = plt.subplots()
#         sns.countplot(y=df['Purchase or Lease?'], order=df['Purchase or Lease?'].value_counts().index, ax=ax)
#         ax.set_title("Leasing vs Purchasing Trends")
#         st.pyplot(fig)
#
#     # Top 10 vehicle models
#     st.subheader("Top 10 EV Models")
#     fig, ax = plt.subplots()
#     df['Vehicle Model'].value_counts().head(10).plot(kind='barh', ax=ax)
#     ax.set_title("Top 10 EV Models")
#     ax.invert_yaxis()
#     st.pyplot(fig)
#
#     # EV Applications by County
#     st.subheader("EV Applications by County")
#     fig, ax = plt.subplots()
#     st.write(df['Applicant: County'].value_counts())
#     df['Applicant: County'].value_counts().plot(kind='bar', ax=ax)
#     ax.set_title("EV Applications by County")
#     plt.xticks(rotation=90)
#     st.pyplot(fig)
#
#     # Top Dealers by Number of Applications
#     if 'Dealer Name' in df.columns:
#         st.subheader("Top Dealers by Number of Applications")
#         fig, ax = plt.subplots()
#         df['Dealer Name'].value_counts().head(10).plot(kind='barh', ax=ax)
#         ax.set_title("Top 10 EV Dealers")
#         ax.invert_yaxis()
#         st.pyplot(fig)
#
#         # Top 15 Cities/Towns/Counties/ZIPs with highest BEV applications
#         st.subheader("Top 15 Locations with Highest BEV Applications")
#         if 'Vehicle Category' in df.columns and 'Applicant: Postal Code' in df.columns and 'Applicant: County' in df.columns:
#             bev_df = df[df['Vehicle Category'] == 'BEV']
#             top_15_bev = bev_df.groupby(['Applicant: County', 'Applicant: Postal Code']).size().reset_index(
#                 name='BEV Applications')
#             top_15_bev = top_15_bev.sort_values(by='BEV Applications', ascending=False).head(15)
#             top_15_bev[['City/Town', 'Latitude', 'Longitude']] = top_15_bev['Applicant: Postal Code'].astype(str).apply(
#                 lambda x: pd.Series(get_location(x)))
#             st.write(top_15_bev)
#
#             # Create a map
#             st.subheader("BEV Applications Map")
#             m = folium.Map(location=[42.4072, -71.3824], zoom_start=8)
#
#             for _, row in top_15_bev.dropna().iterrows():
#                 folium.Marker(
#                     location=[row['Latitude'], row['Longitude']],
#                     popup=f"{row['City/Town']} ({row['Applicant: Postal Code']})\nBEV Applications: {row['BEV Applications']}",
#                     icon=folium.Icon(color="blue", icon="info-sign")
#                 ).add_to(m)
#
#             folium_static(m)
#
#     st.write("EDA Complete.")
#
#
# if __name__ == "__main__":
#     main()
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
