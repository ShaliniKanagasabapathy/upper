import streamlit as st
import boto3
import time

# AWS S3 client
s3 = boto3.client('s3')

# Your bucket name
BUCKET_NAME = "excel-free-pipeline-shalini"

st.title("S3 File Upload & Download Pipeline")

# Upload file
uploaded_file = st.file_uploader("Upload your file")

if uploaded_file is not None:

    file_name = uploaded_file.name

    # Upload to raw folder
    raw_key = f"raw/{file_name}"

    s3.upload_fileobj(uploaded_file, BUCKET_NAME, raw_key)

    st.success(f"{file_name} uploaded to raw folder")

    # Processed file path
    processed_key = f"processed/{file_name}"

    st.info("Waiting for processed file...")

    # Wait until Lambda creates processed file
    for i in range(20):

        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=processed_key)

            st.success("Processed file available!")

            # Download processed file
            processed_file = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=processed_key
            )

            st.download_button(
                label="Download Processed File",
                data=processed_file['Body'].read(),
                file_name=file_name
            )

            break

        except:
            time.sleep(2)

    else:
        st.error("Processed file not found")