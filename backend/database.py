from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./interview_prep.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def apply_sqlite_compatibility_migrations():
    """Adds v3 fields for installations created by the earlier schema."""
    inspector = inspect(engine)
    if "interview_sessions" not in inspector.get_table_names():
        return
    existing = {column["name"] for column in inspector.get_columns("interview_sessions")}
    additions = {
        "user_id": "INTEGER",
        "number_of_questions": "INTEGER NOT NULL DEFAULT 5",
        "current_difficulty": "VARCHAR(20) NOT NULL DEFAULT 'Medium'",
    }
    question_columns = {column["name"] for column in inspector.get_columns("questions")}
    question_additions = {"difficulty": "VARCHAR(20) NOT NULL DEFAULT 'Medium'", "skill": "VARCHAR(100)"}
    answer_columns = {column["name"] for column in inspector.get_columns("answers")}
    answer_additions = {"rubric_json": "TEXT DEFAULT '{}'", "missing_concepts_json": "TEXT DEFAULT '[]'"}
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in existing:
                connection.execute(text(f"ALTER TABLE interview_sessions ADD COLUMN {name} {definition}"))
        for name, definition in question_additions.items():
            if name not in question_columns:
                connection.execute(text(f"ALTER TABLE questions ADD COLUMN {name} {definition}"))
        for name, definition in answer_additions.items():
            if name not in answer_columns:
                connection.execute(text(f"ALTER TABLE answers ADD COLUMN {name} {definition}"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
