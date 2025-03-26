# Fingrid Data Analysis and Visualization

## Project Overview

This project aims to provide interactive data visualizations and analysis of electricity consumption and small-scale production data in Finland. The data is sourced from **Fingrid**, which provides up-to-date electricity data, including both consumption and production from renewable and small-scale energy sources. The project uses **Streamlit** and **Plotly** for visualizing this data, enabling users to explore electricity consumption patterns and small-scale production insights.

## Features

1. **Total Electricity Consumption in Finland**  
   - Displays a line plot of electricity consumption over time.
   - Resampling of data to display weekly averages.
   - Insights on power consumption during different seasons, especially the winter months.

2. **Small-Scale Electricity Production**  
   - Displays data on small-scale electricity production from different sources, including **Hydropower**, **Wind Power**, **Solar Power**, etc.
   - Data is categorized by production type and customer type (companies and consumers).
   - Allows for easy comparison of energy production between companies and consumers.

3. **Interactive Graphs for Power Generation**  
   - Provides graphs for small-scale power generation from **Hydropower**, **Wind Power**, and **Solar Power**.
   - The y-axis is displayed on a **logarithmic scale** for better visualization of variations in production values.

4. **Data Download Link**  
   - The data used in this application can be downloaded from Fingrid’s official website for further analysis.

---

## Technologies Used

- **Streamlit**: For creating interactive web-based applications and visualizations.
- **Plotly**: For creating interactive and aesthetically pleasing plots and graphs.
- **Pandas**: For data manipulation and analysis.
- **Excel**: Data stored in Excel files containing consumption and production metrics.

---

## Getting Started

To get started with this project on your local machine:

### Prerequisites

1. Python 3.7 or higher.
2. Required libraries:
   - Streamlit
   - Plotly
   - Pandas
   - Openpyxl (for reading Excel files)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Inoshas/Data-visualization-with-Streamlit.git
