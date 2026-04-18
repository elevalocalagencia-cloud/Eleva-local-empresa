# Offsite Validation Checklist

## Objetivo

Fechar o bloqueio de lancamento relacionado a copia offsite dos backups.

## Pre-requisitos

- [ ] host ou storage remoto preparado
- [ ] acesso SSH por chave a partir da VPS
- [ ] espaco suficiente no destino remoto
- [ ] `OFFSITE_ENABLED=true` configurado
- [ ] `OFFSITE_TARGET` configurado

## Execucao

1. ajustar `backup-elevalocal.env` na VPS
2. executar backup manual com offsite habilitado
3. listar o diretorio remoto recem-criado
4. conferir os artefatos minimos esperados

## Artefatos minimos no destino remoto

- [ ] `manifest.txt`
- [ ] `n8n-postgres.sql`
- [ ] `chatwoot-postgres.sql`
- [ ] `evolution-postgres.sql`
- [ ] `n8n-data.tar.gz`
- [ ] `chatwoot-rails-data.tar.gz`
- [ ] `evolution-instances.tar.gz`

## Validacao final

- [ ] diretorio remoto contem os SQLs esperados
- [ ] diretorio remoto contem os tarballs esperados
- [ ] owner do destino remoto registrado
- [ ] data da primeira copia valida registrada
- [ ] comando de verificacao documentado

## Evidencia a registrar

- destino remoto:
- owner responsavel:
- data da ultima validacao:
- caminho do diretorio remoto validado:
- observacoes:
