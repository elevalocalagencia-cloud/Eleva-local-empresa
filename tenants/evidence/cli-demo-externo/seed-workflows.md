# Seed workflows - cli-demo-externo

- `agendamento-automatico.json`
- `follow-up-de-lead.json`
- `faq-whatsapp.json`

Todos sao workflows fake e podem ser commitados.

Import esperado:

```bash
docker compose --env-file .env exec -T n8n n8n import:workflow --separate --input=/seed-workflows
```
