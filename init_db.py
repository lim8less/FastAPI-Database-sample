import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from models import Base
from database import engine

async def create_tables():
    async with engine.begin() as conn:
        # Use `Base.metadata.create_all()` to create tables
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
