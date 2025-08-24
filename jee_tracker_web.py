import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# File to save data
DATA_FILE = "jee_scores.csv"

# Initialize or load data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Physics", "Chemistry", "Maths", "Total"])

# Title
st.title("📘 JEE Preparation Tracker")

# Sidebar navigation
menu = st.sidebar.radio("📌 Menu", [
    "Add Score", 
    "Summary", 
    "Progress Graphs", 
    "Subject Comparison", 
    "Weakness Finder", 
    "Daily/Weekly Progress", 
    "Goal Setting", 
    "Export Data"
])

# 1. Add Score
if menu == "Add Score":
    st.header("➕ Add New Test Score")
    date = st.date_input("Select Date", datetime.today())
    physics = st.number_input("Physics Marks", 0, 100)
    chemistry = st.number_input("Chemistry Marks", 0, 100)
    maths = st.number_input("Maths Marks", 0, 100)
    total = physics + chemistry + maths
    
    if st.button("Save Score"):
        new_row = {"Date": date, "Physics": physics, "Chemistry": chemistry, "Maths": maths, "Total": total}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Score saved successfully!")

# 2. Summary
elif menu == "Summary":
    st.header("📊 Performance Summary")
    if not df.empty:
        st.write(df)
        st.write("**Average Marks:**")
        st.write(df[["Physics", "Chemistry", "Maths", "Total"]].mean())
        st.write("**Best Scores:**")
        st.write(df[["Physics", "Chemistry", "Maths", "Total"]].max())
    else:
        st.warning("No data available yet.")

# 3. Progress Graphs
elif menu == "Progress Graphs":
    st.header("📈 Progress Over Time")
    if not df.empty:
        fig, ax = plt.subplots()
        df.plot(x="Date", y=["Physics", "Chemistry", "Maths", "Total"], marker='o', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No data available yet.")

# 4. Subject Comparison
elif menu == "Subject Comparison":
    st.header("⚖️ Subject-wise Comparison")
    if not df.empty:
        st.bar_chart(df[["Physics", "Chemistry", "Maths"]])
    else:
        st.warning("No data available yet.")

# 5. Weakness Finder
elif menu == "Weakness Finder":
    st.header("🕵️ Weakest Subject")
    if not df.empty:
        averages = df[["Physics", "Chemistry", "Maths"]].mean()
        weakest = averages.idxmin()
        st.write(f"📉 Your weakest subject is: **{weakest}**")
    else:
        st.warning("No data available yet.")

# 6. Daily/Weekly Progress
elif menu == "Daily/Weekly Progress":
    st.header("📆 Progress Trends")
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        weekly = df.resample("W").mean()
        st.line_chart(weekly[["Physics", "Chemistry", "Maths", "Total"]])
        df.reset_index(inplace=True)
    else:
        st.warning("No data available yet.")

# 7. Goal Setting
elif menu == "Goal Setting":
    st.header("🎯 Set and Track Your Goals")
    physics_goal = st.number_input("Physics Goal", 0, 100, 90)
    chemistry_goal = st.number_input("Chemistry Goal", 0, 100, 90)
    maths_goal = st.number_input("Maths Goal", 0, 100, 90)
    total_goal = physics_goal + chemistry_goal + maths_goal
    
    if not df.empty:
        latest = df.iloc[-1]
        st.write(f"📌 Latest Scores: Physics={latest['Physics']}, Chemistry={latest['Chemistry']}, Maths={latest['Maths']}, Total={latest['Total']}")
        st.write(f"🎯 Your Goal: Physics={physics_goal}, Chemistry={chemistry_goal}, Maths={maths_goal}, Total={total_goal}")
        
        if latest["Total"] >= total_goal:
            st.success("🏆 Goal Achieved! Keep it up!")
        else:
            st.info("🚀 Keep working towards your goal!")
    else:
        st.warning("Add at least one test to compare with your goal.")

# 8. Export Data
elif menu == "Export Data":
    st.header("📤 Export Your Data")
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", data=csv, file_name="jee_scores.csv", mime="text/csv")
    else:
        st.warning("No data available yet.")
