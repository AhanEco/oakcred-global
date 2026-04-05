import pandas as pd
import numpy as np
import shap
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def train_macro_model():
    print("Loading Real Macro Data...")
    df = pd.read_csv('data/macro_data.csv')
    
    # Feature list
    features = [
        'inflation', 
        'external_debt_gni', 
        'gdp_growth', 
        'fdi_net_inflows_gdp', 
        'total_reserves', 
        'current_account_gdp'
    ]
    
    # Preprocessing: Impute missing values with mean
    imputer = SimpleImputer(strategy='mean')
    df[features] = imputer.fit_transform(df[features])
    
    # Target engineering: "Stability Score"
    # This is a proxy target since we don't have labeled 'crisis' events here
    # 0 to 1: High score means highly stable, low score means vulnerable
    # Weights for a simple heuristic target to teach the model relations:
    # - Negative for Inflation and Debt
    # - Positive for Growth, Reserves, FDI, Current Account
    
    # Normalize features for target calculation
    norm_df = (df[features] - df[features].mean()) / df[features].std()
    
    stability_target = (
        0.2 * norm_df['gdp_growth'] -
        0.2 * norm_df['inflation'] -
        0.2 * norm_df['external_debt_gni'] +
        0.2 * norm_df['total_reserves'] +
        0.1 * norm_df['fdi_net_inflows_gdp'] +
        0.1 * norm_df['current_account_gdp']
    )
    
    # Scale to 0-1 range
    stability_target = (stability_target - stability_target.min()) / (stability_target.max() - stability_target.min())
    
    # Train Model
    print("Training Macro Stability Model (Random Forest)...")
    X = df[features]
    y = stability_target
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Explainability (SHAP)
    explainer = shap.Explainer(model, X)
    
    # Save Artifacts
    os.makedirs('backend/artifacts', exist_ok=True)
    joblib.dump({
        'model': model,
        'features': features,
        'explainer': explainer,
        'imputer': imputer,
        'data_snapshot': df[df['year'] == 2022].to_dict('records') # Latest full year for demo
    }, 'backend/artifacts/macro_model.pkl')
    
    print("Model and Explainer Serialized to backend/artifacts/macro_model.pkl")

if __name__ == "__main__":
    train_macro_model()
