# Inventario de Segredos - Cliente Externo Demo LTDA

- tenant_id: `cli-demo-externo`
- slug: `demo-externo`
Inventario base de segredos por tenant.

Nao preencher este arquivo com o segredo real no repositrio. Use apenas referencia, dono e local de armazenamento.

## Tenant

- `tenant_id`: `cli-demo-externo`
- `company_name`: `Cliente Externo Demo LTDA`
- `owner`: `ops-demo@elevalocal.shop`
- `last_reviewed_at`: `2026-04-17`

## Credenciais obrigatorias

| Tipo | Nome logico | Uso | Onde esta salvo | Dono | Rotacao | Observacoes |
| --- | --- | --- | --- | --- | --- | --- |
| WhatsApp | `tenant-whatsapp-primary` | Sessao/canal do cliente | | | | |
| Evolution | `tenant-evolution-api-key` | API/manager da instancia | | | | |
| Chatwoot | `tenant-chatwoot-token` | Integracao e operacao | | | | |
| n8n | `tenant-n8n-credential-set` | Workflows e webhooks | | | | |
| IA | `tenant-llm-provider-key` | Agente/prompt do tenant | | | | |

## Gate de provisionamento

- `evolution.runtime_mode`: `shared-foundation`
- `chatwoot.runtime_mode`: `shared-foundation`
- `n8n.runtime_mode`: `dedicated`
- `n8n` blast radius documentado: `sim, dedicado por tenant no manifesto`
- excecao compartilhada aprovada por: `nao se aplica`

## Regras

- [ ] Nenhum segredo do tenant e compartilhado com outro tenant
- [ ] Nenhum segredo real foi escrito no repositrio
- [ ] Existe referencia clara de armazenamento seguro
- [ ] Existe periodicidade de rotacao definida
- [ ] Existe dono responsavel por revisao

## Incidentes e excecoes

- Compartilhamento autorizado excepcional:
- Data:
- Aprovador:
- Prazo para remover excecao:
