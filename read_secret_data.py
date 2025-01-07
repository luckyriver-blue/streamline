import streamlit as st

openai_key = st.secrets["OPENAI_API_KEY"]

firebase_project_settings = {
  "type": "service_account",
  "project_id": "chatbot-e8214",
  "private_key_id": st.secrets["PRIVATE_KEY_ID"],
  "private_key": st.secrets["PRIVATE_KEY"].replace(r'\n', '\n'),
  "client_email": st.secrets["CLIENT_EMAIL"],
  "client_id": st.secrets["CLIENT_ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"],
}
