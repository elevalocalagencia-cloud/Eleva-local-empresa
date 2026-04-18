# n8n Migration

## Objetivo

Migrar o `n8n` de um template gerado pelo Coolify para um compose proprio, preservando:

- banco Postgres existente
- Redis existente
- volume de dados existente do `n8n`
- dominio `https://n8m.elevalocal.shop`

## Resultado esperado

- eliminar o drift de `N8N_HOST` causado pelo template atual
- manter o acesso ao editor e webhooks no mesmo dominio
- permitir futuros deploys sem sobrescrever envs criticas

## Artefatos locais

- [n8n-compose/docker-compose.yml](C:/Users/PEDROSO/Downloads/elevalocal-infra/n8n-compose/docker-compose.yml)
- [n8n-compose/.env.example](C:/Users/PEDROSO/Downloads/elevalocal-infra/n8n-compose/.env.example)

## Premissas

- os volumes atuais existem e devem ser reaproveitados
- o Traefik continuara sendo a borda publica
- a migracao deve acontecer em janela controlada
- nao registrar segredos reais neste repositorio
- o stack atual do `n8n` deve permanecer com `redis:7-alpine`

## Volumes a reutilizar

- `mamtm8g3b2mdh7ko0hxdcyr3_n8n-data`
- `mamtm8g3b2mdh7ko0hxdcyr3_postgresql-data`
- `mamtm8g3b2mdh7ko0hxdcyr3_redis-data`

## Sequencia recomendada

1. Capturar o estado atual do stack em `/root/eleva-audit`.
2. Fazer novo dump do banco do `n8n`.
3. Confirmar o nome da rede do Traefik/Coolify na VPS.
4. Nao criar Postgres novo nem Redis novo na fase de cutover.
5. Subir apenas a camada de app (`n8n`, `n8n-worker`, `task-runners`) apontando para o Postgres e Redis atuais.
6. Garantir que a fila esteja drenada antes da virada.
7. Apontar o roteamento do Traefik para o novo servico.
8. Validar editor, login, execucao de workflow e webhook.
9. Desativar o stack antigo somente depois da validacao final.

## Checklist pre-migracao

- `docker volume ls | grep mamtm8g3b2mdh7ko0hxdcyr3`
- `docker network ls`
- `docker ps --format "table {{.Names}}\t{{.Status}}"`
- dump novo do Postgres do `n8n`
- snapshot do compose atual

## Validacao pos-migracao

- `curl -vkI https://n8m.elevalocal.shop`
- login manual no editor
- abrir um workflow existente
- disparar um webhook de teste
- confirmar `N8N_HOST=n8m.elevalocal.shop`
- checar logs do container principal e worker
- confirmar que nao houve execucao duplicada de jobs

## Rollback

1. parar o compose proprio
2. religar o stack antigo
3. validar dominio e login
4. somente considerar rollback concluido apos teste manual do editor
5. nao tentar rollback com Redis 6

## Riscos conhecidos

- nome incorreto da rede externa do Traefik
- labels de proxy divergentes do ambiente atual
- versao da imagem do `n8n` diferente da atual
- variaveis antigas do stack gerado ainda estarem sendo assumidas por automacoes externas
- tentativa de rollback com `redis:6-alpine` em volume que ja gerou RDB compativel com Redis 7

## Regra operacional

Nao executar a migracao sem:

- backup novo do banco
- verificacao do nome real da rede
- plano de rollback pronto
- Redis 7 mantido no stack atual
