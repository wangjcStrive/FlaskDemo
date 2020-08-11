import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=JICWANG1-E7470\MYSQL;DATABASE=DailyTask;UID=sa;PWD=LMwjc7922!')
cursor = conn.cursor()

