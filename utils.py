import streamlit as st

def get_json_credentials():
    credentials = {
    "type" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["type"],
    "project_id" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["project_id"],
    "private_key_id" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["private_key_id"],
    "private_key" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["private_key"],
    "client_email" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["client_email"],
    "client_id" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["client_id"],
    "auth_uri" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["auth_uri"],
    "token_uri" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["token_uri"],
    "auth_provider_x509_cert_url" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["client_x509_cert_url"],
    "universe_domain" : st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["universe_domain"]
    }
    return credentials
    