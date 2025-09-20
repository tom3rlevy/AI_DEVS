import streamlit as st
import sqlite3
import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def init_db():

    conn = sqlite3.connect("clients.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS clients(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          age INTEGER,
          legal_issue TEXT)          
    ''')

    sample_data = [
        ("Levi David", 42, "נדל\"ן"),
        ("Noa Cohen", 35, "משפחה"),
        ("Itamar Ben-Ari", 60, "צוואות וירושות"),
        ("Yael Mizrahi", 29, "חוזים"),
        ("Avi Dahan", 45, "פלילים"),
        ("Rina Azulay", 38, "משפחה"),
        ("Kadosh Daniel", 50, "צוואות וירושות"),
        ("Avrahami Lior", 33, "נדל\"ן"),
        ("Maya Segal", 41, "משפחה"),
        ("Eliad Shlomo", 28, "חוזים")
    ]

    c.execute("SELECT COUNT(*) FROM clients")
    count = c.fetchone()[0]

    if count == 0:
        c.executemany("INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)", sample_data) 

    conn.commit()
    conn.close()

def add_client(name, age, legal_issue):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()

    c.execute("INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)", (name, age, legal_issue))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect("clients.db")
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    conn.close()
    return df

def analyze_data(df):
    from openai import OpenAI
    client = OpenAI()

    prompt = f"""
    הנה טבלת נתונים של לקוחות במשרד עורכי דין
    {df.to_markdown()}

    תן לי ניתוח של:
    1. מהו הגיל הממוצע?
    2. אילו תחומים חוזרים יותר?
    3. האם קיימת נטייה לדפוס גיל לפי תחום משפטי
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    return response.output.text

# --- Chatbot on data ---
def chatbot_response(user_input,df):
    prompt = f"""
    ענה על השאלה הבאה בהתבסס על הנתונים של משרד עורכי הדין:
    {df.to_markdown()}

    שאלה: {user_input}
    """
    from openai import OpenAI
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    return response.output_text

init_db()
st.title("מערכת לייעוץ משפטי")
st.subheader("🧾 טופס הוספת לקוח חדש")
with st.form("new_client_form"):
    name = st.text_input("שם:")
    age = st.number_input("גיל:")
    legal_issue = st.selectbox("תחום משפטי:", [
        "משפחה",
        "נדלן",
        "חוזים",
        "פלילים",
        "צוואות וירושות",
    ])
    submitted = st.form_submit_button("שמור")
    

    if submitted:
        add_client(name, age, legal_issue)
        st.success("נשמר בהצלחה")

st.header("כל הפניות")
df = load_data()
st.dataframe(df)

