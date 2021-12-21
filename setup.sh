mkdir -p ~/.streamlit/

echo "[theme]
base=’light’
primaryColor=’#3886f7’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
