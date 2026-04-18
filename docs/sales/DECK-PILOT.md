% Eleva Local - Deck Piloto
% Eleva Local
% {{DATA}}

# Capa

## Piloto assistido para automacao de atendimento via WhatsApp

- oferta inicial para operacoes que precisam responder mais rapido, organizar agendamentos e reduzir trabalho manual
- demo publica disponivel mediante CTA controlado
- placeholders comerciais:
  - preco piloto: `{{PRECO_PILOT}}`
  - prazo de go-live: `{{PRAZO_GO_LIVE}}`

# Problema

## Onde a operacao perde eficiencia hoje

- leads chegam por WhatsApp e dependem de resposta manual em horarios irregulares
- agendamentos ficam espalhados entre conversa, agenda humana e confirmacoes sem padrao
- gestores nao conseguem provar valor mensal nem auditar o que foi automatizado
- crescer sem isolamento entre clientes aumenta risco operacional e risco de dados

# Solucao

## O que a Eleva Local entrega

- automacao de atendimento via WhatsApp com fluxos controlados
- agendamento automatico e follow-up operacional
- portal do cliente para acompanhar conversas e agendamentos
- onboarding em piloto assistido com rollout guiado e checklist por tenant

# Demo

## Como a demo publica entra na venda

- `Experimentar agora` leva para a demo publica com ambiente seguro e dados fake
- a demo mostra experiencia real de `n8n dedicated` e portal sem expor integracoes produtivas
- a origem do clique pode ser atribuida por `?src=landing` sem alterar a experiencia do usuario

# Arquitetura

## Arquitetura de operacao

- site publico comercial fica em `elevalocal.com.br` fora deste repo
- camada tecnica fica em `elevalocal.shop` com subdominios dedicados para demo, portal e stacks operacionais
- tenants usam manifests, checklists e evidencias separados para reduzir blast radius
- o portal usa acesso server-side para integracoes sensiveis e isolamento por tenant

# Seguranca e LGPD

## Guardrails para piloto assistido

- uso de `DPA-LGPD`, `PSA`, `NDA` e `SLA-PILOT` como pacote base
- segregacao de credenciais, manifests e ownership por tenant
- trilhas de backup, restore e runbooks versionadas
- demo publica sem numero real de cliente, sem dados reais e com reset recorrente

# Modelo comercial

## Estrutura inicial da oferta

- formato: piloto assistido
- valor: `{{PRECO_PILOT}}`
- prazo estimado de go-live: `{{PRAZO_GO_LIVE}}`
- proposta inclui escopo, criterios de aceite, janela operacional e anexos legais

# Proximos passos

## Fechamento recomendado

1. call de discovery com mapeamento de volume, agenda e operacao atual
2. demo guiada com casos aderentes ao cliente
3. envio de proposta comercial e pacote juridico
4. aprovacao do piloto assistido
5. onboarding e ativacao controlada
