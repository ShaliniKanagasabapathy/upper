import streamlit as st
import boto3
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Excel Automation with AWS Pipeline",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Excel Processing Pipeline (AWS + Lambda)")
st.markdown("Upload Excel → S3 → Lambda processes → Get results 🚀")

# -----------------------------
# AWS CLIENT (FROM SECRETS)
# -----------------------------
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_REGION"]
)

BUCKET = st.secrets["BUCKET_NAME"]

# -----------------------------
# FILE UPLOADER UI
# -----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload your Excel file",
    type=["xlsx"]
)

# -----------------------------
# UPLOAD BUTTON ACTION
# -----------------------------
if uploaded_file:

    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("🚀 Upload & Process"):

        with st.spinner("Uploading to AWS S3..."):

            s3_key = f"raw/{uploaded_file.name}"

            s3.upload_fileobj(
                uploaded_file,
                BUCKET,
                s3_key
            )

        st.success("✅ Uploaded successfully to S3!")
        st.info("⚡ Lambda is processing your file...")

        # -----------------------------
        # WAIT SIMULATION (UI ONLY)
        # -----------------------------
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)

        st.success("🎯 Processing triggered successfully!")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit + AWS S3 + Lambda 🚀")