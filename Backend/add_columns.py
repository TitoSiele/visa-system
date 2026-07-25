from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS country_of_origin VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS date_of_birth VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS passport_number VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS address VARCHAR;"))
    conn.commit()
    print("Columns added successfully.")