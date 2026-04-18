# Multi-Client Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a fundação operacional e documental para operar a `Eleva Local` com multiplos clientes sem interferencia entre WhatsApp, atendimento, automacoes, credenciais e restore.

**Architecture:** A base sera um control plane compartilhado com isolamento por cliente no nivel operacional. Nesta fase, o repositorio ganha contratos de tenant, templates de onboarding, padrao de naming, checklist de segregacao e um validador automatizado de manifests para reduzir erro humano antes de qualquer rollout em producao.

**Tech Stack:** Markdown, YAML, Python 3 para validacao, pytest para teste do validador.

---

### Task 1: Criar matriz executiva de prontidao multi-cliente

**Files:**
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/MULTITENANT-AUDIT.md`
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/README.md`
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/ARCHITECTURE.md`

- [ ] **Step 1: Escrever o documento de auditoria multi-cliente**

Criar `MULTITENANT-AUDIT.md` com:
- diagnostico global por dominio: infra, dados/SQL, IA/agentes/automações, atendimento
- riscos `P0/P1/P2`
- modelo recomendado de isolamento por cliente
- plano por fases para 10 clientes

- [ ] **Step 2: Atualizar README com a nova camada multi-cliente**

Adicionar links para:
- `MULTITENANT-AUDIT.md`
- pasta `tenants/`
- validador de manifest

- [ ] **Step 3: Atualizar arquitetura com modelo alvo**

Adicionar visao alvo com:
- control plane compartilhado
- data plane isolado por cliente
- 1 Evolution por cliente
- 1 inbox Chatwoot por cliente
- `n8n` por cliente ou por tier como regra operacional

- [ ] **Step 4: Verificar consistencia textual**

Run: revisar manualmente os 3 arquivos e confirmar que usam a mesma linguagem de tenant, naming e isolamento.
Expected: sem contradicoes entre arquitetura, auditoria e README.

### Task 2: Criar contrato de tenant e templates operacionais

**Files:**
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/README.md`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/tenant-manifest.example.yaml`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/tenant-registry.example.yaml`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/onboarding-checklist.md`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/secrets-inventory.md`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/client-ops-checklist.md`

- [ ] **Step 1: Definir contrato minimo do tenant**

No `tenant-manifest.example.yaml`, incluir campos:
- `tenant_id`
- `slug`
- `domains`
- `whatsapp_number`
- `evolution_instance`
- `chatwoot`
- `n8n`
- `secrets`
- `backup`
- `owners`

- [ ] **Step 2: Definir registry geral**

No `tenant-registry.example.yaml`, incluir uma lista de tenants com resumo operacional:
- slug
- status
- stack strategy
- restore validated
- last backup check

- [ ] **Step 3: Criar checklist de onboarding**

No `onboarding-checklist.md`, listar:
- criar subdominios
- criar instancias
- configurar inbox
- criar workflows
- cadastrar segredos
- validar backup

- [ ] **Step 4: Criar inventario de segredos por cliente**

No `secrets-inventory.md`, incluir tabela com:
- segredo
- sistema
- cliente
- dono
- data da ultima rotacao
- impacto

- [ ] **Step 5: Criar checklist operacional por cliente**

No `client-ops-checklist.md`, incluir:
- healthcheck
- restore
- offboarding
- incidente
- troca de numero/token

### Task 3: Criar validador automatizado de manifest de tenant

**Files:**
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/validate-tenant-manifest.py`
- Create: `C:/Users/PEDROSO/Downloads/elevalocal-infra\ops\tests\test_validate_tenant_manifest.py`

- [ ] **Step 1: Escrever o teste que falha para manifest valido**

Criar teste com fixture YAML minima e expectativa de saida 0.

- [ ] **Step 2: Escrever o teste que falha para campos obrigatorios ausentes**

Cobrir ausencias de:
- `tenant_id`
- `slug`
- `whatsapp_number`
- `evolution_instance`

- [ ] **Step 3: Implementar validador minimo**

Implementar script Python que:
- carrega YAML
- verifica campos obrigatorios
- valida formato simples de `slug`
- valida unicidade basica em registry quando fornecido
- retorna codigo de erro nao-zero em caso de falha

- [ ] **Step 4: Rodar testes**

Run: `pytest ops/tests/test_validate_tenant_manifest.py -q`
Expected: todos os testes passam

### Task 4: Consolidar runbooks executivos para lancamento multi-cliente

**Files:**
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/RUNBOOK-EXECUTIVO.md`
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/OPERATIONS.md`
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-CHECKLIST.md`

- [ ] **Step 1: Adicionar secao de multi-cliente no runbook**

Listar:
- isolamentos obrigatorios
- ordem de provisionamento
- gates antes de vender

- [ ] **Step 2: Adicionar rotina operacional por tenant**

Em `OPERATIONS.md`, incluir regra de naming e operacao por cliente.

- [ ] **Step 3: Adicionar checklist de revisao por tenant**

Em `BACKUP-CHECKLIST.md`, incluir verificacao por cliente/tenant e referencia ao registry.

- [ ] **Step 4: Verificar links e navegacao**

Expected: README, runbook e pasta `tenants/` se referenciam sem links quebrados.

### Task 5: Fechar verificacao final

**Files:**
- Modify: `C:/Users/PEDROSO/Downloads/elevalocal-infra/README.md`

- [ ] **Step 1: Rodar testes do validador**

Run: `pytest ops/tests/test_validate_tenant_manifest.py -q`
Expected: PASS

- [ ] **Step 2: Verificar leitura dos docs principais**

Revisar:
- `README.md`
- `MULTITENANT-AUDIT.md`
- `RUNBOOK-EXECUTIVO.md`
- `tenants/README.md`

- [ ] **Step 3: Atualizar README final**

Adicionar a nova fundacao multi-cliente na secao de arquivos.

- [ ] **Step 4: Commit**

```bash
git add README.md ARCHITECTURE.md RUNBOOK-EXECUTIVO.md OPERATIONS.md BACKUP-CHECKLIST.md MULTITENANT-AUDIT.md tenants ops docs/superpowers/plans/2026-04-17-multiclient-foundation.md
git commit -m "docs: add multiclient operating foundation"
```
