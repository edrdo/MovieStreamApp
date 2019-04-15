# TODO: altere as configurações de acesso à BD se necessário
export DB_HOST="127.0.0.1"
export DB_SCHEMA="guest"
export DB_USER="guest"
export DB_PASS="guest"

# Variáveis de ambiente Flask
export FLASK_APP=app
export FLASK_ENV=development

# Corre flask
flask run
