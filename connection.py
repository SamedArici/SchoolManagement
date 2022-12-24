import mysql.connector

try:
    connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "highschool"
    )
except mysql.connector.DatabaseError:
    print("\n")
    print("Database Connection Failed".center(50,"_"))
    print("\n1. Import sql file inside the 'SQL_DATABASE' folder to the 'MYSQL'\n2. Fill the host, user, password, database informations from the 'connection.py' file!\n")

