# Healthcare Billing Anomaly Detection System

A Streamlit-based application for detecting anomalies in healthcare billing data using machine learning algorithms.

## Features

- User authentication system (login/register)
- Data upload and preprocessing
- Anomaly detection using Isolation Forest algorithm
- Interactive visualizations
- Results export functionality
- Contact form for communication

## Technologies Used

- Python 3.8+
- Streamlit
- OpenAI API (Kluster AI)
- Pandas
- NumPy
- Scikit-learn
- Plotly

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LearnyN24/Healthcare-Billing-App.git
cd Healthcare-Billing-App
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. The application is ready to use! The API keys are already included in the `.env` file.

## Usage

1. Run the Streamlit app using either of these commands:
```bash
# Method 1
streamlit run app.py

# Method 2 (if Method 1 doesn't work)
python -m streamlit run app.py
```

2. Access the application through your web browser at `http://localhost:8501`

3. Register a new account or login with existing credentials

4. Upload your healthcare billing data in CSV format

5. Adjust model parameters in the sidebar if needed

6. View the analysis results and download the findings

## Project Structure

```
healthcare-billing-anomaly-detection/
├── app.py              # Main application file
├── auth.py             # Authentication module
├── contacts.py         # Contact information module
├── requirements.txt    # Python dependencies
├── .env               # Environment variables with API keys
└── README.md          # Project documentation
```

## Contact

- Developer: Munashe Kambaza
- Email: kambazamunashe@gmail.com
- Phone: +263 78 708 1371

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>© 2024 Healthcare Billing Anomaly Detection System. All Rights Reserved.</p>
  <p>Developed by Munashe Kambaza</p>
  <p>
    <a href="https://github.com/LearnyN24/Healthcare-Billing-App">GitHub Repository</a> |
    <a href="mailto:kambazamunashe@gmail.com">Contact Developer</a>
  </p>
</div> 