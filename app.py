import streamlit as st
import joblib

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="AI Phishing Detector",
    page_icon="🔐",
    layout="centered"
)

# =========================
# Custom CSS
# =========================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #1e293b
    );
    color:white;
}

.main-card{
    background: rgba(255,255,255,0.08);
    padding:35px;
    border-radius:25px;
    backdrop-filter: blur(18px);
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 0 30px rgba(0,0,0,0.4);
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}

.result-safe{
    padding:20px;
    border-radius:15px;
    background:rgba(34,197,94,0.15);
    border:1px solid #22c55e;
    color:#86efac;
    text-align:center;
    font-size:22px;
    font-weight:bold;
}

.result-danger{
    padding:20px;
    border-radius:15px;
    background:rgba(239,68,68,0.15);
    border:1px solid #ef4444;
    color:#fca5a5;
    text-align:center;
    font-size:22px;
    font-weight:bold;
}

.footer{
    text-align:center;
    margin-top:25px;
    color:#94a3b8;
    font-size:14px;
}

.stButton>button{

    width:100%;
    height:55px;

    border:none;

    border-radius:12px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #9333ea
    );

    color:white;

    font-size:18px;

    font-weight:bold;

    transition:0.3s;
}

.stButton>button:hover{

    transform:scale(1.02);

    box-shadow:0 0 20px rgba(37,99,235,0.5);
}

</style>
""", unsafe_allow_html=True)

# =========================
# Load Model
# =========================

model = joblib.load("model.pkl")

vectorizer = joblib.load("vectorizer.pkl")

# =========================
# UI
# =========================

st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">🔐 AI Phishing Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Detect fake and malicious URLs using Machine Learning</div>',
    unsafe_allow_html=True
)

# URL Input
url = st.text_input(
    "",
    placeholder="Enter URL to scan..."
)

# Scan Button
if st.button("⬡ Scan URL"):

    if url == "":

        st.warning("Please enter URL")

    else:

        # Convert URL
        data = vectorizer.transform([url])

        # Predict
        prediction = model.predict(data)

        # Confidence
        probability = model.predict_proba(data)

        confidence = max(probability[0]) * 100

        st.markdown("<br>", unsafe_allow_html=True)

        # Result
        if prediction[0] == 1:

            st.markdown(f'''
            <div class="result-danger">
                ⚠️ Phishing URL Detected
                <br><br>
                Confidence: {confidence:.2f}%
            </div>
            ''', unsafe_allow_html=True)

        else:

            st.markdown(f'''
            <div class="result-safe">
                ✅ Legitimate URL
                <br><br>
                Confidence: {confidence:.2f}%
            </div>
            ''', unsafe_allow_html=True)

# Footer
st.markdown(
    '<div class="footer">Powered by XGBoost + Streamlit</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)