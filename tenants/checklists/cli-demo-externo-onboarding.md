# Onboarding Checklist - Cliente Externo Demo LTDA

- tenant_id: `cli-demo-externo`
- slug: `demo-externo`
Checklist base para entrada de um novo tenant.

## 1. Contrato e identificacao

- [x] Definir `tenant_id` unico (`cli-{slug}`)
- [x] Registrar razao social e nome operacional
- [x] Registrar responsavel principal
- [x] Registrar email e telefone de contato
- [x] Registrar plano/escopo contratado

## 2. Naming e manifesto

- [x] Criar manifesto do tenant a partir de `tenant-manifest.example.yaml`
- [x] Preencher `provisioning.evolution`, `provisioning.chatwoot` e `provisioning.n8n`
- [x] Definir nome da instancia `Evolution`
- [x] Definir nome da inbox `Chatwoot`
- [x] Definir prefixo dos workflows `n8n`
- [x] Definir prefixo dos segredos

## 3. Matriz de provisionamento

- [x] Confirmar `Evolution` em `shared-foundation` com instancia dedicada por tenant
- [x] Confirmar `Chatwoot` em `shared-foundation` com inbox dedicada por tenant
- [x] Confirmar `n8n` em `dedicated` para cliente externo ou registrar excecao `internal`
- [x] Registrar ownership de credenciais por stack
- [x] Registrar checklist de rollout por stack no manifesto

## 4. Canais

- [ ] Confirmar numero WhatsApp dedicado ao tenant
- [ ] Criar/atribuir instancia `Evolution` do tenant
- [ ] Criar/atribuir inbox `Chatwoot` do tenant
- [ ] Validar roteamento da inbox
- [ ] Validar envio e recebimento basico no WhatsApp

## 5. Automacoes e IA

- [ ] Criar namespace de automacao do tenant
- [ ] Criar workflows com prefixo do tenant
- [ ] Separar credenciais do tenant no `n8n`
- [ ] Validar que cliente externo nao esta em `n8n shared-foundation`
- [ ] Separar prompts/agentes/memoria do tenant
- [ ] Validar que nada aponta para credencial de outro cliente

## 6. Segredos e acessos

- [x] Criar inventario de segredos do tenant
- [ ] Confirmar que nenhum segredo e compartilhado sem aprovacao
- [ ] Registrar onde cada segredo esta salvo
- [ ] Confirmar acesso minimo necessario para operadores

## 7. Operacao e backup

- [ ] Confirmar que o tenant entra no ciclo de backup
- [ ] Registrar referencia de restore drill
- [ ] Registrar checklist operacional do tenant
- [ ] Registrar data de revisao inicial

## 8. Validacao final

- [ ] WhatsApp responde corretamente
- [ ] Inbox correta recebe as mensagens
- [ ] Workflow de teste dispara no namespace correto
- [x] Runtime do `n8n` confere com a politica do tenant
- [ ] Nenhuma automacao usa ativo de outro tenant
- [ ] Manifesto e inventario revisados
