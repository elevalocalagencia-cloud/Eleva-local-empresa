# Evolution API Status

## Estado documental atual

O stack da `Evolution API` foi observado na VPS e ja tem prova operacional
basica, mas ainda nao tem runbook proprio no mesmo nivel do `n8n`.

## Containers observados

- `api-rh7m1i3wfmf9254fhcb4pn5p`
- `postgres-rh7m1i3wfmf9254fhcb4pn5p`
- `redis-rh7m1i3wfmf9254fhcb4pn5p`

## Volumes observados

- `rh7m1i3wfmf9254fhcb4pn5p_postgres-data`
- `rh7m1i3wfmf9254fhcb4pn5p_evolution-instances`
- `rh7m1i3wfmf9254fhcb4pn5p_evolution-redis`

## O que ja foi provado

- dominio operacional: `api.elevalocal.shop`
- `Evolution` conecta no WhatsApp
- backup local recorrente cobre banco e volumes observados do stack
- restore drill da `Evolution API`: validado em ambiente controlado

## O que ainda nao foi formalizado

- runbook proprio de operacao e recovery
- validacao periodica de webhook e endpoints externos
- registro de RPO/RTO do stack
- trilha operacional por tenant para instancias WhatsApp

## Verificacoes imediatas na VPS

### Estado dos containers

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep rh7m1i3wfmf9254fhcb4pn5p
```

### Env efetiva da API

```bash
docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}'
```

### Labels do proxy

```bash
docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .Config.Labels}}'
```

### Logs da API

```bash
docker logs --tail 200 api-rh7m1i3wfmf9254fhcb4pn5p
```

### Conferencia dos volumes

```bash
docker volume ls | grep rh7m1i3wfmf9254fhcb4pn5p
```

## Candidatos de dominio observados

Com base apenas no inventario atual, `api.elevalocal.shop` e `www.api.elevalocal.shop` parecem candidatos fortes para a `Evolution API`. Isso ainda precisa ser confirmado pelas labels do Traefik e pela env efetiva do container.

## Backup minimo necessario

### Banco

Usar [ops/backup-elevalocal.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh) ou executar manualmente:

```bash
docker inspect postgres-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}'
```

Depois, com usuario, senha e database confirmados:

```bash
docker exec -e PGPASSWORD='SENHA' -t postgres-rh7m1i3wfmf9254fhcb4pn5p pg_dump -U USUARIO -d DATABASE > /root/eleva-backups/evolution-$(date +%F-%H%M).sql
```

### Instancias persistentes

```bash
docker run --rm -v rh7m1i3wfmf9254fhcb4pn5p_evolution-instances:/source:ro -v /root/eleva-backups:/backup alpine sh -lc "cd /source && tar czf /backup/evolution-instances-$(date +%F-%H%M).tar.gz ."
```

## Restore minimo a provar

1. restaurar dump do Postgres em ambiente controlado
2. restaurar volume `evolution-instances`
3. subir a API com as mesmas envs
4. validar health endpoint
5. validar reconexao de uma instancia

## Riscos abertos

- sem runbook proprio de operacao
- sem prova documental local da persistencia das instancias apos reinicio controlado
- sem check operacional de webhook e autenticacao
