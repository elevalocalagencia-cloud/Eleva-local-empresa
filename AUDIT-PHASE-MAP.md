# Audit Phase Map

## Objetivo

Consolidar os entregaveis do bootstrap de auditoria antes de qualquer execucao
em producao.

Este documento responde:

- fase atual da operacao
- riscos principais
- stacks em producao
- tenants cadastrados
- arquivos-alvo das proximas fases
- matriz de comandos de validacao por stack
- ownership operacional atual documentado

## Resumo executivo em 10 linhas

1. Fase atual: fundacao multi-cliente em execucao com readiness comercial ainda `NO-GO`.
2. A operacao ja e utilizavel em modo controlado, mas ainda nao pronta para venda em escala.
3. O maior risco atual continua sendo cross-tenant via `n8n`.
4. O segundo risco principal e credencial/segredo ainda sem rotacao formal pos-investigacao.
5. O terceiro risco principal e disaster recovery incompleto por falta de offsite validado.
6. Stacks em producao hoje: `n8n`, `Chatwoot` e `Evolution API`.
7. Dominios operacionais conhecidos: `n8m.elevalocal.shop`, `chat.elevalocal.shop`, `api.elevalocal.shop`.
8. Tenant interno cadastrado: `cli-eleva-pilot`.
9. Tenant externo de simulacao cadastrado: `cli-demo-externo`.
10. Proximo passo operacional real: primeiro provisionamento externo com `n8n dedicated`.

## Stacks em producao

| Stack | Dominio operacional | Estado documental |
| --- | --- | --- |
| `n8n` | `https://n8m.elevalocal.shop` | operacional |
| `Chatwoot` | `https://chat.elevalocal.shop` | operacional |
| `Evolution API` | `https://api.elevalocal.shop` | operacional |

## Tenants cadastrados no registry

| Tenant | Tipo | Status | Runtime `n8n` | Owner no registry |
| --- | --- | --- | --- | --- |
| `cli-eleva-pilot` | interno | `internal` | `shared-foundation` | `ops@elevalocal.shop` |
| `cli-demo-externo` | simulacao externa | `onboarding` | `dedicated` | `ops-demo@elevalocal.shop` |

## Ownership operacional atual

### Owner de plataforma

- owner team canonico: `eleva-local-ops`

### Leitura objetiva atual

- `n8n`: owner operacional de plataforma documentado como `eleva-local-ops`
- `Chatwoot`: owner operacional de plataforma documentado como `eleva-local-ops`
- `Evolution API`: owner operacional de plataforma documentado como `eleva-local-ops`

### Observacao

O repositorio documenta com seguranca o owner de plataforma (`registry.owner_team`),
mas nao explicita owners distintos por stack. Portanto, a resposta correta hoje e:

- o dono operacional documentado dos 3 stacks e o time `eleva-local-ops`

## Arquivos que devem ser tocados nas proximas 3 fases

### Fase 1. Readiness P0 de launch

- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)
- [LAUNCH-AUDIT.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-AUDIT.md)
- [LAUNCH-EXECUTION-BOARD.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-EXECUTION-BOARD.md)
- [OFFSITE-VALIDATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-VALIDATION-CHECKLIST.md)
- [SECRET-ROTATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECRET-ROTATION-CHECKLIST.md)
- [CHATWOOT-VERSION-FREEZE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-VERSION-FREEZE.md)
- [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md)

### Fase 2. Estado operacional por stack

- [N8N-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-STATUS.md)
- [CHATWOOT-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-STATUS.md)
- [EVOLUTION-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/EVOLUTION-STATUS.md)
- [BACKUP-RESTORE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-RESTORE.md)
- [RUNBOOK-EXECUTIVO.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/RUNBOOK-EXECUTIVO.md)
- [OPERATIONS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OPERATIONS.md)

### Fase 3. Baseline de tenant e rollout externo

- [tenants/registry.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/registry.yaml)
- [tenants/manifests/cli-eleva-pilot.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/manifests/cli-eleva-pilot.yaml)
- [tenants/manifests/cli-demo-externo.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/manifests/cli-demo-externo.yaml)
- [STATE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/STATE.md)
- [HANDOFF.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/HANDOFF.md)

## Matriz de comandos de validacao por stack

### `n8n`

| Objetivo | Comando |
| --- | --- |
| estado dos containers | `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"` |
| host efetivo | `docker inspect n8n-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' \| grep '^N8N_HOST='` |
| HTTPS / dominio | `curl -vkI https://n8m.elevalocal.shop` |
| owner atual no banco | `N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' \| awk -F= '/^POSTGRES_USER=/{print $2}')"` seguido de `docker exec -it postgresql-mamtm8g3b2mdh7ko0hxdcyr3 psql -U "${N8N_DB_USER}" -d n8n -c 'select email, "firstName", "lastName", disabled from "user";'` |

### `Chatwoot`

| Objetivo | Comando |
| --- | --- |
| estado dos containers | `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" \| grep c8ecfzoz3ddr69y9c4bto96s` |
| env efetiva do app | `docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}'` |
| labels do proxy | `docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{json .Config.Labels}}'` |
| logs do app | `docker logs --tail 200 chatwoot-c8ecfzoz3ddr69y9c4bto96s` |
| logs do worker | `docker logs --tail 200 sidekiq-c8ecfzoz3ddr69y9c4bto96s` |
| volumes | `docker volume ls \| grep c8ecfzoz3ddr69y9c4bto96s` |

### `Evolution API`

| Objetivo | Comando |
| --- | --- |
| estado dos containers | `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" \| grep rh7m1i3wfmf9254fhcb4pn5p` |
| env efetiva da API | `docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}'` |
| labels do proxy | `docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .Config.Labels}}'` |
| logs da API | `docker logs --tail 200 api-rh7m1i3wfmf9254fhcb4pn5p` |
| volumes | `docker volume ls \| grep rh7m1i3wfmf9254fhcb4pn5p` |

## Observacoes de auditoria

- todos os comandos acima dependem de acesso a VPS; nenhum foi executado nesta etapa
- o repo hoje permite preparar smoke tests com seguranca, mas nao provar execucao sem evidencia externa
- `tenants/secrets/` foi deliberadamente excluido desta auditoria
