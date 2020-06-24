import sqlite3




class Job:
    dbpath = "data/stacked.db"


    def __init__(self, pk,department,level,years,happy,company,users_pk ):
        self.pk = pk
        self.department = department
        self.level = level
        self.years = years
        self.happy = happy
        self.company = company
        self.users_pk=users_pk
        



    def insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO jobs(
                department,level,years,happy,company,users_pk) 
                VALUES (?,?,?,?,?,?);"""

            values = (str(self.department),str(self.level),str(self.years),str(self.happy),self.company,self.users_pk)
            cursor.execute(SQL, values)


    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()




    @classmethod
    def job_happiness(cls, company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT AVG(happy) FROM jobs WHERE company=?;"""
            cursor.execute(SQL, (company,))
            row = cursor.fetchall()
            return row
            

    @classmethod
    def top_five_happy_companies(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT AVG(happy),company FROM jobs WHERE company=? GROUP BY company ORDER BY AVG(happy) desc LIMIT 5"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row

    @classmethod
    def get_dep_level(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT department,level FROM jobs WHERE company=?"""
            cursor.execute(SQL, (company,))
            row = cursor.fetchall()
            return row


    @classmethod
    def job_authenticate(cls,users_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM jobs WHERE users_pk=?;"""
            cursor.execute(SQL,(users_pk,))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4],row[5],row[6])
            return None
