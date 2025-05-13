import os

from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from alembic import context

config = context.config
fileConfig(config.config_file_name)
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# connectable = engine_from_config(
#     config.get_section(config.config_ini_section, {}),
#     prefix="sqlalchemy.",
#     poolclass=pool.NullPool,
# )

# with connectable.connect() as connection:
#     context.configure(
#         connection=connection, target_metadata=None
#     )

#     with context.begin_transaction():
#         context.run_migrations()