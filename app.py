import streamlit as st
import pandas as pd
from datetime import datetime

# Load the Excel file (must be in the same repo or manually uploaded to Streamlit later)
@st.cache_data
def load_workout():
    try:
        df = pd.read_excel("3_Week_Wrestling_Strength_Program_Updated_June16.xlsx", sheet_name="Workout Plan")
        return df
    except Exception as e:
        st.error("Workout plan not found. Please upload the Excel file.")
        return pd.DataFrame()

df = load_workout()

# Get today's workout
today = datetime.today().strftime('%Y-%m-%d')
today_workout = df[df["Date"] == today]

if today_workout.empty:
    future = df[df["Date"] > today]
    today_workout = future.head(1)

if not today_workout.empty:
    row = today_workout.iloc[0]
    st.title("🏋️ Wrestling Workout of the Day")
    st.subheader(f"{row['Date']} – {row['Focus']}")
    for line in row["Workout Plan"].split("\n"):
        st.markdown(f"- {line}")
else:
    st.warning("No workout scheduled today.")

# Tracking form
st.subheader("📈 Track Your Workout")
with st.form("log_form"):
    reps = st.text_input("Reps")
    weight = st.text_input("Weight Used")
    rpe = st.slider("RPE (Effort)", 1, 10)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Save Log")

    if submitted:
        log = pd.DataFrame([{
            "Date": row.get("Date", today),
            "Focus": row.get("Focus", "N/A"),
            "Reps": reps,
            "Weight": weight,
            "RPE": rpe,
            "Notes": notes
        }])
        try:
            existing = pd.read_csv("logs.csv")
            updated = pd.concat([existing, log], ignore_index=True)
        except FileNotFoundError:
            updated = log
        updated.to_csv("logs.csv", index=False)
        st.success("Log saved!")

if st.checkbox("📋 Show Past Logs"):
    try:
        logs = pd.read_csv("logs.csv")
        st.dataframe(logs)
    except:
        st.info("No logs found.")
