import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("data/database.db")
    #sqlite does not enforce foreign keys so they must be enabled manually
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


#create tables to store data sets and sales
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    #use CREATE TABLE IF NOT EXISTS to prevent overwriting existing tables in the even the query reruns
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS datasets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   file_name TEXT,
                   upload_time TEXT
                   )
                   """)
    
    #use ON DELETE CASCADE to ensure data integraty when deleating data sets
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sales(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   dataset_id INTEGER,
                   date TEXT,
                   product TEXT,
                   category TEXT,
                   sales INTEGER,
                   FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS models(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   filename TEXT,
                   mae REAL
                   )
                   """)
    
    conn.commit()
    conn.close()


def insert_dataset(file_name):
    conn = connect_db()
    cursor = conn.cursor()

    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
                   INSERT INTO datasets (file_name, upload_time)
                   VALUES (?, ?)
                   """, (file_name, upload_time,))
    
    conn.commit()
    
    #get id of the data set
    dataset_id = cursor.lastrowid

    conn.close()
    
    #return dataset_id as it is needed by the insert sales function
    return dataset_id

def insert_sales(sales_data, dataset_id):
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in sales_data.iterrows():
        cursor.execute("""
                       INSERT INTO sales (dataset_id, date, product, category, sales)
                       VALUES (?, ?, ?, ?, ?)
                       """, (
                           dataset_id,
                           str(row["date"].date()),
                           row["product"],
                           row["category"],
                           int(row["sales"])
                       ))
    conn.commit()
    conn.close()

def delete_dataset(dataset_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM datasets WHERE id = ?", (dataset_id,))

    conn.commit()
    conn.close()


def load_datasets(min_uploadtime, max_uploadtime):

    query ="""SELECT id, file_name, upload_time
            FROM datasets""" 
    
    conditions = []
    params = []

    if min_uploadtime:
        conditions.append("upload_time >= ?")
        params.append(min_uploadtime)
    if max_uploadtime:
        conditions.append("upload_time <= ?")
        params.append(max_uploadtime)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY id ORDER BY id DESC"

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.commit()
    conn.close()

    return results

def load_sales_data(min_date, max_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT date, product, sales  FROM sales
                   WHERE date >= ? AND date <= ?
                   ORDER BY date""",(min_date, max_date))
    
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    return results



def load_all_datasets():
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM datasets """)

    results = cursor.fetchall()
    conn.commit()
    conn.close()

    return results


def insert_model(date, filename, mae):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                INSERT INTO models (date, filename, mae)
                VALUES (?, ?, ?)
                """, (
                    str(date),
                    filename,
                    float(mae),
                    ))
    
    conn.commit()
    conn.close()

def get_models():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT filename FROM models""")
    
    results = cursor.fetchall()
    conn.commit()
    conn.close()
 
    
    print(results)
    
    #results is a list of tuples so we need to build a new list containing just the values for filename
    return [row[0] for row in results]

def load_models(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM models
                   WHERE date >= ? AND date <= ?
                   ORDER BY date""", (start_date, end_date)
                   )
    
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    return results

def delete_model(model_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM models WHERE id = ?"""
                   ,(model_id,))
    
    conn.commit()
    conn.close()

def load_all_models():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * FROM models""")
    
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    return results




    
