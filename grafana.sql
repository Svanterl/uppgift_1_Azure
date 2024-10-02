--Koderna för att skapa grafana visualiseringarna

--Average Heart Rate Per Device
SELECT 
  device_id AS "Device ID",
  AVG(heart_rate) AS "Average Heart Rate"
FROM 
  HealthData
GROUP BY 
  device_id

--Använde denna i Pie Chart 
SELECT 
  device_id AS "Device ID",
  SUM(steps_taken) AS "Total Steps"
FROM 
  HealthData
GROUP BY 
  device_id

--Använde denna för att visa Average Steps

SELECT 
    AVG(steps_taken) as average_steps
FROM 
    HealthData

