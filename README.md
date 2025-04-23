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
git clone https://github.com/yourusername/healthcare-billing-anomaly-detection.git
cd healthcare-billing-anomaly-detection
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
OPENAI_API_KEY=your_api_key
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
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
├── .env               # Environment variables
└── README.md          # Project documentation
```

## Contact

- Developer: Munashe Kambaza
- Email: kambazamunashe@gmail.com
- Phone: +263 78 708 1371

## License

This project is licensed under the MIT License - see the LICENSE file for details. 