from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "ops" / "provision-n8n-dedicated.py"


def write_manifest(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        textwrap.dedent(
            """
            tenant:
              tenant_id: cli-eleva-pilot
              status: internal
              company_name: Eleva Local Pilot
              slug: eleva-pilot
              owner:
                name: Eleva Ops
                role: Operacoes
                email: ops@elevalocal.shop
                phone: '+5511999999999'
            naming:
              n8n_prefix: cli-eleva-pilot-wf
            infrastructure:
              domains:
                customer_facing: null
                internal_webhook: webhook.elevalocal.shop
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    return path


def run_script(workspace_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--workspace-root",
            str(workspace_root),
            *args,
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_dry_run_prints_dedicated_compose_without_writing(tmp_path: Path) -> None:
    write_manifest(tmp_path / "tenants" / "manifests" / "cli-eleva-pilot.yaml")

    result = run_script(tmp_path, "--tenant-id", "cli-eleva-pilot", "--dry-run")

    assert result.returncode == 0
    assert "n8nio/n8n:2.15.0" in result.stdout
    assert "postgres:16.4-alpine" in result.stdout
    assert "redis:7.4-alpine" in result.stdout
    assert "cli-eleva-pilot-net" in result.stdout
    assert "traefik.http.routers.n8n-eleva-pilot.rule=Host(`wf-pilot.elevalocal.shop`)" in result.stdout
    assert "traefik.http.routers.n8n-eleva-pilot.entrypoints=https" in result.stdout
    assert "traefik.http.routers.n8n-eleva-pilot.tls=true" in result.stdout
    assert "traefik.http.routers.n8n-eleva-pilot.service=n8n-eleva-pilot" in result.stdout
    assert "traefik.http.routers.n8n-eleva-pilot-http.middlewares=n8n-eleva-pilot-redirect" in result.stdout
    assert "traefik.http.middlewares.n8n-eleva-pilot-redirect.redirectscheme.scheme=https" in result.stdout
    assert "QUEUE_BULL_REDIS_HOST: cli-eleva-pilot-redis" in result.stdout
    assert "  cli-eleva-pilot-redis:" in result.stdout
    assert "mamtm8g3b2mdh7ko0hxdcyr3" not in result.stdout
    assert not (tmp_path / "tenants" / "runtime" / "cli-eleva-pilot").exists()


def test_generates_runtime_compose_and_env_example(tmp_path: Path) -> None:
    write_manifest(tmp_path / "tenants" / "manifests" / "cli-eleva-pilot.yaml")

    result = run_script(tmp_path, "--tenant-id", "cli-eleva-pilot")

    assert result.returncode == 0
    runtime_dir = tmp_path / "tenants" / "runtime" / "cli-eleva-pilot"
    compose = (runtime_dir / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (runtime_dir / ".env.example").read_text(encoding="utf-8")

    assert "name: cli-eleva-pilot-n8n" in compose
    assert "n8n-eleva-pilot" in compose
    assert "  cli-eleva-pilot-redis:" in compose
    assert "QUEUE_BULL_REDIS_HOST: cli-eleva-pilot-redis" in compose
    assert "traefik.http.routers.n8n-eleva-pilot.entrypoints=https" in compose
    assert "traefik.http.routers.n8n-eleva-pilot.tls=true" in compose
    assert "traefik.http.routers.n8n-eleva-pilot.service=n8n-eleva-pilot" in compose
    assert "cli-eleva-pilot-n8n-data" in compose
    assert "mamtm8g3b2mdh7ko0hxdcyr3" not in compose
    assert "N8N_DOMAIN=wf-pilot.elevalocal.shop" in env_example
    assert "N8N_ENCRYPTION_KEY=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32" in env_example
    assert "POSTGRES_PASSWORD=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_BASE64_32" in env_example
