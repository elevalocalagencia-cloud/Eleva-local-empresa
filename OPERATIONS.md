# Operations

## Regras

- executar um comando por vez no terminal da VPS
- evitar colar blocos grandes no console serial
- nao confiar na UI do Coolify como unica fonte de verdade
- usar `docker inspect`, `docker ps` e arquivos em `/root/eleva-audit` como referencia operacional
- antes de qualquer alteracao em producao, gerar backup novo
- cliente novo so entra com `tenant_id` e `slug` definidos
- cliente novo so entra com manifest YAML validado

## Operacao por tenant

### Scaffold inicial

Comando base:

```bash
python ops/create-tenant.py --tenant-id cli-acme --slug acme --company-name "Acme LTDA" --owner-name "Nome" --owner-email ops@acme.com --owner-phone +5511999999999 --whatsapp-number +5511999999999
```

Saida esperada:

- `tenants/manifests/cli-acme.yaml`
- `tenants/secrets/cli-acme.md`
- `tenants/checklists/cli-acme-onboarding.md`
- `tenants/checklists/cli-acme-ops.md`
- `tenants/registry.yaml` atualizado

Regra:

- nao criar tenant novo copiando template na mao se o CLI cobrir o caso
- qualquer ajuste manual no manifest deve ser revalidado antes do rollout
- primeiro cliente externo deve seguir [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md)

### Naming obrigatorio

- `tenant_id`: identificador canonico interno do cliente
- `slug`: identificador kebab-case usado em instancias, inboxes, workflows e segredos
- padrao recomendado:
  - `cli-{slug}-evo`
  - `cli-{slug}-inbox`
  - `cli-{slug}-wf-*`
  - `cli-{slug}-secret-*`

### Validacao de manifest

Arquivo:

```bash
ops/validate-tenant-manifest.py
```

Uso minimo:

```bash
python ops/validate-tenant-manifest.py CAMINHO_DO_MANIFEST.yaml
```

Com registry:

```bash
python ops/validate-tenant-manifest.py CAMINHO_DO_MANIFEST.yaml --registry CAMINHO_DO_REGISTRY.yaml
```

Objetivo:

- garantir o schema canonico aninhado por tenant
- validar formato de `slug`
- impedir conflito basico de `tenant_id` e `slug` com registry existente

## Comandos de verificacao

### Containers

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```

### n8n host efetivo

```bash
docker inspect n8n-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep '^N8N_HOST='
```

### Dominio/SSL

```bash
curl -vkI https://n8m.elevalocal.shop
```

### Owner atual no Postgres do n8n

```bash
N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_USER=/{print $2}')"
docker exec -it postgresql-mamtm8g3b2mdh7ko0hxdcyr3 psql -U "${N8N_DB_USER}" -d n8n -c 'select email, "firstName", "lastName", disabled from "user";'
```

## Recuperacao de acesso do n8n

Usar `n8n user-management:reset` apenas em emergencia real.

Comando:

```bash
docker exec -it n8n-mamtm8g3b2mdh7ko0hxdcyr3 n8n user-management:reset
```

Efeito:

- remove o estado atual de usuarios/owner
- exige recriacao da conta owner

## Hotfix temporario do compose

Arquivo:

```bash
/data/coolify/services/mamtm8g3b2mdh7ko0hxdcyr3/docker-compose.yml
```

Linha correta:

```yaml
N8N_HOST: 'n8m.elevalocal.shop'
```

Aplicacao:

```bash
cd /data/coolify/services/mamtm8g3b2mdh7ko0hxdcyr3 && docker compose up -d
```

## Portas publicas a revisar

- `8000`
- `8080`
- `6001-6002`

Estado atual:

- manter publicos apenas `80` e `443`
- `8000`, `6001` e `6002` foram mitigadas e deixaram de responder externamente
- `Coolify` e `coolify-realtime` foram retirados da internet publica como medida de emergencia

Reabertura administrativa somente sob necessidade controlada:

```bash
docker update --restart=unless-stopped coolify coolify-realtime
docker start coolify-realtime coolify
```

## Backup operacional consolidado

Script base:

```bash
bash /CAMINHO/elevalocal-infra/ops/backup-elevalocal.sh
```

Antes de confiar nesse script em producao:

1. confirmar artefatos nos 3 diretorios mais recentes em `/root/eleva-backups`
2. revisar `/var/log/elevalocal-backup.log`
3. manter restore drill periodico em ambiente controlado
4. registrar ultimo `backup check` por tenant no registry/manifest correspondente

## Troubleshooting validado nesta sessao

### n8n sem acesso

Se o `n8n` abrir mas o owner estiver em estado inconsistente:

1. gerar dump novo do banco
2. verificar tabela `"user"`
3. usar `n8n user-management:reset` somente se houver confirmacao de owner quebrado
4. recriar owner imediatamente

### Evolution + Chatwoot

Foi validado que:

- `Evolution` conecta no WhatsApp
- `Chatwoot` responde corretamente quando autenticado com `api_access_token`

O endpoint de configuracao `/chatwoot/set/{instance}` na `Evolution API v2.3.7` se mostrou instavel nesta operacao.
Preferencia operacional atual:

- configurar via manager da `Evolution`
- validar token do `Chatwoot` manualmente com `curl`

### n8n rollback / Redis

Foi validado que o stack atual do `n8n` nao pode mais voltar para `redis:6-alpine`.

Motivo:

- Redis 6 falha ao ler o formato de dados persistidos gerado por Redis 7

Regra:

- manter `redis:7-alpine` no stack atual do `n8n`
- tratar qualquer futura migracao como troca de camada de app, nao recriacao cega do stack inteiro
