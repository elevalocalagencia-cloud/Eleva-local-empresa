# Objecoes recorrentes

## 1. "Como voces tratam LGPD?"

Usamos pacote juridico com `PSA`, `DPA-LGPD` e `SLA`, alem de segregacao por
tenant, ownership de credenciais e trilha documental para onboarding.

## 2. "Como fica seguranca da operacao?"

A camada tecnica trabalha com isolamento por tenant, secrets separados,
guardrails de onboarding e runbooks de backup/restore versionados.

## 3. "Qual uptime voces garantem?"

No piloto assistido, o compromisso e o previsto em `SLA-PILOT`, com rollout
controlado e acompanhamento manual forte antes de qualquer escala.

## 4. "O preco do piloto e alto."

O piloto reduz risco de rollout errado e encurta o tempo para provar valor sem
contratar estrutura completa de uma vez.

## 5. "Quanto tempo demora para entrar no ar?"

O prazo depende do discovery e dos acessos, mas o modelo foi desenhado para
go-live controlado, com janela operacional clara e escopo fechado.

## 6. "Quem presta suporte no comeco?"

O inicio e assistido. A equipe acompanha onboarding, homologacao e primeiros
passos conforme o anexo `SLA-PILOT`.

## 7. "Preciso trocar o numero de WhatsApp?"

Isso depende do setup atual e do discovery tecnico. A avaliacao entra antes do
go-live para evitar mudanca improvisada em producao.

## 8. "Se eu quiser exportar meus dados?"

Exportacao e retencao devem constar na proposta e nos anexos legais, com regra
definida antes da entrada em operacao.

## 9. "E se eu rescindir?"

Rescisao, retencao e responsabilidades ficam amarradas no contrato e no pacote
legal para evitar ambiguidade operacional.

## 10. "Tenho sistema atual. Voces migram tudo?"

O piloto nao assume migracao total por padrao. Primeiro validamos aderencia,
escopo e integracoes realmente necessarias.
