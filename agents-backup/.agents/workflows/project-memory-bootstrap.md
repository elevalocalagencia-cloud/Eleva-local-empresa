# /project-memory-bootstrap

Use este workflow ao iniciar sessoes neste workspace.

1. Ler `PROJECT.md`
2. Ler `STATE.md`
3. Ler `.memory/session-snapshot.json`
4. Ler `autovenda-pro-b2b-main/docs/HANDOFF.md`
5. Ler `.agents/scratchpad.md` apenas como contexto complementar
6. Confirmar se a tarefa vai atuar na raiz do workspace ou no app em `autovenda-pro-b2b-main/`
7. So depois abrir arquivos de codigo do escopo ativo

## Objetivo

- Reconstruir o contexto util sem depender do chat anterior
- Evitar confundir a raiz Git com a raiz do app
- Preservar a memoria persistente em arquivos simples e auditaveis

## Atualizacao ao encerrar

- Atualizar `STATE.md` se a fase mudou
- Atualizar `.memory/session-snapshot.json` com proximo passo e riscos
- Registrar decisao duravel em `.memory/decisions.md` quando houver mudanca arquitetural ou operacional
