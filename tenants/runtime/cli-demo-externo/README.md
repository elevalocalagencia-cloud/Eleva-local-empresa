# Demo publica - cli-demo-externo

Este runtime e a vitrine publica permanente da `Eleva Local`.

URL alvo:

- `https://wf-demo.elevalocal.shop`

## Guardrails

- nao conectar WhatsApp real do Fernando
- nao conectar numero de cliente pagante
- nao expor token admin em URL publica
- dados resetam automaticamente
- demo mostra `n8n` e portal; integracao `WhatsApp/Chatwoot` fica para onboarding real
- acessos via `?src=landing` devem funcionar sem alterar a experiencia da demo

## Origem de trafego da landing

- CTA publico recomendado: `https://wf-demo.elevalocal.shop/?src=landing`
- objetivo: medir conversao minima landing -> demo
- trilha tecnica esperada: access log do Traefik contendo a query string
- comportamento esperado: se `src` estiver ausente, a demo continua abrindo normalmente

## Deploy

1. gerar `.env` a partir de `.env.example`
2. preencher segredos novos com `openssl rand -hex 32`
3. subir na VPS:

```bash
cd /root/elevalocal-infra/tenants/runtime/cli-demo-externo
docker compose --env-file .env up -d
```
