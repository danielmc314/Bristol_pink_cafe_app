import pandas as pd




def read_data(csv_file):
    #read the first two rows of the csv file
    #dont treat any row as coulmn names yet
    preview = pd.read_csv(csv_file, nrows=2, header=None)

    #get the second row of the preview and convert eveything ti strings, remove extra spaces, and make everything lowercase
    second_row = preview.iloc[1].astype(str).str.strip().str.lower()

    #check weather the second row of preview contains the names of coffee products
    #coffee file stores product names on second row
    if "cappuccino" in second_row.values or "americano" in second_row.values:
        category = "coffee"
        #skip the first row of the data and use second row as column names
        data = pd.read_csv(csv_file, header=1)
        #name the first column date
        data = data.rename(columns={data.columns[0]: "date"})
    else:
        category = "food"
        data = pd.read_csv(csv_file)

    data.columns = data.columns.str.strip().str.lower()
    return category, data
    
def transform_coffee_data(data):
    #build a list of all columns except date
    product_columns = [col for col in data.columns if col != "date"]
    
    #convert data from wide format to long format
    return data.melt(
        #keep date column the same
        id_vars = "date",
        #turn columns in product columns list into rows
        value_vars= product_columns,
        #column names become values in a new column called product 
        var_name = "product",
        #numbers inside of those columns become values in a new column called sales 
        value_name = "sales"
    )

def transform_food_data(data):
    #food file has one product 
    data = data.rename(columns={"number sold": "sales"})
    data["product"] = "croissant"
    return data


#transform data so both data sets are able to join
def transform_data(data, category):
    
    #drop duplicate rows
    data = data.drop_duplicates()

    if category == "coffee":
        data = transform_coffee_data(data)
    else:
        data = transform_food_data(data)
    
    # convert date column from text to real datetime values
    data["date"] = pd.to_datetime(data["date"], dayfirst=True)

    data["category"] = category
    return data


def clean_data(csv_file):
    
    category,data = read_data(csv_file)
    data = transform_data(data, category)

    #convert product column to string and remove spaces at the start and end of the string  
    data["product"] = data["product"].astype(str).str.strip()
    #convert quantity columns in to numbers if data canot convert to string it becomes NaN(missing value)
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
    #drop rows with invalid quantities
    data = data.dropna(subset=["sales"])
    #make sure sales arnt negative
    data = data[data["sales"] >= 0]

    return data


def build_dataset_name(sales_data):
    #find the first and last date in the sales data
    start_date = sales_data["date"].min()
    end_date = sales_data["date"].max()
    
    #build sales data file name
    dataset_name = f"{start_date.date()}_to_{end_date.date()}_sales"
    return dataset_name
    
#clean combined data set
def clean_combined_data(csv_file1, csv_file2):

    data1 = clean_data(csv_file1)
    data2 = clean_data(csv_file2)
    
    #stack the rows of the individual data sets to get the full sales data
    sales_data = pd.concat([data1, data2], ignore_index=True)
    #make sure data is still ordered by date
    sales_data = sales_data.sort_values("date").reset_index(drop=True)

    dataset_name = build_dataset_name(sales_data)

    return sales_data, dataset_name

def single_data_set(csv_file):

    sales_data = clean_data(csv_file)

    dataset_name = build_dataset_name(sales_data)

    return sales_data, dataset_name












