# Portal Eleva Local

Portal client-facing v1 para mostrar valor mensal da operacao automatizada por tenant.

## Stack

- Next.js 15 App Router
- React 19
- TypeScript strict
- Tailwind CSS v4
- Supabase Auth + RLS
- Chatwoot API server-side
- Evolution API server-side
- Vercel

## Rotas

- `/login`: magic link via Supabase Auth
- `/dashboard`: resumo do mes
- `/mensagens`: conversas read-only vindas do Chatwoot
- `/agendamentos`: lista e filtros iniciais
- `/configuracoes`: dados do tenant e assinatura

## Setup local

```bash
corepack enable
pnpm install
cp apps/portal/.env.example apps/portal/.env.local
pnpm --filter portal dev
```

## Variaveis de ambiente

Variaveis `NEXT_PUBLIC_*` podem ir para o browser. Todas as demais sao server-only.

```bash
NEXT_PUBLIC_APP_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
CHATWOOT_BASE_URL=
CHATWOOT_ACCOUNT_ID=
CHATWOOT_API_ACCESS_TOKEN=
EVOLUTION_BASE_URL=
EVOLUTION_API_KEY=
```

Nunca exponha `CHATWOOT_API_ACCESS_TOKEN`, `EVOLUTION_API_KEY` ou `SUPABASE_SERVICE_ROLE_KEY` no client.

## Supabase

Aplicar a migration:

```bash
supabase db push
```

Schema principal:

- `tenant_members(tenant_id, user_id, role)`
- `portal_conversation_snapshots`
- `portal_bookings`

Regra de isolamento:

```sql
auth.uid() in (
  select user_id from tenant_members where tenant_id = row.tenant_id
)
```

## Deploy Vercel

1. Criar projeto Vercel apontando para `apps/portal`.
2. Configurar envs de preview/producao.
3. Rodar build:

```bash
pnpm --filter portal build
```

## Gates

```bash
pnpm --filter portal typecheck
pnpm --filter portal lint
pnpm --filter portal test
```

Lighthouse alvo:

- Performance >= 90
- Accessibility >= 95

Dashboard alvo:

- carregar em menos de 1.5s em 3G simulado apos primeiro cache.
