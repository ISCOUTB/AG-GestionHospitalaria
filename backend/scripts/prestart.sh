set -e
set -x

# Inicializar DB
python3 -m app.backend_pre_start

# Correr migraciones
python3 -m alembic upgrade head

# Crear la información inicial a la DB
python3 -m app.initial_data
