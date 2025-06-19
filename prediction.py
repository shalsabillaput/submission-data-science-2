import streamlit as st

# Configure page
st.set_page_config(
    page_title="🎓 Prediksi Risiko Dropout Mahasiswa",
    layout="centered"
)

# Title and description
st.title("🎓 Prediksi Risiko Dropout Mahasiswa")
st.write("Masukkan data di bawah ini untuk memprediksi apakah mahasiswa berpotensi dropout atau lulus.")

# Create form
with st.form("dropout_prediction_form"):
    # First row of inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tuition_fees = st.selectbox(
            "Tuition Fees Up to Date",
            options=[0, 1],
            index=0,
            help="Status pembayaran uang kuliah"
        )
        
    with col2:
        debtor = st.selectbox(
            "Debtor",
            options=[0, 1],
            index=0,
            help="Status mahasiswa sebagai debitor"
        )
    
    # Grade inputs
    st.subheader("Nilai Akademik")
    grade_col1, grade_col2, grade_col3 = st.columns(3)
    
    with grade_col1:
        first_sem_grade = st.slider(
            "1st Semester Grade",
            min_value=0.0,
            max_value=200.0,
            value=100.0,
            step=0.1
        )
        
    with grade_col2:
        second_sem_grade = st.slider(
            "2nd Semester Grade",
            min_value=0.0,
            max_value=200.0,
            value=100.0,
            step=0.1
        )
        
    with grade_col3:
        admission_grade = st.slider(
            "Admission Grade",
            min_value=0.0,
            max_value=200.0,
            value=120.0,
            step=0.1
        )
    
    # Units information
    st.subheader("Jumlah SKS")
    units_col1, units_col2, units_col3 = st.columns(3)
    
    with units_col1:
        first_sem_approved = st.number_input(
            "1st Semester Approved Units",
            min_value=0,
            max_value=50,
            value=5,
            step=1
        )
        
    with units_col2:
        second_sem_approved = st.number_input(
            "2nd Semester Approved Units",
            min_value=0,
            max_value=50,
            value=5,
            step=1
        )
        
    with units_col3:
        second_sem_enrolled = st.number_input(
            "2nd Semester Enrolled Units",
            min_value=0,
            max_value=50,
            value=6,
            step=1
        )
    
    # Economic factors
    st.subheader("Faktor Ekonomi")
    econ_col1, econ_col2 = st.columns(2)
    
    with econ_col1:
        unemployment_rate = st.slider(
            "Unemployment Rate (%)",
            min_value=0.0,
            max_value=25.0,
            value=5.0,
            step=0.1
        )
        
    with econ_col2:
        gdp_per_capita = st.slider(
            "GDP per Capita",
            min_value=0.0,
            max_value=100000.0,
            value=20000.0,
            step=100.0
        )
    
    # Prediction button
    submitted = st.form_submit_button("Prediksi Risiko Dropout")
    
    if submitted:
        # Simple scoring algorithm (replace with your actual model)
        risk_score = 0
        
        # Financial factors
        if tuition_fees == 0:
            risk_score += 15
        if debtor == 1:
            risk_score += 20
        
        # Academic performance
        if first_sem_grade < 80:
            risk_score += (80 - first_sem_grade) * 0.5
        if second_sem_grade < 80:
            risk_score += (80 - second_sem_grade) * 0.5
        
        # Units progress
        if first_sem_approved < 5:
            risk_score += (5 - first_sem_approved) * 3
        if second_sem_approved < 5:
            risk_score += (5 - second_sem_approved) * 3
        
        # Economic factors
        risk_score += (unemployment_rate * 0.8)
        risk_score += max(0, (20000 - gdp_per_capita) / 1000)
        
        # Cap the score at 100
        risk_score = min(100, risk_score)
        
        # Display results
        st.divider()
        
        if risk_score > 60:
            st.error(f"🚨 Risiko Dropout Tinggi (Skor: {risk_score:.1f}/100)")
            st.write("**Rekomendasi:** Mahasiswa membutuhkan intervensi segera dari dosen wali dan layanan konseling kampus.")
        elif risk_score > 30:
            st.warning(f"⚠️ Risiko Dropout Sedang (Skor: {risk_score:.1f}/100)")
            st.write("**Rekomendasi:** Perlu pemantauan berkala dan bimbingan akademik tambahan.")
        else:
            st.success(f"🎓 Risiko Dropout Rendah (Skor: {risk_score:.1f}/100)")
            st.write("**Rekomendasi:** Lanjutkan pendampingan akademik secara normal.")