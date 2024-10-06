Jag började uppgiften med att skapa python koden "health_data.py" för att få min JSON fil. 
Koden och JSON-filen finns i mitt repo.
Sedan skickade jag in koden till min queue med koden "upload_to_azure.py".
Här kan du se min queue: 
![Här kan du se min queue](Data_Into_Queue.png)
När datan finns i min queue skickar jag vidare från queue till databasen med hjälp av Logic app:
![Här kan du se min Logic app](Logic_App.png)
