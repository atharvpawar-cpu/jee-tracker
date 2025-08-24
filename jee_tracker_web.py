import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if "scores" not in st.session_state:
    st.session_state.scores = {"Physics": [], "Chemistry": [], "Maths": []}

st.title("📘 JEE Prep Tracker")

# Input section
st.header("➕ Add Your Marks")
physics = st.number_input("Physics Marks (out of 60)", min_value=0, max_value=60, step=1)
chemistry = st.number_input("Chemistry Marks (out of 60)", min_value=0, max_value=60, step=1)
maths = st.number_input("Maths Marks (out of 60)", min_value=0, max_value=60, step=1)

if st.button("Add Score"):
    st.session_state.scores["Physics"].append(physics)
    st.session_state.scores["Chemistry"].append(chemistry)
    st.session_state.scores["Maths"].append(maths)
    st.success("✅ Marks added successfully!")

# Show summary
st.header("📊 Summary")
for subject, marks in st.session_state.scores.items():
    if marks:
        avg = sum(marks) / len(marks)
        st.write(f"**{subject}** → Tests: {len(marks)}, Avg: {avg:.2f}, Best: {max(marks)}")
    else:
        st.write(f"**{subject}** → No tests yet")

# Show progress graph
st.header("📈 Progress Graph")
for subject, marks in st.session_state.scores.items():
    if marks:
        plt.plot(range(1, len(marks)+1), marks, marker='o', label=subject)

plt.xlabel("Test Number")
plt.ylabel("Marks")
plt.title("JEE Prep Progress")
plt.legend()
st.pyplot(plt)
