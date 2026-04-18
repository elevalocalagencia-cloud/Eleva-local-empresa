# Launch Audit

## Objetivo

Consolidar a decisao de `GO / NO-GO` para lancamento comercial da operacao
`Eleva Local`, com foco em risco operacional, cross-tenant e recuperacao.

Este documento nao substitui os runbooks existentes. Ele funciona como camada
executiva de readiness para decidir se a operacao pode receber cliente real com
risco aceitavel.

Painel de execucao global:

- [LAUNCH-EXECUTION-BOARD.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-EXECUTION-BOARD.md)

Fonte canonica de readiness:

- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)

## Veredito atual

**Status: `NO-GO` para lancamento comercial amplo**

**Status: `GO CONTROLADO` apenas para onboarding piloto altamente assistido**

Traduzindo:

- a stack esta estavel o bastante para continuar homologacao e onboarding
  controlado
- a stack ainda nao esta pronta para escalar comercialmente com seguranca
- o maior risco residual nao e disponibilidade; e erro operacional com blast
  radius cross-tenant

## O que ja esta provado

- stacks principais operacionais
- backup local recorrente
- restore drill local validado nos 3 stacks
- fundacao multi-cliente ativa no repositorio
- onboarding com guardrail impedindo cliente externo em `n8n shared-foundation`

Referencia canonica:

- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)

## Bloqueios de lancamento

Os bloqueios abaixo refletem o ledger canonico de readiness.

### P0. Offsite backup ainda nao esta validado

Risco:

- perda total da VPS ainda deixa a operacao dependente apenas do que estiver no
  host atual

Impacto:

- alto

Para remover o bloqueio:

1. habilitar destino offsite real
2. executar ao menos uma copia offsite completa
3. validar presenca dos SQLs e tarballs no destino remoto
4. registrar local, owner e data da ultima copia valida

Artefato de execucao:

- [OFFSITE-VALIDATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-VALIDATION-CHECKLIST.md)

### P0. Rotacao de segredos potencialmente expostos continua pendente

Risco:

- token ou credencial antiga continuar valida apos investigacao e troubleshooting

Impacto:

- alto

Para remover o bloqueio:

1. listar segredos impactados por stack
2. rotacionar credenciais administrativas e de integracao
3. registrar data de rotacao e owner responsavel
4. validar que artefatos antigos nao continuam em uso

Artefato de execucao:

- [SECRET-ROTATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECRET-ROTATION-CHECKLIST.md)

### P0. `Chatwoot` ainda esta em `latest`

Risco:

- drift de comportamento e deploy nao deterministico

Impacto:

- alto

Para remover o bloqueio:

1. fixar tag explicita do `Chatwoot`
2. registrar a versao congelada no runbook
3. manter rollback claro para a mesma versao

Artefato de execucao:

- [CHATWOOT-VERSION-FREEZE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-VERSION-FREEZE.md)

### P0. Provisionamento real de cliente externo ainda nao foi executado ponta a ponta

Risco:

- os guardrails de manifesto e checklist estao prontos, mas o fluxo de rollout
  real ainda nao foi provado em producao controlada

Impacto:

- alto

Para remover o bloqueio:

1. promover o tenant de simulacao para cliente real equivalente ou criar tenant real
2. provisionar `Evolution`, `Chatwoot` e `n8n dedicated`
3. registrar smoke tests por stack
4. registrar restore status e owners reais

Artefato de execucao:

- [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md)

## Itens importantes, mas nao bloqueantes para piloto assistido

### P1. RPO/RTO ainda nao estao formalizados por stack

Sem isso, existe backup e restore drill, mas nao existe compromisso operacional
explicito de perda maxima tolerada e tempo de recuperacao.

### P1. Monitoramento e alertas por tenant ainda nao existem

Para escala comercial, isso reduz a capacidade de detectar falhas cedo e
delimitar blast radius.

### P1. Restore ainda esta pensado mais por stack do que por tenant

Isto nao impede piloto assistido, mas ainda nao atende bem escala multi-cliente
mais agressiva.

### P1. Migracao definitiva do `n8n` ainda nao foi concluida

Hoje o contorno operacional funciona, mas a base ainda carrega historico de
incidente e hotfix operacional.

## Gates minimos para `GO CONTROLADO`

Todos abaixo devem estar `DONE` no ledger canonico:

- [x] stacks principais operacionais
- [x] backup local recorrente
- [x] restore drill local validado
- [x] `tenant_id` e `slug` obrigatorios
- [x] scaffolding por tenant
- [x] validacao de manifest no onboarding
- [x] guardrail impedindo cliente externo em `n8n shared-foundation`
- [ ] offsite backup validado
- [ ] segredos rotacionados apos investigacao
- [ ] `Chatwoot` com versao fixada
- [ ] primeiro rollout real de cliente externo validado ponta a ponta

Sem esses quatro ultimos, nao e seguro chamar a operacao de pronta para
lancamento comercial.

## Gates minimos para `GO COMERCIAL`

Todos abaixo devem estar `SIM`:

- [ ] todos os gates de `GO CONTROLADO`
- [ ] RPO/RTO por stack documentados
- [ ] monitoramento e alertas basicos por tenant
- [ ] rotina trimestral de restore drill registrada
- [ ] processo de rotacao de segredo por tenant registrado
- [ ] versoes criticas congeladas em todos os stacks principais

## Decisao recomendada hoje

### O que pode

- continuar homologacao
- executar onboarding controlado de primeiro cliente real
- vender apenas com acompanhamento manual forte e janela operacional controlada

### O que nao pode

- abrir onboarding comercial em escala
- tratar a operacao como pronta para 10 clientes
- depender de rollback improvisado ou backup apenas local

## Sequencia recomendada para sair de `NO-GO`

1. validar offsite backup
2. rotacionar segredos expostos
3. fixar versao explicita do `Chatwoot`
4. executar primeiro provisionamento real ponta a ponta com `n8n dedicated`
5. registrar smoke tests, owners, restore status e rollback path
6. reavaliar auditoria

Execucao coordenada:

- usar [LAUNCH-EXECUTION-BOARD.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-EXECUTION-BOARD.md) como trilha unica de acompanhamento
- usar [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md) como fonte unica de prioridade e status

## Resultado esperado da proxima auditoria

Ao final dessa sequencia, a meta e mudar o veredito de:

- `NO-GO para lancamento comercial amplo`

para:

- `GO CONTROLADO para lancamento comercial inicial`
