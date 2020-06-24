import sqlite3
from .util import hash_pass, generate_key



class User:
    dbpath = "data/stacked.db"


    def __init__(self, pk, email, password,first_name,last_name,company,position,city,salary, api_key=''):
        self.pk = pk
        self.email = email
        self.password = hash_pass(password)
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.position = position
        self.city = city
        self.salary = salary
        self.api_key = api_key



    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO users(
                email, password_hash,first_name,last_name,company,position,city,salary,api_key) 
                VALUES (?,?,?,?,?,?,?,?,?);"""

            values = (self.email, self.password,self.first_name,self.last_name,self.company,self.position,self.city,self.salary,self.api_key)
            cursor.execute(SQL, values)

    def _update(self):
         with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE users SET years=?, salary =?
                    WHERE (pk=?);"""
            values = (self.years,self.salary,self.pk)
            cursor.execute(SQL, values)



    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()



    @classmethod
    def api_authenticate(cls, api_key):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM users WHERE api_key=?;"""
            cursor.execute(SQL, (api_key,))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7],row[8],row[9])
            return None


    @classmethod
    def all_for_account(cls,api_key):
       with sqlite3.connect(cls.dbpath) as conn:
           cursor = conn.cursor()
           SQL = """ SELECT company,position, salary,city FROM users WHERE api_key =?"""
           cursor.execute(SQL,(api_key,))
           data = cursor.fetchall()
           return data

    @classmethod
    def get_name(cls,api_key):
       with sqlite3.connect(cls.dbpath) as conn:
           cursor = conn.cursor()
           SQL = """ SELECT first_name FROM users WHERE api_key =?"""
           cursor.execute(SQL,(api_key,))
           data = cursor.fetchall()
           return data

    @classmethod
    def get_city(cls,api_key):
       with sqlite3.connect(cls.dbpath) as conn:
           cursor = conn.cursor()
           SQL = """ SELECT city FROM users WHERE api_key =?"""
           cursor.execute(SQL,(api_key,))
           data = cursor.fetchall()
           return data


    @classmethod
    def signin(cls, email, password):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM users WHERE email=? AND password_hash=?;"""
            cursor.execute(SQL, (email,hash_pass(password)))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7],row[8],row[9])
            return None

    @classmethod
    def get_company(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT position, salary, city FROM users WHERE company = ?;"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row

    @classmethod
    def get_search_data(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT position, salary, city,company FROM users WHERE company = ?;"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row

    @classmethod
    def get_avg_sal(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT AVG(salary) FROM users WHERE company = ?;"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row

    
    @classmethod
    def get_highest_pos(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT position, MAX(salary),company,city,COUNT( DISTINCT city) FROM users WHERE company = ?;"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row

    @classmethod
    def get_max_city(cls):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT position, AVG(salary) as avg_salary,city,salary FROM users GROUP BY city ORDER BY avg_salary desc LIMIT 1"""
            cursor.execute(SQL,)
            row = cursor.fetchall()
            return row

    @classmethod
    def top_five_cities(cls):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT AVG(salary) as avg_salary,city FROM users GROUP BY city ORDER BY avg_salary desc LIMIT 5"""
            cursor.execute(SQL,)
            row = cursor.fetchall()
            return row

    @classmethod
    def highest_paid_companies_in_your_city(cls,city):
         with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT AVG(salary) as avg_salary,company,COUNT(position),COUNT( DISTINCT city) FROM users WHERE city = ? GROUP BY company ORDER BY avg_salary desc LIMIT 5"""
            cursor.execute(SQL,(city,))
            row = cursor.fetchall()
            return row


    @classmethod
    def top_five_positions(cls):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT salary,position,city,company FROM users GROUP BY position ORDER BY salary desc LIMIT 5"""
            cursor.execute(SQL,)
            row = cursor.fetchall()
            return row

    @classmethod
    def positions(cls,company):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """ SELECT  position, salary, city,company FROM users WHERE company = ? LIMIT 5"""
            cursor.execute(SQL,(company,))
            row = cursor.fetchall()
            return row
