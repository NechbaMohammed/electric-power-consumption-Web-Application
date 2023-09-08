import streamlit as st
import pickle
import numpy as np
import pandas as pd
# Load the trained model
model = pickle.load(open('model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

def create_features(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['day'] = df.index.month
    df['year'] = df.index.year
    df['season'] = df['month'] % 12 // 3 + 1
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    
    # Additional features
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    df['is_month_start'] = (df['dayofmonth'] == 1).astype(int)
    df['is_month_end'] = (df['dayofmonth'] == df.index.days_in_month).astype(int)
    df['is_quarter_start'] = (df['dayofmonth'] == 1) & (df['month'] % 3 == 1).astype(int)
    df['is_quarter_end'] = (df['dayofmonth'] == df.groupby(['year', 'quarter'])['dayofmonth'].transform('max'))
    
    # Additional features
    df['is_working_day'] = df['dayofweek'].isin([0, 1, 2, 3, 4]).astype(int)
    df['is_business_hours'] = df['hour'].between(9, 17).astype(int)
    df['is_peak_hour'] = df['hour'].isin([8, 12, 18]).astype(int)
    
    # Minute-level features
    df['minute_of_day'] = df['hour'] * 60 + df['minute']
    df['minute_of_week'] = (df['dayofweek'] * 24 * 60) + df['minute_of_day']
    
    return df.astype(float)


def show_predict_page():

  
   

    # Add a header section
    st.title('Power Consumption Prediction')
    st.write('Enter the features on the sidebar and click "Predict" to see the power consumption predictions for each zone.')


    # Add input fields for features
    st.header('Input Features')
    date_time = st.text_input('Date Time (e.g., "2023-09-08 10:00:00")')
    temperature = st.number_input('Temperature')
    humidity = st.number_input('Humidity')
    wind_speed = st.number_input('Wind Speed')
    diffuse_flows = st.number_input('Diffuse Flows')
    general_diffuse_flows = st.number_input('General Diffuse Flows')

    # Create a prediction button
    if st.button('Predict'):
        # Prepare input data as a DataFrame
        input_data = pd.DataFrame({
            'Datetime': [date_time],
            'Temperature': [temperature],
            'Humidity': [humidity],
            'WindSpeed': [wind_speed],
            'GeneralDiffuseFlows':[general_diffuse_flows],
            'DiffuseFlows': [diffuse_flows]
            
        })
        input_data['Datetime']=pd.to_datetime(input_data.Datetime)
        input_data = input_data.set_index('Datetime')
        input_data = create_features(input_data)
        # Make a prediction using the trained model
        prediction = model.predict(input_data)
        prediction_scaler = scaler.inverse_transform(prediction)
        # Display the prediction
        st.subheader('Predicted Power Consumption')
        st.write(f'Zone 1: {prediction_scaler[0][0]:.2f}')
        st.write(f'Zone 2: {prediction_scaler[0][1]:.2f}')
        st.write(f'Zone 3: {prediction_scaler[0][2]:.2f}')
