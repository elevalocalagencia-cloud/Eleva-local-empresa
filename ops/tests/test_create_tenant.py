from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "ops" / "create-tenant.py"


def write_file(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return path


def make_workspace(tmp_path: Path) -> Path:
    write_file(tmp_path / "tenants" / "templates" / "onboarding-checklist.md", "# onboarding template")
    write_file(tmp_path / "tenants" / "templates" / "client-ops-checklist.md", "# ops template")
    write_file(tmp_path / "tenants" / "templates" / "secrets-inventory.md", "# secrets template")
    write_file(
        tmp_path / "tenants" / "registry.yaml",
        """
        registry:
          version: 1
        tenants: []
        checks:
          required_per_tenant: []
        """,
    )
    return tmp_path


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


def test_create_tenant_generates_manifest_registry_and_checklists(tmp_path: Path) -> None:
    workspace = make_workspace(tmp_path)

    result = run_script(
        workspace,
        "--tenant-id",
        "cli-eleva-alpha",
        "--slug",
        "eleva-alpha",
        "--company-name",
        "Cliente Alpha LTDA",
        "--owner-name",
        "Fernando",
        "--owner-email",
        "fernando@cliente.com",
        "--owner-phone",
        "+5511999999999",
        "--whatsapp-number",
        "+5511999999999",
    )

    assert result.returncode == 0

    manifest_path = workspace / "tenants" / "manifests" / "cli-eleva-alpha.yaml"
    secrets_path = workspace / "tenants" / "secrets" / "cli-eleva-alpha.md"
    onboarding_path = workspace / "tenants" / "checklists" / "cli-eleva-alpha-onboarding.md"
    ops_path = workspace / "tenants" / "checklists" / "cli-eleva-alpha-ops.md"

    assert manifest_path.exists()
    assert secrets_path.exists()
    assert onboarding_path.exists()
    assert ops_path.exists()

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    assert manifest["tenant"]["tenant_id"] == "cli-eleva-alpha"
    assert manifest["tenant"]["slug"] == "eleva-alpha"
    assert manifest["channels"]["whatsapp"]["number_e164"] == "+5511999999999"
    assert manifest["naming"]["evolution_instance"] == "cli-eleva-alpha-evo"
    assert manifest["provisioning"]["evolution"]["runtime_mode"] == "shared-foundation"
    assert manifest["provisioning"]["n8n"]["runtime_mode"] == "dedicated"
    assert manifest["automation"]["n8n"]["mode"] == "dedicated"

    registry = yaml.safe_load((workspace / "tenants" / "registry.yaml").read_text(encoding="utf-8"))
    assert registry["tenants"][0]["tenant_id"] == "cli-eleva-alpha"
    assert registry["tenants"][0]["slug"] == "eleva-alpha"
    assert registry["tenants"][0]["manifest_path"] == "tenants/manifests/cli-eleva-alpha.yaml"
    assert registry["tenants"][0]["provisioning"]["n8n_runtime_mode"] == "dedicated"

    onboarding_text = onboarding_path.read_text(encoding="utf-8")
    secrets_text = secrets_path.read_text(encoding="utf-8")
    assert "# Onboarding Checklist - Cliente Alpha LTDA" in onboarding_text
    assert onboarding_text.count("# Onboarding Checklist") == 1
    assert "# Inventario de Segredos - Cliente Alpha LTDA" in secrets_text


def test_create_tenant_refuses_to_overwrite_existing_manifest_without_force(tmp_path: Path) -> None:
    workspace = make_workspace(tmp_path)
    write_file(
        workspace / "tenants" / "manifests" / "cli-eleva-alpha.yaml",
        """
        tenant:
          tenant_id: cli-eleva-alpha
          slug: eleva-alpha
        """,
    )

    result = run_script(
        workspace,
        "--tenant-id",
        "cli-eleva-alpha",
        "--slug",
        "eleva-alpha",
        "--company-name",
        "Cliente Alpha LTDA",
        "--owner-name",
        "Fernando",
        "--owner-email",
        "fernando@cliente.com",
        "--owner-phone",
        "+5511999999999",
        "--whatsapp-number",
        "+5511999999999",
    )

    assert result.returncode != 0
    assert "manifest ja existe" in result.stderr


def test_create_tenant_rejects_external_shared_foundation_n8n(tmp_path: Path) -> None:
    workspace = make_workspace(tmp_path)

    result = run_script(
        workspace,
        "--tenant-id",
        "cli-eleva-beta",
        "--slug",
        "eleva-beta",
        "--company-name",
        "Cliente Beta LTDA",
        "--owner-name",
        "Maria",
        "--owner-email",
        "maria@cliente.com",
        "--owner-phone",
        "+5511988888888",
        "--whatsapp-number",
        "+5511988888888",
        "--n8n-runtime-mode",
        "shared-foundation",
    )

    assert result.returncode != 0
    assert "shared-foundation so e permitido para tenant com status internal" in result.stderr


def test_create_tenant_allows_internal_shared_foundation_n8n(tmp_path: Path) -> None:
    workspace = make_workspace(tmp_path)

    result = run_script(
        workspace,
        "--tenant-id",
        "cli-eleva-gamma",
        "--slug",
        "eleva-gamma",
        "--company-name",
        "Cliente Gamma LTDA",
        "--owner-name",
        "Ana",
        "--owner-email",
        "ana@cliente.com",
        "--owner-phone",
        "+5511977777777",
        "--whatsapp-number",
        "+5511977777777",
        "--status",
        "internal",
        "--n8n-runtime-mode",
        "shared-foundation",
    )

    assert result.returncode == 0

    manifest = yaml.safe_load(
        (workspace / "tenants" / "manifests" / "cli-eleva-gamma.yaml").read_text(encoding="utf-8")
    )
    assert manifest["automation"]["n8n"]["mode"] == "shared-foundation"
    assert manifest["provisioning"]["n8n"]["runtime_mode"] == "shared-foundation"
    assert (
        manifest["provisioning"]["n8n"]["tenant_scope"] == "namespace-within-shared-stack"
    )
