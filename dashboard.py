import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Student Dropout Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data_clean.csv")

df = load_data()

# Title
st.title("🎓 Dashboard Dropout Mahasiswa")

# Ringkasan metrik utama
graduate_count = df['Status'].value_counts().get('Graduate', 0)
dropout_count = df['Status'].value_counts().get('Dropout', 0)
total = graduate_count + dropout_count

if total > 0:
    graduate_rate = graduate_count / total * 100
    dropout_rate = dropout_count / total * 100
else:
    graduate_rate = 0
    dropout_rate = 0

# Tampilkan metrik utama
colA, colB = st.columns(2)
with colA:
    st.metric("🎓 Mahasiswa Lulus", graduate_count)
with colB:
    st.metric("🚨 Mahasiswa Dropout", dropout_count)

# Section 1: Pie Chart
st.subheader("Perbandingan Mahasiswa Lulus vs Dropout")
fig, ax = plt.subplots()
ax.pie([graduate_rate, dropout_rate],
       labels=['Graduate', 'Dropout'],
       autopct='%1.1f%%',
       colors=['#4CAF50', '#F44336'],
       startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Section 2: Dropout by Course
st.subheader("Dropout Berdasarkan Program Studi (Course)")
course_dropout = df[df['Status'] == 'Dropout']['Course'].value_counts(normalize=True) * 100
course_dropout = course_dropout.reindex(df['Course'].unique(), fill_value=0)

fig, ax = plt.subplots()
course_dropout.plot(kind='bar', ax=ax, color='#ff9999')
ax.set_ylabel('Persentase Dropout (%)')
ax.set_xlabel('Course')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 3: Dropout by Age Group
st.subheader("Dropout Berdasarkan Usia saat Masuk Kuliah")
bins = [15, 20, 25, 30, 35, 40, 60]
labels = ['15-19', '20-24', '25-29', '30-34', '35-39', '40+']
df['AgeGroup'] = pd.cut(df['Age_at_enrollment'], bins=bins, labels=labels, right=False)

age_dropout = df[df['Status'] == 'Dropout']['AgeGroup'].value_counts().sort_index()
fig, ax = plt.subplots()
age_dropout.plot(kind='bar', ax=ax, color='#ffa07a')
ax.set_ylabel('Jumlah Dropout')
ax.set_xlabel('Kelompok Usia')
st.pyplot(fig)

# Section 4: Dropout by Gender
st.subheader("Dropout Berdasarkan Gender")
gender_dropout = df[df['Status'] == 'Dropout']['Gender'].value_counts()
fig, ax = plt.subplots()
gender_dropout.plot(kind='bar', ax=ax, color='#66b3ff')
ax.set_ylabel('Jumlah Dropout')
ax.set_xlabel('Gender')
st.pyplot(fig)

# Section 5: Metrik Tambahan
st.subheader("📊 Metrik Tambahan")
col5, col6, col7 = st.columns(3)

with col5:
    st.metric(label="Total Mahasiswa Dropout", value=f"{dropout_count}")

with col6:
    try:
        avg_age = df[df['Status'] == 'Dropout']['Age_at_enrollment'].mean()
        st.metric(label="Rata-rata Usia Saat Dropout", value=f"{avg_age:.1f} tahun")
    except:
        st.metric(label="Rata-rata Usia", value="Data tidak tersedia")

with col7:
    try:
        top_course = df[df['Status'] == 'Dropout']['Course'].value_counts().idxmax()
        st.metric(label="Program Studi Dropout Tertinggi", value=top_course)
    except:
        st.metric(label="Program Studi Dropout Tertinggi", value="Data tidak tersedia")
