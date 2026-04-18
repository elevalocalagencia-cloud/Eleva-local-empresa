# Chatwoot Version Freeze

## Objetivo

Fechar o bloqueio de lancamento relacionado ao uso de `latest` no `Chatwoot`.

## Estado atual

- imagem observada no runbook: `chatwoot/chatwoot:latest`
- risco atual: drift de deploy e rollback nao deterministico

## Passos obrigatorios

1. inspecionar a imagem atualmente em execucao na VPS
2. registrar a tag ou digest efetivo
3. escolher a versao explicita alvo
4. atualizar stack para usar tag fixa
5. registrar rollback para a mesma versao

## Evidencia a coletar

- imagem atual observada:
- digest atual observado:
- versao congelada escolhida:
- data da mudanca:
- responsavel:

## Gate de encerramento

- [ ] stack nao usa mais `latest`
- [ ] versao fixa registrada no runbook
- [ ] rollback da mesma versao documentado
- [ ] smoke test do app e worker executado
