---
name: session-close
description: Fechamento de sessao enxuto para atualizar contexto persistente antes de trocar de conta ou encerrar a thread
---

# session-close

Use esta skill no fim de uma sessao para atualizar a memoria persistente do projeto sem gastar tokens desnecessarios.

## Objetivo

Registrar apenas o estado real e atual da sessao nos arquivos canonicos, para que a proxima conta consiga retomar com um bootstrap curto.

## Sequencia obrigatoria

1. Revisar rapidamente o que realmente mudou na sessao atual
2. Atualizar `LAUNCH-READINESS-LEDGER.md` apenas se houve mudanca real de status, evidencia, owner ou prioridade
3. Atualizar `LAUNCH-AUDIT.md` apenas se o veredito `GO / NO-GO` mudou
4. Atualizar `LAUNCH-EXECUTION-BOARD.md` com proximo passo concreto, bloqueios e evidencias novas
5. Atualizar `docs/PROMPT-1.3-B-DEPLOY-PILOT.md` apenas se o runbook do pilot mudou
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
- `LAUNCH-EXECUTION-BOARD.md` deve permanecer curto, operacional e orientado a retomada

## Prompt de uso

`Use $session-close.`
