import streamlit as st
import boto3
import time
from processor import process_excel
import pandas as pd
from io import BytesIO

# --------- AWS CONFIG FROM SECRETS ----------
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_DEFAULT_REGION"]
)

BUCKET_NAME = st.secrets["BUCKET_NAME"]

st.title("Excel S3 + Lambda Pipeline")

# --------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    file_name = uploaded_file.name

    raw_key = f"raw/{file_name}"
    processed_key = f"processed/{file_name}"

    # --------- UPLOAD TO S3 RAW ----------
    s3.upload_fileobj(uploaded_file, BUCKET_NAME, raw_key)
    st.success("File uploaded to S3 raw folder")

    st.info("Waiting for Lambda processing...")

    # --------- WAIT FOR PROCESSED FILE ----------
    timeout = 120
    start = time.time()

    while time.time() - start < timeout:
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=processed_key)

            st.success("Processed file found!")

            # Read file
            file_bytes = response["Body"].read()

            st.download_button(
                label="Download Processed File",
                data=file_bytes,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            break

        except:
            time.sleep(3)

    else:
        st.error("Processed file not found. Check Lambda trigger.")