---
name: session-close
description: Fechamento de sessao enxuto para atualizar contexto persistente antes de trocar de conta ou encerrar a thread
---

# session-close

Use esta skill no fim de uma sessao para atualizar a memoria persistente do projeto sem gastar tokens desnecessarios.

## Objetivo

Registrar apenas o estado real e atual da sessao nos arquivos de contexto persistente, para que a proxima conta consiga retomar com um bootstrap curto.

## Sequencia obrigatoria

1. Revisar rapidamente o que realmente mudou na sessao atual
2. Atualizar `CONTEXT.md` com:
   - o que foi feito nesta sessao
   - validacoes executadas
   - riscos ainda abertos
3. Atualizar `STATE.md` com:
   - fase atual
   - status
   - proximo passo concreto
   - snapshot curto de verificacao
4. Atualizar `CONTINUAMENTO-DA-SESSAO.md` com:
   - resumo curto do ponto em que a sessao parou
   - proximo passo imediato
   - comandos/arquivos de retomada
   - riscos ou travas abertas
5. Atualizar `autovenda-pro-b2b-main/docs/HANDOFF.md` apenas se houve mudanca relevante de fluxo, prioridade, estado do produto ou instrucoes de retomada
6. Atualizar `PROJECT.md` somente se houve mudanca estrutural real:
   - stack
   - objetivo principal
   - arquitetura
   - app root
   - prioridades centrais
7. Remover ou substituir informacao obsoleta que possa confundir a proxima conta
8. No final, responder apenas:
   - `contexto atualizado`

## Regras

- Ser enxuto e factual
- Nao inventar progresso
- Nao duplicar historico desnecessario
- Nao transformar os arquivos em changelog longo
- Preservar o que ainda e verdade
- Se `PROJECT.md` nao precisar mudar, nao force mudanca
- Priorizar continuidade entre contas, nao documentacao perfeita
- `CONTINUAMENTO-DA-SESSAO.md` deve ser curto, operacional e orientado a retomada

## Prompt de uso

`Use $session-close.`
