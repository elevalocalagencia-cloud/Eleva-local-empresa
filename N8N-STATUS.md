# n8n Status

## Dominio atual

- `https://n8m.elevalocal.shop`

## Diagnostico fechado

### O que nao era o problema

- nao foi falta de volume
- nao foi container quebrado
- nao foi perda de Postgres

### O que realmente aconteceu

1. o owner foi apagado por `n8n user-management:reset`
2. o template do Coolify reescrevia `N8N_HOST` para `${SERVICE_URL_N8N}`
3. isso criava configuracao errada para proxy reverso

## Estado confirmado

- volumes persistentes do `n8n`: OK
- Postgres do `n8n`: OK
- SSL/Traefik para `n8m.elevalocal.shop`: OK
- hotfix runtime no compose local: OK
- owner recriado com sucesso apos `n8n user-management:reset`
- stack atual estabilizado com `redis:7-alpine`

## Valor correto das envs

```env
N8N_HOST=n8m.elevalocal.shop
N8N_PROTOCOL=https
N8N_EDITOR_BASE_URL=https://n8m.elevalocal.shop
WEBHOOK_URL=https://n8m.elevalocal.shop
N8N_SECURE_COOKIE=true
N8N_PROXY_HOPS=1
```

## Hotfix aplicado

No compose local do servico:

```yaml
N8N_HOST: 'n8m.elevalocal.shop'
```

## Risco aberto

Se houver novo deploy pela UI/template atual do Coolify, o valor pode voltar a ser sobrescrito.

## Incidente de auth encerrado

Foi confirmado no banco que o estado quebrado era um usuario owner incompleto, com `userManagement.isInstanceOwnerSetUp=true`.

Correcao aplicada:

1. backup novo do banco
2. `n8n user-management:reset`
3. recriacao do owner

Estado final da sessao:

- owner do `n8n`: OK
- login do `n8n`: recuperado

## Correcao definitiva

Mover o `n8n` para um compose proprio, fora do template gerado, reaproveitando os mesmos volumes.

## Licao operacional obrigatoria

Nao tentar rollback do stack atual do `n8n` com `redis:6-alpine`.

Foi provado nesta sessao que:

- o volume do Redis passou a conter dados em formato compativel com Redis 7
- Redis 6 falha com `Can't handle RDB format version 12`

Regra atual:

- manter `redis:7-alpine` no stack antigo ate a migracao definitiva
- replanejar a migracao do `n8n` sem duplicar Redis/Postgres
