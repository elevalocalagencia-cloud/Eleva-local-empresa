---
name: session-bootstrap
description: Bootstrap curto e deterministico para retomar este projeto em contas ou sessoes novas com baixo custo de contexto
---

# session-bootstrap

Use esta skill no inicio de uma sessao nova para reconstruir o contexto minimo antes de implementar qualquer coisa.

## Objetivo

Retomar o projeto com baixo consumo de tokens, lendo apenas os arquivos canonicos que definem status, veredito, execucao e runbook operacional, em ordem deterministica.

## Sequencia obrigatoria

1. Ler `LAUNCH-READINESS-LEDGER.md` na raiz do workspace
2. Ler `LAUNCH-AUDIT.md` na raiz do workspace
3. Ler `LAUNCH-EXECUTION-BOARD.md` na raiz do workspace
4. Ler `docs/PROMPT-1.3-B-DEPLOY-PILOT.md`, se a sessao envolver o pilot n8n dedicado
5. Ler apenas os arquivos citados pela trilogia canonica, e somente se forem necessarios para executar o proximo passo
6. Resumir em poucas linhas:
   - objetivo atual
   - estado atual
   - riscos abertos
   - proximo passo imediato
7. Validar se o pedido atual do usuario continua na mesma trilha do `Proximo passo imediato`
8. So depois continuar a execucao pedida pelo usuario

## Loop de continuidade

O bootstrap deve sempre preservar este ciclo:

1. ler `LAUNCH-READINESS-LEDGER.md`
2. confirmar o proximo passo imediato
3. executar apenas a fatia necessaria
4. ao fechar a sessao, atualizar a trilogia canonica quando houver mudanca real de status, veredito ou execucao

Se o pedido do usuario mudar a direcao, atualizar `LAUNCH-EXECUTION-BOARD.md` no fechamento para refletir a nova trilha.

## Regras

- Nao assumir memoria de outra thread, conta ou subagente
- Nao reler a base inteira sem necessidade
- Preferir modo economico por padrao
- Usar subagentes apenas se houver ganho claro dentro da sessao atual
- `LAUNCH-READINESS-LEDGER.md` e a fonte primaria de status
- `LAUNCH-AUDIT.md` define o veredito `GO / NO-GO`
- `LAUNCH-EXECUTION-BOARD.md` lidera a retomada operacional
- Se um arquivo citado no fluxo nao existir, seguir para o proximo sem inflar contexto
- Ler de forma sequencial, nao paralela, quando o custo de contexto importar
- Nunca abrir muitos arquivos “por garantia”; abrir apenas o minimo necessario para retomar o passo seguinte

## Prompt de uso

`Use $session-bootstrap e continue de onde parou.`
