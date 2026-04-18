---
name: session-bootstrap
description: Bootstrap curto e deterministico para retomar este projeto em contas ou sessoes novas com baixo custo de contexto
---

# session-bootstrap

Use esta skill no inicio de uma sessao nova para reconstruir o contexto minimo antes de implementar qualquer coisa.

## Objetivo

Retomar o projeto com baixo consumo de tokens, lendo apenas os arquivos canonicos que definem status, veredito e execucao operacional.

## Sequencia obrigatoria

1. Ler `LAUNCH-READINESS-LEDGER.md` na raiz do workspace
2. Ler `LAUNCH-AUDIT.md` na raiz do workspace
3. Ler `LAUNCH-EXECUTION-BOARD.md` na raiz do workspace
4. Ler `docs/PROMPT-1.3-B-DEPLOY-PILOT.md` se a sessao envolver o pilot n8n dedicado
5. Confirmar o foco de trabalho em `elevalocal-infra/`
6. Resumir em poucas linhas:
   - objetivo atual
   - estado atual
   - riscos abertos
   - proximo passo recomendado
7. So depois continuar a execucao pedida pelo usuario

## Regras

- Nao assumir memoria de outra thread, conta ou subagente
- Nao reler a base inteira sem necessidade
- Preferir modo economico por padrao
- Usar subagentes apenas se houver ganho claro dentro da sessao atual
- Respeitar que a fonte canonica de launch fica na trilogia ledger/audit/board

## Prompt de uso

`Use $session-bootstrap e continue de onde parou.`
