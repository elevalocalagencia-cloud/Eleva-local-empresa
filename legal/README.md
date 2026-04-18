# Pacote juridico-comercial minimo

Este diretorio concentra os modelos base para venda, onboarding e operacao da `Eleva Local`.

## Ordem recomendada de uso

1. `NDA-TEMPLATE.md`
   - usar na pre-venda, antes de compartilhar detalhes de stack, pricing, fluxos ou dados do cliente.
2. `CONTRATO-PSA-TEMPLATE.md`
   - usar no fechamento comercial como contrato principal.
3. `DPA-LGPD-TEMPLATE.md`
   - anexar obrigatoriamente ao PSA sempre que houver tratamento de dados pessoais do cliente.
4. `SLA-PILOT.md` ou `SLA-COMERCIAL.md`
   - anexar ao PSA conforme a fase contratada.
   - `SLA-PILOT.md`: onboarding controlado, operacao altamente assistida.
   - `SLA-COMERCIAL.md`: operacao pos-lancamento, com dedicacao e janelas de resposta mais curtas.
5. `PRIVACIDADE-PORTAL.md`
   - publicar no footer do portal e revisar os placeholders antes de ir para producao.

## Como preencher

- substituir todos os campos no formato `{{VARIAVEL_UPPERCASE}}`
- validar se o cliente ficara em `piloto` ou `comercial`
- validar no manifesto do tenant:
  - `tenant_id`
  - `runtime_mode` por stack
  - ownership de credenciais
  - `security.lgpd_notes`
- revisar se o escopo vendido bate com:
  - `MULTITENANT-AUDIT.md`
  - `LAUNCH-AUDIT.md`
  - `tenants/templates/onboarding-checklist.md`
  - `tenants/templates/client-ops-checklist.md`

## Regras de assinatura

- `NDA` pode ser assinado sozinho.
- `PSA` nao deve circular sem `DPA`.
- o `SLA` sempre entra como anexo do `PSA`.
- a politica de privacidade nao substitui o `DPA`; ela cobre transparencia ao usuario do portal.

## Exportacao para `.docx`

Os arquivos foram estruturados com headings, listas e numeracao simples para exportacao limpa.

### Opcao 1 - Word

1. abrir o `.md` no Word
2. revisar quebras de pagina e placeholders
3. salvar como `.docx`

### Opcao 2 - Pandoc

Se `pandoc` estiver disponivel no ambiente:

```powershell
pandoc legal\CONTRATO-PSA-TEMPLATE.md -o legal\CONTRATO-PSA-TEMPLATE.docx
pandoc legal\DPA-LGPD-TEMPLATE.md -o legal\DPA-LGPD-TEMPLATE.docx
pandoc legal\NDA-TEMPLATE.md -o legal\NDA-TEMPLATE.docx
pandoc legal\SLA-PILOT.md -o legal\SLA-PILOT.docx
pandoc legal\SLA-COMERCIAL.md -o legal\SLA-COMERCIAL.docx
pandoc legal\PRIVACIDADE-PORTAL.md -o legal\PRIVACIDADE-PORTAL.docx
```

## Ajustes obrigatorios antes de enviar ao cliente

- preencher razao social, CNPJ, representantes e valores
- revisar foro ou arbitragem conforme politica comercial
- confirmar suboperadores efetivamente ativados para o tenant
- confirmar retencao aplicavel apos rescisao
- revisar se o cliente exige anexo proprio de seguranca

## Artefatos tecnicos citados neste pacote

- `MULTITENANT-AUDIT.md`
- `LAUNCH-AUDIT.md`
- `OFFSITE-VALIDATION-CHECKLIST.md`
- `SECRET-ROTATION-CHECKLIST.md`
- `CHATWOOT-VERSION-FREEZE.md`
- `FIRST-EXTERNAL-PROVISIONING.md`
- `docs/RESTIC-RUNBOOK.md`
- `docs/N8N-DEDICATED-RUNBOOK.md`
- `docs/SECRETS-MANAGEMENT.md`
- `tenants/templates/tenant-manifest.example.yaml`
- `tenants/templates/onboarding-checklist.md`
- `tenants/templates/client-ops-checklist.md`
- `apps/portal/supabase/migrations/0001_portal_schema.sql`
- `ops/smoke-test-tenant.sh`
