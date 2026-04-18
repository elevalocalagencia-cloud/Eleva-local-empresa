# STATE

## Fase atual

Fase 2.0 concluida no codigo: provisioner do `n8n dedicated` corrigido apos os hotfixes manuais da VPS. A proxima frente e Prompt 2.1 Observability, depois de PR/merge da correcao ou decisao explicita de seguir na branch.

Readiness de launch:

- operacao controlada: `SIM`
- readiness comercial ampla: `NAO`

## Status

- offsite backup real em `restic` + Backblaze B2 segue validado
- `n8n` dedicado do `cli-eleva-pilot` responde em `https://wf-pilot.elevalocal.shop`
- smoke HTTP do tenant passou com health/login ok e webhook `404` esperado antes de importar workflow de smoke
- provisioner corrigido para evitar colisao Redis na rede Coolify
- provisioner corrigido para gerar labels Traefik compativeis com Coolify
- dry-run de `cli-demo-externo` confirmou que novos tenants usam o mesmo padrao corrigido
- branch atual: `codex/n8n-dedicated-success-checklist`
- ultimo commit funcional pushado: `392d660 fase2/0.1 provisioner n8n: fix redis collision + coolify labels`

## Proximo passo concreto

1. abrir ou revisar PR da branch `codex/n8n-dedicated-success-checklist` contra `main`
2. apos merge, atualizar a VPS com `git pull origin main` em `/root/elevalocal-infra`
3. seguir para Prompt 2.1 Observability
4. registrar evidencia de login owner e importacao manual de ao menos 1 workflow no `wf-pilot.elevalocal.shop`
5. manter `tenants/manifests/cli-eleva-pilot.yaml` em `shared-foundation` ate cutover/migracao real; mudar para `dedicated` apenas em commit separado
6. configurar/conferir Healthchecks semanal para `ops/restic-check.sh`
7. tratar backlog P0 de Chatwoot freeze para remover `latest`

## Snapshot de verificacao

- `curl.exe -I --max-time 20 https://wf-pilot.elevalocal.shop` -> `HTTP/1.1 200 OK`
- `bash ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop` -> `SMOKE_OK tenant=cli-eleva-pilot`
- `python -m py_compile ops/provision-n8n-dedicated.py` -> ok
- `pytest ops/tests -q` -> `13 passed`
- `docker compose ... config --quiet` do runtime `cli-eleva-pilot` -> ok
- dry-run `cli-demo-externo` -> Redis namespaced + labels Coolify corretas
