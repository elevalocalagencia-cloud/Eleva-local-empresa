# Skills Context

## Objetivo

Padronizar como retomar e fechar contexto da infraestrutura `elevalocal` em novas sessoes, sem misturar com o projeto `AutoVenda Pro`.

## Skill para retomar contexto

Comando:

```txt
Use $session-bootstrap.
```

### Ordem de leitura recomendada para a infra

1. [README.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/README.md)
2. [INVENTORY.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/INVENTORY.md)
3. [ARCHITECTURE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/ARCHITECTURE.md)
4. [N8N-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-STATUS.md)
5. [OPERATIONS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OPERATIONS.md)
6. [BACKUP-RESTORE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-RESTORE.md)
7. [HANDOFF.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/HANDOFF.md)

### Prompt recomendado de retomada

```txt
Use $session-bootstrap.
Contexto alvo: infraestrutura da elevalocal na VPS Hostinger.
Leia primeiro elevalocal-infra/README.md e siga a ordem descrita em elevalocal-infra/SKILLS-CONTEXT.md.
Ignore o produto AutoVenda Pro, exceto se eu pedir explicitamente.
```

## Skill para fechar contexto

Comando:

```txt
Use $session-close.
```

### Prompt recomendado de fechamento

```txt
Use $session-close.
Atualize somente o contexto da infraestrutura elevalocal.
Nao misture nada no contexto do AutoVenda Pro.
Se houve mudanca relevante, atualizar:
- elevalocal-infra/HANDOFF.md
- elevalocal-infra/N8N-STATUS.md
- elevalocal-infra/OPERATIONS.md
- elevalocal-infra/BACKUP-RESTORE.md
```

## Regra operacional

Se a sessao for sobre:

- `n8n`
- `Chatwoot`
- `Evolution API`
- `Coolify`
- `Traefik`
- dominios/subdominios
- backup/restore da VPS

entao o contexto deve ficar dentro de `elevalocal-infra/`.

Se a sessao for sobre:

- produto de carros
- frontend/backend do CRM
- Vercel do app
- Supabase do app

entao o contexto deve ficar no projeto `AutoVenda Pro`.
