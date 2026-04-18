# STATE

## Fase atual

Readiness de launch em execucao. Bloqueio P0 de offsite backup foi fechado tecnicamente; proxima frente e provar `n8n dedicated` do tenant piloto antes de qualquer cliente externo.

Readiness de launch:

- operacao controlada: `SIM`
- readiness comercial ampla: `NAO`

## Status

- offsite backup real em `restic` ativo na VPS
- snapshot remoto `e77cf8f6` criado em Backblaze B2
- integridade validada por `restic check`
- restore controlado validado sem diferencas
- chave B2 rotacionada e validada
- runtime dedicado do `n8n` para `cli-eleva-pilot` preparado em codigo e documentacao
- deploy/cutover do `n8n` dedicado ainda nao executado
- tentativa de deploy sem `.env` real falhou de forma segura; nenhum container pilot subiu
- `main` contem `125bab1 fase1/n8n-dedicated: prepare pilot runtime`
- branch `codex/n8n-dedicated-success-checklist` contem `9b23bbc fase1/n8n-dedicated: mark success checklist`

## Proximo passo concreto

1. confirmar no painel Healthchecks se o check diario recebeu o ping do backup real
2. criar/configurar check semanal para `ops/restic-check.sh`
3. abrir PR da branch `codex/n8n-dedicated-success-checklist` se ainda nao estiver aberta
4. gerar `.env` real do runtime na VPS com `python3 ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop --force`
5. executar deploy controlado de `tenants/runtime/cli-eleva-pilot` com `docker compose --env-file .env up -d`
6. validar `curl -I https://wf-pilot.elevalocal.shop`, login owner, importacao manual de ao menos 1 workflow e smoke test
7. somente depois atualizar `tenants/manifests/cli-eleva-pilot.yaml` para `dedicated` em commit separado

## Snapshot de verificacao

- `restic snapshots` -> snapshot `e77cf8f6` listado
- `ops/restic-check.sh` -> `no errors were found`
- restore `e77cf8f6` em `/tmp/r` + `diff -qr` -> sem diferencas
- `pytest ops/tests -q` -> `13 passed`
- `docker compose ... config --quiet` do runtime n8n dedicado -> ok
- VPS: compose sem `.env` real falhou antes de criar container; `docker ps | grep pilot` vazio
