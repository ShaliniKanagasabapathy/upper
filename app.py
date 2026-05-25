import streamlit as st
import boto3
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Excel AWS Pipeline",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Excel Processing Pipeline (AWS + Lambda)")
st.markdown("Upload Excel → S3 → Lambda processes → Download result 🚀")

# -----------------------------
# AWS CLIENT
# -----------------------------
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_REGION"]
)

BUCKET = st.secrets["BUCKET_NAME"]

# -----------------------------
# FUNCTION: GET PROCESSED FILE
# -----------------------------
def get_processed_file(raw_key):
    processed_key = raw_key.replace("raw/", "processed/")

    for i in range(10):  # retry for Lambda delay
        try:
            obj = s3.get_object(Bucket=BUCKET, Key=processed_key)
            return obj["Body"].read(), processed_key
        except:
            time.sleep(3)

    return None, processed_key

# -----------------------------
# UI: FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Excel file",
    type=["xlsx"]
)

# -----------------------------
# PROCESS BUTTON
# -----------------------------
if uploaded_file:

    st.write("Selected file:", uploaded_file.name)

    if st.button("🚀 Upload & Process"):

        raw_key = f"raw/{uploaded_file.name}"

        # Upload to S3
        with st.spinner("Uploading to S3..."):
            s3.upload_fileobj(uploaded_file, BUCKET, raw_key)

        st.success("Uploaded successfully to S3!")

        st.info("⚡ Waiting for Lambda processing...")

        # Wait & fetch processed file
        file_data, processed_key = get_processed_file(raw_key)

        if file_data:

            st.success("🎯 Processing completed!")

            st.write("Processed file:", processed_key)

            # Download button
            st.download_button(
                label="📥 Download Processed File",
                data=file_data,
                file_name=uploaded_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.error("Processed file not found yet. Try again after few seconds.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit + AWS S3 + Lambda 🚀")