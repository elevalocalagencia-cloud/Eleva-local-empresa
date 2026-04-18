# First External Provisioning

## Objetivo

Executar o primeiro provisionamento real de cliente externo com risco controlado,
usando o tenant de simulacao `cli-demo-externo` como baseline operacional.

Este documento fecha o ultimo bloqueio P0 da auditoria de lancamento que ainda
depende de prova ponta a ponta em ambiente real.

## Baseline atual

- tenant de simulacao validado: `cli-demo-externo`
- manifest valido no registry real
- `Evolution`: `shared-foundation` com instancia dedicada por tenant
- `Chatwoot`: `shared-foundation` com inbox dedicada por tenant
- `n8n`: `dedicated` para cliente externo

## Regra de uso

- nao provisionar cliente externo direto na VPS sem manifest valido
- nao usar `n8n shared-foundation` para cliente externo
- nao fazer go-live sem backup novo e rollback claro
- nao marcar lancamento como pronto sem smoke test por stack

## Sequencia executiva

1. promover o tenant demo para cliente real equivalente ou gerar tenant real
2. preencher owners e cofres reais de segredos
3. provisionar `Evolution`
4. provisionar `Chatwoot`
5. provisionar `n8n dedicated`
6. executar smoke tests ponta a ponta
7. registrar rollback path, owners e status final

## Checklist de pre-go-live

### Tenant e governanca

- [ ] tenant real definido com `tenant_id` e `slug` finais
- [ ] manifest revisado e validado no registry real
- [ ] inventario de segredos preenchido sem segredo em markdown
- [ ] owner operacional real registrado
- [ ] checklist de onboarding revisado

### Backup e seguranca

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

## Resultado esperado

Ao concluir este checklist com evidencia completa, a operacao pode reavaliar o
veredito da auditoria de lancamento e tentar mover o status para:

- `GO CONTROLADO para lancamento comercial inicial`
