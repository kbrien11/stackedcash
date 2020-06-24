import sqlite3

class Booking:

    dbpath = "data/stacked.db"

    def __init__(self,pk,first_name,date_stamp,time_stamp,full_date,users_pk):
        self.pk = pk
        self.first_name = first_name
        self.date_stamp = date_stamp
        self.time_stamp = time_stamp
        self.full_date = full_date
        self.users_pk = users_pk


    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO bookings(first_name,date_stamp,time_stamp,full_date,users_pk)
                     VALUES(?,?,?,?,?); """
            
            values=(str(self.first_name),self.date_stamp,str(self.time_stamp),self.full_date,self.users_pk)
            cursor.execute(SQL, values)


    def update(self):
         with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE bookings SET date_stamp =?, time_stamp =?, full_date =?
                    WHERE (pk=?);"""
            values = (self.date_stamp,self.time_stamp,self.full_date,self.pk)
            cursor.execute(SQL, values)

    
    def save(self):
        if self.pk:
            self.update()
        else:
            self._insert()



    @classmethod
    def get_booking(cls,users_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT first_name,date_stamp,time_stamp,pk FROM bookings WHERE users_pk=?"""
            cursor.execute(SQL, (users_pk,))
            row = cursor.fetchall()
            if row:
                return row
            return 0

    @classmethod
    def all_bookings(cls):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT full_date  FROM bookings"""
            cursor.execute(SQL,)
            row = cursor.fetchall()
            return row
            
    @classmethod
    def all_bookings_pk(cls,pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT *  FROM bookings WHERE pk=?"""
            values =(pk,)
            cursor.execute(SQL,values)
            data = cursor.fetchone()
            if data:
                return cls(data[0],data[1],data[2],data[3],data[4],data[5])

    @classmethod
    def remove_booking(cls,pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            sql = """DELETE FROM bookings WHERE pk =?;"""
            cursor.execute(sql,(pk,))
            data = cursor.fetchone()
            return data  