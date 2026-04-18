# Landing CTA Spec

Especificacao para a landing comercial externa mantida fora deste repositorio.

## Regras gerais

- nao recriar landing neste repo
- usar textos leigos na camada publica
- evitar expor `.shop` em texto cru para publico geral
- excecao permitida: CTA de demo pode abrir a URL tecnica em nova aba, desde
  que o rotulo seja amigavel

## CTA 1 - Experimentar agora

- rotulo: `Experimentar agora`
- destino: `https://wf-demo.elevalocal.shop/?src=landing`
- comportamento: abrir em nova aba
- observacao: o parametro `src=landing` serve para atribuicao em access log do Traefik

## CTA 2 - Area do cliente

- rotulo: `Area do cliente`
- destino futuro: `https://portal.elevalocal.shop`
- comportamento: abrir em nova aba quando o portal publico estiver liberado
- status atual: manter oculto ou desabilitado ate publicacao oficial do portal

## CTA 3 - Agendar demo

- rotulo: `Agendar demo`
- destino: `{{FERNANDO_SCHEDULER_URL}}`
- comportamento: abrir em nova aba
- observacao: pode ser `Calendly` ou `Cal.com`

## CTA 4 - Contato comercial

- rotulo: `Contato comercial`
- destino funcional: formulario na landing que dispara webhook para `n8n`
- destino tecnico sugerido: webhook dedicado do fluxo comercial
- campos minimos: nome, empresa, WhatsApp, e-mail, contexto da operacao

## Evento de origem

- a landing deve enviar trafego para a demo com `?src=landing`
- a demo nao deve falhar se o parametro estiver ausente
- a medicao de conversao deve usar o access log do Traefik como trilha minima
