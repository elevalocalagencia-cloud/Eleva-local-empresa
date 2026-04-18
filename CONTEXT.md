# CONTEXT

## O que foi feito nesta sessao

- backup offsite P0 foi ativado na VPS com `restic` + Backblaze B2
- primeiro snapshot remoto foi criado no repositorio `b2:elevalocal-backups-prod:/prod`
- `restic check` rodou sem erros
- restore controlado do snapshot `e77cf8f6` foi executado e comparado com `diff -qr` sem diferencas
- chave B2 exposta durante a operacao foi rotacionada e validada com `restic snapshots`
- audit cleanup foi executado:
  - `.gitignore` endurecido
  - `docs/GIT-WORKFLOW.md` criado
  - caches `.pyc` removidos do indice
  - triagem A4 de historico feita sem suspeitos reais nos 200 primeiros matches
- runtime dedicado de `n8n` para `cli-eleva-pilot` foi preparado, sem deploy/cutover:
  - `ops/provision-n8n-dedicated.py`
  - `ops/smoke-test-tenant.sh`
  - `tenants/runtime/cli-eleva-pilot/docker-compose.yml`
  - `tenants/runtime/cli-eleva-pilot/.env.example`
  - `docs/N8N-DEDICATED-RUNBOOK.md`
  - `MIGRATION-PILOT.md`
- branch `codex/n8n-dedicated-success-checklist` foi criada para marcar checklist de criterio de sucesso comprovado
- na VPS, `git pull origin main` trouxe o runtime dedicado para `/root/elevalocal-infra`
- tentativa de `docker compose up -d` em `tenants/runtime/cli-eleva-pilot` falhou antes de subir containers porque `.env` real nao existia no runtime e as variaveis ficaram vazias

## Validacoes executadas

- `restic snapshots` na VPS -> snapshot `e77cf8f6` listado
- `ops/restic-check.sh` na VPS -> `no errors were found`
- `restic restore e77cf8f6 --target /tmp/r` na VPS -> 16 arquivos/diretorios restaurados
- `diff -qr /root/eleva-backups/2026-04-18-002614 /tmp/r/root/eleva-backups/2026-04-18-002614` -> sem diferencas
- `restic snapshots` apos rotacao da chave B2 -> repositorio abriu e snapshot foi listado
- `python ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --dry-run` -> compose esperado impresso
- `python -m py_compile ops/provision-n8n-dedicated.py` -> ok
- `bash -n ops/smoke-test-tenant.sh` -> ok
- `docker compose --env-file tenants/runtime/cli-eleva-pilot/.env -f tenants/runtime/cli-eleva-pilot/docker-compose.yml config --quiet` -> ok
- `python ops/validate-tenant-manifest.py tenants/manifests/cli-eleva-pilot.yaml --registry tenants/registry.yaml` -> valido
- `pytest ops/tests -q` -> `13 passed`
- VPS: `docker compose up -d` sem `.env` real -> falhou com variaveis `N8N_IMAGE`, `POSTGRES_IMAGE`, `REDIS_IMAGE` vazias; `docker ps | grep pilot` nao retornou container

## Riscos ainda abertos

- Healthchecks diario deve ser conferido no painel para confirmar ping do backup real
- ainda falta criar ou configurar um segundo check semanal para `ops/restic-check.sh`
- `wf-pilot.elevalocal.shop` ainda nao foi deployado nem validado com certificado
- login owner, importacao de workflow e smoke 100% no `n8n` dedicado ainda nao foram executados
- antes do deploy dedicated na VPS, gerar `.env` real com `python3 ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop --force`
- `tenants/manifests/cli-eleva-pilot.yaml` ainda deve permanecer `shared-foundation` ate a migracao real ser executada
- PR nao foi aberto automaticamente porque `gh` nao esta instalado e nao havia `GH_TOKEN/GITHUB_TOKEN`; a branch foi pushada e a tela de PR foi aberta
