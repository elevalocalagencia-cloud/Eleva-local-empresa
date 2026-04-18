# STATE

## Fase atual

Fundacao multi-cliente em execucao.

Readiness de launch:

- operacao controlada: `SIM`
- readiness comercial ampla: `NAO`

## Status

- schema de manifest consolidado
- scaffold operacional por tenant funcionando
- tenant piloto interno criado e validado
- documentacao base de tenant pronta para uso
- matriz de provisionamento por stack consolidada no manifest e na documentacao
- guardrail de onboarding no scaffolder impedindo cliente externo em `n8n shared-foundation`
- templates operacionais alinhados com revisao de `provisioning.*`
- tenant externo de simulacao `cli-demo-externo` criado, revisado e validado

## Proximo passo concreto

Executar o primeiro provisionamento real de cliente externo:

1. promover `cli-demo-externo` para cliente real equivalente ou criar tenant real
2. preencher owners e cofres reais de segredos
3. provisionar `Evolution`, `Chatwoot` e `n8n dedicated`
4. registrar smoke tests e restore status

Bloqueios P0 ainda abertos antes de `GO CONTROLADO`:

- offsite backup validado
- rotacao de segredos
- freeze de versao do `Chatwoot`
- provisionamento externo real ponta a ponta

## Snapshot de verificacao

- testes atuais: `10 passed`
- exemplo de template: valido
- tenant piloto `cli-eleva-pilot`: valido no registry real
- tenant externo `cli-demo-externo`: valido no registry real
