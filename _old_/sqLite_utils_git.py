#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
from PIL import Image
import io

con = sqlite3.connect('pro_1_db.db')


def create_table():
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Pro_table(id INTEGER PRIMARY KEY, password TEXT)")


#        cur.execute("CREATE TABLE IF NOT EXISTS Pro_table(Password TEXT, Image BLOB)")

def drop_table():
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Pro_table")


def data_entry(data):
    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO Pro_table (Password) VALUES (?)", [data])


def data_querry():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pro_table WHERE password LIKE '%jelsz%'")
        #        cur.execute("SELECT * FROM Pro_table WHERE LENGTH(password)>=25 LIMIT 1000000")

        #        cur.execute("SELECT * FROM Pro_table WHERE Password=?", t)
        #        t = ('titkos',)

        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1])


#            Image.open(io.BytesIO(row[1])).resize((200, 300), Image.ANTIALIAS).show()
#            with open('kep2.jpg', 'wb') as img:
#                img.write(row[1])

def read_image():
    with open('kep.jpg', 'rb') as img:
        image = img.read()
        return image


def insert_image():
    with con:
        cur = con.cursor()
        data = read_image()
        binary = sqlite3.Binary(data)
        passw = 'audi'
        cur.execute('INSERT INTO Pro_table (Password, Image) VALUES (?, ?)', (passw, binary))


def data_entry_big():
    big_file = open('500.txt', 'rb')
    with con:
        cur = con.cursor()
        for i in big_file:
            t = i.decode('ascii', 'ignore').strip()
            cur.execute("INSERT INTO Pro_table (password) VALUES (?)", [t])
    big_file.close()


def delete_dup():
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pro_table WHERE id NOT IN (SELECT MAX(id) FROM Pro_table GROUP BY password)")


def delete_len():
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pro_table WHERE LENGTH(password)>=25")


def delete_like():
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pro_table WHERE password LIKE '%class=%'")

# remove passwords length>=25, LIKE '%href%' '%http//%' '%name=%' '%class=%'

# drop_table()
# create_table()
# data_entry_big()
# delete_dup() //create too big temp file
# delete_len()
# delete_like()
# data_querry()
