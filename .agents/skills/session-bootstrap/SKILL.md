---
name: session-bootstrap
description: Bootstrap curto e deterministico para retomar este projeto em contas ou sessoes novas com baixo custo de contexto
---

# session-bootstrap

Use esta skill no inicio de uma sessao nova para reconstruir o contexto minimo antes de implementar qualquer coisa.

## Objetivo

Retomar o projeto com baixo consumo de tokens, lendo apenas os arquivos persistentes que definem contexto, estado, continuamento e handoff operacional, em ordem deterministica.

## Sequencia obrigatoria

1. Ler `CONTINUAMENTO-DA-SESSAO.md` na raiz do workspace
2. Ler `CONTEXT.md` na raiz do workspace
3. Ler `STATE.md` na raiz do workspace
4. Ler `HANDOFF.md` na raiz do workspace, se existir
5. Ler apenas os arquivos citados em `Arquivos de retomada` dentro de `CONTINUAMENTO-DA-SESSAO.md`, e somente se forem necessarios para executar o proximo passo
6. Resumir em poucas linhas:
   - objetivo atual
   - estado atual
   - riscos abertos
   - proximo passo imediato
7. Validar se o pedido atual do usuario continua na mesma trilha do `Proximo passo imediato`
8. So depois continuar a execucao pedida pelo usuario

## Loop de continuidade

O bootstrap deve sempre preservar este ciclo:

1. ler `CONTINUAMENTO-DA-SESSAO.md`
2. confirmar o proximo passo imediato
3. executar apenas a fatia necessaria
4. ao fechar a sessao, atualizar `CONTINUAMENTO-DA-SESSAO.md`, `CONTEXT.md` e `STATE.md`

Se o pedido do usuario mudar a direcao, atualizar o `CONTINUAMENTO-DA-SESSAO.md` no fechamento para refletir a nova trilha.

## Regras

- Nao assumir memoria de outra thread, conta ou subagente
- Nao reler a base inteira sem necessidade
- Preferir modo economico por padrao
- Usar subagentes apenas se houver ganho claro dentro da sessao atual
- `CONTINUAMENTO-DA-SESSAO.md` e a fonte primaria de retomada
- `CONTEXT.md` e `STATE.md` refinam o estado, mas nao substituem o continuamento
- `HANDOFF.md` complementa o quadro, nao lidera a retomada
- Se um arquivo citado no fluxo nao existir, seguir para o proximo sem inflar contexto
- Ler de forma sequencial, nao paralela, quando o custo de contexto importar
- Nunca abrir muitos arquivos “por garantia”; abrir apenas o minimo necessario para retomar o passo seguinte

## Prompt de uso

`Use $session-bootstrap e continue de onde parou.`
