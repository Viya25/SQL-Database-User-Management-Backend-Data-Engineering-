import mysql.connector
from db import get_connection
from hashpass import hash_password, verify_password
import re

#username validation
def valid_username(username):
    return len(username) >= 5

#password Validation
def valid_password(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&]", password):
        return False
    return True

#Email Validation
def valid_email(email):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return re.fullmatch(pattern, email) is not None

#User Registration - Signup
def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from user where username=%s or email=%s",
    (username, email))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False     # duplicate found

    try:
        cursor.execute(
            "insert into user(username, email, password_hash) values (%s,%s,%s)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        cursor.close()
        conn.close()

#Authenticate User - Login
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from user where username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return "not_found"
    if not verify_password(password, user["password_hash"]):
        return "wrong password"
    return user

# Update User
def update_user(user_id, new_email, new_username, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("update user set email=%s ,username=%s, password_hash=%s where id=%s",
    (new_email, new_username, hash_password(new_password), user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Delete User
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("delete from user where id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

#Forget password
def rest_password(username, email, new_password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #verify username & email
    cursor.execute("select * from user where username=%s and email=%s",
    (username, email))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return False

    #update Password
    cursor.execute("update user set password_hash=%s where id=%s",
    (hash_password(new_password), user["id"]))
    conn.commit()
    cursor.close()
    conn.close()
    return True