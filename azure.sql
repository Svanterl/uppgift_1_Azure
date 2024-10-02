
--Detta är sql koden jag använde för att skapa min tabell i azure

CREATE TABLE HealthData (
    id INT PRIMARY KEY IDENTITY(1,1),  -- Auto-incremented primary key
    device_id VARCHAR(50) NOT NULL,     -- Device ID, an integer as a string
    timestamp DATETIME NOT NULL,         -- Timestamp for the data entry
    heart_rate INT NOT NULL,             -- Heart rate in beats per minute
    systolic INT NOT NULL,               -- Systolic blood pressure
    diastolic INT NOT NULL,              -- Diastolic blood pressure
    spo2 INT NOT NULL,                   -- Blood oxygen saturation percentage
    steps_taken INT NOT NULL              -- Number of steps taken
)

