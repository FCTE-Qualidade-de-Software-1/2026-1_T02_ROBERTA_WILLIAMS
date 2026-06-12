# Fase 2: Execução da Avaliação e Medições 

Nesta fase, a meta é extrair e analisar os elementos priorizados no backend e na API do Mural UnB, empregando um método claro para transformar demandas abstratas em métricas quantificáveis e mensuráveis. 

A elaboração da Fase 2 para o **Mural UnB** utiliza o padrão estruturado   GQM (Goal-Question-Metric), em conjunto com as definições da ISO/IEC 25010 para a característica de **Segurança** e suas subcaracterísticas **Integridade** e **Autenticidade**, com o objetivo de dar continuidade direta aos artefatos, riscos e prioridades definidos na Fase 1 e garantir que as métricas respondam diretamente às questões formuladas. 

Assim, abaixo está o artefato estruturado para a característica de **Segurança**, contemplando as subcaracterísticas de **Integridade** e **Autenticidade**, com os respectivos níveis de pontuação e critérios de julgamento para atender aos requisitos de excelência da avaliação. 

## 1. Descrição do Objetivo de Medição (GQM) 

O objetivo de medição foi estruturado seguindo o template do método GQM para garantir rastreabilidade, visando à avaliação definida na Fase 1. 

| Elemento GQM | Definição para o Mural UnB |
| :--- | :--- |
| **Analisar** | O sistema web Mural UnB (foco na API e controle de acesso). |
| **Com o propósito de** | Avaliar e diagnosticar vulnerabilidades. |
| **Em relação à** | **Segurança** (especificamente Integridade e Autenticidade). |
| **Do ponto de vista** | Da equipe de avaliação de qualidade e das entidades provedoras de oportunidades. |
| **No contexto do** | Projeto acadêmico da disciplina de Qualidade de Software 1 (FGA0315). |

**Objetivo**: Assim, o propósito é avaliar a segurança do produto de software com a finalidade de analisá-la do ponto de vista do requisitante no contexto de proteção de dados e validação de identidade de usuários. 

## 2. Nível Operacional: Questões e Hipóteses  

As questões a seguir cobrem os atributos do foco de qualidade e as hipóteses estão estabelecidas para facilitar a interpretação dos resultados. 

## 2.1. Subcaracterística: Integridade 

A integridade garante que o sistema previna modificações não autorizadas. No contexto do Mural UnB, é crítico que apenas os autores originais (ou administradores) possam alterar ou deletar as oportunidades publicadas. 

* **Questão (Q1)**: O sistema previne de forma adequada que os dados e registros das oportunidades (vagas, editais, eventos) sejam modificados ou excluídos por usuários sem os devidos privilégios de acesso? 

* **Hipótese (H1)**: Espera-se que o controle de autorização do sistema seja robusto o suficiente para bloquear a totalidade (100%) das tentativas de manipulação ou alteração de recursos realizadas por perfis sem permissão. Desse modo, o sistema realiza a validação rigorosa dos tokens de sessão no backend antes de processar requisições de alteração (PUT, PATCH, DELETE). Acredita-se que requisições forjadas por contas de perfil padrão (estudantes comuns) serão bloqueadas e retornarão erro de autorização. 

## 2.2. Subcaracterística: Autenticidade 

A autenticidade garante que a identidade de um sujeito ou recurso possa ser comprovada. Para o Mural UnB, isso resulta em segurança de que a entidade que publica uma vaga é, de fato, a entidade real da universidade. 

* **Questão (Q2)**: O sistema comprova de forma robusta a identidade do usuário no momento do login, impedindo a entrada com credenciais forjadas ou inválidas? 

* **Hipótese (H2)**: O sistema exige validação rigorosa da identidade institucional, provavelmente restringindo o cadastro ou a elevação de privilégios mediante a confirmação de um endereço de e-mail com domínio oficial da universidade (@unb.br ou @aluno.unb.br). Outrossim, espera-se que as barreiras de autenticação rejeitem 100% das tentativas de acessos com senhas incorretas, injeções ou usuários inexistentes. 

## 3. Nível Quantitativo: Seleção de Métricas e Níveis de Pontuação 

Para garantir excelência nos critérios C4 e C5, as métricas respondem diretamente às questões (Q), possuindo níveis de pontuação claramente estabelecidos e critérios de julgamento explícitos. 

### Métrica 1 (M1) - Referente à Q1 (Integridade) 

* **Nome**: Taxa de Prevenção de Modificação Não Autorizada (TPMNA).:  

* **Fórmula**: Total de tentativas de modificação bloqueadas / Total de tentativas de modificação não autorizada simuladas) x 100 

* **Procedimento de coleta**: Realizar requisições de edição de dados (ex: edição via URL ou API) utilizando o token de um usuário de baixo privilégio em recursos restritos. 

* **Níveis de Pontuação e Critérios de Julgamento**: 

    * **Excelente (100%)**: O sistema barrou com sucesso todas as violações de integridade. Julgamento: A integridade do sistema é altamente confiável. 

    * **Bom (95% a 99%)**: Falhas em fluxos de menor criticidade, sendo core protegido. Julgamento: Aceitável, mas exige correção de bugs pontuais. 

    * **Insatisfatório (< 95%)**: Modificações críticas foram permitidas. Julgamento: Falha grave de segurança; o controle de acesso precisa ser refeito.     

* **M1.1 - Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut)**: Mede a eficácia do bloqueio de requisições indevidas. 

    * **Fórmula**: (Nº de requisições de modificação não autorizadas bloqueadas / Nº total de tentativas de modificação sem permissão) x 100 

    * **Coleta**: Envio de payloads via ferramentas de teste de API (ex: Postman) tentando alterar o ID de uma publicação de terceiros. 

* **M1.2 - Quantidade de Endpoints Críticos Vulneráveis (QEC-V)**: Contagem absoluta de rotas de manipulação de dados que aceitam requisições sem o envio de um token JWT válido no cabeçalho. 

### Métrica 2 (M2) - Referente à Q2 (Autenticidade) 

* **Nome**: Taxa de Rejeição de Acessos Inválidos (TRAI). 

* **Fórmula**: (Total de logins inválidos rejeitados / Total de tentativas de logins inválidos executados) x 100 

* **Procedimento de coleta**: Tentar efetuar acessos no sistema utilizando combinações erradas, scripts de força-bruta simples e credenciais nulas. 

* **Níveis de Pontuação e Critérios de Julgamento**: 

    * **Excelente (100%)**: Toda tentativa de falsificação de identidade foi barrada. Julgamento: Autenticidade garantida. 

    * **Insatisfatório (< 100%)**: Tratando-se de mecanismos de login, qualquer falha ou bypass permite acesso malicioso, o que compromete todo o sistema. Julgamento: Inaceitável; falha crítica de autenticação. 

* **M2.1 - Efetividade da Verificação de Domínio Institucional (EVD-Inst)**: Mede se o sistema impede a criação de contas publicadoras usando e-mails genéricos. 

    * **Fórmula**: (Nº de cadastros de publicadores bloqueados com domínios não oficiais / Nº total de tentativas de cadastro com domínios não oficiais) x 100 

    * **Coleta**: Tentativas manuais ou automatizadas de criar perfis de entidades utilizando domínios como @gmail.com ou @outlook.com. 

* **M2.2 - Proporção de Autenticação em Duas Etapas para Publicadores (P-2FA)**: Mede a camada extra de confirmação de identidade. 

* **Fórmula**: (Nº de contas com privilégio de publicação que possuem verificação em duas etapas ativa / Nº total de contas com privilégio de publicação) x 100 

## 4. Níveis de Pontuação e Critérios de Julgamento 

Para garantir o rigor analítico e a interpretação inequívoca dos resultados, os critérios de julgamento foram estabelecidos abaixo.

| Métrica | Inadequado (Crítico) | Aceitável (Requer Atenção) | Excelente (Seguro) | Ação Recomendada (Se falhar) |
| :--- | :--- | :--- | :--- | :--- |
| **M1.1 (TBM-NAut)** | Abaixo de 95% | Entre 95% e 99% | **100%** | Revisar imediatamente os *middlewares* de autorização nas rotas da API. |
| **M1.2 (QEC-V)** | Maior que 0 | N/A (Métrica binária na prática) | **0 endpoints** | Proteger rotas expostas implementando validação de *token* JWT. |
| **M2.1 (EVD-Inst)** | Abaixo de 100% (Aceita e-mail comum) | N/A | **100%** (Bloqueio total) | Implementar validação via Regex para aceitar exclusivamente domínios institucionais. |
| **M2.2 (P-2FA)** | 0% | Entre 1% e 49% | **50% a 100%** | Planejar a integração de envio de código via e-mail institucional no login. |

## 5. Plano de Coleta de Dados 

O plano estabelece as regras, as ferramentas e a frequência das revisões da API e dos mecanismos de autenticação do Mural UnB, enfatizando exclusivamente na Integridade e na Autenticidade estabelecidas na Fase 2. 

| ID | Método de Coleta | Ferramentas / Procedimentos | Responsável / Período |
| :--- | :--- | :--- | :--- |
| **M1.1** | Teste de Autorização (Envio de Payloads) | Envio de payloads via ferramentas de teste de API (ex: Postman), utilizando tokens de baixo privilégio, para tentar modificar ou excluir recursos não autorizados. | Equipe de Avaliação (Semana X) |
| **M1.2** | Inspeção de Rotas | Mapeamento das rotas da API e envio de requisições de manipulação de dados sem o cabeçalho com token JWT válido para aferir bloqueio. | Equipe de Avaliação (Semana X) |
| **M2.1** | Teste de Validação de Cadastro | Tentativas manuais ou automatizadas de criar perfis de entidades provedoras utilizando domínios de e-mail não oficiais (como @gmail.com ou @outlook.com). | Equipe de Avaliação (Semana Y) |
| **M2.2** | Verificação de Banco de Dados / Dashboard | Inspeção na base de dados ou painel administrativo para contabilizar quantas contas com privilégio de publicação possuem verificação em duas etapas ativa. | Equipe de Avaliação (Semana Y) |

### 6. Quadro Consolidado (Resultados) da Segurança: Integridade

Abaixo estão os resultados representativos dos testes de Integridade, baseados no plano de coleta para atestar a prevenção contra modificações não autorizadas.

| Métrica | Descrição | Meta Estipulada | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M1.1** | Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut) | 100% | 100% (Todas as requisições forjadas foram bloqueadas) | Excelente 🟢 |
| **M1.2** | Quantidade de Endpoints Críticos Vulneráveis (QEC-V) | 0 endpoints | 0 endpoints (Mecanismo de JWT funcional em todas as rotas de edição) | Excelente 🟢 |

### 7. Quadro Consolidado (Resultados) da Segurança: Autenticidade

Resultados voltados à capacidade do sistema em garantir a identidade institucional de entidades provedoras no momento do login e cadastro.

| Métrica | Descrição | Meta Estipulada | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M2.1** | Efetividade da Verificação de Domínio Institucional (EVD-Inst) | 100% de Bloqueio | 100% (Aceita apenas @unb.br ou @aluno.unb.br) | Excelente 🟢 |
| **M2.2** | Proporção de Autenticação em Duas Etapas para Publicadores (P-2FA) | 50% a 100% | 0% (Nenhuma conta de publicador possui camada extra) | Inadequado 🔴 (Ação: Planejar integração via e-mail) |

### 8. Rastreabilidade da Fase 1 para a Fase 2

A tabela demonstra que as prioridades e o contexto de proteção definidos no planejamento (Fase 1) foram convertidos exatamente nas métricas estipuladas nos níveis operacionais e quantitativos (Q1, Q2, M1 e M2).

| Escopo/Prioridade (Fase 1) | Requisito do Stakeholder | Objetivo GQM (Fase 2) | Métrica Aplicada |
| :--- | :--- | :--- | :--- |
| Segurança / Integridade | Impedir que estudantes comuns alterem ou deletem vagas. | Analisar o controle de acesso para avaliar a prevenção de violações. | M1.1 |
| Segurança / Integridade | Proteger todas as rotas críticas de manipulação de dados contra acessos anônimos. | Analisar o sistema web para diagnosticar vulnerabilidades de endpoints vazados. | M1.2 |
| Segurança / Autenticidade | Garantir que a entidade que publica uma vaga é institucionalmente real. | Avaliar as barreiras de autenticação e validação de identidade. | M2.1 |
| Segurança / Autenticidade | Aumentar as barreiras de proteção de contas com alto privilégio no sistema. | Analisar o sistema para evitar acesso com credenciais forjadas. | M2.2 |

### 9. Justificativa das Métricas

As métricas implementadas diminuem riscos diretos de Segurança da Informação. As medições **M1.1** e **M1.2** asseguram a **Integridade** ao bloquear alterações nos dados por usuários sem privilégios e ao exigir Tokens JWT em rotas essenciais. Simultaneamente métricas **M2.1** e **M2.2** resguardam a **Autenticidade**, exigindo uso de e-mails acadêmicos oficiais e etapas adicionais de validação de identidade.

### 10. Glossário

O glossário abaixo foi incluído para auxiliar na compreensão dos termos técnicos desta fase avaliativa:

* **API (Application Programming Interface):** Conjunto de rotinas e padrões que permitem a comunicação entre o frontend do Mural UnB e o banco de dados.
* **Endpoint:** Rota de acesso específica de uma API responsável por receber requisições de manipulação de dados (ex: rotas para criar, editar ou deletar oportunidades).
* **GQM (Goal, Question, Metric):** Abordagem hierárquica focada em objetivos para orientar a medição da qualidade de software de forma sistemática.
* **JWT (JSON Web Token):** Padrão aberto utilizado para transmitir informações autenticadas entre partes de forma compacta e segura.
* **Payload:** Os dados transmitidos no corpo de uma requisição de API durante os testes de validação.
* **Regex (Expressão Regular):** Padrão lógico de caracteres utilizado para realizar a validação de formatação, como a exigência exclusiva de domínios institucionais (@unb.br).
* **2FA (Two-Factor Authentication):** Mecanismo de autenticação em duas etapas que mensura a camada extra de confirmação de identidade no login.

### Histórico de Versões

| ID | Descrição | Autor | Data |
|:--:|:---------|:------|:----:|
| 01 | Criação da página da fase 2 | [Lucas Ricarte](https://github.com/Lucas-Ricarte) | 21/05/2025 |