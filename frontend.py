import streamlit as st
import requests

st.title("AI Recruitment System - Offline NLP")

menu = st.sidebar.selectbox("Menu",
        ["Upload Resume","Match with JD"])


# ========== UPLOAD ==========

if menu == "Upload Resume":

    file = st.file_uploader("Upload PDF/DOCX")

    if file and st.button("Submit"):

        res = requests.post(
            "http://localhost:8000/upload_resume",
            files={"file": file}
        )

        data = res.json()

        st.session_state["resume"] = data["resume"]

        st.success("Resume Loaded Successfully")


# ========== MATCH ==========

if menu == "Match with JD":

    if "resume" not in st.session_state:
        st.warning("First upload resume")
    else:
        st.text_area("Resume Text",
                     st.session_state["resume"],
                     height=200)

                # ----- JOB DESCRIPTION INPUT -----

        jd_text = st.text_area("Paste Job Description (Optional)")

        jd_file = st.file_uploader("Upload JD PDF (Optional)", key="jd")

        if jd_file:
            res = requests.post(
                "http://localhost:8000/upload_resume",
                files={"file": jd_file}
            )
            jd_text = res.json()["resume"]
            st.success("JD PDF Loaded")


        if st.button("Analyze"):

            res = requests.post(
                "http://localhost:8000/match",
                json={
                    "resume": st.session_state["resume"],
                    "jd": jd_text
                }
            )

            result = res.json()

                        # ===== CANDIDATE DETAILS =====
            st.subheader("Candidate Details")

            st.write("**Name:**", result["name"])
            st.write("**Email:**", result["email"])
            st.write("**Phone:**", result["phone"])

            # ===== ATS SCORE =====
            st.subheader("ATS Score")
            st.write(result["ATS_Score"])

            # ===== CLICKABLE EMAIL IF SCORE > 70 =====
            if result["ATS_Score"] >= 70 and result["email"] != "Not Found":

                mailto = f"mailto:{result['email']}?subject=Interview Shortlist&body=Congratulations, you have been shortlisted."

                st.markdown(
                    f'''
                    <a href="{mailto}" target="_blank">
                    <button style="
                        background:#28a745;
                        color:white;
                        padding:10px;
                        border:none;
                        border-radius:6px;
                        cursor:pointer;">
                        Email Candidate
                    </button>
                    </a>
                    ''',
                    unsafe_allow_html=True
                )

            # ===== SKILLS =====
            st.subheader("Matching Skills")
            st.write(result["matching_skills"])

            st.subheader("Missing Skills")
            st.write(result["missing_skills"])
