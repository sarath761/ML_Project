import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

import io
import base64
import matplotlib.pyplot as plt

def train_fun(path1, path2):

    # Function to convert time from the format 'HH:MM' to minutes
    def convert_time_to_minutes(time_str):
        if pd.isna(time_str) or time_str == 0 or time_str == '0':
            return 0
        else:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes

    # Function to convert activity level from the format 'XX %' to a number between 0 and 1
    def convert_activity_level_to_decimal(activity_str):
        if pd.isna(activity_str):
            return 0
        else:
            return int(activity_str.strip(' %')) / 100

    # Load the data
    df1 = pd.read_csv(path1, encoding='utf-8')
    df2 = pd.read_csv(path2, encoding='utf-8')

    # Convert time spent and activity level data
    for col in df1.columns[2:-1]:
        df1[col] = df1[col].apply(convert_time_to_minutes)
        df2[col] = df2[col].apply(convert_activity_level_to_decimal)

    # Convert 'Total' and 'Average' columns
    df1['Total'] = df1['Total'].apply(convert_time_to_minutes)
    df2['Average'] = df2['Average'].apply(convert_activity_level_to_decimal)



    # Aggregate the data at the user level
    df1_agg = df1.groupby('User').sum().reset_index()
    # df1_agg = df1.groupby('User').sum().reset_index()
    df2_agg = df2.groupby('User').sum().reset_index()

    # Find best weights for performance definition
    best_weights = (0, 0)
    best_r2 = 0

    # Vary the weights from 0 to 1 with a step size of 0.1
    for a in np.arange(0, 1.1, 0.1):
        for b in np.arange(0, 1.1, 0.1):
            # Skip if the weights do not sum to 1
            if a + b != 1:
                continue

            # Define performance with the current weights
            df1_agg['Performance'] = a * df1_agg['Total'] + b * df2_agg['Average']
            df2_agg['Performance'] = df1_agg['Performance']

            # Split the data into a training set and a test set
            X1 = df1_agg.drop(['User', 'Total', 'Performance'], axis=1)
            y1 = df1_agg['Performance']
            X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

            X2 = df2_agg.drop(['User', 'Average', 'Performance'], axis=1)
            y2 = df2_agg['Performance']
            X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)
            
            # Train a linear regression model on the time spent data
            model1 = LinearRegression()
            print(X1_train)
            print(y1_train)
            model1.fit(X1_train, y1_train)
            

            # Train a linear regression model on the activity level data
            model2 = LinearRegression()
            model2.fit(X2_train, y2_train)

            # Predict performance on the test set
            y1_pred = model1.predict(X1_test)
            y2_pred = model2.predict(X2_test)

            # Calculate R-squared
            r21 = r2_score(y1_test, y1_pred)
            r22 = r2_score(y2_test, y2_pred)

            # Update the best weights and the best R-squared if the current R-squared is better
            if max(r21, r22) > best_r2:
                best_r2 = max(r21, r22)
                best_weights = (a, b)

    # Plot the performance of the staffs
    plt.figure(figsize=(10, 6))
    plt.bar(df1_agg['User'], df1_agg['Performance'])
    plt.xlabel('User')
    plt.ylabel('Performance')
    plt.title('Performance of Staffs')
    plt.xticks(rotation=90)
    # plt.show()
    
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()
    
    
    img_buffer.seek(0)
    base64_encoded_image = base64.b64encode(img_buffer.read()).decode('utf-8')
    return(base64_encoded_image)

