import psycopg2

def db_connection():
    try:
      #connect to db
      return psycopg2.connect(host="127.0.0.1",database="LAB",user="postgres", password="V#nnie100") 
      print("Conn Passed")
    except Exception as e:
      print(e) #conection error
db_connection()
