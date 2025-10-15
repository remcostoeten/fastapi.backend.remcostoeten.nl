from prisma import Prisma
from .config import settings

# Global database instance
db = Prisma()


async def connect_to_database():
    """Connect to the database."""
    if not db.is_connected():
        await db.connect()
        print("✅ Connected to database")


async def disconnect_from_database():
    """Disconnect from the database."""
    if db.is_connected():
        await db.disconnect()
        print("✅ Disconnected from database")


async def get_database():
    """Get database instance for dependency injection."""
    return db