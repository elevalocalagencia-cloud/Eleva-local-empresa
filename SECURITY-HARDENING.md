# Security Hardening

## Objetivo

Reducao objetiva de risco para a VPS `elevalocal` sem quebrar a operacao dos stacks atuais.

## Superficie publica observada

- `80`
- `443`
- `8000` antes da mitigacao
- `8080` antes da mitigacao
- `6001-6002` antes da mitigacao

## Meta operacional

Deixar publicos apenas `80` e `443`.

## Prioridades

### P0 - imediatas

- manter `Coolify` e `coolify-realtime` fora da internet publica
- registrar como reabrir administracao apenas sob necessidade controlada
- rotacionar segredos potencialmente expostos na investigacao
- parar de usar `n8n user-management:reset` como procedimento operacional
- congelar versoes criticas do stack do `n8n`, principalmente Redis

### P1 - ate estabilizar os stacks

- confirmar periodicamente que `8000`, `8080` e `6001-6002` seguem fechados externamente
- restringir painel administrativo por IP, VPN ou tunnel
- revisar labels do Traefik por servico
- fixar versoes de imagem criticas e remover `latest`
- validar politicas de backup com copia fora da VPS

### P2 - padronizacao

- formalizar inventario de segredos
- definir janela de restore drill trimestral
- registrar RPO e RTO por stack

## Checklist pratico na VPS

### Mapear portas escutando

```bash
ss -tulpn
```

### Mapear containers e portas

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
```

### Verificar firewall

```bash
ufw status verbose
```

### Verificar labels do Traefik

```bash
docker inspect coolify-proxy --format '{{json .Config.Labels}}'
```

## Politica minima de segredos

- nao registrar segredo real em markdown do projeto
- guardar segredos fora do repositorio
- manter inventario privado de onde cada segredo vive
- rotacionar segredos sempre que houver suspeita de exposicao
- registrar data da ultima rotacao por stack

## Politica minima de imagens

- nao usar `latest` em producao para servicos criticos
- registrar versao atual antes de qualquer migracao
- promover upgrade apenas com backup + rollback prontos
- manter compatibilidade de versao de Redis com o formato dos dados persistidos
