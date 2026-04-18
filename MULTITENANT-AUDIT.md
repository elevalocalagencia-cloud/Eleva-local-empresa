# Multitenant Audit

## Objetivo

Auditar a prontidao da `Eleva Local` para operar ate 10 clientes sem interferencia entre:

- WhatsApps
- inboxes
- agentes humanos
- agentes de IA
- workflows
- credenciais
- backup e restore

Este documento trata de isolamento operacional e risco de cross-tenant. Ele parte do estado atual da VPS e da stack existente, nao de uma plataforma idealizada.

## Veredito executivo

A stack atual esta operacional, mas ainda nao esta pronta para 10 clientes com garantia forte de isolamento.

O maior risco restante nao e mais disponibilidade basica. O maior risco e contaminacao cruzada entre clientes:

- conta WhatsApp errada
- inbox errada
- automacao errada
- segredo errado
- agente de IA errado
- restore errado

## Riscos centrais de cross-tenant

### 1. Automacao compartilhada demais

`n8n` ainda e o maior ponto de risco para mistura entre clientes.

Riscos:

- credenciais compartilhadas em workflows
- disparo no tenant errado
- nomenclatura inconsistente
- reuse de nodes e secrets sem boundary claro
- restore de stack sem recorte por cliente

Impacto:

- alto

### 2. Integracao WhatsApp e inbox

`Evolution API` e `Chatwoot` sao funcionais, mas ainda nao estao formalizados como camadas multi-cliente com runbook por tenant.

Riscos:

- inbox do cliente A recebendo trafego do cliente B
- instancias de WhatsApp sem naming forte
- configuracao de Chatwoot aplicada na instancia errada
- troubleshooting sem trilha clara por cliente

Impacto:

- alto

### 3. Credenciais e segredos

Ainda nao existe um inventario formalizado por cliente.

Riscos:

- API keys compartilhadas
- reaproveitamento de credenciais
- dificuldade de rotacao por tenant
- incidente em um cliente afetando os outros

Impacto:

- alto

### 4. Backup e restore por stack, nao por cliente

Backup recorrente e restore drill da stack ja foram provados. O problema agora e granularidade operacional.

Riscos:

- restore total quando o incidente e parcial
- dificuldade de recuperar apenas um cliente
- maior blast radius em incidente de dados

Impacto:

- medio a alto

### 5. Operacao de IA

Prompts, memoria, agentes e automacoes ainda podem ser tratados de forma global demais se nao houver regra rigida de namespace.

Riscos:

- contexto de IA cruzando clientes
- agente errado atendendo cliente errado
- webhook global sem tenant boundary
- prompt e toolchain compartilhados sem isolamento

Impacto:

- alto

## Estado atual por camada

### Infra e seguranca

Pontos fortes:

- `api.elevalocal.shop` com HTTPS valido
- `Coolify` fora da internet publica
- `6001/6002` fora da internet publica
- backup recorrente instalado
- restore drill validado nos tres stacks

Lacunas:

- sem offsite backup
- segredos expostos ainda pendentes de rotacao
- governanca administrativa ainda precisa ser formalizada

### Backend

Pontos fortes:

- stacks principais estaveis
- rollback do `n8n` compreendido
- redis do stack atual do `n8n` corrigido para `redis:7-alpine`

Lacunas:

- migracao definitiva do `n8n` ainda nao concluida
- automacoes ainda nao foram repartidas por tenant

### SQL e persistencia

Pontos fortes:

- persistencia confirmada
- restore drill executado

Lacunas:

- recuperacao ainda e pensada por stack
- falta modelo formal de recorte por cliente

### IA e agentes

Pontos fortes:

- stack atual permite operar IA e automacoes

Lacunas:

- falta boundary forte por cliente
- falta politica de naming e ownership de prompts, memorias e tools

## Arquitetura recomendada para 10 clientes

### Principio

Compartilhar base de infraestrutura e observabilidade, mas nao compartilhar identidade operacional do cliente.

### Recomendacao

- `1 Evolution instance por cliente` sobre runtime `shared-foundation`
- `1 inbox Chatwoot por cliente` sobre runtime `shared-foundation`
- `1 conjunto de credenciais por cliente`
- `1 namespace obrigatorio por cliente em workflows`
- `1 n8n dedicado por cliente externo`

### Minimo aceitavel se o `n8n` continuar compartilhado

- prefixo obrigatorio por tenant em workflows e credenciais
- secrets separados por cliente
- naming padronizado
- inventario por cliente
- checklist de revisao antes de publicar workflow
- restore documentado com impacto delimitado

## Naming padrao recomendado

- `cli-{slug}-evo`
- `cli-{slug}-inbox`
- `cli-{slug}-wf-{dominio}`
- `cli-{slug}-secret-{tipo}`
- `cli-{slug}-backup`
- `cli-{slug}-restore`

## Matriz de provisionamento fechada

| Stack | Runtime decidido | Recurso dedicado por tenant | Ownership de credenciais | Gate de rollout |
| --- | --- | --- | --- | --- |
| `Evolution` | `shared-foundation` | instancia `cli-{slug}-evo` | `eleva-local-ops` com segredo exclusivo por tenant | validar numero, webhook e smoke test antes do go-live |
| `Chatwoot` | `shared-foundation` | inbox `cli-{slug}-inbox` | `eleva-local-ops` com token e owner no inventario do tenant | validar inbox, labels, automacoes e roteamento |
| `n8n` | `dedicated` para cliente externo | workspace/stack `cli-{slug}-wf-*` | `eleva-local-ops` com credenciais exclusivas por tenant | nao onboardar cliente externo em stack compartilhada |

Excecao operacional atual:

- `cli-eleva-pilot` permanece em `n8n shared-foundation` apenas para homologacao interna, com blast radius explicitado no manifest e bloqueio para onboarding externo nessa modalidade

## Plano por fases

### Fase 1 — Fundacao multi-cliente

Objetivo:

- criar fronteira operacional por cliente

Entregas:

- `tenant_id` padrao
- naming padrao
- inventario por cliente
- matriz cliente -> numero -> inbox -> workflow -> segredo

### Fase 2 — Isolamento de credenciais e dados

Objetivo:

- impedir vazamento operacional entre clientes

Entregas:

- segredo por cliente
- politica de rotacao por cliente
- ownership claro por credencial
- restore e backup com recorte por tenant sempre que viavel

### Fase 3 — Isolamento de automacao e IA

Objetivo:

- impedir mistura de workflow, contexto e agente

Entregas:

- namespace obrigatorio em `n8n`
- prompts e memoria por cliente
- padrao de tools e webhooks por tenant
- revisao de blast radius antes de publicar alteracoes

### Fase 4 — Atendimento multi-cliente

Objetivo:

- garantir operacao segura no `Chatwoot`

Entregas:

- inbox por cliente
- roteamento por cliente
- tags por cliente
- onboarding e offboarding padronizados

### Fase 5 — Escala operacional

Objetivo:

- preparar a operacao para 10 clientes com baixa interferencia cruzada

Entregas:

- monitoramento por cliente
- checklist de mudanca
- rollback por cliente
- alerta por cliente
- versoes congeladas por stack

## Prioridades

### P0

- definir modelo de isolamento por cliente
- padronizar naming
- padronizar credenciais por cliente

### P1

- tratar `n8n` como maior vetor de cross-tenant
- formalizar `Evolution` e `Chatwoot` por cliente
- alinhar inventario operacional por tenant

### P2

- offsite backup
- rotacao de segredos
- migracao definitiva do `n8n`
- observabilidade por cliente

## Regras de decisao

Antes de adicionar novo cliente, a operacao deve responder "sim" para:

- esse cliente tem `tenant_id` claro?
- esse cliente tem inbox propria?
- esse cliente tem segredo proprio?
- esse cliente tem workflows identificaveis por namespace?
- esse cliente pode ser desativado sem afetar os demais?
- esse cliente pode ser restaurado sem restaurar a stack inteira?

Se qualquer resposta for "nao", a operacao ainda nao esta madura para escalar com seguranca.
