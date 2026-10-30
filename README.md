# VPN Detector ML

### Machine Learning-Based VPN and Proxy Detection System

## Project Overview

VPN Detector ML is a Python-based application designed to identify VPN and proxy usage using machine learning and rule-based risk analysis.

The system analyses IP-related information, network latency, request frequency and location changes to identify potentially suspicious activity and classify requests into different risk levels.

## Key Features

- VPN and proxy detection
- IP address analysis
- Geographical location tracking
- Network latency monitoring
- Request frequency monitoring
- Location change detection
- Random Forest machine learning prediction
- Dynamic risk scoring
- Flask-based web application
- Admin dashboard with activity logs

## Technologies Used

- Python
- Flask
- Machine Learning
- Random Forest
- Scikit-learn
- NumPy
- Pandas
- Joblib
- Requests
- HTML

## System Workflow

1. User accesses the web application.
2. The application identifies the user's IP address.
3. VPN and proxy information is collected.
4. Location and network latency are analysed.
5. User activity features are extracted.
6. The trained Random Forest model generates a prediction.
7. A rule-based engine calculates the risk score.
8. The system displays the risk classification.
9. Admin can monitor activity through the log dashboard.

## Machine Learning Model

The project uses a trained Random Forest classifier to analyse network and behavioural features.

The model is loaded using Joblib and integrated into the Flask application for prediction.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/VPN-Detector-ML.git
```

### 2. Navigate to the project

```bash
cd VPN-Detector-ML
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set the following variables:

- FLASK_SECRET_KEY
- VPNAPI_KEY
- IPINFO_TOKEN

Do not hardcode API credentials in the source code.

### 5. Run the application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Future Enhancements

- Improved user authentication
- Database integration
- Advanced anomaly detection
- Enhanced dashboard visualisation
- Cloud deployment
- Improved model evaluation using real-world labelled datasets

## Author

Ahana Dinesh N

Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning

## Acknowledgement

This project was developed with reference to an open-source VPN detection project and subsequently extended with additional machine learning integration, risk analysis and monitoring functionality.

Original project copyright: Copyright (c) 2024 mo6in

Original licence: MIT License
