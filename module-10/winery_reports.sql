-- CSD-310
-- Milestone 3 Queries

USE Winery;

-- Report 1: Supplier Delivery Gaps

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

-- Report 2: Wine Sales and Distribution 

SELECT w.WineName, w.WineType, w.YearProduced,
        SUM(sw.QuantityShipped) AS TotalSold
FROM Shipment s
JOIN Shipment_Wine sw
ON s.ShipmentID = sw.ShipmentID
JOIN Wine w
ON sw.WineID = w.WineID
GROUP BY w.WineID, w.WineName, w.WineType, w.YearProduced
ORDER BY TotalSold DESC;

-- Report 3: Employee Hours Tracking

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
