DATABASE_NAME="${SNOWFLAKE_DATABASE:-YOUR_DATABASE_NAME}"
SCHEMA_NAME="${SNOWFLAKE_SCHEMA:-YOUR_SCHEMA_NAME}"

cd app

# deploy streamlit app
snow --config-file="$GITHUB_WORKSPACE/config.toml" streamlit deploy --database "$DATABASE_NAME" --schema "$SCHEMA_NAME" --replace
