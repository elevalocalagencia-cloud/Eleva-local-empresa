# ANEXO DE PROCESSAMENTO DE DADOS PESSOAIS - DPA LGPD

Este anexo integra o `CONTRATO-PSA-TEMPLATE.md` celebrado entre:

- **Controladora**: `{{CLIENTE_RAZAO_SOCIAL}}`, CNPJ `{{CLIENTE_CNPJ}}`
- **Operadora**: `{{CONTRATADA_RAZAO_SOCIAL}}`, CNPJ `{{CONTRATADA_CNPJ}}`

## 1. Definicoes

1.1. Aplicam-se as definicoes da Lei no 13.709/2018, especialmente as de dado pessoal, titular, controlador, operador e tratamento previstas no art. 5o.

1.2. Para os fins deste anexo:
- **Controladora**: a CONTRATANTE, a quem competem as decisoes sobre o tratamento relacionado ao atendimento e as automacoes do seu negocio;
- **Operadora**: a CONTRATADA, que realiza tratamento em nome da Controladora, nos termos do art. 39 da LGPD;
- **Suboperador**: terceiro contratado pela Operadora para executar parte da infraestrutura, hospedagem, mensageria, banco de dados, backup, observabilidade ou IA.

## 2. Objeto e finalidade

2.1. Os dados pessoais tratados pela Operadora limitam-se ao necessario para a execucao do objeto contratual, incluindo implementacao, suporte, operacao continua de automacoes B2B, atendimento omnichannel, portal de acompanhamento, suporte tecnico, seguranca, auditoria e continuidade.

2.2. A Operadora nao utilizara os dados pessoais para finalidade propria incompativel com o objeto contratado.

2.3. A Operadora observara os principios da finalidade, adequacao, necessidade, transparencia, seguranca, prevencao e responsabilizacao previstos no art. 6o da LGPD.

## 3. Categorias de dados e titulares

3.1. Salvo ajuste especifico em `{{ANEXO_MAPEAMENTO_DADOS}}`, o tratamento podera envolver:
- dados cadastrais de representantes, colaboradores e contatos da Controladora;
- dados de atendimento e relacionamento comercial de clientes finais da Controladora;
- logs de acesso, trilhas de auditoria, identificadores de tenant e metadados de operacao;
- registros de agenda, funil, historico de mensagens e snapshots operacionais do portal.

3.2. Em regra, nao se pretende o tratamento de dados pessoais sensiveis. Se houver essa necessidade, devera haver aprovacao previa e escrita da Controladora, com ajuste de escopo e salvaguardas.

## 4. Bases legais

4.1. A Controladora declara que o tratamento por ela instruido conta com base legal valida.

4.2. Sem prejuizo de outras hipoteses cabiveis, este anexo considera como bases legais principais:
- **execucao de contrato** ou procedimentos preliminares relacionados a contrato do qual seja parte o titular, nos termos do art. 7o, V, da LGPD; e
- **legitimo interesse**, nos termos do art. 7o, IX, e art. 10 da LGPD, para operacao, seguranca, prevencao a fraude, continuidade, suporte e melhoria operacional, observadas as legitimas expectativas do titular e o minimo necessario.

4.3. Quando o tratamento exigir outra base legal, a Controladora devera instruir expressamente a Operadora.

## 5. Instrucoes e governanca

5.1. A Operadora tratara os dados pessoais segundo as instrucoes documentadas da Controladora, nos termos do art. 39 da LGPD.

5.2. A Operadora podera recusar instrucao manifestamente ilegal, insegura ou que contrarie este anexo, as auditorias tecnicas ou a LGPD.

5.3. A Controladora respondera pela licitude da coleta, pela definicao de finalidade e pela transparencia perante o titular.

## 6. Suboperadores

6.1. A Controladora autoriza a contratacao dos seguintes Suboperadores, conforme necessidade tecnica do tenant e do plano contratado:
- `Hostinger` - hospedagem e infraestrutura de VPS, quando aplicavel;
- `Chatwoot OSS` - atendimento omnichannel e inbox por tenant;
- `n8n` - automacao e orquestracao de workflows;
- `Supabase` - autenticacao, banco de dados e RLS do portal;
- `Backblaze B2` - repositorio de backup offsite criptografado, quando ativado;
- `OpenAI` - processamento de linguagem natural e automacoes com IA, quando habilitado;
- `Anthropic` - processamento de linguagem natural e automacoes com IA, quando habilitado.

6.2. O uso de cada Suboperador deve ser compativel com o tenant manifest, a proposta comercial e os controles previstos no repositorio.

6.3. Havendo alteracao material de Suboperador, a Operadora informara a Controladora com antecedencia razoavel ou, em caso emergencial, assim que viavel.

## 7. Transferencia internacional

7.1. Havendo uso de Suboperadores ou infraestrutura fora do Brasil, as Partes reconhecem que pode haver transferencia internacional de dados.

7.2. Nesses casos, a Operadora adotara as medidas contratuais e organizacionais cabiveis, em linha com o art. 33 da LGPD.

## 8. Medidas tecnicas e administrativas

8.1. A Operadora adotara medidas tecnicas e administrativas aptas a proteger os dados pessoais, em linha com os arts. 46 a 49 da LGPD, consideradas a natureza do servico e o estado atual da operacao.

8.2. As medidas atualmente praticadas incluem, conforme artefatos reais do repositorio:
- segregacao operacional por tenant com naming, namespace e ownership, conforme `MULTITENANT-AUDIT.md` e `tenants/templates/tenant-manifest.example.yaml`;
- inbox dedicada por tenant em `Chatwoot` e instancia dedicada por tenant em `Evolution`, conforme `FIRST-EXTERNAL-PROVISIONING.md`;
- `n8n dedicated` para cliente externo, com rollback controlado, conforme `docs/N8N-DEDICATED-RUNBOOK.md`;
- controles de acesso no portal por membership de tenant e RLS, conforme `apps/portal/supabase/migrations/0001_portal_schema.sql`;
- autenticacao com `Supabase` e verificacao server-side de membership do tenant no portal;
- criptografia em transito via HTTPS/TLS nas aplicacoes expostas;
- backup recorrente, restore seletivo e verificacoes de integridade conforme `docs/RESTIC-RUNBOOK.md`;
- politica de rotacao e ownership de segredos conforme `docs/SECRETS-MANAGEMENT.md` e `SECRET-ROTATION-CHECKLIST.md`;
- smoke tests operacionais e validacao de rotas/ambiente conforme `ops/smoke-test-tenant.sh`.

8.3. A Operadora nao garante isolamento absoluto ou seguranca total. A obrigacao assumida e de adotar medidas razoaveis, proporcionais e tecnicamente defensaveis.

## 9. Incidentes de seguranca

9.1. A Operadora comunicara a Controladora sobre incidente de seguranca com potencial de risco ou dano relevante em ate **24 horas** da confirmacao interna inicial.

9.2. Em ate **72 horas** da comunicacao inicial, a Operadora entregara relatorio tecnico preliminar contendo, no minimo:
- natureza dos dados afetados;
- categorias de titulares;
- tenant ou tenants potencialmente impactados;
- data e horario estimados;
- medidas tecnicas e organizacionais conhecidas;
- risco identificado;
- acoes de contencao, mitigacao e proximo passo.

9.3. O procedimento contratual acima complementa, sem substituir, o art. 48 da LGPD. Na relacao com a ANPD e com os titulares, a comunicacao legal segue o prazo e o rito regulamentar aplicaveis ao controlador, inclusive a Resoluacao CD/ANPD no 15/2024.

## 10. Direitos dos titulares

10.1. A Operadora apoiara a Controladora no atendimento dos direitos previstos no art. 18 da LGPD, na medida do papel de operadora e dos limites tecnicos do servico.

10.2. O canal inicial para demandas de titulares sera `dpo@elevalocal.shop`, sem prejuizo do canal principal da Controladora.

10.3. As Partes envidarao esforcos para responder solicitacoes validas em ate `{{PRAZO_DIREITOS_TITULAR_DIAS}}` dias corridos, ressalvados casos complexos ou dependentes de terceiro.

## 11. Retencao e eliminacao

11.1. Os dados pessoais serao mantidos pelo prazo necessario ao cumprimento do contrato e das finalidades legitimas, observados os arts. 15 e 16 da LGPD.

11.2. Apos a rescisao, a Operadora podera manter os dados por ate `{{RETENCAO_POS_RESCISAO_MESES}}` meses para:
- transicao assistida;
- exportacao ao cliente;
- defesa de direitos;
- cumprimento de obrigacoes legais;
- preservacao de backup e trilha de auditoria dentro dos limites tecnicos.

11.3. Findo o prazo contratual de retencao e inexistindo base legal de conservacao, a Operadora eliminara ou anonimizara os dados, emitindo atestado de eliminacao quando solicitado pela Controladora.

## 12. Auditoria e evidencias

12.1. Mediante aviso previo razoavel de `{{PRAZO_AVISO_AUDITORIA_DIAS}}` dias, a Controladora podera solicitar evidencias documentais razoaveis sobre medidas de seguranca, desde que sem acesso a segredos, tenants de terceiros ou informacoes cobertas por sigilo comercial.

12.2. Em regra, a Operadora atendera a essa obrigacao por meio de:
- checklists e runbooks do repositorio;
- evidencias de onboarding, rotacao, backup e restore;
- descricao de controles de acesso e segregacao;
- relatorios operacionais anonimizados quando necessario.

## 13. Responsabilidade

13.1. Cada Parte respondera na medida de sua atuacao e de sua violacao a obrigacoes legais ou contratuais.

13.2. A Operadora nao responde por:
- instrucao ilegal ou indevida da Controladora;
- dado inserido incorretamente pela Controladora;
- compartilhamento indevido feito pela propria Controladora;
- manutencao de credencial ou acesso sob exclusiva governanca da Controladora.

## 14. Encerramento

14.1. Este anexo vigorara enquanto houver tratamento de dados pessoais pela Operadora em nome da Controladora.

14.2. Em caso de conflito entre este anexo e o contrato principal, prevalecera a regra mais especifica de protecao de dados.
