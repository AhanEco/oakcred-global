# INFRASCOR - Alternative Credit Scoring Platform

An AI-powered alternative credit scoring and loan eligibility platform designed for India's unorganised and informal sector.

## Architecture

- **Frontend**: React (Vite) + Tailwind CSS + Recharts + Framer Motion
- **Backend**: FastAPI + Python 3.9
- **Machine Learning**: RandomForest / XGBoost ensemble trained with SMOTE targeting a synthetically generated dataset mapping alternative indicators (UPI, Utility, Telecom, Assets).
- **Interpretability**: SHAP (SHapley Additive exPlanations) for plain-language transparency in scoring.

## System Workflow

1. A user (Street vendor, small trader) fills out the 6-step wizard providing alternative data signals based on the Account Aggregator schema.
2. The UI posts the applicant schema to `/api/score`.
3. The FastAPI scoring engine evaluates the inputs using the serialized predictive model `infrascor_model.pkl` and a heuristic blending mapping to a 300-850 scale.
4. The React Result Dashboard visualises the score, estimates eligibility, and renders plain-language SHAP explanations ("What's Helping You" / "Areas to Build").

## How to Run

Requirements: Docker and docker-compose.

1. Clone or navigate to the source repository.
2. Build and launch the platform:
   ```bash
   docker-compose up --build
   ```
   *(Note: The build process automatically generates a master 500-profile synthetic dataset and trains/serializes the ML model prior to backend initialisation.)*

3. Access the web applications:
   - **Frontend UI**: http://localhost:3000
   - **Backend OpenAPI Sandbox**: http://localhost:8000/docs

## Demo Credentials (Mocked Authentication)
- Applicant: `applicant@demo.com / demo123`
- Bank Officer: `officer@demo.com / demo123`
- Admin: `admin@demo.com / demo123`
