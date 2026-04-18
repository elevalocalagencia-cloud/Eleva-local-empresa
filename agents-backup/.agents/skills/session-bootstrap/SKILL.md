---
name: session-bootstrap
description: Bootstrap curto e deterministico para retomar este projeto em contas ou sessoes novas com baixo custo de contexto
---

# session-bootstrap

Use esta skill no inicio de uma sessao nova para reconstruir o contexto minimo antes de implementar qualquer coisa.

## Objetivo

Retomar o projeto com baixo consumo de tokens, lendo apenas os arquivos persistentes que definem contexto, estado e handoff operacional.

## Sequencia obrigatoria

1. Ler `PROJECT.md` na raiz do workspace
2. Ler `CONTEXT.md` na raiz do workspace
3. Ler `STATE.md` na raiz do workspace
4. Ler `autovenda-pro-b2b-main/docs/HANDOFF.md`
5. Trocar o foco de trabalho para `autovenda-pro-b2b-main/`
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
- Respeitar que o app real fica em `autovenda-pro-b2b-main/`, nao apenas na raiz do workspace

## Prompt de uso

`Use $session-bootstrap e continue de onde parou.`
