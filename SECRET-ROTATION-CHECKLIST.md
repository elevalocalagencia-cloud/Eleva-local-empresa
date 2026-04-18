# Secret Rotation Checklist

## Objetivo

Fechar o bloqueio de lancamento relacionado a credenciais potencialmente
expostas durante investigacao, troubleshooting e operacao manual.

## Escopo minimo por stack

### n8n

- [ ] credenciais administrativas do owner
- [ ] credenciais de banco
- [ ] credenciais de webhook e integracoes criticas

### Chatwoot

- [ ] token administrativo ou `api_access_token`
- [ ] credenciais do banco
- [ ] credenciais de integracoes externas

### Evolution

- [ ] chave ou token administrativo da API
- [ ] credenciais do banco
- [ ] credenciais de webhooks e integracoes

### Infra

- [ ] credenciais administrativas do painel/orquestracao
- [ ] chaves SSH ou acessos auxiliares revisados
- [ ] credenciais do destino offsite revisadas

## Passos de execucao

1. listar os segredos afetados por stack
2. rotacionar um stack por vez
3. validar login ou integracao apos cada rotacao
4. invalidar credencial anterior
5. registrar owner, data e impacto
6. registrar evidencia cifrada no vault local

## Responsaveis

- owner operacional da infra compartilhada: `eleva-local-ops`
- owner do tenant: registrar no inventario do tenant antes da rotacao

## Tabela de rotacao por stack

| Stack | Segredo | Owner | Data de rotacao | Validacao apos troca | Evidencia | Observacoes |
| --- | --- | --- | --- | --- | --- | --- |
| `n8n` | credenciais do banco, webhook e administracao | `eleva-local-ops` | `TBD` | `TBD` | `TBD` | preencher antes de qualquer rollout externo |
| `Chatwoot` | token administrativo, banco e integracoes | `eleva-local-ops` | `TBD` | `TBD` | `TBD` | alinhar com freeze de versao |
| `Evolution` | chave da API, banco e webhooks | `eleva-local-ops` | `TBD` | `TBD` | `TBD` | validar impacto por inbox/tenant |
| `Infra` | SSH, painel e offsite | `eleva-local-ops` | `TBD` | `TBD` | `TBD` | revisar sem compartilhar entre tenants |

## Gate de encerramento

- [ ] nenhum segredo anterior continua ativo sem justificativa
- [ ] owners responsaveis registrados
- [ ] tenants impactados mapeados
- [ ] inventario privado atualizado
