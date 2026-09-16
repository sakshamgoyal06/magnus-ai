import subprocess
import sys


def test_alembic_current_shows_head(db_migrated):
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "current"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "20250914_0001" in result.stdout
