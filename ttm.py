import streamlit as st
import pandas as pd
import random

# Title and description of the project
st.title("AI TutorCommando")
st.subheader("Personalized AI-Driven Study Assistant for Army Public School Students")

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Create Study Plan", "Quiz Mode", "Performance Tracking"])

# Home Page
if selection == "Home":
    st.header("Welcome to AI TutorCommando!")
    st.write("This AI tool helps you with customized study plans, quizzes, and progress tracking.")
    st.write("Choose an option from the sidebar to get started.")
    
# Create Study Plan Page
elif selection == "Create Study Plan":
    st.header("Personalized Study Plan")
    st.write("Input your study goals, and let the AI help you craft a disciplined study schedule.")

    # Input fields for subjects and study hours
    subjects = st.text_input("Enter the subjects (separated by commas)", "Math, Science, History")
    study_hours = st.slider("How many hours per day can you study?", 1, 10, 3)

    if st.button("Generate Study Plan"):
        subject_list = [s.strip() for s in subjects.split(",")]
        study_plan = {}
        hours_per_subject = study_hours / len(subject_list)

        for subject in subject_list:
            study_plan[subject] = round(hours_per_subject, 2)

        st.write("Here is your personalized study plan:")
        st.write(pd.DataFrame(study_plan.items(), columns=["Subject", "Study Hours/Day"]))

# Quiz Mode Page
elif selection == "Quiz Mode":
    st.header("Quiz Mode: Test Your Knowledge!")
    
    # Sample questions for demonstration
    questions = {
        "Math": [
            {"question": "What is 5 + 3?", "options": [6, 8, 9], "answer": 8},
            {"question": "What is 12 / 4?", "options": [2, 3, 4], "answer": 3}
        ],
        "Science": [
            {"question": "What planet is closest to the Sun?", "options": ["Earth", "Mars", "Mercury"], "answer": "Mercury"},
            {"question": "What is H2O?", "options": ["Hydrogen", "Oxygen", "Water"], "answer": "Water"}
        ]
    }

    subject = st.selectbox("Select subject for quiz", ["Math", "Science"])
    
    selected_questions = random.sample(questions[subject], len(questions[subject]))

    for i, q in enumerate(selected_questions):
        st.write(f"Q{i+1}: {q['question']}")
        answer = st.radio(f"Select answer for Q{i+1}", q['options'], key=i)
        if st.button("Submit Answer", key=i):
            if answer == q['answer']:
                st.success("Correct!")
            else:
                st.error("Wrong answer. Try again!")

# Performance Tracking Page (placeholder for now)
elif selection == "Performance Tracking":
    st.header("Performance Tracking")
    st.write("Feature coming soon! You'll be able to track your progress here.")
