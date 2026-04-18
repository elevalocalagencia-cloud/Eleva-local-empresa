# Demo publica - cli-demo-externo

Este runtime e a vitrine publica permanente da Eleva Local.

URL alvo:

- `https://wf-demo.elevalocal.shop`

## Guardrails

- nao conectar WhatsApp real do Fernando
- nao conectar numero de cliente pagante
- nao expor token admin em URL publica
- dados resetam automaticamente
- demo mostra `n8n` e portal; integracao `WhatsApp/Chatwoot` fica para onboarding real

## Deploy

1. gerar `.env` a partir de `.env.example`
2. preencher segredos novos com `openssl rand -hex 32`
3. subir na VPS:

```bash
cd /root/elevalocal-infra/tenants/runtime/cli-demo-externo
docker compose --env-file .env up -d
```

## Import de workflows fake

O volume `./seed-workflows` e montado no container `n8n` como `/seed-workflows`.

Import:

```bash
docker compose --env-file .env exec -T n8n n8n import:workflow --separate --input=/seed-workflows
```

Referencia oficial do CLI n8n:

- [CLI commands](https://docs.n8n.io/hosting/cli-commands/)

## Owner demo

- e-mail previsto: `demo@elevalocal.shop`
- senha: guardar apenas em cofre interno
- 2FA: opcional para demo

Observacao:

- o CLI do n8n documenta `user-management:reset`, mas a criacao do owner volta
  para o fluxo de setup da UI. Por isso, a recriacao do owner continua sendo
  passo manual controlado na primeira subida apos reset total de banco.

## Reset semanal

Script:

- [ops/reset-demo.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/reset-demo.sh)

Cron alvo na VPS:

```cron
0 3 * * 0 /root/elevalocal-infra/ops/reset-demo.sh
```
