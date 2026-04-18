# HANDOFF

## Escopo

Infraestrutura operacional da `Eleva Local` na VPS Hostinger. Este repo cobre stacks, runbooks, backup, tenant onboarding e readiness de launch.

## Estado atual

- `n8n`, `Chatwoot` e `Evolution` compartilhados seguem como rollback operacional
- offsite backup com `restic` + Backblaze B2 foi ativado e validado anteriormente
- `n8n` dedicado do tenant interno `cli-eleva-pilot` esta no ar em `https://wf-pilot.elevalocal.shop`
- compose vivo da VPS precisou de hotfix manual; provisioner ja foi corrigido para reproduzir esse padrao
- PR aberto com a correcao: `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`
- Redis do n8n dedicated deve ser sempre namespaced por tenant para evitar colisao via rede Coolify
- Traefik do Coolify deve usar `entrypoints=http`/`entrypoints=https`, redirect middleware, `tls=true` e `router.service=<service>`
- o stack shared `n8n-mamtm8g3b2mdh7ko0hxdcyr3` nao deve ser alterado durante observability e preparacao de cutover

## O que ja foi provado

- dominio `https://wf-pilot.elevalocal.shop` responde `HTTP 200`
- smoke script do tenant retorna `SMOKE_OK`
- provisioner gera compose valido para o pilot e para `cli-demo-externo`
- testes locais do repo passam com `13 passed`
- compose do runtime `cli-eleva-pilot` passa em `docker compose config --quiet`

## Proximo passo concreto

1. revisar/mergear PR `https://github.com/elevalocalagencia-cloud/Eleva-local-empresa/pull/1`
2. apos merge, atualizar a copia da VPS com `git pull origin main`
3. executar Prompt 2.1 Observability
4. registrar evidencia de login owner e importacao manual de ao menos 1 workflow no dedicated
5. manter `tenants/manifests/cli-eleva-pilot.yaml` em `shared-foundation` ate cutover real; mudar para `dedicated` em commit separado
6. configurar/conferir Healthchecks semanal para `ops/restic-check.sh`
7. tratar Chatwoot freeze para substituir imagem `latest`

## Observacoes operacionais

- nao usar `nano`/paste longo no console Hostinger para comandos complexos; ele mistura linhas
- preferir comandos curtos, SSH real ou arquivo pronto quando houver segredo
- nao commitar `.env` real de `ops/backup-elevalocal.env` nem `tenants/runtime/*/.env`
- manter Redis 7 como baseline do n8n; nao tentar rollback para Redis 6
