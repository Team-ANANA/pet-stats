import mysql.connector

cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                              host='localhost',
                              database='pet-stats')
mycursor = cnx.cursor()
mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("Show tables;")
 
myresult = mycursor.fetchone()
print(myresult) 

cnx.close()
