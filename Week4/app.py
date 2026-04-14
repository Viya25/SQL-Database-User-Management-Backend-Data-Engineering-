import streamlit as st
from hashpass import  hash_password, verify_password
from users import (valid_password, valid_username, valid_email, register_user, login_user, update_user, delete_user, rest_password)

#Streamlit UI Pages
st.set_page_config(page_title = "User Management System")
st.title("USER MANAGEMENT SYSTEM...!")

# session handling
if "user" not in st.session_state:
    st.session_state.user = None

if "menu" not in st.session_state:
    st.session_state.menu = "Login"


# MENU OPTIONS (FIXED)
if st.session_state.user is None:
    menu_options = ["Signup", "Login", "Forgot Password"]
else:
    menu_options = ["Welcome"]


# SAFE MENU SELECTION
menu = st.selectbox(
    "Menu",
    menu_options,
    index=menu_options.index(st.session_state.menu)
    if st.session_state.menu in menu_options else 0
)

st.session_state.menu = menu


#Signup Page
if menu == "Signup":
    st.subheader("Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Re-type Password", type="password")

    if st.button("Register"):
        if not valid_username(username):
            st.warning("Username must be at least 5 characters...!")
        elif not valid_email(email):
            st.warning("Please enter a valid email address...!")
        elif not valid_password(password):
            st.warning("Password must contain Uppercase, Lowercase, Digits & Special Character...!")
        elif password != confirm:
            st.warning("Password Do Not Match...!")
        elif register_user(username, email, password):
            st.success("Account Created Successfully...!")
            st.session_state.menu = "Login"
            st.rerun()
        else:
            st.error("Username or Email Already Exists...!")

elif menu == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user == "not_found":
            st.error("Username dose not Exist...!")
        elif user == "wrong_password":
            st.error("Incorrect Password")    
        else:
            st.session_state.user = user
            st.success("Logged in Successfully...!")
            st.session_state.menu = "Welcome"
            st.rerun()
            

elif menu == "Welcome":

    user = st.session_state.user
    if not user:
        st.session_state.menu = "Login"
        st.rerun()

    st.subheader(f"Welcome, {user['username']}")

    new_username = st.text_input("Update Username", user["username"])
    new_email = st.text_input("Update Email", user["email"])
    new_password = st.text_input("New Password", type="password")
       

    if st.button("Update Account"):
        if not valid_username(new_username):
            st.warning("Invalid username")
        elif not valid_email(new_email):
            st.warning("Invalid email")
        elif new_password and not valid_password(new_password):
            st.warning("Weak password")
        else:
            update_user(user["id"], new_username, new_email, new_password)
            st.success("Account updated. Please login again.")
            st.session_state.user = None
            st.session_state.menu = "Login"
            st.rerun()

    if st.button("Delete Account"):
        delete_user(user["id"])
        st.session_state.user = None
        st.session_state.menu = "Signup"
        st.success("Account Delete Successfully...!")
        st.rerun()


    st.markdown("---")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.menu = "Login"
        st.success("Logged out successfully!")
        st.rerun()

elif menu == "Forgot Password":
    st.subheader("Forgot Password")

    username = st.text_input("username")
    email = st.text_input("Registered Email")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Reset Password"):
        if not valid_email(email):
            st.warning("Invalid Email format..!")
        elif not valid_password(new_password):
            st.warning("Weak Password...!")
        elif new_password != confirm_password:
            st.warning("Password do not Match...!")
        elif rest_password(username, email, new_password):
            st.success("Password Reset Successfully..! Please Login...!")
        else:
            st.error("Username and Email do not match!")            