#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PHONE_RE = re.compile(r"^\+?[1-9]\d{7,14}$")
REQUIRED_SECTIONS = (
    "tenant",
    "naming",
    "channels",
    "automation",
    "provisioning",
    "infrastructure",
    "operations",
    "security",
)
REQUIRED_NAMING_FIELDS = (
    "evolution_instance",
    "chatwoot_inbox",
    "chatwoot_labels_prefix",
    "n8n_prefix",
    "secrets_prefix",
    "backups_prefix",
)
REQUIRED_PROVISIONING_STACKS = ("evolution", "chatwoot", "n8n")
VALID_RUNTIME_MODES = {"shared-foundation", "dedicated"}
VALID_CREDENTIAL_SCOPES = {"tenant-exclusive", "shared-readonly", "shared-ops"}


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"arquivo nao encontrado: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"yaml invalido em {path}: {exc}") from exc


def ensure_mapping(value: Any, field: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict) or not value:
        errors.append(f"campo '{field}' deve ser um objeto nao-vazio")
        return None
    return value


def ensure_string(value: Any, field: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"campo '{field}' deve ser uma string nao-vazia")
        return None
    return value.strip()


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest deve ser um objeto YAML no topo do arquivo"]

    for section in REQUIRED_SECTIONS:
        if section not in data:
            errors.append(f"secao obrigatoria ausente: {section}")

    if errors:
        return errors

    tenant = ensure_mapping(data.get("tenant"), "tenant", errors)
    naming = ensure_mapping(data.get("naming"), "naming", errors)
    channels = ensure_mapping(data.get("channels"), "channels", errors)
    automation = ensure_mapping(data.get("automation"), "automation", errors)
    provisioning = ensure_mapping(data.get("provisioning"), "provisioning", errors)
    infrastructure = ensure_mapping(data.get("infrastructure"), "infrastructure", errors)
    operations = ensure_mapping(data.get("operations"), "operations", errors)
    security = ensure_mapping(data.get("security"), "security", errors)

    if not all(
        (tenant, naming, channels, automation, provisioning, infrastructure, operations, security)
    ):
        return errors

    tenant_id = ensure_string(tenant.get("tenant_id"), "tenant.tenant_id", errors)
    slug = ensure_string(tenant.get("slug"), "tenant.slug", errors)
    ensure_string(tenant.get("company_name"), "tenant.company_name", errors)
    owner = ensure_mapping(tenant.get("owner"), "tenant.owner", errors)

    if owner:
        ensure_string(owner.get("name"), "tenant.owner.name", errors)
        ensure_string(owner.get("email"), "tenant.owner.email", errors)
        phone = ensure_string(owner.get("phone"), "tenant.owner.phone", errors)
        if phone and not PHONE_RE.fullmatch(phone):
            errors.append(
                "campo 'tenant.owner.phone' deve ser string em formato internacional "
                "(ex: +5511999999999)"
            )

    if slug and not SLUG_RE.fullmatch(slug):
        errors.append(
            "campo 'tenant.slug' deve seguir o padrao kebab-case minusculo "
            "(ex: cliente-alpha)"
        )

    if tenant_id and not tenant_id.startswith("cli-"):
        errors.append("campo 'tenant.tenant_id' deve comecar com 'cli-'")

    for field in REQUIRED_NAMING_FIELDS:
        ensure_string(naming.get(field), f"naming.{field}", errors)

    whatsapp = ensure_mapping(channels.get("whatsapp"), "channels.whatsapp", errors)
    chatwoot = ensure_mapping(channels.get("chatwoot"), "channels.chatwoot", errors)
    if whatsapp:
        whatsapp_number = ensure_string(
            whatsapp.get("number_e164"), "channels.whatsapp.number_e164", errors
        )
        if whatsapp_number and not PHONE_RE.fullmatch(whatsapp_number):
            errors.append(
                "campo 'channels.whatsapp.number_e164' deve ser string em formato "
                "internacional (ex: +5511999999999)"
            )
        ensure_string(
            whatsapp.get("evolution_instance"),
            "channels.whatsapp.evolution_instance",
            errors,
        )
    if chatwoot:
        ensure_string(chatwoot.get("inbox_name"), "channels.chatwoot.inbox_name", errors)

    n8n = ensure_mapping(automation.get("n8n"), "automation.n8n", errors)
    ai = ensure_mapping(automation.get("ai"), "automation.ai", errors)
    if n8n:
        ensure_string(n8n.get("mode"), "automation.n8n.mode", errors)
        workflows = n8n.get("workflows")
        if not isinstance(workflows, list):
            errors.append("campo 'automation.n8n.workflows' deve ser uma lista")
    if ai:
        ensure_string(ai.get("agent_namespace"), "automation.ai.agent_namespace", errors)
        ensure_string(ai.get("memory_scope"), "automation.ai.memory_scope", errors)

    for stack in REQUIRED_PROVISIONING_STACKS:
        config = ensure_mapping(provisioning.get(stack), f"provisioning.{stack}", errors)
        if not config:
            continue

        runtime_mode = ensure_string(
            config.get("runtime_mode"), f"provisioning.{stack}.runtime_mode", errors
        )
        ensure_string(config.get("tenant_scope"), f"provisioning.{stack}.tenant_scope", errors)
        ensure_string(config.get("resource_name"), f"provisioning.{stack}.resource_name", errors)
        ensure_string(config.get("naming_pattern"), f"provisioning.{stack}.naming_pattern", errors)
        credential_scope = ensure_string(
            config.get("credential_scope"), f"provisioning.{stack}.credential_scope", errors
        )
        ensure_string(config.get("credential_owner"), f"provisioning.{stack}.credential_owner", errors)
        rollout_checklist = config.get("rollout_checklist")

        if runtime_mode and runtime_mode not in VALID_RUNTIME_MODES:
            errors.append(
                f"campo 'provisioning.{stack}.runtime_mode' deve ser um de: "
                f"{', '.join(sorted(VALID_RUNTIME_MODES))}"
            )
        if credential_scope and credential_scope not in VALID_CREDENTIAL_SCOPES:
            errors.append(
                f"campo 'provisioning.{stack}.credential_scope' deve ser um de: "
                f"{', '.join(sorted(VALID_CREDENTIAL_SCOPES))}"
            )
        if not isinstance(rollout_checklist, list) or not rollout_checklist:
            errors.append(
                f"campo 'provisioning.{stack}.rollout_checklist' deve ser uma lista nao-vazia"
            )

    domains = ensure_mapping(infrastructure.get("domains"), "infrastructure.domains", errors)
    integrations = ensure_mapping(
        infrastructure.get("integrations"), "infrastructure.integrations", errors
    )
    backup = ensure_mapping(infrastructure.get("backup"), "infrastructure.backup", errors)
    if domains:
        customer_facing = domains.get("customer_facing")
        if customer_facing is not None:
            ensure_string(customer_facing, "infrastructure.domains.customer_facing", errors)
    if integrations:
        for field in ("evolution_api", "chatwoot", "n8n"):
            ensure_string(integrations.get(field), f"infrastructure.integrations.{field}", errors)
    if backup:
        included = backup.get("included")
        restore_required = backup.get("restore_drill_required")
        if not isinstance(included, bool):
            errors.append("campo 'infrastructure.backup.included' deve ser booleano")
        if not isinstance(restore_required, bool):
            errors.append(
                "campo 'infrastructure.backup.restore_drill_required' deve ser booleano"
            )

    ensure_string(
        operations.get("onboarding_checklist"), "operations.onboarding_checklist", errors
    )
    ensure_string(operations.get("ops_checklist"), "operations.ops_checklist", errors)
    ensure_string(operations.get("secrets_inventory"), "operations.secrets_inventory", errors)

    if not isinstance(security.get("secrets_segregated"), bool):
        errors.append("campo 'security.secrets_segregated' deve ser booleano")
    if not isinstance(security.get("shared_credentials_allowed"), bool):
        errors.append("campo 'security.shared_credentials_allowed' deve ser booleano")

    return errors


def iter_registry_entries(data: Any) -> list[dict[str, Any]]:
    if data is None:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        tenants = data.get("tenants")
        if isinstance(tenants, list):
            return [item for item in tenants if isinstance(item, dict)]
    raise ValueError("registry deve ser uma lista YAML ou um objeto com chave 'tenants'")


def validate_registry_uniqueness(
    manifest: dict[str, Any],
    registry: Any,
    manifest_path: Path | None = None,
    registry_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    entries = iter_registry_entries(registry)
    manifest_tenant = manifest.get("tenant", {})
    manifest_slug = manifest_tenant.get("slug")
    manifest_tenant_id = manifest_tenant.get("tenant_id")
    manifest_path_resolved = manifest_path.resolve() if manifest_path else None

    for index, entry in enumerate(entries):
        entry_slug = entry.get("slug")
        entry_tenant_id = entry.get("tenant_id")
        entry_manifest_path = entry.get("manifest_path")
        if manifest_path_resolved and isinstance(entry_manifest_path, str):
            try:
                resolved_entry_path = Path(entry_manifest_path)
                if not resolved_entry_path.is_absolute() and registry_path:
                    resolved_entry_path = (
                        registry_path.resolve().parent.parent / resolved_entry_path
                    ).resolve()
                else:
                    resolved_entry_path = resolved_entry_path.resolve()

                if resolved_entry_path == manifest_path_resolved:
                    continue
            except OSError:
                pass
        if entry_slug == manifest_slug:
            errors.append(f"slug duplicado no registry na entrada {index}: {entry_slug}")
        if entry_tenant_id == manifest_tenant_id:
            errors.append(
                f"tenant_id duplicado no registry na entrada {index}: {entry_tenant_id}"
            )

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valida manifest YAML de tenant para a operacao multi-cliente."
    )
    parser.add_argument("manifest", type=Path, help="caminho do manifest YAML do tenant")
    parser.add_argument(
        "--registry",
        type=Path,
        help="caminho opcional do registry YAML para validar unicidade de tenant_id/slug",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        manifest_data = load_yaml(args.manifest)
        errors = validate_manifest(manifest_data)

        if not errors and args.registry:
            registry_data = load_yaml(args.registry)
            errors.extend(
                validate_registry_uniqueness(
                    manifest_data,
                    registry_data,
                    manifest_path=args.manifest,
                    registry_path=args.registry,
                )
            )
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1

    print(f"Manifest valido: {args.manifest}")
    if args.registry:
        print(f"Registry validado: {args.registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
