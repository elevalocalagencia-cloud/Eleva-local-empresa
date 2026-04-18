# Restore Drill - 2026-Q2 - n8n-dedicated

- data: 2026-04-18
- owner: eleva-local-ops
- stack: n8n-dedicated
- modo: dry-run curto controlado
- snapshot_ou_backup: runtime `cli-eleva-pilot` + trilha valida de restore em [docs/N8N-DEDICATED-RUNBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/N8N-DEDICATED-RUNBOOK.md)
- target_rpo: 1h
- target_rto: 2h

## Execucao

1. Selecionado o stack `n8n dedicado` como drill inaugural do ciclo `2026-Q2`.
2. Validada a stack de referencia em [tenants/runtime/cli-eleva-pilot/docker-compose.yml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/runtime/cli-eleva-pilot/docker-compose.yml) e [tenants/runtime/cli-eleva-pilot/.env.example](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/runtime/cli-eleva-pilot/.env.example).
3. Executado `docker compose config` em ambiente temporario para verificar que o runtime pode ser remontado fora da producao.

## Resultado

- rpo_real: nao mensurado neste dry-run; baseline operacional continua sendo `1h` ate restore com snapshot real do host
- rto_real: 00h00m01s (`1122 ms`) para remontar e validar o runtime temporario local
- dentro_do_target: sim, para o ensaio de restauracao de configuracao; restore de dados continua dependente de execucao no host

## Evidencia

- ambiente_temporario: `C:\Users\PEDROSO\AppData\Local\Temp\elevalocal-drill-q2-n8n-dedicated`
- comandos:
  - `docker compose --env-file tenants/runtime/cli-eleva-pilot/.env.example -f tenants/runtime/cli-eleva-pilot/docker-compose.yml config`
- smoke: nao executado a partir desta sessao; os requests HTTP para `wf-pilot.elevalocal.shop` expiraram

## Acao

- decisao: manter target interno e exigir proximo drill com snapshot real do host
- proximo_passo: executar restore com artefato real da VPS no proximo ciclo trimestral ou em janela operacional controlada antes disso
