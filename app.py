import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="COVID-19 Storytelling Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🦠 COVID-19 Global Impact: A Story Told by Data")
st.markdown("---")


@st.cache_data
def load_data(file_path):
    """Loads the CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file '{file_path}' not found. Please ensure it is in the same directory.")
        return None

df = load_data('country_wise_latest.csv')

if df is not None:
 
    st.sidebar.header("Filter & Explore")
    
 
    region_options = df['WHO Region'].unique().tolist()
    selected_region = st.sidebar.selectbox(
        'Select a WHO Region for quick stats:', 
        ['All'] + region_options
    )

   
    if selected_region != 'All':
        df_filtered = df[df['WHO Region'] == selected_region]
    else:
        df_filtered = df.copy()

    
    total_confirmed = df_filtered['Confirmed'].sum()
    total_deaths = df_filtered['Deaths'].sum()
    
    st.sidebar.metric(
        label=f"Total Confirmed Cases ({selected_region})", 
        value=f"{total_confirmed:,.0f}"
    )
    st.sidebar.metric(
        label=f"Total Deaths ({selected_region})", 
        value=f"{total_deaths:,.0f}"
    )
    st.sidebar.markdown("---")


    df_top_confirmed = df.nlargest(10, 'Confirmed').sort_values('Confirmed', ascending=True)

    
    df_top_increase = df.nlargest(15, '1 week % increase').sort_values('1 week % increase', ascending=True)


    
    
    st.header("1. Magnitude: Global Hotspots")
    st.write("This chart highlights the countries with the largest *total number* of confirmed cases, showing the sheer scale of the crisis in specific regions.")

  
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        ax=ax1, 
        x='Confirmed', 
        y='Country/Region', 
        data=df_top_confirmed, 
        palette='Reds_d', 
        hue='WHO Region',
    )
    ax1.set_title('Top 10 Countries by Total Confirmed Cases', fontsize=14)
    ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax1.set_xlabel('Confirmed Cases (x$10^6$)', fontsize=12)
    ax1.set_ylabel('')
    ax1.legend(title='WHO Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)
    
    st.markdown("---")


    st.header("2. Severity: Case Fatality Rate (CFR)")
    st.write("The box plot illustrates the *distribution* of the Case Fatality Rate (Deaths per 100 Cases) across different WHO Regions. This reveals that severity is not uniform and depends heavily on regional factors.")

   
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        ax=ax2, 
        x='WHO Region', 
        y='Deaths / 100 Cases', 
        data=df,
        palette='viridis'
    )
    ax2.set_title('CFR Distribution by WHO Region', fontsize=14)
    ax2.set_xlabel('WHO Region', fontsize=12)
    ax2.set_ylabel('Deaths per 100 Cases (%)', fontsize=12)
    ax2.tick_params(axis='x', rotation=15)
    st.pyplot(fig2)
    
    st.markdown("---")


    st.header("3. Trajectory: Where is the Virus Accelerating?")
    st.write("This bar chart shows the 15 countries with the highest *recent percentage increase* in cases, highlighting where the crisis is currently worsening or expanding rapidly.")

    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        ax=ax3, 
        x='1 week % increase', 
        y='Country/Region', 
        data=df_top_increase, 
        palette='plasma'
    )
    ax3.set_title('Top 15 Countries by Percentage Increase in Cases (Last Week)', fontsize=14)
    ax3.set_xlabel('1 Week % Increase (%)', fontsize=12)
    ax3.set_ylabel('')
    st.pyplot(fig3)

    st.markdown("---")
    st.header("Raw Data")
    st.dataframe(df)