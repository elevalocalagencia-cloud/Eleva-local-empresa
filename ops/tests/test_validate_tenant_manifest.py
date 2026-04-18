from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "ops" / "validate-tenant-manifest.py"
PROVISIONING_BLOCK = """
provisioning:
  evolution:
    runtime_mode: shared-foundation
    tenant_scope: instance-per-tenant
    resource_name: cli-eleva-alpha-evo
    naming_pattern: cli-{slug}-evo
    credential_owner: eleva-local-ops
    credential_scope: tenant-exclusive
    rollout_checklist:
      - criar instancia Evolution
  chatwoot:
    runtime_mode: shared-foundation
    tenant_scope: inbox-per-tenant
    resource_name: cli-eleva-alpha-inbox
    naming_pattern: cli-{slug}-inbox
    credential_owner: eleva-local-ops
    credential_scope: tenant-exclusive
    rollout_checklist:
      - criar inbox dedicada
  n8n:
    runtime_mode: dedicated
    tenant_scope: workspace-per-tenant
    resource_name: cli-eleva-alpha-wf
    naming_pattern: cli-{slug}-wf-{dominio}
    credential_owner: eleva-local-ops
    credential_scope: tenant-exclusive
    rollout_checklist:
      - provisionar n8n dedicada
"""


def write_yaml(path: Path, content: str) -> Path:
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return path


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def make_manifest(slug: str = "eleva-alpha", provisioning_block: str = PROVISIONING_BLOCK) -> str:
    manifest = f"""
tenant:
  tenant_id: cli-eleva-alpha
  status: onboarding
  company_name: Cliente Alpha LTDA
  slug: {slug}
  owner:
    name: Fernando
    role: ops
    email: fernando@cliente.com
    phone: "+5511999999999"
naming:
  evolution_instance: cli-eleva-alpha-evo
  chatwoot_inbox: cli-eleva-alpha-inbox
  chatwoot_labels_prefix: cli-eleva-alpha
  n8n_prefix: cli-eleva-alpha-wf
  secrets_prefix: cli-eleva-alpha-secret
  backups_prefix: cli-eleva-alpha
channels:
  whatsapp:
    number_e164: "+5511999999999"
    display_name: Cliente Alpha
    evolution_instance: cli-eleva-alpha-evo
    status: pending
  chatwoot:
    account_name: Eleva Local
    inbox_name: cli-eleva-alpha-inbox
    inbox_id: null
    status: pending
automation:
  n8n:
    mode: dedicated
    workflows:
      - name: cli-eleva-alpha-wf-onboarding
        purpose: fluxo inicial
        status: planned
  ai:
    agent_namespace: cli-eleva-alpha
    prompt_set: cli-eleva-alpha-default
    memory_scope: isolated
{provisioning_block.strip()}
infrastructure:
  domains:
    customer_facing: alpha.elevalocal.shop
    internal_webhook: alpha-webhook.elevalocal.shop
  integrations:
    evolution_api: api.elevalocal.shop
    chatwoot: chat.elevalocal.shop
    n8n: n8m.elevalocal.shop
  backup:
    included: true
    restore_drill_required: true
    last_restore_drill: null
operations:
  onboarding_checklist: tenants/checklists/cli-eleva-alpha-onboarding.md
  ops_checklist: tenants/checklists/cli-eleva-alpha-ops.md
  secrets_inventory: tenants/secrets/cli-eleva-alpha.md
  last_reviewed_at: null
  reviewed_by: null
security:
  secrets_segregated: true
  shared_credentials_allowed: false
  lgpd_notes: sem observacoes
"""
    return textwrap.dedent(manifest)


def test_valid_nested_manifest_returns_zero(tmp_path: Path) -> None:
    manifest = write_yaml(tmp_path / "tenant.yaml", make_manifest())

    result = run_validator(str(manifest))

    assert result.returncode == 0
    assert "Manifest valido" in result.stdout


def test_missing_required_nested_sections_return_non_zero(tmp_path: Path) -> None:
    manifest = write_yaml(
        tmp_path / "tenant-missing.yaml",
        """
        tenant:
          tenant_id: cli-eleva-alpha
          company_name: Cliente Alpha LTDA
          slug: eleva-alpha
        naming:
          evolution_instance: cli-eleva-alpha-evo
        channels:
          chatwoot:
            inbox_name: cli-eleva-alpha-inbox
        """,
    )

    result = run_validator(str(manifest))

    assert result.returncode != 0
    assert "secao obrigatoria ausente: automation" in result.stderr
    assert "secao obrigatoria ausente: provisioning" in result.stderr
    assert "secao obrigatoria ausente: infrastructure" in result.stderr
    assert "secao obrigatoria ausente: operations" in result.stderr
    assert "secao obrigatoria ausente: security" in result.stderr


def test_invalid_slug_in_nested_manifest_returns_non_zero(tmp_path: Path) -> None:
    manifest = write_yaml(tmp_path / "tenant-invalid-slug.yaml", make_manifest(slug="Eleva Alpha"))

    result = run_validator(str(manifest))

    assert result.returncode != 0
    assert "campo 'tenant.slug' deve seguir o padrao kebab-case minusculo" in result.stderr


def test_invalid_provisioning_runtime_mode_returns_non_zero(tmp_path: Path) -> None:
    manifest = write_yaml(
        tmp_path / "tenant-invalid-provisioning.yaml",
        make_manifest(provisioning_block=PROVISIONING_BLOCK.replace("dedicated", "segregated", 1)),
    )

    result = run_validator(str(manifest))

    assert result.returncode != 0
    assert "campo 'provisioning.n8n.runtime_mode' deve ser um de" in result.stderr


def test_registry_duplicate_slug_returns_non_zero(tmp_path: Path) -> None:
    manifest = write_yaml(tmp_path / "tenant.yaml", make_manifest())
    registry = write_yaml(
        tmp_path / "registry.yaml",
        """
        tenants:
          - tenant_id: cli-eleva-bravo
            slug: eleva-alpha
            status: active
        """,
    )

    result = run_validator(str(manifest), "--registry", str(registry))

    assert result.returncode != 0
    assert "slug duplicado no registry" in result.stderr


def test_registry_allows_same_manifest_entry(tmp_path: Path) -> None:
    manifest = write_yaml(tmp_path / "cli-eleva-alpha.yaml", make_manifest())
    registry = write_yaml(
        tmp_path / "registry.yaml",
        f"""
        tenants:
          - tenant_id: cli-eleva-alpha
            slug: eleva-alpha
            manifest_path: {manifest.as_posix()}
            status: active
        """,
    )

    result = run_validator(str(manifest), "--registry", str(registry))

    assert result.returncode == 0
    assert "Registry validado" in result.stdout
