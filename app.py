import sqlite3
import pandas as pd
import streamlit as st

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create the users table if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        age INTEGER
    )
""")
conn.commit()

# Title and description
st.title("User Information App")
st.write("This app allows you to submit a name and age, stores them in a SQLite database, and displays all entries.")

# Form for new user entry
st.header("Add a New User")
with st.form(key="user_form"):
    name = st.text_input("Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    submit_btn = st.form_submit_button(label="Submit")

# Handle form submission
if submit_btn:
    # Insert the new record into the database
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    st.success(f"Stored new entry: **{name} (Age {age})**")

# Display current entries in the database
st.subheader("Current Users in Database")
c.execute("SELECT name, age FROM users")
rows = c.fetchall()
if rows:
    df = pd.DataFrame(rows, columns=["Name", "Age"])
    st.table(df)
else:
    st.write("No entries yet.")