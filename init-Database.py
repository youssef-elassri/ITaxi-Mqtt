import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Itaxi_db1"
)
TableSchema = """
create table Locations(
    id VARCHAR(10) PRIMARY KEY,
    lon FLOAT,
    lat FLOAT,
    alt FLOAT,
    etat int,
    type VARCHAR(10));
"""

# Connect or Create DB File
mycursor = mydb.cursor()

mycursor.execute("drop table if exists Locations;")
mycursor.execute(TableSchema)

# Close DB
mycursor.close()
