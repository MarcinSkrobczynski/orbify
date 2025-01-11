import logging
import os

from sqlalchemy import engine_from_config

from alembic import context
from orbify_projects.core.config import settings
from orbify_projects.db.base import Base
from orbify_projects.models import *  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alembic.env")


def get_url():
    if not os.path.isfile("/.dockerenv"):
        settings.postgres_server = "localhost"

    return settings.database_uri


def run_migrations_online() -> None:
    logger.info("Running migrations online")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", get_url())

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            prefix="sqlalchemy.",
        )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline() -> None:
    logger.info("Running migrations offline")
    context.configure(url=get_url())

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
