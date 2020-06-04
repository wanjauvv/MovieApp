import dbcon
import pandas as pd

def Inquiry(movieTitle):
    con = dbcon.db_connection()
    con.autocommit = True
    cur = con.cursor()

    cur.execute ("Select * from movie_catalogue.movies_list where title like  %s", (movieTitle +'%',))
    row = cur.fetchall()
    for i in row:
        print(i)

Inquiry('Toy')
