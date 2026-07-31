"""
CSD 310 - Module 10 Milestone 3
by Group Delta
July 21, 2026
This script connects to a MySQL database and generates three reports:
1. Supplier Delivery Gaps
2. Wine Sales and Distribution
3. Employee Hours Tracking
It uses the mysql.connector library to connect to the database and execute SQL queries.
The results of each report are printed to the console."""

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

def old_show_tables(cursor, sql, title):
    cursor.execute(sql)
    records = cursor.fetchall()
    print("\n{}".format(title))

    if cursor.column_names:
        print(", ".join(cursor.column_names))
            
    for row in records:
        row_strings = [str(item) if item is not None else "NULL" for item in row]
        print(", ".join(row_strings))

def show_tables(cursor, sql, title):
    cursor.execute(sql)
    records = cursor.fetchall()
    
    print("\n" + "=" * 80)
    print("  {}".format(title))
    print("=" * 80)

    if not records:
        print("No records found.")
        return

    # Convert all record items to clean strings upfront (handling NULLs)
    formatted_records = [
        [str(item) if item is not None else "NULL" for item in row]
        for row in records
    ]

    # Calculate exact max width needed for EACH column (header vs longest data row)
    col_widths = []
    for i, col_name in enumerate(cursor.column_names):
        # Find max string length in column 'i' across all data rows
        max_data_len = max(len(row[i]) for row in formatted_records) if formatted_records else 0
        # Column width is whichever is larger: header length or data length, plus 4 spaces for padding
        width = max(len(col_name), max_data_len) + 4
        col_widths.append(width)

    # 1. Print Headers with custom per-column padding
    header_str = "".join(f"{col_name:<{col_widths[i]}}" for i, col_name in enumerate(cursor.column_names))
    print(header_str)
    print("-" * len(header_str))

    # 2. Print Data Rows using matching column padding
    for row in formatted_records:
        row_str = "".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row))
        print(row_str)
        
    print("-" * len(header_str))

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    
    # -- Report 1: Supplier Delivery Gaps
    supplier_delivery_gaps_query = """
    SELECT NOW() AS ReportGenerated, s.SupplierName, d.DeliveryID, d.ExpectedDate, d.ActualDate,
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
    SELECT NOW() AS ReportGenerated, w.WineName, w.WineType, w.YearProduced,
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
    SELECT NOW() AS ReportGenerated,
        YEAR(t.DateWorked) AS Year,
        QUARTER(t.DateWorked) AS Quarter,
        CONCAT(e.FirstName, ' ', e.LastName) AS Employee,
        SUM(t.HoursWorked) AS TotalHours,
        q.QuarterTotalHours
    FROM Employee e
    JOIN TimeSheet t
        ON e.EmployeeID = t.EmployeeID
    JOIN (
        SELECT
            YEAR(DateWorked) AS Year,
            QUARTER(DateWorked) AS Quarter,
            SUM(HoursWorked) AS QuarterTotalHours
        FROM TimeSheet
        GROUP BY
            YEAR(DateWorked),
            QUARTER(DateWorked)
    ) q
    ON YEAR(t.DateWorked) = q.year
    AND QUARTER(t.DateWorked) = q.Quarter
    GROUP BY YEAR(t.DateWorked), QUARTER(t.DateWorked), e.EmployeeID, e.FirstName, e.LastName, q.QuarterTotalHours
    ORDER BY YEAR, Quarter, e.LastName, e.FirstName;
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

