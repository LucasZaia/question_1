from sqlalchemy import create_engine

from app.config import Settings
from app.database import Base, create_session_factory


def test_default_settings_use_sqlite() -> None:
    settings = Settings()

    assert settings.database_url.startswith("sqlite")


def test_session_factory_can_create_a_session() -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        assert session.is_active

