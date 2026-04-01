import plotly.graph_objects as go
import pandas as pd

def create_sales_line_chart(data):
    
    #convert data into a dataframe
    df = pd.DataFrame(data, columns=["date", "total_sales", "coffee_sales", "food_sales"])

    #make sure data in date column is recognised as a date value
    df["date"] = pd.to_datetime(df["date"]) 

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = df["date"],
        y = df["total_sales"],
        mode = "lines",
        name = "Total Sales"
    ))

    fig.add_trace(go.Scatter(
        x = df["date"],
        y = df["coffee_sales"],
        mode = "lines",
        name = "Coffee Sales"
    ))

    fig.add_trace(go.Scatter(
        x = df["date"],
        y = df["food_sales"],
        mode = "lines",
        name = "Food Sales"
    ))

    fig.update_layout(
        title = " Sales Over Time",
        xaxis_title = "Date",
        yaxis_title = "Sales",
        template = "plotly_white"
    )

    return fig

def create_sales_by_product_chart(data):
    
    #convert data to data frame
    df = pd.DataFrame(data, columns = ["product", "sales"])

    #sort products by number of sales
    df = df.sort_values("sales", ascending = True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = df["sales"],
        y = df["product"],
        orientation = "h"
    ))

    fig.update_layout(
        height = 240,
        margin=dict(l=120, r=30, t=40, b=50),
        xaxis_title = "sales",
        yaxis_title = "product",
        template = "plotly_white",
        bargap = 0.2
    )

    return fig


def create_sales_by_weekday_chart(data):
    
    #convert data to dataframe
    df = pd.DataFrame(data, columns = ["weekday", "weekday_num", "sales"])

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x = df["sales"],
        y = df["weekday"],
        orientation = "h"
    ))

    fig.update_layout(
        height = 240,
        margin=dict(l=120, r=30, t=40, b=50),
        xaxis_title = "Sales",
        yaxis_title = "Product",
        template = "plotly_white",
        bargap = 0.2
    )

    return fig


def create_predicted_vs_actual (data):

    fig = go.Figure()
    
    #get product names
    products = data["product"].unique()
    
    #plot the predicted vs actual sales for each product in products
    for product in products:
        
        df = data[data["product"] == product]
        df = df.sort_values("date")

        #plot actual sales
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["actual"],
            mode="lines",
            name=f"{product} (actual)"
        ))

        #plot predicted sales
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["predicted"],
            mode="lines",
            name=f"{product} (predicted)",
            #dashed line for predicted sales
            line=dict(dash="dash")
        ))
    
    fig.update_layout(
        title="Actual vs Predicted (sales)",
        xaxis_title="date",
        yaxis_title="sales",
        template="plotly_white"
    )

    return fig
    

def create_predicted_sales_chart(data):


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["cappuccino"],
        mode="lines",
        name="cappuccino"
    ))

    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["americano"],
        mode="lines",
        name="Americano"
    ))

    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["croissant"],
        mode="lines",
        name="Croissant"
    ))
    
    
    fig.update_layout(
        title="Predicted Future Sales",
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white"
    )

    return fig
