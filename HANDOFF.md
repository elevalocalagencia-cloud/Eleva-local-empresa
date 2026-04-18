# HANDOFF

## Escopo

Infraestrutura operacional da `Eleva Local` na VPS Hostinger. Este repo cobre stacks, runbooks, backup, tenant onboarding e readiness de launch.

## Estado atual

- `n8n`, `Chatwoot` e `Evolution` seguem operacionais no stack atual
- offsite backup com `restic` + Backblaze B2 foi ativado e validado
- snapshot remoto `e77cf8f6` existe e foi restaurado com sucesso
- chave B2 exposta durante a operacao foi rotacionada e validada
- runtime dedicado do `n8n` para o tenant interno `cli-eleva-pilot` foi preparado no repositorio, mas ainda nao foi deployado
- tentativa de deploy do runtime dedicado sem `.env` real falhou antes de criar container; nao houve impacto no shared
- o stack shared `n8n-mamtm8g3b2mdh7ko0hxdcyr3` nao deve ser alterado na fase de preparacao do dedicated

## O que ja foi provado

- backup offsite real roda em `BACKUP_MODE=restic`
- `restic snapshots` lista `e77cf8f6`
- `ops/restic-check.sh` retornou sem erros
- restore de `e77cf8f6` foi comparado contra o backup local sem diferencas
- runtime dedicado gera compose valido para `wf-pilot.elevalocal.shop`
- testes locais do repo passam com `13 passed`

## Proximo passo concreto

1. confirmar Healthchecks diario no painel
2. criar/configurar Healthchecks semanal para `ops/restic-check.sh`
3. abrir PR da branch `codex/n8n-dedicated-success-checklist`, se ainda nao foi aberta
4. na VPS, gerar `.env` real com `python3 ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop --force`
5. executar deploy controlado de `tenants/runtime/cli-eleva-pilot` com `docker compose --env-file .env up -d`
6. validar:
   - `curl -I https://wf-pilot.elevalocal.shop`
   - login owner
   - importacao manual de ao menos 1 workflow
   - `ops/smoke-test-tenant.sh`
   - shared `n8n-mamtm8g3b2mdh7ko0hxdcyr3` ainda no ar
7. apos migracao real, atualizar `tenants/manifests/cli-eleva-pilot.yaml` para `dedicated` em commit separado

## Observacoes operacionais

- nao usar `nano`/paste longo no console Hostinger para comandos complexos; ele mistura linhas
- preferir comandos curtos, SSH real ou arquivo pronto quando houver segredo
- nao commitar `.env` real de `ops/backup-elevalocal.env` nem `tenants/runtime/*/.env`
- manter Redis 7 como baseline do n8n; nao tentar rollback para Redis 6
