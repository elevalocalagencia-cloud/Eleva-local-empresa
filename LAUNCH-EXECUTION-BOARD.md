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
3. congelar versao do `Chatwoot`
4. executar primeiro provisionamento real de cliente externo
5. reavaliar auditoria de lancamento

## Painel P0

| Frente | Status de execucao | Dependencia anterior | Artefato principal | Evidencia minima para fechar |
| --- | --- | --- | --- | --- |
| Offsite backup | `OPEN` | nenhuma | [OFFSITE-VALIDATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-VALIDATION-CHECKLIST.md) | destino remoto validado com SQLs e tarballs |
| Rotacao de segredos | `OPEN` | offsite preferencialmente validado | [SECRET-ROTATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECRET-ROTATION-CHECKLIST.md) | credenciais antigas invalidadas e owners registrados |
| Freeze do `Chatwoot` | `OPEN` | backup novo e rollback claro | [CHATWOOT-VERSION-FREEZE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-VERSION-FREEZE.md) | stack fora de `latest` com smoke test executado |
| Primeiro provisionamento externo | `OPEN` | segredos e stack base confiaveis | [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md) | cliente real provisionado com smoke test ponta a ponta |

## Gates de passagem

### Gate 1. Antes de mexer em producao

- [ ] backup novo executado
- [ ] rollback path conhecido
- [ ] owner responsavel definido
- [ ] janela operacional definida

### Gate 2. Antes de chamar `GO CONTROLADO`

- [ ] offsite validado
- [ ] segredos rotacionados
- [ ] `Chatwoot` fora de `latest`
- [ ] primeiro provisionamento real validado

### Gate 3. Antes de chamar `GO COMERCIAL`

- [ ] RPO/RTO documentados
- [ ] monitoramento e alertas basicos por tenant
- [ ] rotina trimestral de restore drill registrada
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

- owner:
- versao congelada:
- data:
- observacoes:

### Primeiro provisionamento externo

- tenant real:
- owner:
- data:
- resultado:

## Regra de atualizacao

- atualizar este board apenas quando houver evidencia real
- nao marcar item como concluido sem artefato e validacao
- ao fechar um item P0, refletir primeiro o status em [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)
- `LAUNCH-AUDIT.md` deve derivar do ledger, nao deste board
