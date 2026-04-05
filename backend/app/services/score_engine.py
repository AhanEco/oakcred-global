import joblib
import pandas as pd
import numpy as np
import os
import shap

# Load macro model artifacts
ARTIFACTS_PATH = os.path.join(os.path.dirname(__file__), '../../artifacts/macro_model.pkl')
try:
    artifacts = joblib.load(ARTIFACTS_PATH)
    model = artifacts['model']
    features = artifacts['features']
    explainer = artifacts['explainer']
    imputer = artifacts['imputer']
    data_snapshot = artifacts['data_snapshot'] # List of dicts for 2022
    print("Macro Stability Model loaded successfully.")
except Exception as e:
    print(f"Warning: Macro Model could not be loaded. {e}")
    model, features, explainer, imputer, data_snapshot = None, None, None, None, []

# Feature definitions for Macro SHAP plain language
MACRO_DESCRIPTIONS = {
    'inflation': ('Inflation Control', 'Low inflation preserves purchasing power', 'High inflation erodes currency value'),
    'external_debt_gni': ('Sovereign Debt Stress', 'Manageable debt levels relative to income', 'High external debt increases default risk'),
    'gdp_growth': ('Economic Vitality', 'Strong GDP growth signals a healthy economy', 'Low or negative growth indicates stagnation/recession'),
    'fdi_net_inflows_gdp': ('Capital Attraction', 'Net FDI inflows show global investor confidence', 'Low capital attraction limits growth potential'),
    'total_reserves': ('Reserve Coverage', 'Large reserves provide a buffer against external shocks', 'Low reserves increase vulnerability to balance of payment crises'),
    'current_account_gdp': ('Trade Balance', 'Strong current account position', 'Current account deficit may require external financing')
}

def get_macro_description(feature, value, is_positive):
    desc = MACRO_DESCRIPTIONS.get(feature)
    if not desc:
        clean_name = feature.replace('_', ' ').title()
        return (clean_name, f"Optimal {clean_name} levels", f"Sub-optimal {clean_name} levels")
    
    name = desc[0]
    reason = desc[1] if is_positive else desc[2]
    return (name, reason)

def process_economy(economy_data: dict):
    # Prep data
    df_input = pd.DataFrame([economy_data])
    
    # Select only required features
    df_eval = df_input[features]
    
    # Handle missing values using the saved imputer
    df_eval_imputed = pd.DataFrame(imputer.transform(df_eval), columns=features)
    
    # 1. Model Prediction (0 to 1)
    stability_raw = model.predict(df_eval_imputed)[0]
    
    # 2. Scale to 300-850 (Standard Risk Score range)
    final_score = int(300 + (stability_raw * 550))
    final_score = max(300, min(850, final_score))
    
    # 3. Resilience Band
    if final_score >= 750: band = "ROBUST"
    elif final_score >= 650: band = "RESILIENT"
    elif final_score >= 550: band = "VULNERABLE"
    elif final_score >= 450: band = "FRAGILE"
    else: band = "STRESSED"
    
    # 4. SHAP Interpretability
    shap_values = explainer(df_eval_imputed)
    sv = shap_values.values[0]
    
    contributions = []
    for i, name in enumerate(features):
        contributions.append({"feature": name, "shap": float(sv[i]), "value": df_eval_imputed.iloc[0, i]})
        
    contributions.sort(key=lambda x: x["shap"], reverse=True)
    
    top_positive = []
    for c in contributions:
        if c["shap"] > 0 and len(top_positive) < 4:
            pts = int(c["shap"] * 100) # Heuristic scaling
            name, reason = get_macro_description(c["feature"], c["value"], True)
            top_positive.append({
                "factor_name": name,
                "reason": reason,
                "score_impact": f"+{pts} pts"
            })
            
    top_negative = []
    for c in contributions[::-1]:
        if c["shap"] < 0 and len(top_negative) < 4:
            pts = int(abs(c["shap"]) * 100)
            name, reason = get_macro_description(c["feature"], c["value"], False)
            top_negative.append({
                "factor_name": name,
                "reason": reason,
                "score_impact": f"-{pts} pts"
            })
            
    # 5. Radar/Sub-Metrics (Normalized 0-100)
    # Mapping our 6 features to the radar categories
    radar_data = [
        {"category": "Stability", "value": int(stability_raw * 100)},
        {"category": "Debt/GNI", "value": max(0, min(100, 100 - economy_data.get('external_debt_gni', 0)))},
        {"category": "Inflation", "value": max(0, min(100, 100 - economy_data.get('inflation', 0)))},
        {"category": "Growth", "value": max(0, min(100, (economy_data.get('gdp_growth', 0) + 10) * 5))}, # -10 to 10 range
        {"category": "Reserves", "value": 100 if economy_data.get('total_reserves', 0) > 1e11 else 50},
        {"category": "Capital Flow", "value": max(0, min(100, (economy_data.get('fdi_net_inflows_gdp', 0) + 5) * 10))}
    ]
    
    return {
        "score": final_score,
        "band": band,
        "metrics": economy_data,
        "radar_data": radar_data,
        "shap": {
            "positive": top_positive,
            "negative": top_negative
        }
    }

def get_demo_economies():
    # Return available ISO codes from mapping
    return [d['economy'] for d in data_snapshot]

def get_economy_data(iso_code):
    for d in data_snapshot:
        if d['economy'] == iso_code:
            return d
    return None
