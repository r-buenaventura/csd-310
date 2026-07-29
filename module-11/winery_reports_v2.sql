-- CSD-310
-- Milestone 3 Queries

USE Winery;

-- Report 1: Supplier Delivery Gaps


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

-- Report 2: Wine Sales and Distribution 
SELECT NOW() AS ReportGenerated, w.WineName, w.WineType, w.YearProduced,
        SUM(sw.QuantityShipped) AS TotalSold
FROM Shipment s
JOIN Shipment_Wine sw
ON s.ShipmentID = sw.ShipmentID
JOIN Wine w
ON sw.WineID = w.WineID
GROUP BY w.WineID, w.WineName, w.WineType, w.YearProduced
ORDER BY TotalSold DESC;

-- Report 3: Employee Hours Tracking
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
GROUP BY YEAR(t.DateWorked), QUARTER(t.DateWorked), e.EmployeeIS, e.FirstName, e.LastName, q.QuarterTotalHours
ORDER BY YEAR, Quarter, e.LastName, e.FirstName;
