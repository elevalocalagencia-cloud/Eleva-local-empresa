# Inventario de Segredos - Eleva Local Pilot

- tenant_id: `cli-eleva-pilot`
- slug: `eleva-pilot`
- company_name: `Eleva Local Pilot`
- owner: `ops@elevalocal.shop`
- classification: `tenant interno de homologacao`

## Uso deste arquivo

- registrar apenas referencias de segredo
- nao gravar valor real no repositorio
- usar este tenant para mapear quais segredos precisam deixar de ser compartilhados antes de onboarding externo

# Secrets Inventory

Inventario base de segredos por tenant.

Nao preencher este arquivo com o segredo real no repositorio. Use apenas referencia, dono e local de armazenamento.

## Tenant

- `tenant_id`: `cli-eleva-pilot`
- `company_name`: `Eleva Local Pilot`
- `owner`: `ops@elevalocal.shop`
- `last_reviewed_at`:

## Credenciais obrigatorias

| Tipo | Nome logico | Uso | Onde esta salvo | Dono | Rotacao | Observacoes |
| --- | --- | --- | --- | --- | --- | --- |
| WhatsApp | `tenant-whatsapp-primary` | Sessao/canal do cliente | | | | |
| Evolution | `tenant-evolution-api-key` | API/manager da instancia | | | | |
| Chatwoot | `tenant-chatwoot-token` | Integracao e operacao | | | | |
| n8n | `tenant-n8n-credential-set` | Workflows e webhooks | | | | |
| IA | `tenant-llm-provider-key` | Agente/prompt do tenant | | | | |

## Regras

- [ ] Nenhum segredo do tenant e compartilhado com outro tenant
- [ ] Nenhum segredo real foi escrito no repositorio
- [ ] Existe referencia clara de armazenamento seguro
- [ ] Existe periodicidade de rotacao definida
- [ ] Existe dono responsavel por revisao

## Incidentes e excecoes

- Compartilhamento autorizado excepcional:
- Data:
- Aprovador:
- Prazo para remover excecao:
