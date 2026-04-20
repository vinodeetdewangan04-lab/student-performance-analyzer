import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

st.markdown("### Upload your dataset")
file = st.file_uploader("", type=["csv"])

if file:
    df = pd.read_csv(file)

    # ---------------- DATA PROCESSING ----------------
    df['Total'] = df[['Maths','Physics','Chemistry']].sum(axis=1)
    df['Average'] = df['Total'] / 3
    df['Rank'] = df['Total'].rank(ascending=False)

    def performance(avg):
        if avg >= 85: return "Excellent"
        elif avg >= 70: return "Good"
        elif avg >= 50: return "Average"
        else: return "Poor"

    df['Performance'] = df['Average'].apply(performance)

    # ---------------- IMPROVEMENT SUGGESTIONS ----------------
    def suggestion(row):
        if row['Average'] < 60:
            return "Increase study hours + revise basics"
        elif row['Attendance'] < 75:
            return "Improve attendance"
        else:
            return "Keep consistent"

    df['Suggestion'] = df.apply(suggestion, axis=1)

    # ---------------- PREDICTION (SIMPLE) ----------------
    # linear approximation
    slope = df['StudyHours'].corr(df['Average']) * (df['Average'].std() / df['StudyHours'].std())

    def predict(row):
        return row['Average'] + slope * 1  # +1 hour

    df['Predicted Avg (+1hr study)'] = df.apply(predict, axis=1)

    # ---------------- SIDEBAR ----------------
    st.sidebar.header("Filters")
    min_avg = st.sidebar.slider("Minimum Average", 0, 100, 50)
    df_filtered = df[df['Average'] >= min_avg]

    # ---------------- DASHBOARD ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", len(df))
    col2.metric("Average Score", round(df['Average'].mean(),2))
    col3.metric("Top Score", df['Average'].max())

    st.divider()

    # ---------------- TABLE ----------------
    st.subheader("📊 Data Overview")
    st.dataframe(df_filtered)

    # ---------------- CHARTS ----------------
    st.subheader("📈 Marks Visualization")

    fig, ax = plt.subplots()
    ax.bar(df['Name'], df['Average'])
    ax.set_title("Average Marks per Student")
    ax.set_xlabel("Students")
    ax.set_ylabel("Marks")
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # ---------------- INSIGHTS ----------------
    st.subheader("📌 Insights")

    corr = df['StudyHours'].corr(df['Average'])

    st.write(f"📊 Correlation between study hours & marks: **{corr:.2f}**")

    if corr > 0.5:
        st.success("Strong positive relationship 🚀")
    elif corr > 0:
        st.info("Moderate relationship")
    else:
        st.warning("Weak relationship")

    # ---------------- TOP STUDENTS ----------------
    st.subheader("🏆 Top Students")
    st.dataframe(df.sort_values(by="Total", ascending=False).head(3))

    # ---------------- AT RISK ----------------
    st.subheader("⚠️ At Risk Students")
    at_risk = df[(df['Attendance'] < 75) & (df['Average'] < 60)]
    st.dataframe(at_risk)

    # ---------------- DOWNLOAD ----------------
    st.download_button(
        "⬇️ Download Data",
        df.to_csv(index=False),
        "final_data.csv"
    )

else:
    st.info("Upload a CSV file to begin.")