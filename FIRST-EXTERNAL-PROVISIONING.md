# First External Provisioning

## Objetivo

Deixar o rollout do primeiro cliente externo em estado `shelf-ready`.

Ou seja: a parte tecnica esta preparada, com scaffold, checklist, inventario e
evidencia padronizada. A execucao real continua bloqueada ate existir cliente
comercial valido.

## Estado atual

- stack tecnica pronta para provisionamento controlado
- tenant de simulacao validado: `cli-demo-externo`
- portal sem hardcode do tenant piloto
- evidencias por tenant padronizadas em
  [tenants/evidence/TEMPLATE-evidence.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/TEMPLATE-evidence.md)
- contratos assinados fora do repo publico, com politica em
  [legal/signed/README.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/legal/signed/README.md)

## Pre-requisitos comerciais obrigatorios

Sem estes insumos, o gate nao pode ser executado de ponta a ponta:

- razao social e nome fantasia do cliente
- CNPJ valido
- `tenant_id` e `slug` finais
- owner operacional real com nome, e-mail e telefone
- numero WhatsApp dedicado do cliente
- cofre definido para segredos reais
- NDA assinado
- PSA assinado
- DPA assinado
- usuario inicial do portal com membership em `tenant_members`
- janela de go-live aprovada

## O que ja esta pronto para rodar

1. gerar tenant real com [ops/create-tenant.py](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/create-tenant.py)
2. validar manifest com
   [ops/validate-tenant-manifest.py](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/validate-tenant-manifest.py)
3. provisionar `Evolution`
4. provisionar `Chatwoot`
5. provisionar `n8n dedicated`
6. registrar evidencia datada em
   [tenants/evidence/TEMPLATE-evidence.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/TEMPLATE-evidence.md)
7. registrar assinados fora do repo publico conforme
   [legal/signed/README.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/legal/signed/README.md)

## Sequencia executiva

1. confirmar os pre-requisitos comerciais
2. executar backup novo antes da mudanca
3. gerar e validar o manifest do tenant
4. preencher inventario de segredos sem expor segredo em markdown
5. provisionar `Evolution`
6. provisionar `Chatwoot`
7. provisionar `n8n dedicated`
8. criar membership do usuario inicial no portal
9. rodar smoke tests ponta a ponta
10. registrar rollback path, owner, data e status final

## Checklist de pre-go-live

### A. Insumo comercial

- [ ] cliente real definido com razao social, CNPJ, `tenant_id` e `slug`
- [ ] owner operacional real registrado
- [ ] NDA assinado e arquivado fora do repo publico
- [ ] PSA assinado e arquivado fora do repo publico
- [ ] DPA assinado e arquivado fora do repo publico
- [ ] cofre real definido para segredos do tenant
- [ ] usuario inicial do portal definido
- [ ] janela de go-live aprovada

### B. Preparacao tecnica

- [ ] manifest revisado e validado no registry real
- [ ] inventario de segredos preenchido sem segredo em markdown
- [ ] checklist de onboarding revisado
- [ ] backup novo executado antes da mudanca
- [ ] restore path conhecido por stack
- [ ] offsite validado ou risco aceito formalmente para piloto controlado
- [ ] segredos necessarios rotacionados ou validados
- [ ] portas administrativas seguem fechadas externamente

## Provisionamento por stack

### 1. Evolution

- [ ] criar instancia `cli-{slug}-evo`
- [ ] vincular numero WhatsApp exclusivo do tenant
- [ ] registrar credencial da instancia no cofre correto
- [ ] validar webhook do tenant
- [ ] validar envio e recebimento basico

Evidencia a registrar:

- nome da instancia:
- numero vinculado:
- owner da credencial:
- resultado do smoke test:

### 2. Chatwoot

- [ ] criar inbox `cli-{slug}-inbox`
- [ ] registrar token e owner operacional
- [ ] aplicar labels e roteamento do tenant
- [ ] validar recebimento na inbox correta
- [ ] validar operacao basica do app e `sidekiq`

Evidencia a registrar:

- inbox criada:
- token armazenado em:
- owner:
- resultado do smoke test:

### 3. n8n dedicated

- [ ] provisionar workspace ou stack dedicada
- [ ] aplicar naming `cli-{slug}-wf-*`
- [ ] criar credenciais exclusivas do tenant
- [ ] publicar workflow minimo de onboarding
- [ ] registrar rollback path da stack

Evidencia a registrar:

- stack/workspace criada:
- prefixo dos workflows:
- owner das credenciais:
- rollback path:
- resultado do smoke test:

## Smoke tests obrigatorios

### Smoke test funcional

- [ ] mensagem entra pelo WhatsApp correto
- [ ] mensagem aparece na inbox correta do `Chatwoot`
- [ ] workflow do tenant roda no namespace correto
- [ ] nenhuma automacao usa credencial de outro tenant
- [ ] logs basicos nao mostram erro critico

### Smoke test de segregacao

- [ ] `n8n` do tenant e `dedicated`
- [ ] `Evolution` usa instancia exclusiva do tenant
- [ ] `Chatwoot` usa inbox exclusiva do tenant
- [ ] segredos do tenant nao aparecem no inventario de outro tenant
- [ ] rollback do tenant nao depende de desativar outro cliente

## Gate de encerramento

- [ ] onboarding checklist atualizado
- [ ] inventario de segredos atualizado
- [ ] `registry.yaml` revisado
- [ ] owner e data de revisao registrados
- [ ] status final do tenant marcado corretamente
- [ ] evidencia datada registrada em
      [tenants/evidence/TEMPLATE-evidence.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/TEMPLATE-evidence.md)

## Resultado esperado

Quando os insumos comerciais existirem e este checklist for concluido com
evidencia completa, a operacao pode reavaliar o veredito de lancamento para:

- `GO CONTROLADO para lancamento comercial inicial`
