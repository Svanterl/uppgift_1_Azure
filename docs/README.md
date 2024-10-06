Jag började uppgiften med att skapa python koden "health_data.py" för att få min JSON fil. 
Koden och JSON-filen finns i mitt repo.
Sedan skickade jag in koden till min queue med koden "upload_to_azure.py".
Här kan du se min queue: 
![Här kan du se min queue](Data_Into_Queue.png)
När datan finns i min queue skickar jag vidare från queue till databasen med hjälp av Logic app:
![Här kan du se min Logic app](Logic_App.png)
Här är en bild på att jag kan se min data i min databas:
![Här kan du se min Databas](Data_In_Database.png)
Sedan använder jag min data för att visualisera lokalt med Power BI:
![Här kan du se min PowerBI](PowerBI.png)
Jag använder även grafana i en VM för att visualisera:
![Här kan du se min Logic app](grafana.png)
