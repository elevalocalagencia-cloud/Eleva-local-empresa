from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_SCRIPT = REPO_ROOT / "ops" / "backup-elevalocal.sh"


def test_backup_script_dry_run_local_only_generates_expected_structure(tmp_path: Path) -> None:
    backup_root = tmp_path / "backups"
    timestamp = "2026-04-17-030000"
    log_file = tmp_path / "backup.log"
    ops_dir = tmp_path / "ops"
    ops_dir.mkdir(parents=True, exist_ok=True)

    script_path = ops_dir / "backup-elevalocal.sh"
    script_path.write_text(SOURCE_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    (ops_dir / "backup-elevalocal.env").write_text(
        "\n".join(
            [
                "BACKUP_ROOT=./backups",
                "BACKUP_MODE=local_only",
                "DRY_RUN=true",
                f"BACKUP_TIMESTAMP={timestamp}",
                "BACKUP_LOG_FILE=./backup.log",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        ["bash", "./ops/backup-elevalocal.sh"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    dest_dir = backup_root / timestamp
    assert dest_dir.exists()

    expected_files = {
        "manifest.txt",
        "n8n-postgres.sql",
        "chatwoot-postgres.sql",
        "evolution-postgres.sql",
        "n8n-data.tar.gz",
        "n8n-postgresql-data.tar.gz",
        "n8n-redis-data.tar.gz",
        "chatwoot-postgres-data.tar.gz",
        "chatwoot-rails-data.tar.gz",
        "chatwoot-redis-data.tar.gz",
        "evolution-postgres-data.tar.gz",
        "evolution-instances.tar.gz",
        "evolution-redis.tar.gz",
    }
    assert expected_files.issubset({path.name for path in dest_dir.iterdir()})

    manifest = (dest_dir / "manifest.txt").read_text(encoding="utf-8")
    assert "backup_mode=local_only" in manifest
    assert "dry_run=true" in manifest

    log_output = log_file.read_text(encoding="utf-8")
    assert "iniciando backup completo da elevalocal" in log_output
    assert "backup concluido" in log_output
