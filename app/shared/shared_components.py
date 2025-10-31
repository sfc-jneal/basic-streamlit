import os
import streamlit as st
from snowflake.snowpark.context import get_active_session
from typing import List, Dict, Any, Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector
from snowflake.snowpark import Session


def remote_connection() -> snowflake.connector.SnowflakeConnection:
    if not os.getenv('SNOWFLAKE_PRIVATE_KEY_PATH') or not os.path.exists('/run/secrets/rsa_key.p8'):
        print("No private key path found")
        return None

    creds = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'private_key_file': '/run/secrets/rsa_key.p8',
        'private_key_file_pwd':os.getenv('SNOWFLAKE_PRIVATE_KEY_PASSPHRASE', None),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'database': os.getenv('SNOWFLAKE_DATABASE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        'client_session_keep_alive': True
    }

    return snowflake.connector.connect(**creds)

def get_snowflake_session() -> Optional[Session]:
    # 1) Try to use active session (Streamlit in Snowflake)
    try:
        return (get_active_session(), True)
    except Exception:
        pass

    # 2) Fallback to remote Snowflakeconnection (Local Development)
    conn = remote_connection()
    if conn is None:
        return (None, False)

    return (Session.builder.configs({"connection": conn}).create(), False)


def get_current_user_info() -> Dict[str, str]:
    try:
        user_info = st.user
        return {
            "email": user_info.get("email", "na@acme.com"),
            "username": user_info.get("user_name", "na"),
            "login_name": user_info.get("login_name", "na")
        }
    except:
        # Fallback
        return {
            "email": "na@acme.com",
            "username": "na",
            "login_name": "na"
        }


def is_admin_user() -> bool:
    # Check if current user email is in ADMIN_EMAILS configuration
    try:
        user_info = get_current_user_info()
        current_email = user_info.get("email", "").strip().lower()

        if not current_email:
            return False

        admin_emails_str = get_app_config("ADMIN_EMAILS", "")
        if not admin_emails_str:
            return False

        admin_emails = [email.strip().lower() for email in admin_emails_str.split(",") if email.strip()]
        return current_email in admin_emails
    except Exception as e:
        return False


def apply_custom_css() -> None:
    st.markdown(
        """
    <style>
       
    </style>
    """,
        unsafe_allow_html=True,
    )