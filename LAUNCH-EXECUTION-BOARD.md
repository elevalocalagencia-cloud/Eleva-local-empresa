# Launch Execution Board

## Objetivo

Centralizar a execucao global da prontidao de lancamento em uma unica trilha
operacional.

Use este arquivo como painel-mestre. Os demais documentos continuam sendo a
fonte de execucao de cada frente especifica.

Prioridade e status canonicos:

- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)

## Papel deste board

- acompanhar execucao das frentes P0
- concentrar evidencia operacional
- nao redefinir prioridade ou criterio de `GO / NO-GO`

## Ordem global recomendada

1. validar offsite backup
2. rotacionar segredos expostos
3. executar primeiro provisionamento real de cliente externo
4. fechar P1 comercial: monitoramento por tenant
5. fechar P1 comercial: rotacao recorrente por tenant

## Painel operacional

| Frente | Status de execucao | Dependencia anterior | Artefato principal | Evidencia minima para fechar |
| --- | --- | --- | --- | --- |
| Offsite backup | `OPEN` | nenhuma | [OFFSITE-VALIDATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-VALIDATION-CHECKLIST.md) | destino remoto validado com SQLs e tarballs |
| Rotacao de segredos | `OPEN` | offsite preferencialmente validado | [SECRET-ROTATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECRET-ROTATION-CHECKLIST.md) | credenciais antigas invalidadas e owners registrados |
| Freeze do `Chatwoot` | `DONE` | backup novo e rollback claro | [CHATWOOT-VERSION-FREEZE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-VERSION-FREEZE.md) | stack fora de `latest` com smoke test executado |
| Primeiro provisionamento externo real | `READY-PENDING-CLIENT` | segredos e stack base confiaveis | [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md) | cliente real provisionado com smoke test ponta a ponta |
| RPO/RTO por stack | `DONE-TARGETS` | base de backup e restore definida | [docs/RPO-RTO.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RPO-RTO.md) | targets internos publicados por stack |
| Restore drill trimestral | `DONE-PLAYBOOK` | RPO/RTO definidos | [docs/RESTORE-DRILL-PLAYBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTORE-DRILL-PLAYBOOK.md) | cadencia formalizada e evidencia inaugural registrada |
| Demo publica | `PARTIAL` | runtime demo preparado no repo | [tenants/evidence/cli-demo-externo/setup-2026-04-18.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/cli-demo-externo/setup-2026-04-18.md) | DNS resolvendo, deploy VPS validado e smoke `200/302` |

## Gates de passagem

### Gate 1. Antes de mexer em producao

- [ ] backup novo executado
- [ ] rollback path conhecido
- [ ] owner responsavel definido
- [ ] janela operacional definida

### Gate 2. Antes de chamar `GO CONTROLADO`

- [ ] offsite validado
- [ ] segredos rotacionados
- [x] `Chatwoot` fora de `latest`
- [ ] primeiro provisionamento real validado

### Gate 3. Antes de chamar `GO COMERCIAL`

- [x] RPO/RTO documentados
- [ ] monitoramento e alertas basicos por tenant
- [x] rotina trimestral de restore drill registrada
- [ ] processo recorrente de rotacao por tenant formalizado

## Evidencia consolidada

### Offsite backup

- owner:
- ultima validacao:
- destino remoto:
- observacoes:

### Rotacao de segredos

- owner:
- ultima validacao:
- stacks cobertos:
- observacoes:

### Freeze do `Chatwoot`

- owner: `eleva-local-ops`
- versao congelada: `chatwoot/chatwoot:v4.12.0`
- data: `2026-04-18`
- observacoes: backup local pre-freeze e rollback registrados; validacao manual de login/mensagem ainda nao anexada

### Primeiro provisionamento externo

- tenant real:
- owner:
- data:
- resultado:

### Demo publica

- tenant: `cli-demo-externo`
- dominio-alvo: `wf-demo.elevalocal.shop`
- evidencias no repo: setup, smoke inicial sem DNS e inventario de seed workflows
- bloqueios: DNS ainda `NXDOMAIN`, deploy VPS nao executado nesta sessao, cron e Healthchecks ainda nao instalados

## Proximo passo concreto

1. criar o `A record` de `wf-demo.elevalocal.shop` para `2.24.199.157`
2. aguardar propagacao e validar com `nslookup`
3. na VPS, gerar `.env` real do demo e subir `tenants/runtime/cli-demo-externo`
4. importar seed workflows, criar `demo@elevalocal.shop` e instalar cron do reset semanal
5. registrar curl, screenshot e resposta de `/healthz` em `tenants/evidence/cli-demo-externo/`

## Regra de atualizacao

- atualizar este board apenas quando houver evidencia real
- nao marcar item como concluido sem artefato e validacao
- ao fechar um item P0, refletir primeiro o status em [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)
- `LAUNCH-AUDIT.md` deve derivar do ledger, nao deste board
