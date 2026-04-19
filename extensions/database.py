"""
This module provides functions to initialize and access a MongoDB database connection. It uses the `pymongo` library to manage the connection and ensures that the connection is established in a thread-safe manner. The MongoDB URI is expected to be set in the environment variable `MONGO_URI`. The module includes error handling to log any connection issues and raises exceptions if the connection fails.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:09 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from configs.database import get_db

db = (
    get_db()
)  # Initialize the database connection and assign it to the global variable `db` for use throughout the application. This ensures that we have a single, shared database connection that can be accessed from any module that imports this `database` module.


if db is None:
    raise Exception("Failed to initialize database connection")

try:
    db.users.create_index("auth.email", unique=True, sparse=True)
except Exception as e:
    print(f"Error creating index on users collection: {e}")
