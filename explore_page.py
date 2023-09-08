import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



@st.cache_data
def load_data():
    df = pd.read_csv("powerconsumption.csv")
    return df



def show_explore_page():
    st.title("Explore Power Consumption Data")

    st.write(
        """
    ### Power Consumption Data tetouan 2017
    """
    )
    # Resample the data for more meaningful time series analysis (e.g., daily, weekly)
    df = load_data()
    df['Datetime']=pd.to_datetime(df.Datetime)
    df = df.set_index('Datetime')
    daily_resampled = df.resample('D').mean()

    # Plot daily Power Consumption for each zone
    fig1 =plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_resampled[['PowerConsumption_Zone1', 'PowerConsumption_Zone2', 'PowerConsumption_Zone3']])
    plt.xlabel('Date')
    plt.ylabel('Average Power Consumption')
    plt.title('Average Daily Power Consumption')
    plt.legend(labels=['Zone 1', 'Zone 2', 'Zone 3'])
    st.pyplot(plt)

    
    st.write("""#### Number of Data from different countries""")

    #st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    #data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    #st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    #data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    #st.line_chart(data)

