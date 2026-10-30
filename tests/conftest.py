from pathlib import Path


def test_project_test_configuration_is_available() -> None:
    assert Path("src/app").is_dir()

