#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cria a estrutura operacional minima de um tenant da Eleva Local."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--company-name", required=True)
    parser.add_argument("--owner-name", required=True)
    parser.add_argument("--owner-email", required=True)
    parser.add_argument("--owner-phone", required=True)
    parser.add_argument("--whatsapp-number", required=True)
    parser.add_argument("--plan", default="piloto")
    parser.add_argument("--status", default="onboarding")
    parser.add_argument(
        "--n8n-runtime-mode",
        default="dedicated",
        choices=("shared-foundation", "dedicated"),
    )
    parser.add_argument("--customer-domain")
    parser.add_argument("--internal-webhook-domain")
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_outputs(
    *,
    manifest_path: Path,
    secrets_path: Path,
    onboarding_path: Path,
    ops_path: Path,
    registry_path: Path,
    manifest: dict[str, Any],
    registry: dict[str, Any],
    company_name: str,
    tenant_id: str,
    slug: str,
    onboarding_template: str,
    ops_template: str,
    secrets_template: str,
) -> None:
    for path in (manifest_path, secrets_path, onboarding_path, ops_path, registry_path):
        ensure_parent(path)

    manifest_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    registry_path.write_text(
        yaml.safe_dump(registry, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    secrets_path.write_text(
        render_markdown("Inventario de Segredos", company_name, tenant_id, slug, secrets_template),
        encoding="utf-8",
    )
    onboarding_path.write_text(
        render_markdown("Onboarding Checklist", company_name, tenant_id, slug, onboarding_template),
        encoding="utf-8",
    )
    ops_path.write_text(
        render_markdown("Client Ops Checklist", company_name, tenant_id, slug, ops_template),
        encoding="utf-8",
    )


def render_markdown(prefix: str, company_name: str, tenant_id: str, slug: str, template: str) -> str:
    lines = template.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].lstrip().startswith("#"):
        lines.pop(0)
    body = "\n".join(lines).lstrip()

    header = [
        f"# {prefix} - {company_name}",
        "",
        f"- tenant_id: `{tenant_id}`",
        f"- slug: `{slug}`",
        "",
    ]
    return "\n".join(header) + body + ("\n" if body else "")


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    n8n_is_dedicated = args.n8n_runtime_mode == "dedicated"
    n8n_scope = "workspace-per-tenant" if n8n_is_dedicated else "namespace-within-shared-stack"
    n8n_rollout = [
        "provisionar workspace ou stack dedicada de n8n para o tenant",
        "criar credenciais exclusivas com prefixo do tenant",
        "publicar workflows apenas dentro do namespace do tenant",
        "executar smoke test e registrar rollback path no checklist",
    ]
    if not n8n_is_dedicated:
        n8n_rollout = [
            "manter prefixo obrigatorio em workflows e credenciais do tenant",
            "registrar stack compartilhada e blast radius no inventario operacional",
            "validar namespace isolado antes de publicar qualquer workflow",
            "bloquear onboarding externo ate migracao para runtime dedicada",
        ]

    return {
        "tenant": {
            "tenant_id": args.tenant_id,
            "status": args.status,
            "company_name": args.company_name,
            "slug": args.slug,
            "owner": {
                "name": args.owner_name,
                "role": "Operacoes",
                "email": args.owner_email,
                "phone": args.owner_phone,
            },
            "contract": {
                "plan": args.plan,
                "billing_cycle": "mensal",
                "start_date": None,
                "notes": "Preencher observacoes contratuais e restricoes do cliente.",
            },
        },
        "naming": {
            "evolution_instance": f"{args.tenant_id}-evo",
            "chatwoot_inbox": f"{args.tenant_id}-inbox",
            "chatwoot_labels_prefix": args.tenant_id,
            "n8n_prefix": f"{args.tenant_id}-wf",
            "secrets_prefix": f"{args.tenant_id}-secret",
            "backups_prefix": args.tenant_id,
        },
        "channels": {
            "whatsapp": {
                "number_e164": args.whatsapp_number,
                "display_name": args.company_name,
                "evolution_instance": f"{args.tenant_id}-evo",
                "status": "pending",
            },
            "chatwoot": {
                "account_name": "Eleva Local",
                "inbox_name": f"{args.tenant_id}-inbox",
                "inbox_id": None,
                "status": "pending",
            },
        },
        "automation": {
            "n8n": {
                "mode": args.n8n_runtime_mode,
                "workflows": [
                    {
                        "name": f"{args.tenant_id}-wf-onboarding",
                        "purpose": "fluxo inicial de triagem",
                        "status": "planned",
                    }
                ],
            },
            "ai": {
                "agent_namespace": args.tenant_id,
                "prompt_set": f"{args.tenant_id}-default",
                "memory_scope": "isolated",
                "notes": "Nao compartilhar prompt, memoria ou credencial com outros tenants.",
            },
        },
        "provisioning": {
            "evolution": {
                "runtime_mode": "shared-foundation",
                "tenant_scope": "instance-per-tenant",
                "resource_name": f"{args.tenant_id}-evo",
                "naming_pattern": "cli-{slug}-evo",
                "credential_owner": "eleva-local-ops",
                "credential_scope": "tenant-exclusive",
                "rollout_checklist": [
                    "criar instancia Evolution nomeada pelo tenant_id",
                    "vincular numero WhatsApp exclusivo do tenant",
                    "registrar credenciais no inventario do tenant",
                    "validar webhook e teste de envio/recebimento",
                ],
            },
            "chatwoot": {
                "runtime_mode": "shared-foundation",
                "tenant_scope": "inbox-per-tenant",
                "resource_name": f"{args.tenant_id}-inbox",
                "naming_pattern": "cli-{slug}-inbox",
                "credential_owner": "eleva-local-ops",
                "credential_scope": "tenant-exclusive",
                "rollout_checklist": [
                    "criar inbox dedicada no Chatwoot",
                    "aplicar labels e automacoes com prefixo do tenant",
                    "registrar token e owner operacional no inventario do tenant",
                    "validar roteamento e recebimento na inbox correta",
                ],
            },
            "n8n": {
                "runtime_mode": args.n8n_runtime_mode,
                "tenant_scope": n8n_scope,
                "resource_name": f"{args.tenant_id}-wf",
                "naming_pattern": "cli-{slug}-wf-{dominio}",
                "credential_owner": "eleva-local-ops",
                "credential_scope": "tenant-exclusive",
                "rollout_checklist": n8n_rollout,
            },
        },
        "infrastructure": {
            "domains": {
                "customer_facing": args.customer_domain,
                "internal_webhook": args.internal_webhook_domain,
            },
            "integrations": {
                "evolution_api": "api.elevalocal.shop",
                "chatwoot": "chat.elevalocal.shop",
                "n8n": "n8m.elevalocal.shop",
            },
            "backup": {
                "included": True,
                "restore_drill_required": True,
                "last_restore_drill": None,
            },
        },
        "operations": {
            "onboarding_checklist": f"tenants/checklists/{args.tenant_id}-onboarding.md",
            "ops_checklist": f"tenants/checklists/{args.tenant_id}-ops.md",
            "secrets_inventory": f"tenants/secrets/{args.tenant_id}.md",
            "last_reviewed_at": None,
            "reviewed_by": None,
        },
        "security": {
            "secrets_segregated": True,
            "shared_credentials_allowed": False,
            "lgpd_notes": "Preencher observacoes de dados, retencao e acesso.",
        },
    }


def append_registry_entry(registry_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    registry = load_yaml(registry_path) or {
        "registry": {"version": 1},
        "tenants": [],
        "checks": {"required_per_tenant": []},
    }
    tenants = registry.setdefault("tenants", [])
    if not isinstance(tenants, list):
        raise ValueError("registry invalido: chave 'tenants' deve ser uma lista")

    for entry in tenants:
        if not isinstance(entry, dict):
            continue
        if entry.get("tenant_id") == args.tenant_id:
            raise ValueError(f"tenant_id ja existe no registry: {args.tenant_id}")
        if entry.get("slug") == args.slug:
            raise ValueError(f"slug ja existe no registry: {args.slug}")

    tenants.append(
        {
            "tenant_id": args.tenant_id,
            "slug": args.slug,
            "company_name": args.company_name,
            "status": args.status,
            "tier": args.plan,
            "owner": args.owner_email,
            "manifest_path": f"tenants/manifests/{args.tenant_id}.yaml",
            "secrets_inventory_path": f"tenants/secrets/{args.tenant_id}.md",
            "onboarding_status": "pending",
            "operations_status": "pending",
            "backup_status": "protected",
            "restore_status": "pending",
            "channels": {
                "whatsapp_number": args.whatsapp_number,
                "evolution_instance": f"{args.tenant_id}-evo",
                "chatwoot_inbox": f"{args.tenant_id}-inbox",
            },
            "automation": {
                "n8n_prefix": f"{args.tenant_id}-wf",
                "agent_namespace": args.tenant_id,
            },
            "provisioning": {
                "evolution_runtime_mode": "shared-foundation",
                "chatwoot_runtime_mode": "shared-foundation",
                "n8n_runtime_mode": args.n8n_runtime_mode,
            },
            "notes": "Tenant criado via ops/create-tenant.py",
        }
    )
    return registry


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace_root = args.workspace_root.resolve()

    if args.n8n_runtime_mode == "shared-foundation" and args.status != "internal":
        print(
            "ERRO: n8n em shared-foundation so e permitido para tenant com status internal",
            file=sys.stderr,
        )
        return 1

    templates_root = workspace_root / "tenants" / "templates"
    manifest_path = workspace_root / "tenants" / "manifests" / f"{args.tenant_id}.yaml"
    secrets_path = workspace_root / "tenants" / "secrets" / f"{args.tenant_id}.md"
    onboarding_path = workspace_root / "tenants" / "checklists" / f"{args.tenant_id}-onboarding.md"
    ops_path = workspace_root / "tenants" / "checklists" / f"{args.tenant_id}-ops.md"
    registry_path = (args.registry or (workspace_root / "tenants" / "registry.yaml")).resolve()

    for template_name in (
        "onboarding-checklist.md",
        "client-ops-checklist.md",
        "secrets-inventory.md",
    ):
        if not (templates_root / template_name).exists():
            print(f"ERRO: template ausente: {templates_root / template_name}", file=sys.stderr)
            return 1

    if manifest_path.exists() and not args.force:
        print(f"ERRO: manifest ja existe: {manifest_path}", file=sys.stderr)
        return 1

    try:
        registry = append_registry_entry(registry_path, args)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    manifest = build_manifest(args)
    onboarding_template = (templates_root / "onboarding-checklist.md").read_text(encoding="utf-8")
    ops_template = (templates_root / "client-ops-checklist.md").read_text(encoding="utf-8")
    secrets_template = (templates_root / "secrets-inventory.md").read_text(encoding="utf-8")

    if args.dry_run:
        preview_root = Path(tempfile.gettempdir()) / "elevalocal-create-tenant-dry-run" / args.tenant_id
        if preview_root.exists():
            shutil.rmtree(preview_root)

        preview_manifest_path = preview_root / "tenants" / "manifests" / f"{args.tenant_id}.yaml"
        preview_secrets_path = preview_root / "tenants" / "secrets" / f"{args.tenant_id}.md"
        preview_onboarding_path = (
            preview_root / "tenants" / "checklists" / f"{args.tenant_id}-onboarding.md"
        )
        preview_ops_path = preview_root / "tenants" / "checklists" / f"{args.tenant_id}-ops.md"
        preview_registry_path = preview_root / "tenants" / "registry.yaml"

        write_outputs(
            manifest_path=preview_manifest_path,
            secrets_path=preview_secrets_path,
            onboarding_path=preview_onboarding_path,
            ops_path=preview_ops_path,
            registry_path=preview_registry_path,
            manifest=manifest,
            registry=registry,
            company_name=args.company_name,
            tenant_id=args.tenant_id,
            slug=args.slug,
            onboarding_template=onboarding_template,
            ops_template=ops_template,
            secrets_template=secrets_template,
        )

        print(f"[dry-run] preview_root: {preview_root}")
        print(f"[dry-run] manifest: {preview_manifest_path}")
        print(f"[dry-run] registry: {preview_registry_path}")
        print(f"[dry-run] secrets: {preview_secrets_path}")
        print(f"[dry-run] onboarding: {preview_onboarding_path}")
        print(f"[dry-run] ops: {preview_ops_path}")
        return 0

    write_outputs(
        manifest_path=manifest_path,
        secrets_path=secrets_path,
        onboarding_path=onboarding_path,
        ops_path=ops_path,
        registry_path=registry_path,
        manifest=manifest,
        registry=registry,
        company_name=args.company_name,
        tenant_id=args.tenant_id,
        slug=args.slug,
        onboarding_template=onboarding_template,
        ops_template=ops_template,
        secrets_template=secrets_template,
    )

    print(f"Tenant criado: {args.tenant_id}")
    print(f"Manifest: {manifest_path}")
    print(f"Registry: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
