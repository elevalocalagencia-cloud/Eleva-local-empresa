# Smoke test - cli-demo-externo

- data: 2026-04-18
- alvo: `wf-demo.elevalocal.shop`

## Resultado desta sessao

- `nslookup wf-demo.elevalocal.shop` -> `NXDOMAIN`
- `curl` para `https://wf-demo.elevalocal.shop` nao foi executavel nesta sessao porque o DNS ainda nao resolve

## Proximo passo

1. criar o record `A` apontando para `2.24.199.157`
2. aguardar propagacao
3. subir a stack na VPS
4. repetir `curl -I` e `curl /healthz`
