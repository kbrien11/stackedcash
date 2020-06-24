import sqlite3


class Review:
    dbpath = "data/stacked.db"


    def __init__(self, pk,review,company,time_stamp,pros,cons,users_pk ):
        self.pk = pk
        self.review = review
        self.company = company
        self.time_stamp = time_stamp
        self.pros = pros
        self.cons = cons
        self.users_pk=users_pk
        



    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO reviews(
                review,company,time_stamp,pros,cons,users_pk) 
                VALUES (?,?,?,?,?,?);"""

            values = (self.review,self.company,self.time_stamp,self.pros,self.cons,self.users_pk)
            cursor.execute(SQL, values)


    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()



    @classmethod
    def count_reviews(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT COUNT(review) FROM reviews WHERE company=?"""
            cursor.execute(SQL, (company,))
            row = cursor.fetchall()
            return row


    @classmethod
    def get_reviews(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT review,time_Stamp ,pros,cons FROM reviews WHERE company=?"""
            cursor.execute(SQL, (company,))
            row = cursor.fetchall()
            return row