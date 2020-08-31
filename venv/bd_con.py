import mysql.connector

conn = mysql.connector.connect(
    host="b5o9m32q9rds06udvs6v-mysql.services.clever-cloud.com",
    user="upi1ralkoajjg0md",
    password="4BlNb1TyEhXjngxWHXOY",
    database="b5o9m32q9rds06udvs6v"
)

mycursor = conn.cursor()
mycursor.execute("select * from users;")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

mycursor.execute("show tables;")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)