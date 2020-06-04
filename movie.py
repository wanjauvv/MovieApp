import dbcon
import pandas as pd

class Person:

    def __init__(self,fname,IDno,PhoneNo):
        self.con = dbcon.db_connection()
        self.con.autocommit = True
        self.cur = self.con.cursor()
        self.Clientname =  fname
        self.IDno =IDno
        self.PhoneNo = PhoneNo

    def Inquiry(self, title):
        sql = ("Select * from movie_catalogue.movies_list where title like %s")
        self.cur.execute (sql,(title +'%',))
        row = self.cur.fetchall()
        rc= self.cur.rowcount
        print('Movie Search results: ' + str(rc))
        if rc <= 0:
           print ("Movie not Found")
           Q = input("Do you want to search again, Y or N?")
           if str.upper(Q) == "Y":
               MovieTitle = input("Enter Movie Title to Search: ")
               someone.Inquiry(MovieTitle)
           elif str.upper(Q) == "N":
               print ("Thanks, Try again some other time")
        else:
          for i in row:
              print(i)

    def Reserve(self,MvID):
        #MvID = input('Enter the Movie ID to reserve')
        #MvID = int(self.MvID)
        sql = ("Select * from movie_catalogue.movies_list where movieid = %s ") # Check if Movie is on the Movie DB
        self.cur.execute(sql,(MvID,))
        rc = self.cur.rowcount
        if rc <= 0:
            print("Movie ID not Found")
        else:
            # Check if Movie is Available by having a status 0
            sql = ("Select * from movie_catalogue.movies_list where movieid = %s and reserve = 0 ")
            self.cur.execute(sql,(MvID,))
            rc = self.cur.rowcount
            if rc <= 0:
                print("Movie is on our Database but Not available")
            else:
                print("Movie is on our Database and is available")
                MvTitle = self.cur.fetchone()
                print("Would you like to reserve the Movie: ", MvTitle[2], '+?')

                Q = input("Enter Y or N: ")
                if str.upper(Q) == "Y":
                    #insert a record into the Booked Table
                    sql = """INSERT INTO movie_catalogue.booked_movie (movieid,clientname,idno,phoneno,borrowed)
                             VALUES(%s, %s, %s, %s,%s)"""
                    self.cur.execute(sql,(MvID,fname,IDno,PhoneNo,0))
                    #Update the status of the Movie to 1 IE booked/reserved
                    updateSQL = """ UPDATE movie_catalogue.movies_list SET reserve=1 WHERE id = %s """
                    self.cur.execute(updateSQL,(MvID,))
                    print("Movie has been Reserved")

                elif str.upper(Q) == 'N':
                    print("Movie Not Booked")

    def Borrow(self,clientName):
        counter = 0
        #show all movies under client name which have not been borrowed but were reserved/booked
        sql =  "Select * from movie_catalogue.booked_movie where clientname = %s and  borrowed = %s"
        self.cur.execute(sql,(clientName,0))
        rows = self.cur.fetchall()
        print("List of booked Movies: ")
        print("ID,MovieID,ClientName,IDNO,PhoneNo,borrowed_Status")
        for data in rows:
            print(data)
        for counter in range(counter,self.borrowcounter):
            MovID = int(input("Enter the ID of Movies to Borrow: "))
            #CHECK IF THE MOVIE ID IS EXISTING ON DB
            sql = "Select * from movie_catalogue.booked_movie where movieid = %s"
            self.cur.execute(sql,(MovID,))
            rc = self.cur.rowcount
            data = self.cur.fetchall()
            for i in data:
                print(i)
            if rc > 0:
                try:
                    sql =  """ UPDATE movie_catalogue.booked_movie SET borrowed = 1 WHERE movieid = %s and clientName = %s"""
                    try:
                        self.cur.execute(sql,(MovID,clientName))
                        print("Movie Hass been borrowed!")
                    except Exception:
                       print("User Does not Match the reserved Movie User")
                    QA = input("Do you want to borrow another Movie? Y or N?")
                    if (str.upper(QA) == 'Y'):
                        counter += 1
                    else:
                        break
                except Exception:
                    print("Movie Name has not being reserved")
            else:
                print("MovieID enter has Not been booked/reserved to be borrowed")
                break
        else:
            print("You have exceeded Your Borrow Limit")

    def Return(self,clientName):
        sql =  "Select * from movie_catalogue.booked_movie where clientname = %s and  borrowed = %s"
        self.cur.execute(sql,(clientName,1))
        rows = self.cur.fetchall()
        print("List of Borrowed Movies")
        for data in rows:
            print(data)
        MvIDRt = int(input("Enter Movie ID to return: "))
        sql = "DELETE FROM movie_catalogue.booked_movie where movieid = %s" #delete entry Movie on Booked Table
        self.cur.execute(sql,(MvIDRt,))

        sql = "UPDATE movie_catalogue.movies_list SET reserve=0 WHERE movieid = %s" #Mark the movie has not RESERVED
        self.cur.execute(sql,(MvIDRt,))

        print("Movie has been returned")


class User(Person):
    borrowcounter = 3
    def __init__(self,fname,IDno,PhoneNo,MvID):
      super().__init__(fname,IDno,PhoneNo)
      self.MvID = MvID



if __name__ == '__main__':
      fname = input("Enter Client Name: ")
      IDno = input("Enter ID Number: ")
      PhoneNo = input("Enter PhoneNo: ")
     # MovieTitle = input("Enter Movie Title to Search: ")
      MovieID = int(input("Enter Movie ID to Search: "))
      someone = Person('fname',IDno,PhoneNo)
      #someone.Inquiry(MovieTitle)  #step 1
      somebody= User('fname',IDno,PhoneNo,MovieID)
      #User.borrowcounter = 3
      #somebody.Reserve(MovieID) #step 2
      somebody.Borrow(fname)  #step 3
      #somebody.Return(fname)
