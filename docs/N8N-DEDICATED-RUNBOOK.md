# n8n Dedicated Migration Runbook

## Objetivo

Migrar o `n8n` do stack compartilhado do Coolify para uma instancia dedicada, com corte controlado, sem migracao automatica de credenciais e com rollback seguro que preserva o container e os volumes compartilhados.

## Escopo

- inclui provisionamento da instancia dedicada
- inclui exportacao manual de workflows do ambiente compartilhado
- inclui importacao manual no ambiente dedicado
- inclui validacao de smoke test antes do corte
- inclui plano de rollback para o ambiente compartilhado
- nao inclui alteracao do stack shared do Coolify nem cutover automatico de DNS/webhook

## Premissas

- o `n8n` compartilhado continua disponivel ate a virada final
- o ambiente dedicado deve nascer com seus proprios recursos e sem reaproveitar o ciclo de vida do container compartilhado
- credenciais nao sao auto-migradas
- qualquer segredo usado no dedicado deve ser recriado manualmente com revisao humana
- o rollback preserva o stack compartilhado do Coolify, incluindo container e volumes atuais, sem limpeza destrutiva

## Provisionamento

### 1. Criar a instancia dedicada

Gerar a stack dedicada a partir do manifest:

```bash
python ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --dry-run
python ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot
```

Provisionar uma nova stack dedicada para `n8n` com:

- dominio proprio `wf-pilot.elevalocal.shop`
- Postgres proprio
- Redis proprio em Redis 7
- volume proprio para dados do `n8n`, sem reaproveitar `mamtm8g3b2mdh7ko0hxdcyr3_*`
- runtime independente do stack compartilhado
- labels e roteamento separados do ambiente antigo

Para subir na VPS depois de revisar `.env` real:

```bash
cd tenants/runtime/cli-eleva-pilot
docker compose --env-file .env up -d
```

### 2. Validar a base tecnica

Confirmar antes do corte:

- o novo container sobe com sucesso
- o editor responde no dominio dedicado
- a persistencia do volume novo esta funcional
- logs iniciais nao mostram erro de bootstrap
- o ambiente compartilhado permanece intacto
- `docker ps` ainda lista `n8n-mamtm8g3b2mdh7ko0hxdcyr3`

## Exportacao e importacao manual

### Exportar do compartilhado

1. congelar alteracoes de usuarios e automacoes no ambiente compartilhado
2. exportar workflows manualmente a partir do `n8n` compartilhado
3. registrar a lista de workflows exportados
4. registrar dependencias visiveis de cada workflow
5. conferir quais workflows usam credenciais que precisarao ser recriadas

### Importar no dedicado

1. importar os workflows manualmente no `n8n` dedicado
2. revisar nomes, tags, pastas e ativa/inativa de cada fluxo
3. apontar cada workflow para credenciais recriadas no dedicado
4. validar se os gatilhos e webhooks mantiveram o comportamento esperado
5. manter o compartilhado como fallback ate o smoke final

## Credenciais

- nao existe migracao automatica de credenciais entre o compartilhado e o dedicado
- nao copiar o cofre interno de credenciais do `n8n` entre instancias
- recriar credenciais manualmente no dedicado, uma a uma, com validacao humana
- manter a lista de mapeamento `workflow -> credencial` fora do fluxo de export/import automatico
- qualquer senha, token ou API key usada no dedicado deve vir do inventario de segredos, nao de replica cega

## Janela de corte

O corte deve ser tratado como janela curta e controlada:

1. deixar o dedicado pronto antes da virada
2. pausar escrita no compartilhado apenas no instante necessario para o delta final
3. executar o delta final de export/import manual
4. validar os smoke tests no dedicado
5. alterar o roteamento para o dominio dedicado
6. manter o compartilhado vivo por um periodo curto de observacao

Objetivo operacional:

- zero indisponibilidade perceptivel para usuarios finais durante a preparacao
- janela minima de bloqueio apenas no momento do switch
- nenhuma limpeza do compartilhado antes da aprovacao final

## Smoke validation

Executar smoke tests no dedicado antes de declarar o corte concluido:

- abrir o editor no dominio novo
- autenticar com o owner esperado
- carregar um workflow importado
- executar manualmente um workflow simples
- disparar um webhook de teste
- confirmar que logs do dedicado nao mostram erro de fila, banco ou proxy
- confirmar que o compartilhado ainda sobe e responde como fallback

Script de smoke:

```bash
ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop
```

Depois de importar um workflow de webhook dedicado para smoke:

```bash
EXPECTED_WEBHOOK_STATUS=200 ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop
```

Evidencia minima:

- URL do editor
- status do login
- nome do workflow testado
- resultado do webhook
- trecho de log sem erro critico

## Rollback

Se o smoke falhar ou surgir regressao apos o corte:

1. restaurar o roteamento para o stack compartilhado
2. manter intactos o container e os volumes compartilhados do Coolify
3. nao apagar o volume novo do dedicado durante o incidente
4. registrar a causa observada
5. validar acesso ao editor compartilhado
6. retomar operacao no estado anterior

Regras do rollback:

- nao destruir dados do compartilhado
- nao limpar volumes como parte do retorno
- nao tentar "corrigir" o compartilhado durante a janela de rollback
- nao considerar o rollback concluido sem validacao manual do editor

## Comunicacao

Usar as mensagens abaixo exatamente como copy operacional para a janela:

### Before

`Vamos mover seu fluxo de automação para um ambiente exclusivo seu. Janela prevista: {data} entre {hora_inicio} e {hora_fim}. Zero perda de histórico. Durante a janela, mensagens ficam na fila e são processadas ao final.`

### Success

`Migração concluída. Seu ambiente agora é 100% exclusivo, com performance e isolamento reforçados.`

### Fallback

`Detectamos comportamento fora do esperado. Retornamos ao ambiente anterior sem perda. Reagendaremos a migração após ajuste.`

## Checklist executavel

- [ ] instancia dedicada provisionada
- [ ] dominio dedicado respondendo
- [ ] exportacao manual dos workflows concluida
- [ ] importacao manual no dedicado concluida
- [ ] credenciais recriadas manualmente
- [ ] smoke tests aprovados
- [ ] janela de corte executada
- [ ] compartilhado mantido como fallback
- [ ] rollback testado ou pronto para acao

## Licoes aprendidas — Fase 1 Prompt 1.3-B

### Bug 1: colisao de hostname redis via rede coolify

- sintoma: `NOAUTH Authentication required` em crashloop no `n8n` dedicado.
- causa raiz: o service `redis` podia resolver o Redis da stack shared pela rede externa `coolify`, onde havia auth diferente da configuracao do dedicado.
- fix: service renomeado para `{tenant_id}-redis`, aplicado no provisioner e refletido em `depends_on` e `QUEUE_BULL_REDIS_HOST` do `n8n` e do `n8n-worker`.
- validacao: `grep` em `ops/provision-n8n-dedicated.py` deve mostrar `{tenant_id}-redis` ou `redis_service_name` cobrindo service, `depends_on` x2 e `QUEUE_BULL_REDIS_HOST` x2.

### Bug 2: labels Traefik fora do padrao Coolify

- sintoma: `404` em `http://dominio`; TLS e roteamento nao seguiam a convencao operacional esperada no Coolify.
- causa raiz: labels usavam `websecure` sem o router HTTP de redirect esperado pelo Traefik do Coolify.
- fix: labels reescritas para o padrao Coolify observado na VPS: router HTTP com middleware `redirect-to-https`, router HTTPS com `entrypoints=https`, `tls=true`, `tls.certresolver=letsencrypt`, `router.service=<service>` e service amarrado na porta `5678`.
- validacao: `render_compose` deve emitir router `-http`, router TLS, middleware `redirect-to-https` e `router.service` amarrado ao service do tenant.

## Regras finais

- nao automatizar a migracao de credenciais
- nao apagar o ambiente compartilhado antes da estabilizacao
- nao alterar `tenants/manifests/cli-eleva-pilot.yaml` para `dedicated` antes da migracao executada
- nao declarar migracao concluida sem smoke test e plano de rollback validado
