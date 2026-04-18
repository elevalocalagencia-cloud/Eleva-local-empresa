# CONTEXT

## O que foi feito nesta sessao

- `n8n` dedicado do tenant interno `cli-eleva-pilot` ficou operacional em producao:
  - dominio: `https://wf-pilot.elevalocal.shop`
  - stack dedicada: `n8n` + `n8n-worker` + `postgresql` + Redis proprio
  - rede dedicada: `cli-eleva-pilot-net`
- o deploy na VPS exigiu dois hotfixes manuais no compose vivo; esses bugs foram corrigidos no repo:
  - Redis agora e namespaced por tenant, ex: `cli-eleva-pilot-redis`
  - `QUEUE_BULL_REDIS_HOST` aponta para o Redis namespaced
  - labels Traefik seguem o padrao Coolify: `entrypoints=http`, redirect para HTTPS, `entrypoints=https`, `tls=true`, `router.service=<service>` e service dedicado na porta `5678`
- `ops/provision-n8n-dedicated.py` foi corrigido e coberto por testes
- `tenants/runtime/cli-eleva-pilot/docker-compose.yml` foi regenerado com o padrao correto
- dry-run do tenant `cli-demo-externo` validou que novos tenants saem com o mesmo padrao Coolify/Redis namespaced
- `docs/N8N-DEDICATED-RUNBOOK.md` recebeu a licao aprendida do deploy real
- commit da correcao foi criado e pushado:
  - `392d660 fase2/0.1 provisioner n8n: fix redis collision + coolify labels`
- PR aberto:
  - `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`
- deploy/pull na VPS nao foi executado a partir deste ambiente porque SSH para `root@2.24.199.157:22` deu timeout

## Validacoes executadas

- `curl.exe -I --max-time 20 https://wf-pilot.elevalocal.shop` -> `HTTP/1.1 200 OK`
- `bash ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop` -> `SMOKE_OK tenant=cli-eleva-pilot`
- `python -m py_compile ops/provision-n8n-dedicated.py` -> ok
- `pytest ops/tests -q` -> `13 passed`
- `python ops/provision-n8n-dedicated.py --tenant-id cli-demo-externo --domain wf-demo-externo.elevalocal.shop --dry-run` -> output contem Redis namespaced e labels Coolify corretas
- `docker compose --env-file tenants/runtime/cli-eleva-pilot/.env -f tenants/runtime/cli-eleva-pilot/docker-compose.yml config --quiet` -> ok
- `git diff --check` -> sem erro

## Riscos ainda abertos

- `tenants/manifests/cli-eleva-pilot.yaml` ainda esta em `shared-foundation`; so mudar para `dedicated` em commit separado depois da migracao/importacao real de workflow e cutover combinados
- login owner e importacao manual de ao menos 1 workflow no dedicated ainda precisam ser registrados como evidencia
- webhook de smoke ainda retorna `404`, esperado enquanto o workflow de smoke nao for importado
- PR aberto e pronto para revisao/merge: `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`
- deploy do codigo corrigido na VPS depende de merge do PR e acesso SSH/console para rodar `git pull origin main`
- Healthchecks semanal para `ops/restic-check.sh` ainda precisa ser configurado/conferido
- Chatwoot ainda tem backlog P0 de version freeze porque segue em `latest`
