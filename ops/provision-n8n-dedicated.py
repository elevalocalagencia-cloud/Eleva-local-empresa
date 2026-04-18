#!/usr/bin/env python3
from __future__ import annotations

import argparse
import secrets
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


N8N_IMAGE = "n8nio/n8n:2.15.0"
POSTGRES_IMAGE = "postgres:16.4-alpine"
REDIS_IMAGE = "redis:7.4-alpine"
DEFAULT_TRAEFIK_NETWORK = "coolify"


@dataclass(frozen=True)
class TenantRuntime:
    tenant_id: str
    slug: str
    domain: str
    project_name: str
    router_name: str
    internal_network: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gera runtime n8n dedicado por tenant sem tocar no stack shared."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--domain", help="Dominio dedicado do n8n. Default: wf-{slug-curto}.elevalocal.shop")
    parser.add_argument("--traefik-network", default=DEFAULT_TRAEFIK_NETWORK)
    parser.add_argument("--force", action="store_true", help="Sobrescreve docker-compose.yml e .env.example gerados")
    parser.add_argument("--dry-run", action="store_true", help="Imprime compose/env sem escrever arquivos")
    parser.add_argument("--deploy", action="store_true", help="Executa docker compose up -d apos gerar arquivos")
    return parser


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest nao encontrado: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"yaml invalido em {path}: {exc}") from exc


def require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"campo obrigatorio invalido: {field}")
    return value


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"campo obrigatorio invalido: {field}")
    return value.strip()


def short_slug(slug: str) -> str:
    if slug.startswith("eleva-"):
        return slug.removeprefix("eleva-")
    if slug.startswith("cli-"):
        return slug.removeprefix("cli-")
    return slug


def build_runtime(manifest: dict[str, Any], domain: str | None) -> TenantRuntime:
    tenant = require_mapping(manifest.get("tenant"), "tenant")
    tenant_id = require_string(tenant.get("tenant_id"), "tenant.tenant_id")
    slug = require_string(tenant.get("slug"), "tenant.slug")
    n8n_domain = domain or f"wf-{short_slug(slug)}.elevalocal.shop"
    return TenantRuntime(
        tenant_id=tenant_id,
        slug=slug,
        domain=n8n_domain,
        project_name=f"{tenant_id}-n8n",
        router_name=f"n8n-{slug}",
        internal_network=f"cli-{slug}-net",
    )


def render_compose(runtime: TenantRuntime, traefik_network: str) -> str:
    return f"""name: {runtime.project_name}

services:
  n8n:
    image: ${{N8N_IMAGE}}
    restart: unless-stopped
    depends_on:
      - postgresql
      - redis
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgresql
      DB_POSTGRESDB_PORT: "5432"
      DB_POSTGRESDB_DATABASE: ${{POSTGRES_DB}}
      DB_POSTGRESDB_USER: ${{POSTGRES_USER}}
      DB_POSTGRESDB_PASSWORD: ${{POSTGRES_PASSWORD}}
      EXECUTIONS_MODE: queue
      N8N_EDITOR_BASE_URL: https://${{N8N_DOMAIN}}
      N8N_ENCRYPTION_KEY: ${{N8N_ENCRYPTION_KEY}}
      N8N_HOST: ${{N8N_DOMAIN}}
      N8N_PORT: "5678"
      N8N_PROTOCOL: https
      N8N_PROXY_HOPS: "1"
      N8N_SECURE_COOKIE: "true"
      N8N_USER_MANAGEMENT_JWT_SECRET: ${{N8N_USER_MANAGEMENT_JWT_SECRET}}
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: "6379"
      WEBHOOK_URL: https://${{N8N_DOMAIN}}
    volumes:
      - n8n-data:/home/node/.n8n
    networks:
      - internal
      - traefik
    labels:
      - traefik.enable=true
      - traefik.http.routers.{runtime.router_name}.rule=Host(`{runtime.domain}`)
      - traefik.http.routers.{runtime.router_name}.entrypoints=websecure
      - traefik.http.routers.{runtime.router_name}.tls.certresolver=letsencrypt
      - traefik.http.services.{runtime.router_name}.loadbalancer.server.port=5678

  n8n-worker:
    image: ${{N8N_IMAGE}}
    restart: unless-stopped
    depends_on:
      - postgresql
      - redis
    command: worker
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgresql
      DB_POSTGRESDB_PORT: "5432"
      DB_POSTGRESDB_DATABASE: ${{POSTGRES_DB}}
      DB_POSTGRESDB_USER: ${{POSTGRES_USER}}
      DB_POSTGRESDB_PASSWORD: ${{POSTGRES_PASSWORD}}
      EXECUTIONS_MODE: queue
      N8N_ENCRYPTION_KEY: ${{N8N_ENCRYPTION_KEY}}
      N8N_USER_MANAGEMENT_JWT_SECRET: ${{N8N_USER_MANAGEMENT_JWT_SECRET}}
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: "6379"
    volumes:
      - n8n-data:/home/node/.n8n
    networks:
      - internal

  postgresql:
    image: ${{POSTGRES_IMAGE}}
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${{POSTGRES_DB}}
      POSTGRES_USER: ${{POSTGRES_USER}}
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD}}
    volumes:
      - postgresql-data:/var/lib/postgresql/data
    networks:
      - internal

  redis:
    image: ${{REDIS_IMAGE}}
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - internal

volumes:
  n8n-data:
    name: {runtime.tenant_id}-n8n-data
  postgresql-data:
    name: {runtime.tenant_id}-postgresql-data
  redis-data:
    name: {runtime.tenant_id}-redis-data

networks:
  internal:
    name: {runtime.internal_network}
    driver: bridge
  traefik:
    external: true
    name: {traefik_network}
"""


def render_env(runtime: TenantRuntime) -> str:
    return f"""N8N_IMAGE={N8N_IMAGE}
POSTGRES_IMAGE={POSTGRES_IMAGE}
REDIS_IMAGE={REDIS_IMAGE}
N8N_DOMAIN={runtime.domain}
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_BASE64_32
N8N_ENCRYPTION_KEY=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32
N8N_USER_MANAGEMENT_JWT_SECRET=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32
TRAEFIK_NETWORK={DEFAULT_TRAEFIK_NETWORK}
"""


def render_real_env(runtime: TenantRuntime) -> str:
    return f"""N8N_IMAGE={N8N_IMAGE}
POSTGRES_IMAGE={POSTGRES_IMAGE}
REDIS_IMAGE={REDIS_IMAGE}
N8N_DOMAIN={runtime.domain}
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD={secrets.token_urlsafe(32)}
N8N_ENCRYPTION_KEY={secrets.token_hex(32)}
N8N_USER_MANAGEMENT_JWT_SECRET={secrets.token_hex(32)}
TRAEFIK_NETWORK={DEFAULT_TRAEFIK_NETWORK}
"""


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise ValueError(f"arquivo ja existe: {path} (use --force para sobrescrever)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def deploy(runtime_dir: Path) -> None:
    env_file = runtime_dir / ".env"
    if not env_file.exists():
        raise ValueError(f".env real ausente para deploy: {env_file}")
    subprocess.run(
        ["docker", "compose", "--env-file", ".env", "up", "-d"],
        cwd=runtime_dir,
        check=True,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace_root = args.workspace_root.resolve()
    manifest_path = workspace_root / "tenants" / "manifests" / f"{args.tenant_id}.yaml"

    try:
        manifest = require_mapping(load_yaml(manifest_path), "manifest")
        runtime = build_runtime(manifest, args.domain)
        compose = render_compose(runtime, args.traefik_network)
        env_example = render_env(runtime)
        runtime_dir = workspace_root / "tenants" / "runtime" / args.tenant_id

        if args.dry_run:
            print(f"# runtime_dir: {runtime_dir}")
            print("# docker-compose.yml")
            print(compose)
            print("# .env.example")
            print(env_example)
            return 0

        write_file(runtime_dir / "docker-compose.yml", compose, force=args.force)
        write_file(runtime_dir / ".env.example", env_example, force=args.force)
        env_path = runtime_dir / ".env"
        if not env_path.exists():
            write_file(env_path, render_real_env(runtime), force=False)

        if args.deploy:
            deploy(runtime_dir)

        print(f"Runtime n8n dedicado gerado: {runtime_dir}")
        print(f"Dominio: https://{runtime.domain}")
        print("Deploy nao executado" if not args.deploy else "Deploy executado")
        return 0
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
