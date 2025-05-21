import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="Stacked Model", page_icon="📚")
st.title("📚 Klasik Supervised Stack Model ile Kredi Skoru Tahmini")

st.write("Bu model, denetimli öğrenme ve stacking yöntemiyle optimize edilmiştir. Aşağıdaki formu doldurarak kredi skoru tahmini alabilirsiniz.")

# === Kullanıcı Girdileri ===
age = st.slider("Yaş", 18, 85, 30)
annual_income = st.number_input("Yıllık Gelir (₺)", min_value=0.0, value=50000.0)
monthly_salary = st.number_input("Aylık Maaş", min_value=0.0, value=4000.0)
num_accounts = st.slider("Banka Hesap Sayısı", 0, 10, 2)
num_credit_cards = st.slider("Kredi Kartı Sayısı", 0, 10, 2)
interest_rate = st.slider("Kredi Faiz Oranı (%)", 0.0, 50.0, 10.0)
num_loans = st.slider("Kredi Sayısı", 0, 10, 1)
delay_from_due = st.slider("Vade Gecikme Süresi (gün)", 0, 60, 5)
num_delayed_payments = st.slider("Gecikmiş Ödeme Sayısı", 0, 20, 2)
changed_credit_limit = st.slider("Kredi Limit Değişimi (%)", -100.0, 100.0, 10.0)
num_credit_inquiries = st.slider("Kredi Sorgusu Sayısı", 0, 20, 1)
outstanding_debt = st.number_input("Kalan Borç (₺)", min_value=0.0, value=20000.0)
credit_utilization_ratio = st.slider("Kredi Kullanım Oranı (%)", 0.0, 100.0, 45.0)
credit_history_age = st.slider("Kredi Geçmişi (Ay)", 0, 500, 12)
payment_of_min = st.selectbox("Asgari Ödeme Yapıldı mı?", ["Yes", "No"])
payment_of_min_map = {"Yes": 1, "No": 0}[payment_of_min]
monthly_investment = st.number_input("Aylık Yatırım (₺)", min_value=0.0, value=500.0)
total_emi = st.number_input("Aylık EMI (₺)", min_value=0.0, value=1000.0)
monthly_balance = st.number_input("Aylık Bakiye (₺)", min_value=0.0, value=3000.0)

# === Meslek
occupation = st.selectbox("Meslek", [
    'Accountant', 'Architect', 'Developer', 'Doctor', 'Engineer',
    'Entrepreneur', 'Journalist', 'Lawyer', 'Manager', 'Mechanic',
    'Media_Manager', 'Musician', 'Scientist', 'Teacher', 'Writer', 'Other'
])
occupation_map = {
    'Accountant': 0, 'Architect': 1, 'Developer': 2, 'Doctor': 3,
    'Engineer': 4, 'Entrepreneur': 5, 'Journalist': 6, 'Lawyer': 7,
    'Manager': 8, 'Mechanic': 9, 'Media_Manager': 10, 'Musician': 11,
    'Scientist': 12, 'Teacher': 13, 'Writer': 14, 'Other': 15
}
occupation_label = occupation_map[occupation]

# === Ödeme Davranışı
payment_behaviour = st.selectbox("Ödeme Davranışı", [
    "Low_spent_Small_value_payments",
    "Low_spent_Medium_value_payments",
    "Low_spent_Large_value_payments",
    "High_spent_Small_value_payments",
    "High_spent_Medium_value_payments",
    "High_spent_Large_value_payments"
])
payment_behaviour_map = {
    "Low_spent_Small_value_payments": 0,
    "Low_spent_Medium_value_payments": 1,
    "Low_spent_Large_value_payments": 2,
    "High_spent_Small_value_payments": 3,
    "High_spent_Medium_value_payments": 4,
    "High_spent_Large_value_payments": 5
}
payment_behaviour_value = payment_behaviour_map[payment_behaviour]

# === Kredi Karışımı
credit_mix = st.selectbox("Kredi Karışımı", ["Standard", "Good", "Bad"])
credit_mix_map = {"Standard": 1, "Good": 2, "Bad": 0}[credit_mix]

# === Çoklu Kredi Türü (One-hot)
loan_types = [
    "Auto Loan", "Credit-Builder Loan", "Debt Consolidation Loan", "Home Equity Loan",
    "Mortgage Loan", "Not Specified", "Payday Loan", "Personal Loan", "Student Loan"
]
loan_selected = st.multiselect("Kredi Tür(leri)", loan_types, default=["Not Specified"])
loan_encoded = [1 if l in loan_selected else 0 for l in loan_types]

# === Feature Engineering
total_accounts = num_accounts + num_credit_cards
debt_per_account = outstanding_debt / total_accounts if total_accounts > 0 else 0
debt_to_income = outstanding_debt / annual_income if annual_income > 0 else 0
delayed_payments_per_account = num_delayed_payments / total_accounts if total_accounts > 0 else 0
total_monthly_expenses = monthly_investment + total_emi

# === Numeric Feature Vektörü (17 original + 5 engineered + 1 binary = 23)
numeric_features = np.array([[
    age, annual_income, monthly_salary, num_accounts, num_credit_cards,
    interest_rate, num_loans, delay_from_due, num_delayed_payments,
    changed_credit_limit, num_credit_inquiries, outstanding_debt,
    credit_utilization_ratio, credit_history_age, total_emi,
    monthly_investment, monthly_balance,
    total_accounts, debt_per_account, debt_to_income,
    delayed_payments_per_account, total_monthly_expenses,
    payment_of_min_map
]])

# === Model ve Scaler Yükle
try:
    with open("models/classic_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    numeric_scaled = scaler.transform(numeric_features)
except Exception as e:
    st.error(f"❌ Scaler yüklenemedi:\n{e}")
    st.stop()

try:
    with open("models/stack_supervised.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"❌ Model yüklenemedi:\n{e}")
    st.stop()

# === Final Feature Vektörü (23 scaled + 9 one-hot + 3 kategorik = 35)
final_features = np.hstack([
    numeric_scaled,
    np.array(loan_encoded).reshape(1, -1),
    np.array([[occupation_label, payment_behaviour_value, credit_mix_map]])
])

# === Tahmin
if st.button("🎯 Skoru Tahmin Et"):
    prediction = model.predict(final_features.reshape(1, -1))[0]
    label_map = {0: "Approved", 1: "Rejected"}
    if prediction == 0:
        st.markdown("### ✅ <span style='color:green'><strong>Approved</strong></span>", unsafe_allow_html=True)
    else:
        st.markdown("### ❌ <span style='color:red'><strong>Rejected</strong></span>", unsafe_allow_html=True)
