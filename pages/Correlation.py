import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Main content
st.title("Correlation between predictions and actual")
st.write("This page is dedicatied analyze the correlation between predicted forecast and actual generation. ")
st.write("""
        Fingrid has provided both the forecasted and actual wind power generation values on a national scale.
        """)


# File paths for the forecast and actual data
file_path_forecast = 'data/windpower_prediction_forecast.xlsx'
file_path_actual = 'data/Windpower_production.xlsx'

# Read the data from Excel files
df_forecast = pd.read_excel(file_path_forecast)
df_actual = pd.read_excel(file_path_actual)

# Convert 'endTime' to datetime format for both datasets
df_forecast['endTime'] = pd.to_datetime(df_forecast['endTime'])
df_actual['endTime'] = pd.to_datetime(df_actual['endTime'])

# Add a column to distinguish between forecast and actual
df_forecast['Type'] = 'Forecasted Wind Power'
df_actual['Type'] = 'Actual Wind Power'

# Combine both dataframes into one
df_combined = pd.concat([df_forecast, df_actual], ignore_index=True)

# Merge the forecasted and actual data on the 'endTime' column for correlation calculation
merged_df = pd.merge(df_forecast[['endTime', 'amount']], df_actual[['endTime', 'amount']], 
                     on='endTime', suffixes=('_forecast', '_actual'))

# Calculate the Pearson Correlation Coefficient
correlation = merged_df['amount_forecast'].corr(merged_df['amount_actual'])

# Display the Pearson Correlation Coefficient
st.write(f"**Pearson Correlation Coefficient** between forecasted and actual wind power generation: **{correlation:.2f}**")

# Scatter plot: Actual vs. Forecasted Wind Power
st.write("Scatter Plot: Actual vs Forecasted Wind Power")
scatter_fig = go.Figure()

# Add scatter plot for actual vs forecasted data
scatter_fig.add_trace(go.Scatter(
    x=merged_df['amount_actual'],
    y=merged_df['amount_forecast'],
    mode='markers',
    name='Actual vs Forecasted',
    marker=dict(color='blue', size=6)
))

# Update layout for the scatter plot
scatter_fig.update_layout(
    title="Scatter Plot: Actual vs Forecasted Wind Power",
    xaxis_title="Actual Wind Power (MWh/h)",
    yaxis_title="Forecasted Wind Power (MWh/h)",
    showlegend=True
)

# Display the scatter plot
st.plotly_chart(scatter_fig)
st.write("""
        This Pearson correlation value indicates a very strong positive correlation between the predicted and actual values. A correlation of **0.94** suggests that 
        the forecasting mechanism is highly accurate in predicting the wind power generation. This high correlation demonstrates that the predictions made 
        by the model are closely aligned with the actual values, proving the effectiveness of the forecasting system. 
        Such a high correlation is an excellent indicator of the reliability of the forecast, which is crucial for energy management, grid stability, and planning.
""")

st.write(" If you like to visualize the actual distribution of actual production value vs the forecast value you can click on the load graph button on the left side bar.")
# Sidebar button to trigger the line graph
if st.sidebar.button('Load Graph'):
    # Create the line plot using Plotly
    fig = px.line(df_combined, 
                  x='endTime', 
                  y='amount', 
                  color='Type', 
                  title="Forecasted vs Actual Wind Power Generation",
                  labels={"endTime": "Time", "amount": "Wind Power Generation (MWh/h)", "Type": "Data Type"},
                  color_discrete_map={
                      'Forecasted Wind Power': 'brown',  # Forecast 
                      'Actual Wind Power': 'green'       # Actual 
                  })

    # Update layout for the line plot
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Wind Power Generation (MWh/h)",
        yaxis_type="log",  # Set Y-axis to log scale
        showlegend=True
    )

    # Display the line plot
    st.plotly_chart(fig)

with open("main.py", "r") as file:
    code = file.read()

st.code(code, language="python")