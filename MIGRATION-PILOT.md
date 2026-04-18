# Migration Pilot

## executado em {data} por {owner}

## Objetivo

Registrar o piloto operacional da migracao do `n8n` compartilhado para uma instancia dedicada, com foco em corte controlado, exportacao/importacao manual e rollback preservando o stack legado.

## Escopo do piloto

- provisionar a instancia dedicada
- exportar workflows do compartilhado manualmente
- importar workflows no dedicado manualmente
- recriar credenciais manualmente
- validar smoke test
- executar corte e fallback sem destruir o stack compartilhado

## Decisoes do piloto

- credenciais nao serao migradas automaticamente
- o stack compartilhado permanece vivo ate a validacao final
- o rollback preserva container e volumes compartilhados do Coolify
- o corte sera feito em janela curta, com bloqueio minimo para o delta final

## Sequencia do piloto

1. provisionar o ambiente dedicado
2. validar acesso inicial ao editor dedicado
3. congelar mudancas no compartilhado
4. exportar workflows manualmente
5. importar workflows no dedicado
6. recriar credenciais manualmente
7. executar smoke test
8. promover o corte
9. monitorar o pos-corte
10. aplicar rollback se houver regressao

## Comandos de preparacao

```bash
python ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot --dry-run
python ops/provision-n8n-dedicated.py --tenant-id cli-eleva-pilot
```

Na VPS, apos revisar `tenants/runtime/cli-eleva-pilot/.env`:

```bash
cd /root/elevalocal-infra/tenants/runtime/cli-eleva-pilot
docker compose --env-file .env up -d
```

Smoke:

```bash
ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop
```

## Evidencias

- URL do ambiente dedicado:
- owner responsavel:
- workflows exportados:
- workflows importados:
- credenciais recriadas:
- smoke test executado:
- shared ainda no ar (`n8n-mamtm8g3b2mdh7ko0hxdcyr3`):
- resultado do corte:
- resultado do fallback:

## Comunicacao ao cliente

### Antes

Vamos mover seu fluxo de automação para um ambiente exclusivo seu. Janela prevista: {data} entre {hora_inicio} e {hora_fim}. Zero perda de histórico. Durante a janela, mensagens ficam na fila e são processadas ao final.

### Sucesso

Migração concluída. Seu ambiente agora é 100% exclusivo, com performance e isolamento reforçados.

### Fallback

Detectamos comportamento fora do esperado. Retornamos ao ambiente anterior sem perda. Reagendaremos a migração após ajuste.

## Criterio de aceite

- editor do dedicado abre e autentica
- workflow importado executa com sucesso
- webhook responde no dominio novo
- nenhum segredo foi auto-migrado
- o compartilhado continua disponivel como fallback
- o rollback preserva o ambiente legado

## Registro operacional

Ao final do piloto, registrar se a operacao:

- aprovou o corte definitivo
- exigiu novo ciclo de ajuste
- retornou ao compartilhado por incidente
