from database.database_manager import connect_db

def get_sales_by_product(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT product, SUM(sales) AS total_sales
                   FROM sales
                   WHERE date BETWEEN ? AND ?
                   GROUP BY product
                   ORDER BY total_sales DESC
                   """, (start_date, end_date))
    
    results = cursor.fetchall()

    conn.close()

    return results

def get_total_sales(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT SUM(sales) AS total_sales
                   FROM sales
                   WHERE date BETWEEN ? AND ?
                   """, (start_date, end_date))
    
    result = cursor.fetchone()

    conn.close()

    return result

def get_coffee_sales(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT SUM(sales) AS total_sales
                   FROM sales
                   WHERE category = "coffee"
                   AND date BETWEEN ? AND ?
                   """, (start_date, end_date))
    
    result = cursor.fetchone()

    conn.close()

    return result

def get_food_sales(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT SUM(sales) AS total_sales
                   FROM sales
                   WHERE category = "food"
                   AND date BETWEEN ? AND ?
                   """, (start_date, end_date))
    
    result = cursor.fetchone()

    conn.close()

    return result

def get_sales_by_weekday(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT 
                   CASE strftime('%w', date)
                        WHEN '0' THEN 'Sunday'
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                   END AS weekday,
                   CAST(strftime('%w', date) AS INTEGER) AS weekday_num,
                   SUM(sales) AS total_sales
                   FROM sales
                   WHERE date BETWEEN ? AND ?
                   GROUP BY weekday
                   ORDER BY weekday
                   """, (start_date, end_date))
    
    results = cursor.fetchall()

    conn.close()

    return results
    
def get_sales_by_date(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT
                    date,
                    SUM(sales) AS total_sales,
                    SUM(CASE WHEN category = 'coffee' THEN sales ELSE 0 END) as coffee_sales,
                    SUM(CASE WHEN category = 'food' THEN sales ELSE 0 END) AS food_sales
                   FROM sales
                   WHERE date BETWEEN ? AND ?
                   GROUP BY date
                   ORDER BY date
                   """, (start_date, end_date))
    
    results = cursor.fetchall()

    conn.close()

    return results
