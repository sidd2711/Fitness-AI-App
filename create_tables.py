from app.database import (
    engine,
    Base
)

# IMPORTANT:
# Import all models so SQLAlchemy registers them
import app.models

Base.metadata.create_all(bind=engine)

print("Tables created successfully ✅")