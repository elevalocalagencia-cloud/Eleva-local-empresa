# Restore Drill Playbook

## Objetivo

Formalizar a rotina trimestral de restore drill da Eleva Local.

O drill existe para validar se os targets definidos em
[docs/RPO-RTO.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RPO-RTO.md)
seguem factiveis, e para detectar cedo quando um stack deixou de ser
recuperavel no tempo esperado.

## Cadencia trimestral

Datas baseadas em `2026-04-18`:

- `2026-Q2`: `2026-06-18`
- `2026-Q3`: `2026-09-18`
- `2026-Q4`: `2026-12-18`
- `2027-Q1`: `2027-03-18`

## Checklist por drill

1. escolher 1 stack aleatorio:

```bash
printf '%s\n' \
  'n8n-shared-foundation' \
  'n8n-dedicated' \
  'chatwoot' \
  'evolution-api' \
  'postgres-shared' \
  'portal-supabase' | shuf -n 1
```

2. executar restore em ambiente temporario, nunca em producao
3. cronometrar o `RTO` real do exercicio
4. validar qual o ultimo registro recuperado e calcular `RPO` real
5. comparar `RPO/RTO` reais com
   [docs/RPO-RTO.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RPO-RTO.md)
6. registrar evidencia em
   `tenants/evidence/_drills/{YYYY-QN}-{stack}.md`
7. se houver divergencia material, atualizar a documentacao e o ledger

## Regras do exercicio

- o ambiente de restore deve ser temporario e isolado
- nao reutilizar diretamente o stack de producao
- registrar data, owner, snapshot usado e stack escolhido
- manter output de comandos relevante no relatorio

## Regra de escalonamento

Se 2 drills consecutivos falharem no mesmo stack:

1. reclassificar o stack como `P0`
2. congelar onboarding de novo cliente ate correcao
3. abrir trilha de investigacao tecnica antes do proximo ciclo

## Template de relatorio

```md
# Restore Drill - {{QUARTER}} - {{STACK}}

- data: {{DATE}}
- owner: {{OWNER}}
- stack: {{STACK}}
- modo: {{MODE}}
- snapshot_ou_backup: {{SNAPSHOT}}
- target_rpo: {{TARGET_RPO}}
- target_rto: {{TARGET_RTO}}

## Execucao

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

## Resultado

- rpo_real: {{RPO_REAL}}
- rto_real: {{RTO_REAL}}
- dentro_do_target: {{YES_NO}}

## Evidencia

- ambiente_temporario: {{TEMP_ENV}}
- comandos: {{COMMANDS}}
- smoke: {{SMOKE}}

## Acao

- decisao: {{DECISION}}
- proximo_passo: {{NEXT_STEP}}
```

## Inaugural `2026-Q2`

O primeiro registro formal desta cadencia esta em:

- [tenants/evidence/_drills/2026-Q2-n8n-dedicated.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/_drills/2026-Q2-n8n-dedicated.md)
