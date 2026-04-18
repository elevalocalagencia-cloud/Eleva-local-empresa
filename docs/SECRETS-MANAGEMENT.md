# Secrets Management

## Objetivo

Padronizar rotacao, ownership e armazenamento seguro de segredos operacionais da infraestrutura Eleva Local.

## Regras base

- nenhum segredo real fica em markdown do repositorio
- qualquer inventario legivel deve morar em `tenants/secrets/.vault/` e ser cifrado com `sops` + `age`
- a chave privada local (`*.key`) nao entra no git
- a evidencia operacional da rotacao deve ser registrada fora do corpo do segredo

## Ownership

- `eleva-local-ops` e o owner operacional da infraestrutura compartilhada
- o owner do tenant responde pelos segredos especificos daquele cliente
- toda rotacao precisa registrar quem executou, quem aprovou e quem valida

## Cadencia

- rotacao trimestral para segredos de producao
- rotacao imediata apos incidente, suspeita de exposicao ou acesso indevido
- revisao extraordinaria apos onboarding de cliente novo ou alteracao de provider

## Fluxo recomendado

1. identificar o stack afetado
2. registrar o conjunto de segredos no checklist
3. rotacionar um stack por vez
4. validar acesso funcional depois da troca
5. invalidar a credencial anterior
6. registrar evidencia no vault cifrado e no checklist de rotacao

## Pontos de integracao

- `ops/rotate-secrets.sh`
- `SECRET-ROTATION-CHECKLIST.md`
- `tenants/secrets/.vault/README.md`

## Politica de excecao

Qualquer compartilhamento temporario de segredo precisa ter:

- justificativa
- aprovador
- prazo de expiracao
- data de remocao da excecao

Sem isso, a excecao nao e aceitavel.
