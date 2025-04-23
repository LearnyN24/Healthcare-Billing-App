import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sqlite3
from datetime import datetime
import plotly.express as px
import auth
import contacts

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with Kluster AI configuration
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

# Set page config
st.set_page_config(
    page_title="Healthcare Billing Anomaly Detection",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Authentication functions
def login_page():
    st.title("🏥 Healthcare Billing Anomaly Detection")
    
    # Create two columns for login and registration
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if auth.verify_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with col2:
        st.header("Register")
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            email = st.text_input("Email")
            register = st.form_submit_button("Register")
            
            if register:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif auth.user_exists(new_username):
                    st.error("Username already exists")
                else:
                    if auth.register_user(new_username, new_password, email):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Please try again.")

def main_app():
    # Create a container for the header with user info
    header_container = st.container()
    with header_container:
        # Create three columns: title, empty space, and user info
        title_col, _, user_col = st.columns([3, 1, 1])
        
        with title_col:
            st.title("🏥 Healthcare Billing Anomaly Detection")
        
        with user_col:
            # Display username with improved visibility
            st.markdown(
                f"""
                <div style="
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: right;
                    margin-top: 10px;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                ">
                    👤 {st.session_state.username}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Upload Data", "About", "How It Works", "Contacts"]
    )
    
    # Add logout button to sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    # Sidebar for model parameters
    with st.sidebar:
        st.header("Model Parameters")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.6, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 4000, 100)
        top_p = st.slider("Top P", 0.0, 1.0, 1.0, 0.1)
        
        st.header("Anomaly Detection Settings")
        contamination = st.slider("Contamination Rate", 0.01, 0.1, 0.05, 0.01)
        n_estimators = st.slider("Number of Trees", 100, 500, 200, 50)
    
    if page == "Upload Data":
        st.markdown("""
        Upload your healthcare billing data to detect potential anomalies and fraudulent patterns.
        """)
        
        # File uploader for data
        uploaded_file = st.file_uploader("Upload your billing data (CSV)", type=['csv'])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(data.head())
            
            if st.button("Run Anomaly Detection"):
                # Prepare data for anomaly detection
                scaler = StandardScaler()
                numeric_data = data.select_dtypes(include=[np.number])
                scaled_data = scaler.fit_transform(numeric_data)
                
                # Apply Isolation Forest
                iso_forest = IsolationForest(contamination=contamination, n_estimators=n_estimators, random_state=42)
                predictions = iso_forest.fit_predict(scaled_data)
                
                # Add predictions to dataframe
                data['anomaly_score'] = iso_forest.score_samples(scaled_data)
                data['is_anomaly'] = predictions == -1
                
                # Display results
                st.write("Anomaly Detection Results:")
                st.dataframe(data[['anomaly_score', 'is_anomaly']].head())
                
                # Plot histogram using plotly
                fig = px.histogram(data, x='anomaly_score', title='Anomaly Score Distribution')
                st.plotly_chart(fig)
                
                # Display suspicious records
                suspicious_records = data[data['is_anomaly']]
                st.write(f"Number of suspicious records: {len(suspicious_records)}")
                if len(suspicious_records) > 0:
                    st.dataframe(suspicious_records)
                    
                # Download option
                csv = data.to_csv(index=False)
                st.download_button(
                    label="Download Analysis Results",
                    data=csv,
                    file_name="anomaly_analysis_results.csv",
                    mime="text/csv"
                )
    
    elif page == "About":
        st.header("About This Application")
        st.markdown("""
        This application helps healthcare providers and insurers detect potential fraud or unusual billing patterns 
        in health insurance claims using advanced AI models. It provides a user-friendly interface for uploading 
        billing data and receiving detailed analysis of potential anomalies.
        
        ### Key Features:
        - Simple data upload interface
        - Advanced anomaly detection algorithms
        - Detailed analysis reports
        - Interactive visualization of results
        - Export capabilities for further investigation
        """)
    
    elif page == "How It Works":
        st.header("How It Works")
        
        steps = [
            {
                "title": "1. Data Loading and Preprocessing",
                "description": "Loads and preprocesses healthcare billing data - Cleans, normalizes, and transforms claim records for analysis (e.g., removing duplicates, formatting dates, encoding variables)."
            },
            {
                "title": "2. Feature Extraction",
                "description": "Extracts relevant features from each record (e.g., total billed amount, number of procedures, billing codes, frequency of visits)."
            },
            {
                "title": "3. Anomaly Detection",
                "description": "Applies anomaly detection algorithms - Algorithms like Isolation Forest identify records that significantly differ from normal billing behavior."
            },
            {
                "title": "4. Anomaly Scoring",
                "description": "Calculates anomaly scores for each record - Higher scores indicate a higher likelihood of fraud or unusual billing."
            },
            {
                "title": "5. Flagging Suspicious Records",
                "description": "Flags and stores suspicious records - Marks these for review and stores them in a structured format."
            },
            {
                "title": "6. Interactive Interface",
                "description": "Provides an interactive interface - Allows users to search, filter, and manually review flagged billing entries."
            },
            {
                "title": "7. Audit Support",
                "description": "Supports audits or investigation - Helps healthcare providers or insurers verify or investigate irregular billing activities."
            }
        ]
        
        for step in steps:
            with st.expander(step["title"]):
                st.write(step["description"])
    
    elif page == "Contacts":
        st.header("Contact Information")
        
        # Display developer contact information with improved visibility
        st.markdown(
            """
            <div style="
                background-color: #4CAF50;
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            ">
                <h3 style="color: white; font-size: 24px; margin-bottom: 15px;">Developer Contact</h3>
                <p style="font-size: 18px; margin-bottom: 10px;"><strong>Name:</strong> Munashe Kambaza</p>
                <p style="font-size: 18px; margin-bottom: 10px;"><strong>Phone:</strong> <a href="tel:+263787081371" style="color: white; text-decoration: underline;">+263 78 708 1371</a></p>
                <p style="font-size: 18px; margin-bottom: 10px;"><strong>Email:</strong> <a href="mailto:kambazamunashe@gmail.com" style="color: white; text-decoration: underline;">kambazamunashe@gmail.com</a></p>
                <p style="font-size: 18px; margin-bottom: 10px;"><strong>Role:</strong> Application Developer</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add a contact form
        st.subheader("Send a Message")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            submit = st.form_submit_button("Send Message")
            
            if submit:
                st.success("Thank you for your message! We will get back to you soon.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your healthcare billing data or question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    completion = client.chat.completions.create(
                        model="klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
                        max_completion_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    
                    response = completion.choices[0].message.content
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    # Add a clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main app logic
if not st.session_state.authenticated:
    login_page()
else:
    main_app()

# Add footer
st.markdown(
    """
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    ">
        © 2024 Healthcare Billing Anomaly Detection System. All Rights Reserved. | 
        <a href="mailto:kambazamunashe@gmail.com" style="color: white; text-decoration: underline;">Contact Developer</a>
    </div>
    """,
    unsafe_allow_html=True
) 