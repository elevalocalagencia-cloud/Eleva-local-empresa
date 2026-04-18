# Domain Strategy

## Objetivo

Separar com clareza a camada comercial publica da camada tecnica operacional da
`Eleva Local`.

## Dominio comercial

- `elevalocal.com.br`
- papel: site publico comercial
- ownership atual: mantido fora deste repositorio
- uso esperado: copy comercial, prova social, formularios e CTA leigo

## Dominio tecnico

- `elevalocal.shop`
- papel: infraestrutura tecnica e subdominios operacionais
- subdominios conhecidos:
  - `chat.elevalocal.shop`
  - `api.elevalocal.shop`
  - `wf-demo.elevalocal.shop`
  - `portal.elevalocal.shop`
  - `wf-*` para runtimes tecnicos por tenant

## Regra de exposicao

- nunca expor `.shop` em material comercial voltado a publico leigo
- usar `.shop` apenas em contexto tecnico, onboarding, suporte ou cliente ja contratado
- em materiais comerciais, preferir rotulos funcionais como `Experimentar agora`
  e `Area do cliente`

## Excecao controlada

- `wf-demo.elevalocal.shop` pode aparecer como destino tecnico do CTA de demo
- na camada publica, o CTA deve usar wrapper amigavel como `Experimentar aqui`
  ou `Experimentar agora`, sem mostrar o dominio cru no corpo do texto

## Regra operacional

- documentacao comercial aponta para esta estrategia antes de citar qualquer dominio
- a landing externa segue a especificacao em [docs/sales/LANDING-CTA-SPEC.md](C:/Users/PEDROSO/Downloads/elevalocal-infra-sales/docs/sales/LANDING-CTA-SPEC.md)
- a documentacao tecnica continua registrando os subdominios reais em runbooks e evidencias
