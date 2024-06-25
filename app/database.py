from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from dotenv import load_dotenv
from .settings import debug
import logging
import os


load_dotenv()

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')



def get_database_url():
    # print(debug)
    if debug:
        return f"postgresql+psycopg://postgres:postgres@localhost/europass_fa"
    else:

        return f"postgresql+psycopg://{username}:{password}@{host}/{db_name}"



SQLALCHEMY_DATABASE_URL = get_database_url()


engine = create_async_engine(
    # global_settings.asyncpg_url.unicode_string(),
    SQLALCHEMY_DATABASE_URL,
    future=True,
    # echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


# Setup logger
logger = logging.getLogger(__name__)

# Assuming AsyncSessionFactory is already defined somewhere
# Example: AsyncSessionFactory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionFactory() as session:
            logger.debug("Created new async session.")
            yield session
    except Exception as e:
        logger.error(f"Error occurred in async database session: {e}")
        raise
    finally:
        await session.close()
        logger.debug("Closed async session.")