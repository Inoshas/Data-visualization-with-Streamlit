import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json


# Main content
st.title("Welcome to Fingrid Data Analysis Application")

# Sidebar content
#st.sidebar.title("Navigation")
#st.sidebar.success("Graphs.")


# Load the Excel file for total consumption data
df_consumption = pd.read_excel('data/consumptions.xlsx')
st.write("Fingrid data provides up-to-date electricity data information in Finland. Some data has been updated every 15 min, and some are updated every 1 hour.")

# Create a line plot for Total Electricity Consumption
st.markdown("### Total electricity consumption in Finland")
st.write("The below graph illustrates the total electricity consumption for different times of the year. It shows that during winter, power consumption increases, as expected, due to the dark and cold weather.")

line_plot = px.line(df_consumption, x="endTime", y="Total_electricity_consumption",
                    title="Total Electricity Consumption in MWh/h",
                    labels={"endTime": "Time", "Total_electricity_consumption": "Electricity Consumption (MWh/h)"})
st.plotly_chart(line_plot)

st.write("The data looks very noisey and thus I resample the data weekly.")

df_consumption['endTime'] = pd.to_datetime(df_consumption['endTime'])

# Set 'endTime' as the index before resampling
df_consumption.set_index('endTime', inplace=True)

numeric_cols = df_consumption.select_dtypes(include=['number'])

# Resample to weekly and take the mean
df_weekly = numeric_cols.resample('W').mean()

line_plot = px.line(df_weekly, x="endTime", y="Total_electricity_consumption",
                    title="Total Electricity Consumption (Daily Average)",
                    labels={"endTime": "Time", "Total_electricity_consumption": "Electricity Consumption (MWh/h)"})
st.plotly_chart(line_plot)


st.markdown("### Small scale productions in Finland")
st.write("Aggregate hourly metering data for small-scale electricity production sites in Finland, categorised by production type. The data is available starting from 1.8.2023. These data has been categories further as company produce electricity and consumer produce electricity.")


st.markdown("### Small scale productions in Finland")
st.write("Aggregate hourly metering data for small-scale electricity production sites in Finland, categorised by production type. The data is available starting from 1.8.2023. These data has been categories further as company produce electricity and consumer produce electricity.")



############################################################################

# Load the Excel file
file_path = 'data/small_scale_type_prod.xlsx'
df = pd.read_excel(file_path)

# Convert 'endTime' to datetime format
df['endTime'] = pd.to_datetime(df['endTime'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# Convert 'value' column to numeric, coercing errors to NaN
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Define the mapping for production types
production_type_mapping = {
    'AV01': 'Hydropower',
    'AV02': 'Wind power',
    'AV03': 'Nuclear power',
    'AV04': 'Gas turbine',
    'AV05': 'Diesel engine',
    'AV06': 'Solar power',
    'AV07': 'Wave power',
    'AV08': 'Combined production',
    'AV09': 'Biopower',
    'AV10': 'Other production'
}

# Replace the 'ProductionType' values with the corresponding names
df['ProductionType'] = df['ProductionType'].map(production_type_mapping)

# Filter for AB01 and AB02
df_filtered = df[df['CustomerType'].isin(['AB01', 'AB02'])]

# Ensure we have the data for each hour, for each day, and sort it
df_filtered.sort_values(by=['endTime', 'CustomerType', 'ProductionType'], inplace=True)

# Pivot the table to have 'ProductionType' as rows and 'CustomerType' as columns
pivoted = df_filtered.pivot_table(index='ProductionType', columns='CustomerType', values='value', aggfunc='mean')

# Round the values to 2 decimal places
pivoted = pivoted.round(2)

# Sort the table in ascending order based on the 'AB01' values
pivoted = pivoted.sort_values(by='AB01', ascending=True)

# Display the average values for each combination of 'ProductionType' and 'CustomerType'
st.write("Average Values for Each Production Type and Customer Type:")
st.write(pivoted)

st.write("By clicking on each header, you can easily sort the values, and according to the data, consumers and companies generate hydro, wind, and solar power in their distributed networks. For further analysis, data can be downloaded from below link as well. In Fingrid these information is available from 01.08.2023")

# Adding the URL as a clickable link
st.markdown("[Download the data here](https://data.fingrid.fi/en/datasets/357)")
# Filter the data for Solar power, Hydropower, and Wind power only
production_types_to_plot = ['Solar power', 'Hydropower', 'Wind power']
df_filtered_plot = df_filtered[df_filtered['ProductionType'].isin(production_types_to_plot)]

st.write("""
The two graphs below illustrate the electricity generated from hydro, solar, and wind power in a small-scale system. 
To provide a clearer view of the data, please note that the y-axis is displayed on a logarithmic scale.
""")
# Create the line plot for AB01
fig_ab01 = px.line(df_filtered_plot[df_filtered_plot['CustomerType'] == 'AB01'], 
                   x='endTime', 
                   y='value', 
                   color='ProductionType', 
                   title="Power Generation from AB01 (Companies)",
                   labels={"endTime": "Time", "value": "Power Generation (MWh/h)", "ProductionType": "Production Type"},
                   color_discrete_map={
                       'Wind power': 'green',  # Wind power in green
                       'Hydropower': 'blue',   # Hydropower in blue
                       'Solar power': 'purple'  # Solar power in brown
                   })

# Update layout for AB01 plot
fig_ab01.update_layout(
    xaxis_title="Time",
    yaxis_title="Power Generation (MWh/h)",
    yaxis_type="log",  # Set Y-axis to log scale
    showlegend=True
)

# Display the graph for AB01
st.plotly_chart(fig_ab01)

# Create the line plot for AB02
fig_ab02 = px.line(df_filtered_plot[df_filtered_plot['CustomerType'] == 'AB02'], 
                   x='endTime', 
                   y='value', 
                   color='ProductionType', 
                   title="Power Generation from AB02 (Consumers)",
                   labels={"endTime": "Time", "value": "Power Generation (MWh/h)", "ProductionType": "Production Type"},
                   color_discrete_map={
                       'Wind power': 'green',  # Wind power in green
                       'Hydropower': 'blue',   # Hydropower in blue
                       'Solar power': 'purple'  # Solar power in brown
                   })

# Update layout for AB02 plot
fig_ab02.update_layout(
    xaxis_title="Time",
    yaxis_title="Power Generation (MWh/h)",
    yaxis_type="log",  # Set Y-axis to log scale
    showlegend=True
)

# Display the graph for AB02
st.plotly_chart(fig_ab02)