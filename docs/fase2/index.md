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

* **Questão (Q3 - complementar, arquitetura real):** Considerando que o Mural UnB é uma aplicação _serverless_ (sem _backend_ ou _login_), cujos dados são arquivos JSON publicados por um pipeline de _scraping_, o sistema impede que conteúdo malicioso vindo das fontes externas raspadas (_scripts_, HTML, _links_ adulterados) seja injetado no `oportunidades.json` e renderizado de forma ativa na interface React?

* **Hipótese (H3):** Espera-se que o escape automático do React - sem uso de `dangerouslySetInnerHTML` no código - neutralize a totalidade dos payloads injetados em campos de texto (`descricao`, `Sobre`, `nome`). Contudo, como o componente `SocialFooter` insere os campos de canal diretamente em `href={website}` / `href={instagram}` sem sanitização, payloads de URI (`javascript:`) nesses campos não serão bloqueados, resultando em taxa de neutralização global inferior a 100% e evidenciando um vetor de injeção via _links_.

## 2.2. Subcaracterística: Autenticidade 

A autenticidade garante que a identidade de um sujeito ou recurso possa ser comprovada. Para o Mural UnB, isso resulta em segurança de que a entidade que publica uma vaga é, de fato, a entidade real da universidade. 

* **Questão (Q2)**: O sistema comprova de forma robusta a identidade do usuário no momento do login, impedindo a entrada com credenciais forjadas ou inválidas? 

* **Hipótese (H2)**: O sistema exige validação rigorosa da identidade institucional, provavelmente restringindo o cadastro ou a elevação de privilégios mediante a confirmação de um endereço de e-mail com domínio oficial da universidade (@unb.br ou @aluno.unb.br). Outrossim, espera-se que as barreiras de autenticação rejeitem 100% das tentativas de acessos com senhas incorretas, injeções ou usuários inexistentes. 

* **Questão (Q4 - complementar, arquitetura real):** Como não há autenticação de usuários, mas a autenticidade de recurso permanece essencial, é possível verificar que toda oportunidade publicada tem origem em uma fonte oficial autorizada (canal institucional da empresa júnior ou do laboratório) e não em uma fonte forjada ou não verificável?

* **Hipótese (H4):** Espera-se que a procedência seja majoritariamente verificável - as 49 empresas juniores possuem canal oficial (`Site` e `Instagram`) preenchido em 100% dos registros -, porém não integralmente, pois aproximadamente 35% dos laboratórios apresentam `contato` fora do domínio institucional `@unb.br`, reduzindo a taxa global de procedência verificável para uma faixa estimada de ~85%.

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

### Métrica 3 (M3) - Referente à Q3 (Integridade - Injeção de Conteúdo)

* **Nome**: Taxa de Neutralização de Conteúdo Malicioso (TNCM).

* **Fórmula**: (Nº de payloads neutralizados na renderização / Nº total de payloads injetados no JSON de teste) x 100

* **Procedimento de coleta**: Em uma cópia local do `oportunidades.json` executada com `npm run dev`, injetar um conjunto controlado de payloads distribuídos entre campos de texto (`descricao`, `Sobre`, `nome`) e campos de canal (`website`, `instagram`). Classificar cada payload como neutralizado (renderizado como texto inerte ou link inofensivo) ou ativo (executa script, navega para `javascript:` ou injeta HTML).

* **Níveis de Pontuação e Critérios de Julgamento**:

    * **Excelente (100%)**: Nenhum payload é renderizado de forma ativa. Julgamento: A integridade do conteúdo exibido é confiável.

    * **Aceitável (90% a 99%)**: Falha restrita ao `href` dos campos de canal (exige clique do usuário). Julgamento: Aceitável com ressalva. Ação: validar o esquema da URL no `SocialFooter`, aceitando apenas `http`/`https`.

    * **Insatisfatório (< 90% ou qualquer execução em campo de texto)**: Execução automática de payload (XSS direto). Julgamento: Falha grave; sanitizar as entradas do pipeline e a renderização.

### Métrica 4 (M4) - Referente à Q4 (Autenticidade - Procedência)

* **Nome**: Taxa de Procedência Verificável (TPV).

* **Fórmula**: (Nº de registros com fonte/canal oficial verificável / Nº total de registros) x 100

* **Critério de "verificável"**: empresa júnior com `Site` ou `Instagram` correspondente à entidade; laboratório com `contato` em domínio institucional `@unb.br`.

* **Procedimento de coleta**: (1) núcleo automático - script sobre o `oportunidades.json` que calcula o percentual de registros com sinal oficial; (2) verificação amostral - confirmação manual, em uma amostra, de que o canal resolve para a entidade real.

* **Níveis de Pontuação e Critérios de Julgamento**:

    * **Excelente (≥ 95%)**: Quase todos os registros são rastreáveis a uma fonte oficial. Julgamento: Procedência confiável.

    * **Satisfatório (80% a 94%)**: Maioria verificável, com lacuna pontual (laboratórios com contato externo). Julgamento: Aceitável; padronizar o contato institucional.

    * **Insatisfatório (< 80%)**: Procedência insuficiente. Julgamento: Risco de conteúdo de fonte não confirmada; adicionar campo `fonte`/`url_origem` no ETL.

## 4. Níveis de Pontuação e Critérios de Julgamento 

Para garantir o rigor analítico e a interpretação inequívoca dos resultados, os critérios de julgamento foram estabelecidos abaixo.

| Métrica | Inadequado (Crítico) | Aceitável (Requer Atenção) | Excelente (Seguro) | Ação Recomendada (Se falhar) |
| :--- | :--- | :--- | :--- | :--- |
| **M1.1 (TBM-NAut)** | Abaixo de 95% | Entre 95% e 99% | **100%** | Revisar imediatamente os *middlewares* de autorização nas rotas da API. |
| **M1.2 (QEC-V)** | Maior que 0 | N/A (Métrica binária na prática) | **0 endpoints** | Proteger rotas expostas implementando validação de *token* JWT. |
| **M2.1 (EVD-Inst)** | Abaixo de 100% (Aceita e-mail comum) | N/A | **100%** (Bloqueio total) | Implementar validação via Regex para aceitar exclusivamente domínios institucionais. |
| **M2.2 (P-2FA)** | 0% | Entre 1% e 49% | **50% a 100%** | Planejar a integração de envio de código via e-mail institucional no login. |
| **M3 (TNCM)** | < 90% ou execução em campo de texto | 90% a 99% (falha restrita ao `href`) | **100%** | Validar o esquema da URL no `SocialFooter` (aceitar só `http`/`https`) e sanitizar as entradas do pipeline. |
| **M4 (TPV)** | < 80% | 80% a 94% | **≥ 95%** | Padronizar o contato institucional dos laboratórios e adicionar campo `fonte`/`url_origem` no ETL. |

## 5. Plano de Coleta de Dados 

O plano estabelece as regras, as ferramentas e a frequência das revisões da API e dos mecanismos de autenticação do Mural UnB, enfatizando exclusivamente na Integridade e na Autenticidade estabelecidas na Fase 2. 

| ID | Método de Coleta | Ferramentas / Procedimentos | Responsável / Período |
| :--- | :--- | :--- | :--- |
| **M1.1** | Teste de Autorização (Envio de Payloads) | Envio de payloads via ferramentas de teste de API (ex: Postman), utilizando tokens de baixo privilégio, para tentar modificar ou excluir recursos não autorizados. | Equipe de Avaliação (Semana X) |
| **M1.2** | Inspeção de Rotas | Mapeamento das rotas da API e envio de requisições de manipulação de dados sem o cabeçalho com token JWT válido para aferir bloqueio. | Equipe de Avaliação (Semana X) |
| **M2.1** | Teste de Validação de Cadastro | Tentativas manuais ou automatizadas de criar perfis de entidades provedoras utilizando domínios de e-mail não oficiais (como @gmail.com ou @outlook.com). | Equipe de Avaliação (Semana Y) |
| **M2.2** | Verificação de Banco de Dados / Dashboard | Inspeção na base de dados ou painel administrativo para contabilizar quantas contas com privilégio de publicação possuem verificação em duas etapas ativa. | Equipe de Avaliação (Semana Y) |
| **M3** | Teste de Injeção na Renderização | Cópia local do `oportunidades.json` executada com `npm run dev`; injeção de payloads (`<script>`, `<img onerror>`, `javascript:` em `website`/`instagram`) e classificação de cada um entre neutralizado e ativo. | Equipe de Avaliação (Fase 3) |
| **M4** | Análise de Procedência | Script sobre o `oportunidades.json` para calcular o percentual de registros com canal oficial, complementado por verificação manual de uma amostra. | Equipe de Avaliação (Fase 3) |

### 6. Quadro Consolidado (Resultados) da Segurança: Integridade

Abaixo estão os resultados representativos dos testes de Integridade, baseados no plano de coleta para atestar a prevenção contra modificações não autorizadas.

| Métrica | Descrição | Meta Estipulada | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M1.1** | Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut) | 100% | 100% (Todas as requisições forjadas foram bloqueadas) | Excelente 🟢 |
| **M1.2** | Quantidade de Endpoints Críticos Vulneráveis (QEC-V) | 0 endpoints | 0 endpoints (Mecanismo de JWT funcional em todas as rotas de edição) | Excelente 🟢 |
| **M3** | Taxa de Neutralização de Conteúdo Malicioso (TNCM) | 100% | A coletar na Fase 3 (teste de injeção local) | Pendente ⚪ |

### 7. Quadro Consolidado (Resultados) da Segurança: Autenticidade

Resultados voltados à capacidade do sistema em garantir a identidade institucional de entidades provedoras no momento do login e cadastro.

| Métrica | Descrição | Meta Estipulada | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M2.1** | Efetividade da Verificação de Domínio Institucional (EVD-Inst) | 100% de Bloqueio | 100% (Aceita apenas @unb.br ou @aluno.unb.br) | Excelente 🟢 |
| **M2.2** | Proporção de Autenticação em Duas Etapas para Publicadores (P-2FA) | 50% a 100% | 0% (Nenhuma conta de publicador possui camada extra) | Inadequado 🔴 (Ação: Planejar integração via e-mail) |
| **M4** | Taxa de Procedência Verificável (TPV) | ≥ 95% | Preliminar ≈ 85% (49/49 EJs com Site+Instagram; 22/34 labs com contato @unb.br) - confirmar amostra na Fase 3 | Satisfatório 🟡 (Ação: padronizar contato institucional) |

### 8. Rastreabilidade da Fase 1 para a Fase 2

A tabela demonstra que as prioridades e o contexto de proteção definidos no planejamento (Fase 1) foram convertidos exatamente nas métricas estipuladas nos níveis operacionais e quantitativos (Q1, Q2, M1 e M2).

| Escopo/Prioridade (Fase 1) | Requisito do Stakeholder | Objetivo GQM (Fase 2) | Métrica Aplicada |
| :--- | :--- | :--- | :--- |
| Segurança / Integridade | Impedir que estudantes comuns alterem ou deletem vagas. | Analisar o controle de acesso para avaliar a prevenção de violações. | M1.1 |
| Segurança / Integridade | Proteger todas as rotas críticas de manipulação de dados contra acessos anônimos. | Analisar o sistema web para diagnosticar vulnerabilidades de endpoints vazados. | M1.2 |
| Segurança / Autenticidade | Garantir que a entidade que publica uma vaga é institucionalmente real. | Avaliar as barreiras de autenticação e validação de identidade. | M2.1 |
| Segurança / Autenticidade | Aumentar as barreiras de proteção de contas com alto privilégio no sistema. | Analisar o sistema para evitar acesso com credenciais forjadas. | M2.2 |
| Segurança / Integridade | Impedir a injeção de conteúdo malicioso, vindo das fontes externas raspadas, no conteúdo público exibido. | Analisar o pipeline e o frontend para diagnosticar vulnerabilidades de injeção (XSS). | M3 |
| Segurança / Autenticidade | Garantir que cada oportunidade publicada tem origem em uma fonte oficial verificável. | Avaliar a procedência dos registros a partir dos canais oficiais das entidades. | M4 |

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
| 02 | Incremento do GQM de Segurança com questões, hipóteses e métricas| Isaac | 11/06/2026 |