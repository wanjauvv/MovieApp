import dbcon
import pandas as pd

class DataManuplication:
      def __init__(self): #initialize the class
         self.con = dbcon.db_connection()
         self.con.autocommit = True
         self.cur=self.con.cursor()
         self.MovieDataFrame= pd.read_csv('csv/movies.csv')
         self.RatingDataFrame= pd.read_csv('csv/ratings.csv', parse_dates=['timestamp'], date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))
         self.TagsDataFrame= pd.read_csv('csv/tags.csv', parse_dates=['timestamp'], date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))

      def MergeData(self): #merge the data
         self.Merge_data_set1 =pd.merge(self.MovieDataFrame,self.RatingDataFrame[['movieid','rating', 'timestamp']], on= 'movieid', how='left')
         self.Merge_data_set2 =pd.merge(self.Merge_data_set1, self.TagsDataFrame[['movieid', 'tag']], on='movieid',how='left')

      def InsertData(self): #insert data on the DB
          self.getColumns = self.MovieDataFrame.columns.tolist()
          self.cols = ','.join([str(i) for i in self.getColumns ])

          #insert data into table
          for i,row in self.MovieDataFrame.iterrows():
              sql = 'INSERT INTO movie_catalogue.movies_list (' + self.cols + ') VALUES ('+'%s,' *(len(row)-1)+'%s)'
              self.cur.execute(sql, tuple(row))
              #conn.commit()

      def showData(self): #print dataFrame
          print(self.TagsDataFrame.tail())
          print(self.Merge_data_set2.tail())

      def showDBData(self): #show merged data on the db
         sql='select * from movie_catalogue.movies LIMIT 10'
         self.cur.execute(sql)
         rows = self.cur.fetchall()
         for i in rows:
              print(i)

if __name__=='__main__':
    dataM = DataManuplication()
    #dataM.MergeData()
    #dataM.showData()
    dataM.InsertData()
    #dataM.showDBData()
