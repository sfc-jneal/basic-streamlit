import os
import re
import streamlit as st
from shared.shared_components import apply_custom_css, get_snowflake_session 

st.set_page_config(page_title="Example Streamlit App", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

apply_custom_css()
st.logo("logo.svg")

@st.cache_resource
def connect_to_snowflake():
    return get_snowflake_session()

session, running_in_snowflake = connect_to_snowflake()

st.subheader("Environment")
env_text = "Snowflake (Streamlit in Snowflake)" if running_in_snowflake else "Local development"
st.info(f"Environment: {env_text} | Snowflake session available: {'Yes' if session else 'No'}")
if session:
    try:
        info = session.sql("select current_account() as account, current_user() as user, current_role() as role").to_pandas()
        acct = info.loc[0, 'ACCOUNT'] if 'ACCOUNT' in info.columns else ''
        usr = info.loc[0, 'USER'] if 'USER' in info.columns else ''
        rol = info.loc[0, 'ROLE'] if 'ROLE' in info.columns else ''
        st.caption(f"Connected to account: {acct} | user: {usr} | role: {rol}")
    except Exception:
        pass

st.divider()
st.subheader("CI/CD Overview")
st.caption("High-level steps to deploy Streamlit to Snowflake using GitHub Actions")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
**1) Prepare Snowflake**
- Create/choose a deploy role
- Grant USAGE on DB/Schema, CREATE STREAMLIT
- Ensure a warehouse is available
- Update `app/snowflake.yml` and `app/deploy_streamlit_app.sh`
""")
with c2:
    st.markdown("""
**2) Configure GitHub**
- Set repo Variables: `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`
- Add Secret: `SNOWFLAKE_PRIVATE_KEY`
- Use Environments (DEV/QA/PROD) as needed
""")
with c3:
    st.markdown("""
**3) Deploy with Actions**
- Push to `dev` (affecting `app/**`) to auto-deploy
- Or run the workflow manually
- QA/PROD can be gated via protected branches
""")

st.markdown("""
---
**Local Development**
- `cp env.sample .env` and fill values if testing remote Snowflake
- `make up` to start at http://localhost:8501
- This app shows whether it’s running locally or in Snowflake
- Ensure Streamlit versions match between `requirements.txt` and `app/environment.yml`
""")