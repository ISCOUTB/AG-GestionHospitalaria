set -e
set -x

# Let the DB start
python3 -m app.backend_pre_start

# # Run migrations
python3 -m alembic upgrade head

# # Create initial data in DB
python3 -m app.initial_data
