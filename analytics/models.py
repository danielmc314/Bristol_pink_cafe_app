import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import datetime
from database.database_manager import insert_model



def generate_training_data(sales_data):
    # convert list to dataframe
    training_data = pd.DataFrame(sales_data, columns=["date", "product", "sales"])

    # make sure date is a date time value
    training_data["date"] = pd.to_datetime(training_data["date"])
    
    #make training data wide formate for model training
    training_data = training_data.pivot(index="date", columns="product", values="sales")

    #add day of the week to sales_data
    training_data['day_of_week'] = training_data.index.dayofweek
    #add month to sales_data
    training_data['month'] = training_data.index.month
    #add is weekend column
    training_data['is_weekend'] = training_data["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

    return training_data

def train_ai_models(sales_data, file_version):
    
    df = generate_training_data(sales_data)

    # 2. Define our Features (X)
    # This is the context the AI uses to make its prediction
    X = df[['day_of_week', 'month', 'is_weekend']]

    # 3. Define our Targets (y)
    # These are the actual items we want to predict
    targets = ['cappuccino', 'americano', 'croissant']
    
    print("Training Machine Learning Models...\n")
    
 
    results = []
    prediction_row = []

    # We will loop through and train a separate, dedicated AI for each item
    for item in targets:
        y = df[item]
        
        # We give the AI 80% of the past data to learn from.
        # We hide the remaining 20% to test it like a pop-quiz later.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 5. Initialize the Algorithm
        # n_estimators=100 means we are using 100 "decision trees" working together
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # 6. Train the AI! (This is where the actual learning happens)
        model.fit(X_train, y_train)
        
        # 7. Evaluate the AI
        # We force the AI to predict sales for the 20% of days it hasn't seen yet
        predictions = model.predict(X_test)
        
        # We calculate the Mean Absolute Error (MAE) - how far off it was on average
        error = mean_absolute_error(y_test, predictions)
        
        print(f"--- {item} Prediction Model ---")
        print(f"Average Margin of Error: +/- {error:.2f} {item}s per day")
        
        # 8. Save the trained model to your hard drive
        #query models database for the most recent versions of each model
        filename = f'{item}_model_{file_version}.pkl'
            

        joblib.dump(model, filename)
        print(f"Successfully saved AI model as: {filename}\n")

        #store results for each model
        results.append({
            "product": item,
            "mae": error,
            "model_file": filename
        })

        #insert new model into database
        #get current date
        


        for date, actual, predicted in zip(X_test.index, y_test, predictions):
            prediction_row.append({
                "date": date,
                "product": item,
                "actual": float(actual),
                "predicted": float(predicted)
            })

    #create dataframes for results and predictions
    results_df = pd.DataFrame(results)
    predictions_df = pd.DataFrame(prediction_row)
    
    #initilise model version
    model_version = f'model_{file_version}'

    #insert model version into database
    date = pd.Timestamp.today().normalize()
    insert_model(date, model_version, error)

    print("All models successfully trained and ready for the Dashboard!")

    return results_df, predictions_df


#builds the dataframe that will be passed to models to predict future sales
def build_prediction_dataframe(date):
    current_date = pd.Timestamp.today().normalize()

    #make sure date inputted is type dtae/time
    end_date = pd.to_datetime(date)
    
    #get all dates from current_date to end_date
    dates = pd.date_range(start=current_date, end=end_date) 

    #create predicted sales df
    predicted_sales = pd.DataFrame({"date": dates})

    #add features for model
    #add day of the week to sales_data
    predicted_sales['day_of_week'] = predicted_sales["date"].dt.dayofweek
    #add month to sales_data
    predicted_sales['month'] = predicted_sales["date"].dt.month
    #add is weekend column
    predicted_sales['is_weekend'] = predicted_sales["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

    return predicted_sales


def predict_future_sales(date, models_version):

    #build future dates dataframe
    future_sales = build_prediction_dataframe(date)

    #extract features
    X_future = future_sales[["day_of_week", "month", "is_weekend"]]

    #load models
    cappuccino_model = joblib.load(f"cappuccino_{models_version}.pkl")
    americano_model = joblib.load(f"americano_{models_version}.pkl")
    croissant_model = joblib.load(f"croissant_{models_version}.pkl")

    #make predictions
    future_sales["cappuccino"] = cappuccino_model.predict(X_future)
    future_sales["americano"] = americano_model.predict(X_future)
    future_sales["croissant"] = croissant_model.predict(X_future)

    #round sale values to nearest integer in dataframe
    future_sales[["cappuccino", "americano", "croissant"]] = (
        future_sales[["cappuccino", "americano", "croissant"]].round()
    )
    #get future sales datframe in long formate for tabular display using melt
    #remove 
    future_sales_long_formate = future_sales.melt(
        id_vars = ["date"],
        value_vars=["cappuccino", "americano", "croissant"],
        var_name="product",
        value_name ="sales"
    )
     
    #sort data in future_sales_Long_formate by date
    future_sales_long_formate = future_sales_long_formate.sort_values(by="date")

    #convert dates in date column from yyyy/mm/dd to day date month (e.g friday 06 january)
    future_sales_long_formate["date"] = pd.to_datetime(
        future_sales_long_formate["date"]
    ).dt.strftime("%A %d %b")

    return future_sales, future_sales_long_formate