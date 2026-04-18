# RPO / RTO

## Definicoes

### O que e RPO

RPO e a perda maxima de dados que a operacao aceita em um incidente.

Em termos simples: se um stack cair e precisarmos restaurar backup, o RPO diz
qual o atraso maximo aceitavel entre o ultimo dado valido recuperado e o
momento da falha.

Exemplo: `RPO 1h` significa que, no pior caso, ate 1 hora de dados recentes
pode precisar ser reprocessada manualmente.

### O que e RTO

RTO e o tempo maximo alvo para recolocar um stack em condicao operacional
controlada.

Em termos simples: e quanto tempo a operacao aceita ficar sem aquele stack ate
ter uma recuperacao funcional.

Exemplo: `RTO 4h` significa que a meta interna e restaurar o stack em ate 4
horas, incluindo triagem, restauracao e smoke test basico.

## Targets por stack

| Stack | RPO target | RTO target | Fonte de backup | Caminho de restore |
| --- | --- | --- | --- | --- |
| n8n compartilhado (`shared-foundation`) | 1h | 4h | Restic+B2 | [docs/RESTIC-RUNBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTIC-RUNBOOK.md) |
| n8n dedicado (por tenant) | 1h | 2h | Restic+B2 | [docs/N8N-DEDICATED-RUNBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/N8N-DEDICATED-RUNBOOK.md) |
| Chatwoot | 1h | 4h | Restic+B2 | [docs/RESTIC-RUNBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTIC-RUNBOOK.md) |
| Evolution API | 4h | 4h | Restic+B2 (snapshot Redis/SQLite) | [docs/RESTIC-RUNBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTIC-RUNBOOK.md) |
| Postgres (pilot + shared) | 1h | 2h | pg_dump diario + Restic | [BACKUP-RESTORE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-RESTORE.md) |
| Portal Supabase | 24h | 8h | snapshot Supabase gerenciado | a definir em 3.1 |

## Justificativas dos targets

### n8n compartilhado (`shared-foundation`) - RPO 1h / RTO 4h

O `n8n shared` concentra mais dependencias e maior blast radius operacional.
Por isso, o tempo de restauracao alvo e mais folgado que no dedicado. O alvo de
`1h` de RPO parte da rotina de backup e do fato de que prometer `15min` hoje
seria especulativo, sem trilha real de snapshot e replay nesse intervalo.

### n8n dedicado (por tenant) - RPO 1h / RTO 2h

O dedicado tem escopo menor, menos dependencia cruzada e restore mais objetivo
por tenant. O `RTO 2h` e mais agressivo que no shared porque o volume de
decisao e menor e o rollback tende a ser mais curto. Ainda assim, `1h` de RPO e
mais realista que `15min`, porque a operacao atual nao foi desenhada para
replicacao continua nem replay fino.

### Chatwoot - RPO 1h / RTO 4h

O `Chatwoot` envolve app, `sidekiq`, Postgres e Redis. O restore exige
validacao funcional alem do banco. Por isso o `RTO` fica em `4h`, nao `1h`.
`RPO 1h` segue a mesma disciplina do backup offsite e evita prometer
granularidade que o stack nao demonstrou.

### Evolution API - RPO 4h / RTO 4h

O maior risco aqui nao e so banco; e o estado das instancias e reconexao. Por
isso o `RPO` e menos agressivo: `4h`. Um alvo menor hoje seria otimista demais.
O `RTO 4h` considera restauracao do estado e validacao basica de conexao.

### Postgres (pilot + shared) - RPO 1h / RTO 2h

O Postgres tem caminho de backup e restore mais deterministico que os apps que
dependem dele. Por isso o `RTO 2h` e plausivel como alvo interno. O `RPO 1h`
continua prudente porque a rotina atual e orientada por dumps e Restic, nao por
replicacao continua.

### Portal Supabase - RPO 24h / RTO 8h

O portal depende de restore gerenciado por terceiro. Sem plano proprio
documentado ainda, o alvo precisa ser conservador. `24h` de RPO e `8h` de RTO
servem como baseline interno ate a fase `3.1`, quando o restore do portal sera
formalizado com mais precisao.

## Premissas

1. Estes targets sao internos e nao contratuais enquanto nao houver cliente
   real coberto por SLA assinado.
2. O drill trimestral valida se os targets continuam factiveis na pratica.
3. Se o drill mostrar numero pior de forma recorrente, o target deve ser
   revisado para cima antes de virar promessa externa.
4. O objetivo operacional e preservar blast radius por tenant: restaurar um
   tenant nao deve exigir parada de outro cliente.

## Dependencias externas

- Backblaze B2 (`offsite`)
- Hostinger VPS (`primary`)
- Supabase (`portal`)
- LetsEncrypt (`TLS`)

## Gaps conhecidos

- nao ha plano de contingencia para perda total da Hostinger
- nao ha regiao secundaria de restore
- restore do portal depende de `Supabase` gerenciado por terceiro

## Regra de revisao

- revisar este documento a cada drill trimestral
- registrar divergencia material em
  [docs/RESTORE-DRILL-PLAYBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTORE-DRILL-PLAYBOOK.md)
- refletir mudancas relevantes no
  [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)
