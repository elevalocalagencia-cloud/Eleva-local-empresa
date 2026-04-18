# Seed workflows da demo

Arquivos JSON com workflows fake para demonstrar capacidade do `n8n`.

Import oficial:

```bash
docker compose --env-file .env exec -T n8n n8n import:workflow --separate --input=/seed-workflows
```

Workflows incluídos:

- `agendamento-automatico.json`
- `follow-up-de-lead.json`
- `faq-whatsapp.json`
