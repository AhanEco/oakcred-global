import pandas as pd
import numpy as np
from faker import Faker
from pydantic import BaseModel
import random
import os

fake = Faker('en_IN')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Indian states and occupations for the demo
STATES = ['Uttar Pradesh', 'Maharashtra', 'Tamil Nadu', 'West Bengal', 'Rajasthan']
OCCUPATIONS = [
    'Street Vendor', 'Artisan', 'Daily Wage Worker', 'Farmer', 
    'Domestic Worker', 'Small Trader', 'Transport Worker', 
    'Construction Worker', 'Tailor', 'Food Stall Owner'
]
APPLICANT_TYPES = ['Individual', 'Proprietorship', 'Partnership']

class ApplicantSchema(BaseModel):
    # Base Profile
    applicant_id: str
    name: str
    mobile: str
    state: str
    district: str
    occupation: str
    years_in_occupation: int
    applicant_type: str
    monthly_income_estimate: float
    income_seasonality: str # Stable, Seasonal, Irregular

    # 1. UPI Data
    upi_transactions_per_month: int
    upi_avg_ticket_size: float
    upi_merchant_diversity: int
    upi_consistency_score: float # 0 to 1
    upi_inflow_outflow_ratio: float
    
    # 2. Utility Payment
    utility_electric_on_time_pct: float # 0 to 100
    utility_water_streak_months: int
    utility_mobile_recharge_amt: int
    
    # 3. Jan Dhan / Bank
    bank_avg_monthly_balance: float
    bank_income_credit_regularity: float # 0 to 1 scale
    bank_zero_balance_months_past_12: int
    
    # 4. MGNREGA / Government Scheme
    mgnrega_days_worked: int
    mgnrega_wage_regularity: float # 0 to 1
    
    # 5. Mobile Usage
    mobile_sim_age_months: int
    mobile_sim_changes_2yr: int
    mobile_data_usage_trend: float # slope, positive = increasing
    
    # 6. Supply Chain / Trade
    trade_regular_suppliers: int
    trade_regular_customers: int
    trade_monthly_purchase_value: float
    trade_tenure_years: int
    
    # 7. Asset & Geospatial
    asset_ownership_status: str # Own House, Rented, Family
    asset_years_at_address: int
    asset_vehicle: str # None, Two-Wheeler, Auto, Goods Vehicle
    
    # 8. Social Capital
    social_shg_member: int # 1 = Yes, 0 = No
    social_shg_tenure_years: int
    social_mfi_repaid_count: int
    
    # Target Variable
    repayment_probability: int # 1 = Repaid, 0 = Defaulted (target for ML)

def generate_synthetic_profile(profile_type="repaid"):
    """
    profile_type: 'repaid' or 'defaulted'
    """
    
    # Adjust distribution parameters based on target to create valid signals for the model
    if profile_type == "repaid":
        # Better profile
        years_occ = max(1, int(np.random.normal(5, 2)))
        income = np.random.uniform(15000, 50000)
        upi_tx = int(np.random.normal(45, 15))
        upi_ticket = np.random.uniform(500, 3000)
        upi_cons = min(1.0, max(0.4, np.random.normal(0.8, 0.15)))
        util_on_time = min(100, max(50, np.random.normal(90, 10)))
        bank_balance = np.random.uniform(1000, 15000)
        bank_zero = max(0, int(np.random.normal(1, 1)))
        shg_prob = 0.6
        mfi_repaid = max(0, int(np.random.normal(1, 1)))
        sim_age = int(np.random.normal(36, 12))
        sim_changes = max(0, int(np.random.normal(0.5, 0.6)))
    else:
        # Defaulted profile (weaker signals)
        years_occ = max(1, int(np.random.normal(2, 1.5)))
        income = np.random.uniform(5000, 25000)
        upi_tx = max(0, int(np.random.normal(10, 8)))
        upi_ticket = np.random.uniform(100, 1000)
        upi_cons = min(1.0, max(0.1, np.random.normal(0.4, 0.2)))
        util_on_time = min(100, max(0, np.random.normal(50, 25)))
        bank_balance = np.random.uniform(0, 3000)
        bank_zero = min(12, max(2, int(np.random.normal(5, 2))))
        shg_prob = 0.2
        mfi_repaid = 0
        sim_age = max(1, int(np.random.normal(12, 6)))
        sim_changes = max(0, int(np.random.normal(2, 1)))

    state = random.choice(STATES)
    occ = random.choice(OCCUPATIONS)
    is_shg = 1 if random.random() < shg_prob else 0

    return ApplicantSchema(
        applicant_id=fake.uuid4()[:8],
        name=fake.name(),
        mobile=fake.phone_number(),
        state=state,
        district=fake.city(),
        occupation=occ,
        years_in_occupation=years_occ,
        applicant_type=random.choice(APPLICANT_TYPES),
        monthly_income_estimate=round(income, 2),
        income_seasonality=random.choices(['Stable', 'Seasonal', 'Irregular'], weights=[0.5, 0.3, 0.2])[0],
        upi_transactions_per_month=max(0, upi_tx),
        upi_avg_ticket_size=round(max(50, upi_ticket), 2),
        upi_merchant_diversity=max(1, int(upi_tx * 0.3)),
        upi_consistency_score=round(upi_cons, 2),
        upi_inflow_outflow_ratio=round(np.random.uniform(0.8, 1.5), 2),
        utility_electric_on_time_pct=round(util_on_time, 2),
        utility_water_streak_months=max(0, int(util_on_time / 10)),
        utility_mobile_recharge_amt=int(np.random.choice([199, 299, 499, 699])),
        bank_avg_monthly_balance=round(bank_balance, 2),
        bank_income_credit_regularity=round(min(1.0, upi_cons + np.random.uniform(-0.1, 0.1)), 2),
        bank_zero_balance_months_past_12=bank_zero,
        mgnrega_days_worked=int(np.random.choice([0, 0, 30, 50, 100])),
        mgnrega_wage_regularity=round(np.random.uniform(0.3, 0.9), 2),
        mobile_sim_age_months=max(1, sim_age),
        mobile_sim_changes_2yr=sim_changes,
        mobile_data_usage_trend=round(np.random.uniform(-0.2, 0.8), 2),
        trade_regular_suppliers=max(0, int(years_occ * np.random.uniform(0, 3))),
        trade_regular_customers=max(0, int(years_occ * np.random.uniform(5, 20))),
        trade_monthly_purchase_value=round(income * np.random.uniform(0.4, 0.8), 2),
        trade_tenure_years=years_occ,
        asset_ownership_status=random.choices(['Own House', 'Rented', 'Family'], weights=[0.4, 0.4, 0.2])[0],
        asset_years_at_address=max(1, int(np.random.normal(years_occ + 2, 3))),
        asset_vehicle=random.choices(['None', 'Two-Wheeler', 'Auto', 'Goods Vehicle'], weights=[0.5, 0.4, 0.05, 0.05])[0],
        social_shg_member=is_shg,
        social_shg_tenure_years=max(1, int(np.random.normal(3, 1))) if is_shg else 0,
        social_mfi_repaid_count=mfi_repaid,
        repayment_probability=1 if profile_type == "repaid" else 0
    )

def generate_dataset(n=500):
    profiles = []
    # 90% repaid, 10% default
    n_repaid = int(n * 0.9)
    n_default = n - n_repaid
    
    for _ in range(n_repaid):
        profiles.append(generate_synthetic_profile("repaid"))
        
    for _ in range(n_default):
        profiles.append(generate_synthetic_profile("defaulted"))
        
    random.shuffle(profiles)
    
    df = pd.DataFrame([p.dict() for p in profiles])
    return df

if __name__ == "__main__":
    print("Generating INFRASCOR Synthetic Dataset...")
    df = generate_dataset(500)
    
    # Save to ML directory and DATA directory
    os.makedirs('data', exist_ok=True)
    out_path = 'data/synthetic_applicants.csv'
    df.to_csv(out_path, index=False)
    print(f"Successfully generated {len(df)} records and saved to {out_path}")
    print(df['repayment_probability'].value_counts())
