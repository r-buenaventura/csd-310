import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

secrets = dotenv_values(".env")
 
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

def show_tables(cursor, sql, title):
    cursor.execute(sql)
    records = cursor.fetchall()
    print("\n{}".format(title))

    if cursor.column_names:
        print(", ".join(cursor.column_names))
            
    for row in records:
        row_strings = [str(item) if item is not None else "NULL" for item in row]
        print(", ".join(row_strings))

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    
    # -- Report 1: Supplier Delivery Gaps
    supplier_delivery_gaps_query = """
    SELECT s.SupplierName, d.DeliveryID, d.ExpectedDate, d.ActualDate,
        DATEDIFF(d.ActualDate, d.ExpectedDate) AS DaysLate,
        CASE 
            WHEN d.ActualDate IS NULL THEN 'Pending'
            WHEN d.ActualDate > d.ExpectedDate THEN 'Late'
            ELSE 'On Time'
        END AS DeliveryStatus
    FROM Delivery d
    JOIN Supplier s
    ON d.SupplierID = s.SupplierID
    ORDER BY 
        s.SupplierName, d.ExpectedDate;
    """
    show_tables(cursor, supplier_delivery_gaps_query, "-- SUPPLIER DELIVERY GAPS --")

    # -- Report 2: Wine Sales and Distribution 
    wine_sales_distribution_query = """
    SELECT w.WineName, w.WineType, w.YearProduced,
        SUM(sw.QuantityShipped) AS TotalSold
    FROM Shipment s
    JOIN Shipment_Wine sw
    ON s.ShipmentID = sw.ShipmentID
    JOIN Wine w
    ON sw.WineID = w.WineID
    GROUP BY w.WineID, w.WineName, w.WineType, w.YearProduced
    ORDER BY TotalSold DESC;
    """
    show_tables(cursor, wine_sales_distribution_query, "-- WINE SALES AND DISTRIBUTION --")

    # -- Report 3: Employee Hours Tracking
    employee_hours_tracking_query = """
    SELECT
        YEAR(t.DateWorked) AS Year,
        QUARTER(t.DateWorked) AS Quarter,
        CONCAT(e.FirstName, ' ', e.LastName) AS Employee,
        SUM(t.HoursWorked) AS TotalHours
    FROM Employee e
    JOIN TimeSheet t
        ON e.EmployeeID = t.EmployeeID
    GROUP BY
        YEAR(t.DateWorked),
        QUARTER(t.DateWorked),
        e.EmployeeID,
        e.FirstName,
        e.LastName
    ORDER BY
        Year,
        Quarter,
        e.LastName,
        e.FirstName;
    """
    show_tables(cursor, employee_hours_tracking_query, "-- EMPLOYEE HOURS TRACKING --")

except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
 
finally:
    """ close the connection to MySQL """
    db.close()
