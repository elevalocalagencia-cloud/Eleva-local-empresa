# Onboarding Checklist - Eleva Local Pilot

- tenant_id: `cli-eleva-pilot`
- slug: `eleva-pilot`
- status: `internal`
- objetivo: `homologacao da operacao multi-cliente`

## Contexto atual

- usa os dominios compartilhados atuais da Eleva Local
- serve para provar o fluxo de tenant manifest, registry, checklist e naming
- nao representa ainda isolamento final por cliente externo

# Onboarding Checklist

Checklist base para entrada de um novo tenant.

## 1. Contrato e identificacao

- [ ] Definir `tenant_id` unico (`cli-{slug}`)
- [ ] Registrar razao social e nome operacional
- [ ] Registrar responsavel principal
- [ ] Registrar email e telefone de contato
- [ ] Registrar plano/escopo contratado

## 2. Naming e manifesto

- [ ] Criar manifesto do tenant a partir de `tenant-manifest.example.yaml`
- [ ] Definir nome da instancia `Evolution`
- [ ] Definir nome da inbox `Chatwoot`
- [ ] Definir prefixo dos workflows `n8n`
- [ ] Definir prefixo dos segredos

## 3. Canais

- [ ] Confirmar numero WhatsApp dedicado ao tenant
- [ ] Criar/atribuir instancia `Evolution` do tenant
- [ ] Criar/atribuir inbox `Chatwoot` do tenant
- [ ] Validar roteamento da inbox
- [ ] Validar envio e recebimento basico no WhatsApp

## 4. Automacoes e IA

- [ ] Criar namespace de automacao do tenant
- [ ] Criar workflows com prefixo do tenant
- [ ] Separar credenciais do tenant no `n8n`
- [ ] Separar prompts/agentes/memoria do tenant
- [ ] Validar que nada aponta para credencial de outro cliente

## 5. Segredos e acessos

- [ ] Criar inventario de segredos do tenant
- [ ] Confirmar que nenhum segredo e compartilhado sem aprovacao
- [ ] Registrar onde cada segredo esta salvo
- [ ] Confirmar acesso minimo necessario para operadores

## 6. Operacao e backup

- [ ] Confirmar que o tenant entra no ciclo de backup
- [ ] Registrar referencia de restore drill
- [ ] Registrar checklist operacional do tenant
- [ ] Registrar data de revisao inicial

## 7. Validacao final

- [ ] WhatsApp responde corretamente
- [ ] Inbox correta recebe as mensagens
- [ ] Workflow de teste dispara no namespace correto
- [ ] Nenhuma automacao usa ativo de outro tenant
- [ ] Manifesto e inventario revisados
