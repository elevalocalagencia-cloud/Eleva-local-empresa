# Politica de Privacidade do Portal

Ultima atualizacao: `{{DATA_ATUALIZACAO_POLITICA}}`

Esta Politica explica como a `{{CONTROLADORA_PORTAL_RAZAO_SOCIAL}}`, CNPJ `{{CONTROLADORA_PORTAL_CNPJ}}`, trata dados pessoais no portal `{{PORTAL_URL}}`.

## 1. Para quem esta politica vale

Esta Politica vale para:
- usuarios convidados pela empresa cliente para acessar o portal;
- representantes comerciais, operacionais e administrativos que usem o portal;
- pessoas que entrem em contato conosco pelos canais indicados nesta pagina.

## 2. Que dados tratamos

Podemos tratar, conforme o uso do portal:
- nome, e-mail corporativo, cargo e empresa;
- dados de autenticacao e logs de acesso;
- identificador de tenant e perfil de acesso;
- registros de mensagens, agendamentos e snapshots operacionais exibidos no portal;
- dados tecnicos do navegador, IP, data e hora de acesso.

## 3. Para que usamos esses dados

Usamos os dados para:
- criar e manter o acesso ao portal;
- autenticar o usuario e aplicar permissoes por tenant;
- exibir informacoes operacionais do ambiente contratado;
- prevenir uso indevido, fraude, acesso nao autorizado e falha operacional;
- cumprir obrigacoes legais e defender direitos.

## 4. Bases legais

As bases legais normalmente usadas sao:
- execucao de contrato ou de procedimentos preliminares relacionados a contrato, nos termos do art. 7o, V, da LGPD;
- legitimo interesse, nos termos do art. 7o, IX, e art. 10 da LGPD, para seguranca, logs, continuidade, prevencao a fraude e melhoria operacional;
- cumprimento de obrigacao legal ou regulatoria, quando aplicavel.

## 5. Como funciona o acesso por tenant

O portal foi estruturado para mostrar dados apenas ao tenant do usuario autenticado.

Na pratica, isso inclui:
- verificacao de membership por tenant;
- politicas de acesso no banco;
- roteamento e recursos segregados por tenant.

Esses controles reduzem risco de acesso indevido, mas nenhuma arquitetura promete risco zero.

## 6. Compartilhamento de dados

Podemos compartilhar dados com operadores e suboperadores estritamente necessarios para prestar o servico, como:
- `Supabase`, para autenticacao e banco do portal;
- `Chatwoot OSS`, para operacao de inbox e atendimento;
- `n8n`, para automacoes;
- `Evolution`, para mensageria;
- `Hostinger`, para infraestrutura, quando aplicavel;
- `Backblaze B2`, para backup offsite, quando habilitado;
- `OpenAI` e `Anthropic`, quando o cliente habilitar recursos de IA.

Se algum desses prestadores operar fora do Brasil, pode haver transferencia internacional de dados com salvaguardas contratuais e operacionais.

## 7. Retencao

Mantemos dados pessoais pelo tempo necessario para cumprir as finalidades desta Politica, o contrato e obrigacoes legais.

Como regra operacional:
- logs, acessos e registros do portal podem ser mantidos pelo prazo necessario a seguranca e auditoria;
- dados contratuais e de faturamento seguem os prazos legais aplicaveis;
- apos o encerramento do contrato, dados do tenant podem ser mantidos por ate `{{RETENCAO_POS_RESCISAO_MESES}}` meses para transicao, backup, exercicio regular de direitos e eliminacao controlada.

## 8. Seguranca

Adotamos medidas tecnicas e administrativas razoaveis para proteger os dados, incluindo controles de autenticacao, segregacao por tenant, criptografia em transito, gestao de segredos e rotinas de backup e restore.

## 9. Seus direitos

Nos termos da LGPD, voce pode solicitar, quando cabivel:
- confirmacao da existencia de tratamento;
- acesso aos dados;
- correcao de dados incompletos, inexatos ou desatualizados;
- anonimizacao, bloqueio ou eliminacao, quando aplicavel;
- informacao sobre compartilhamento;
- revisao de tratamento e oposicao, nos limites da lei.

## 10. Como falar conosco

Para pedidos relacionados a dados pessoais:

- E-mail: `dpo@elevalocal.shop`
- Canal do cliente: `{{CANAL_PRIVACIDADE_CLIENTE}}`

Se voce acessar o portal a convite de uma empresa cliente, ela tambem pode atuar como controladora dos dados relacionados ao atendimento e a operacao do seu proprio negocio.

## 11. Atualizacoes

Podemos atualizar esta Politica para refletir mudancas legais, tecnicas ou operacionais. A versao vigente sera sempre publicada nesta pagina.
