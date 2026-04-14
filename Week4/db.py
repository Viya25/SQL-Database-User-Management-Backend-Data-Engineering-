import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "user_sys",
        charset = "utf8"    #utf8 support by all mysql version
    )