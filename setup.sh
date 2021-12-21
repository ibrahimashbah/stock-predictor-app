mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor = ‘#84a3a7’\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
