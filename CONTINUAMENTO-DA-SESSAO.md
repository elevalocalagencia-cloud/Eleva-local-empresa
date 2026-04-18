# CONTINUAMENTO DA SESSAO

## Ponto em que parou

O `n8n dedicated` do `cli-eleva-pilot` esta no ar em `https://wf-pilot.elevalocal.shop` e respondeu `HTTP 200` a partir do ambiente local.

Os dois bugs descobertos no deploy manual da VPS foram corrigidos no provisioner:

- Redis deixou de ser `redis` generico e passou a ser namespaced por tenant
- labels Traefik passaram para o padrao Coolify com HTTP redirect, `entrypoints=https`, `tls=true` e `router.service`

Commit pushado:

- `392d660 fase2/0.1 provisioner n8n: fix redis collision + coolify labels`

PR aberto:

- `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`

## Proximo passo imediato

1. revisar/mergear PR `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`
2. depois do merge, fazer `git pull origin main` na VPS em `/root/elevalocal-infra`
3. iniciar Prompt 2.1 Observability
4. registrar evidencia de login owner e importacao manual de 1 workflow no dedicated
5. so depois de cutover/migracao real atualizar `tenants/manifests/cli-eleva-pilot.yaml` para `dedicated`

## Comandos de retomada

```bash
git status --short --branch
git log --oneline -5
pytest ops/tests -q
python ops/provision-n8n-dedicated.py --tenant-id cli-demo-externo --domain wf-demo-externo.elevalocal.shop --dry-run
bash ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop
```

Na VPS, apos merge:

```bash
cd /root/elevalocal-infra
git pull origin main
```

## Arquivos de retomada

- `ops/provision-n8n-dedicated.py`
- `ops/tests/test_provision_n8n_dedicated.py`
- `tenants/runtime/cli-eleva-pilot/docker-compose.yml`
- `docs/N8N-DEDICATED-RUNBOOK.md`
- `MIGRATION-PILOT.md`
- `tenants/manifests/cli-eleva-pilot.yaml`

## Travas abertas

- PR aberto e aguardando revisao/merge
- manifest do pilot ainda deve permanecer `shared-foundation` ate migracao/cutover real
- webhook smoke retorna `404` ate importar workflow de smoke
- Healthchecks semanal do `restic-check` ainda falta
- Chatwoot freeze ainda pendente porque stack segue em `latest`
