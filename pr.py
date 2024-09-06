import streamlit as st
import pandas as pd
import sqlite3
from PIL import Image
import base64
import streamlit.components.v1 as components

# Load the datasets
suspects = pd.read_csv('suspects_dataset.csv')
crime_scenes = pd.read_csv('crime_scene_dataset.csv')
evidence = pd.read_csv('evidence_dataset.csv')

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create tables with primary and foreign keys
cursor.execute('''CREATE TABLE suspects (DR_NO TEXT PRIMARY KEY, DATE_OCC TEXT, TIME_OCC TEXT, AREA_NAME TEXT, Crm_Cd_Desc TEXT, Status_Desc TEXT)''')
cursor.execute('''CREATE TABLE crime_scenes (DR_NO TEXT PRIMARY KEY, DATE_OCC TEXT, TIME_OCC TEXT, AREA_NAME TEXT, Crm_Cd_Desc TEXT, LOCATION TEXT, LAT REAL, LON REAL, FOREIGN KEY(DR_NO) REFERENCES suspects(DR_NO))''')
cursor.execute('''CREATE TABLE evidence (DR_NO TEXT PRIMARY KEY, DATE_OCC TEXT, TIME_OCC TEXT, AREA_NAME TEXT, Crm_Cd_Desc TEXT, FOREIGN KEY(DR_NO) REFERENCES suspects(DR_NO))''')

# Insert data into tables
suspects.columns = [col.replace(' ', '_') for col in suspects.columns]
crime_scenes.columns = [col.replace(' ', '_') for col in crime_scenes.columns]
evidence.columns = [col.replace(' ', '_') for col in evidence.columns]
suspects.to_sql('suspects', conn, index=False, if_exists='append')
crime_scenes.to_sql('crime_scenes', conn, index=False, if_exists='append')
evidence.to_sql('evidence', conn, index=False, if_exists='append')

# Function to add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Function to inject custom JavaScript
def inject_custom_js():
    js_code = """
    <script>
    function fixQueryBox(id) {
        const allBoxes = document.querySelectorAll('.query-box-container');
        allBoxes.forEach(box => box.classList.remove('fixed'));
        
        const boxToFix = document.getElementById(id);
        if (boxToFix) {
            boxToFix.classList.add('fixed');
        }
    }

    // Intersection Observer to detect when a query box is in view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                fixQueryBox(entry.target.id);
            }
        });
    }, { threshold: 0.5 });

    // Observe all query boxes
    document.querySelectorAll('.query-box-container').forEach(box => {
        observer.observe(box);
    });
    </script>
    """
    components.html(js_code, height=0)

# Streamlit app configuration
st.set_page_config(page_title="Murder Mystery Game", page_icon="🔍", layout="wide")

# Add background image
add_bg_from_local('crime.jpg')

# Add custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
    color: #f8f8ff;
}

.title-text {
    font-size: 60px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.7);
    background: rgba(0, 0, 0, 0.5);
    padding: 25px 45px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
    border: 3px solid #ff6f61;
}

.section-title {
    color: #1c1c1c;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.6);
    margin-top: 20px;
    padding: 15px 25px;
    background: #f8f8ff;
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    margin-bottom: 20px;
}

.query-title {
    color: #f8f8ff;
    font-size: 24px;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 10px;
    padding: 10px;
    background: #1c3d5a;
    border-radius: 10px;
    text-align: center;
}

.stTextArea > div > textarea {
    color: #000000;
    font-size: 16px;
}

.stButton > button {
    background-color: #34495e;
    color: white;
    border-radius: 8px;
    padding: 12px 25px;
    border: none;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    transition: background-color 0.3s, transform 0.2s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    margin-top: 10px;
}

.stButton > button:hover {
    background-color: #2c3e50;
    transform: scale(1.05);
}

.toggle-button {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.tip-text {
    font-size: 18px;
    color: #f8f8ff;
    background-color: #2a52be;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    margin-top: 10px;
}

.tip-text::before {
    content: '💡';
    margin-right: 8px;
}

.stAlert {
    background-color: #ff4b4b;
    color: white;
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
}

.query-box-container {
    transition: all 0.3s ease;
}

.query-box-container.fixed {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.9);
    padding: 20px;
    box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.query-box-container.fixed .query-title {
    margin-top: 0;
}

.query-box-container.fixed textarea {
    height: 100px !important;
}

.query-box-container.fixed button {
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<h1 class='title-text'>
    <span style="font-size: 70px; text-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);">
        🔍 MURDER MYSTERY
    </span>
    <br>
    <span style="font-size: 30px; font-weight: 400; color: #ffffff; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);">
        Solve the Crime, Unravel the Truth
    </span>
</h1>
""", unsafe_allow_html=True)

# Toggle Schema button
if 'show_schema' not in st.session_state:
    st.session_state.show_schema = False

if st.button("Toggle Schema", key="schema_toggle"):
    st.session_state.show_schema = not st.session_state.show_schema

# Align button under title
st.markdown("<div class='toggle-button'>", unsafe_allow_html=True)
if st.session_state.show_schema:
    schema_image = Image.open('image.png')
    schema_image = schema_image.resize((800, 600))  # Adjust size as needed
    st.image(schema_image, caption='Schema Image', use_column_width=False)
st.markdown("</div>", unsafe_allow_html=True)

# Tips Section with improved visibility
if 'show_tips' not in st.session_state:
    st.session_state.show_tips = False

if st.button("Show/Hide Tips", key="tips_toggle"):
    st.session_state.show_tips = not st.session_state.show_tips

if st.session_state.show_tips:
    st.markdown("<h2 class='section-title'>Tips for Solving the Mystery</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='tip-text'>1. Read the Introduction: Familiarize yourself with the purpose of the game and how to use the app.</div>
    <div class='tip-text'>2. Explore the Suspects Table: Look for all available information about the suspects.</div>
    <div class='tip-text'>3. Investigate Crime Scenes: Examine the details of crime scenes to find potential clues.</div>
    <div class='tip-text'>4. Analyze the Evidence: Study the evidence collected to find connections to suspects or crime scenes.</div>
    <div class='tip-text'>5. Cross-Reference Information: Compare information between tables to find inconsistencies or links.</div>
    <div class='tip-text'>6. Look for Patterns: Identify any patterns or anomalies in the data.</div>
    <div class='tip-text'>7. Form Hypotheses: Based on the data, propose possible scenarios or explanations.</div>
    <div class='tip-text'>8. Test Your Hypotheses: Use the data to test your hypotheses and look for supporting evidence.</div>
    <div class='tip-text'>9. Draw Conclusions: Based on your analysis, identify the most likely culprit and justify your conclusion.</div>
    """, unsafe_allow_html=True)

# Run query blocks with updated titles
for i in range(1, 7):
    st.markdown(f"""
    <div id="query-box-{i}" class="query-box-container">
        <div class='query-title'>Run Query Box {i}</div>
    </div>
    """, unsafe_allow_html=True)
    
    query = st.text_area("", height=150, key=f"query_{i}")
    if st.button(f"Run Query {i}", key=f"run_query_{i}"):
        if query:
            try:
                result = pd.read_sql_query(query, conn)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error: {e}")

# Inject custom JavaScript at the end
inject_custom_js()

# Close database connection
conn.close()