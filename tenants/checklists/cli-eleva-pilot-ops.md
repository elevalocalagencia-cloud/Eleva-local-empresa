# Client Ops Checklist - Eleva Local Pilot

- tenant_id: `cli-eleva-pilot`
- slug: `eleva-pilot`
- objetivo: `monitorar o tenant interno de homologacao`

## Contexto atual

- `n8n` compartilhado: `n8n-mamtm8g3b2mdh7ko0hxdcyr3`
- `Chatwoot` compartilhado: `chatwoot-c8ecfzoz3ddr69y9c4bto96s`
- `Evolution` compartilhada: `api-rh7m1i3wfmf9254fhcb4pn5p`

# Client Ops Checklist

Checklist recorrente de operacao por tenant.

## Diario

- [ ] Confirmar que a inbox do tenant recebe mensagens
- [ ] Confirmar que a instancia `Evolution` do tenant esta saudavel
- [ ] Confirmar que os workflows criticos do tenant nao falharam
- [ ] Confirmar que nao houve evento de cross-tenant

## Semanal

- [ ] Revisar automacoes com prefixo do tenant
- [ ] Revisar credenciais e conexoes usadas pelo tenant
- [ ] Revisar volume de atendimento e filas do tenant
- [ ] Revisar erros de IA/agent/prompt do tenant
- [ ] Revisar log de backup e ultimo artefato do tenant

## Mensal

- [ ] Revisar manifesto operacional do tenant
- [ ] Revisar inventario de segredos
- [ ] Revisar necessidade de rotacao de credenciais
- [ ] Revisar restore status do tenant
- [ ] Revisar naming e recursos abandonados

## Gatilhos de incidente

- [ ] Mensagem de um tenant apareceu na inbox errada
- [ ] Workflow rodou com credencial de outro tenant
- [ ] Prompt/agente usou contexto de outro tenant
- [ ] Backup/restore sem rastreabilidade por tenant
- [ ] Numero WhatsApp vinculado a instancia errada

## Acao imediata em caso de cross-tenant

1. pausar automacoes afetadas
2. isolar credenciais e canais envolvidos
3. registrar tenant impactado e horario
4. confirmar origem do vazamento
5. corrigir naming, segredo ou workflow antes de retomar
