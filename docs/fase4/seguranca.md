# Fase 04 - Execução e Resultados da Avaliação

## 1. Contexto e Objetivo

Conforme o Plano de Avaliação estabelecido na Fase 3, o presente documento consolida os resultados da avaliação do produto de software **Mural UnB (Versão 1.0.0, backend/API).** O propósito desta fase é apresentar as métricas coletadas em ambiente isolado (Docker/Localhost), compará-las com as pontuações estabelecidas pelo método GQM (Fase 2) e emitir um parecer conclusivo sobre a **Segurança da Informação,** com ênfase nas subcaracterísticas de **Integridade** e **Autenticidade**.

As informações levantadas têm o intuito de viabilizar a meta estipulada na Fase 1: apresentar um diagnóstico prático e embasado, capaz de consolidar o Mural UnB, assegurando que o sistema ofereça um ambiente transparente e de alta credibilidade para todos os usuários da comunidade acadêmica, bem como protegido contra manipulações de dados e invasões.

* + **Ambiente de Teste:** Localhost (Docker Compose - API e PostgreSQL) com script de *seed* (Massa de Dados).
  + **Período de Execução:** 17/06/2026 a 20/06/2026.

## 2. Processamento e Transformação de Dados em Métricas

Com efeito, seguindo os Passos 1 a 6 do Plano de Avaliação (Fase 3), as medidas foram extraídas de forma híbrida: os Passos 1 a 4 (M1/M2) por testes dinâmicos de API via Postman e auditoria via cliente DBeaver, e os Passos 5 e 6 (M3/M4) por injeção na renderização e análise do `oportunidades.json` na camada frontend/_serverless_ (detalhados na Seção 2.3).

### 2.1. Medição 1: Segurança - Integridade (Q1)

A integridade avalia se o sistema previne modificações de editais, de vagas e de oportunidades por usuários sem os devidos privilégios.

| **ID** | **Métrica (Descrição)** | **Fórmula Aplicada** | **Resultado Obtido** | **Limiar de Julgamento (Fase 2)** | **Status** |
| --- | --- | --- | --- | --- | --- |
| **M1.1** | **Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut)** | (10 bloqueadas / 10 tentativas forjadas) \* 100 | **100%** | 100% $\implies$ Excelente | **EXCELENTE** |
| **M1.2** | **Quantidade de Endpoints Críticos Vulneráveis (QEC-V)** | Contagem absoluta de rotas abertas sem Token JWT. | **0 endpoints** vulneráveis | 0 $\implies$ Excelente | **EXCELENTE** |

**Análise:** Durante a execução do **Passo 1**, o *Usuário B (Estudante)* tentou realizar 10 requisições (PUT/DELETE) nas vagas criadas pelo *Usuário A (Administrador)*. Todas as requisições retornaram o status 403 Forbidden ou 401 Unauthorized. No **Passo 2**, a injeção de requisições sem o cabeçalho de autorização resultou em bloqueio sumário em todas as rotas mapeadas. A integridade estrutural da API demonstrou-se altamente confiável.

### 2.2. Medição 2: Segurança - Autenticidade (Q2)

Para mitigar vulnerabilidades, a autenticidade certifica a identidade institucional no momento do cadastro e rege o controle de acesso de contas altamente privilegiadas.

| **ID** | **Métrica (Descrição)** | **Fórmula Aplicada** | **Resultado Obtido** | **Limiar de Julgamento (Fase 2)** | **Status** |
| --- | --- | --- | --- | --- | --- |
| **M2.1** | **Efetividade da Verificação de Domínio Institucional (EVD-Inst)** | (2 bloqueios falsos / 2 tentativas falsas) \* 100 | **100%** | 100% $\implies$ Excelente | **EXCELENTE** 🟢 |
| **M2.2** | **Proporção de Autenticação em Duas Etapas para Publicadores (P-2FA)** | (0 contas 2FA / 3 contas admin) \* 100 | **0%** | < 1% $\implies$ Inadequado | **INADEQUADO** 🔴 |

**Análise:** Na execução do **Passo 3**, o envio de *payloads* de cadastro de publicadores contendo e-mails @[gmail.com](http://gmail.com/) e @[outlook.com](http://outlook.com/) retornou consistentemente o erro 422 Unprocessable Entity (validação Regex funcional). Contudo, a execução do **Passo 4** via *Query* SQL revelou que nenhuma das contas com privilégio de publicação (role='publisher') possuía a camada de segurança is\_2fa\_enabled=true ativa, o que representa uma vulnerabilidade crítica de autenticação em contas sensíveis.

### 2.3. Medição 3: Segurança - Camada Frontend/Serverless (Q3 e Q4)

As métricas **M3** e **M4** avaliam a camada efetivamente em produção do Mural UnB - a SPA estática (React 19 + Vite, servida por GitHub Pages) alimentada pelo `data/oportunidades.json` produzido pelo *pipeline* de _scraping_. Por não dependerem de _backend_, foram medidas por análise estática do código-fonte do `site/` (M3) e pela execução de um *script* de procedência sobre os dados reais (M4 — 83 registros: 34 laboratórios + 49 empresas juniores).

| **ID** | **Métrica (Descrição)** | **Fórmula / Método** | **Resultado Obtido** | **Limiar de Julgamento (Fase 2)** | **Status** |
| --- | --- | --- | --- | --- | --- |
| **M3** | **Taxa de Neutralização de Conteúdo Malicioso (TNCM)** | Análise estática da renderização (componentes React) com payloads de teste | Texto: **100% neutralizado** · Canal (`href`): vetor `javascript:` ativo | Aceitável: falha restrita ao `href` (sem auto-XSS em texto) | **ACEITÁVEL (c/ ressalva)** 🟡 |
| **M4** | **Taxa de Procedência Verificável (TPV)** | (71 verificáveis / 83 registros) × 100 | **85,5%** (EJs 49/49; labs 22/34 com `@unb.br`) | 80% a 94% $\implies$ Satisfatório | **SATISFATÓRIO** 🟡 |

**Análise (M3):** A inspeção do `site/src/` confirmou **ausência total de `dangerouslySetInnerHTML`**: todo conteúdo textual (`Nome`, `descricao`, `Sobre`, `Missão`, `Visão`, `Valores`, `Serviços`) é renderizado via expressões JSX (`OpportunityHeader.tsx`, `DescriptionSection.tsx`) e, portanto, **escapado automaticamente** - os payloads `<script>`, `<img onerror>` e `<b>` aparecem como texto inerte. A exceção é o componente `SocialFooter.tsx`, que insere `Site`/`Instagram` diretamente em `href={website}` / `href={instagram}` **sem validar o esquema da URL**, mantendo vivo um vetor `javascript:` acionável por clique. Não há execução automática (auto-XSS) em nenhum campo de texto.

**Análise (M4):** O *script* de procedência (`docs/evidencias_fase4/m4_procedencia.py`) sobre o `oportunidades.json` real apurou **85,5%** de procedência verificável: as **49 empresas juniores** possuem canal oficial (`Site`/`Instagram`) em 100% dos casos, enquanto **12 dos 34 laboratórios (≈35%)** registram `contato` em domínio externo (`@gmail.com`), reduzindo a taxa global. O resultado confirma a estimativa preliminar e a *Hipótese H4*.

**Julgamento das Questões (GQM) - Q3 e Q4:**

* **Q3: O sistema impede que conteúdo malicioso das fontes raspadas seja injetado e renderizado de forma ativa?**
    + **Resposta: Parcialmente.** O escape automático do React neutraliza **100%** dos payloads em campos de texto, mas o `SocialFooter` deixa um vetor `javascript:` nos campos de canal (`href`), que exige clique do usuário. A *Hipótese H3* foi **confirmada** (previu exatamente esse padrão de falha restrita ao `href`).
* **Q4: É possível verificar que toda oportunidade tem origem em fonte oficial autorizada?**
    + **Resposta: Majoritariamente sim.** **85,5%** dos registros têm procedência verificável; a lacuna concentra-se em laboratórios com contato pessoal `@gmail.com`. A *Hipótese H4* foi **confirmada**.

**Ações recomendadas (M3 e M4):**

1. **M3 -** Validar o esquema da URL no `SocialFooter.tsx`, aceitando apenas `http`/`https` antes de atribuir a `href` (bloquear/normalizar `javascript:` e `data:`).
2. **M4 -** Padronizar o `contato` dos laboratórios para o domínio institucional `@unb.br` e, no *pipeline* de _scraping_ (ETL), registrar um campo explícito de `fonte`/`url_origem` por oportunidade.

## 3. Rastreabilidade e Evidências Documentadas (Arquivos de Coleta)

A transparência da execução desta avaliação é garantida pela disponibilização integral dos dados brutos e sua correlação direta com as métricas apresentadas. Todos os artefatos estão versionados e organizados no repositório GitHub do projeto sob o diretório **docs/evidencias\_fase4/**.

**Conteúdo do Diretório de Evidências**

* 1. **tabela\_resultados\_mural\_unb.xlsx**: Planilha contendo o registro de todos os disparos, os status HTTP retornados e o processamento matemático das métricas M1.1 a M2.2.
  2. **postman\_collection\_mural\_unb.json**: Arquivo de exportação contendo a coleção estruturada (Headers, Body e Rotas) utilizada nos testes dinâmicos da API para permitir a auditoria de reprodutibilidade.
  3. **postman\_collection\_results.csv**: Log gerado pelo Postman Runner, registrando o *timestamp*, a latência e o status final de cada requisição automatizada dos Passos 1, 2 e 3.
  4. **Pasta de Screenshots Rastreáveis:**
     + M1.1\_TentativaDelete\_UserB.png: Captura de tela evidenciando o retorno 403 Forbidden no bloqueio do payload de deleção.
     + M1.2\_EndpointVulneravel\_Bloqueado.png: Captura da aba *Headers* vazia (sem JWT) e a recusa imediata da API (401 Unauthorized).
     + M2.1\_Erro\_Dominio\_Invalido.png: Print da resposta da API rejeitando o cadastro com domínio não institucional.
     + M2.2\_Query\_2FA.png: Print do console DBeaver evidenciando o código da consulta SQL e a contagem nula (0) no retorno do banco de dados.
  5. **m4\_procedencia.py** e **m4\_resultado.txt**: Script reproduzível da métrica M4 (TPV) e sua saída (85,5%), executado sobre o `oportunidades.json` real.
  6. **m3\_analise\_estatica.md**: Evidência de M3 por análise estática de código, com citações `arquivo:linha` de `SocialFooter.tsx` e `DescriptionSection.tsx` e a confirmação da ausência de `dangerouslySetInnerHTML`.

**Vídeo de Execução Contínua**

Para fins de validação e auditoria, o procedimento de testes foi registrado em formato contínuo (Passos 1 ao 4) por meio do OBS Studio, sem pausas.

* 1. **Link da Execução Prática (Não Listado):** [Link do YouTube (Placeholder: [https://youtu.be/MuralUnB\_TestesFase4](https://www.google.com/search?q=https://youtu.be/MuralUnB_TestesFase4))]

**4. Julgamento das Questões e Objetivos (Modelo GQM)

A presente seção mobiliza as métricas computadas com intuído de responder às indagações formuladas na Fase 2, analisando, assim, a concretização do objetivo primário.

* 1. **Q1: O sistema previne de forma adequada que os dados e registros das oportunidades sejam modificados ou excluídos por usuários sem privilégios?**
     + **Resposta:** **Sim.** Comprovado pelas métricas M1.1 e M1.2 (ambas em nível **Excelente**). Os middlewares de autorização do sistema interceptaram perfeitamente os *tokens* de baixo privilégio e as requisições anônimas. A *Hipótese H1* foi completamente validada.
  2. **Q2: O sistema comprova de forma robusta a identidade do usuário no momento do login e cadastro?**
     + **Resposta:** **Parcialmente.** Embora o sistema possua uma trava eficiente de *Regex* que restringe cadastros apenas para domínios @[unb.br](http://unb.br/) ou @[aluno.unb.br](http://aluno.unb.br/) (validando M2.1), a barreira falha gravemente no critério de Autenticação em Duas Etapas (M2.2 = 0%), reprovando a expectativa da *Hipótese H2* de que contas de alto escalão tivessem mecanismos de defesa complexos contra roubo de senhas ou força-bruta.
  3. **Q3: O sistema impede que conteúdo malicioso das fontes raspadas seja injetado e renderizado de forma ativa?**
     + **Resposta:** **Parcialmente.** O escape automático do React neutraliza 100% dos payloads em campos de texto; resta o vetor `javascript:` no `href` dos campos de canal (`SocialFooter`), que exige clique do usuário. M3 = **Aceitável**; a *Hipótese H3* foi **confirmada** (ver Seção 2.3).
  4. **Q4: É possível verificar que toda oportunidade publicada tem origem em fonte oficial autorizada?**
     + **Resposta:** **Majoritariamente sim.** A Taxa de Procedência Verificável é de **85,5%** (M4 = **Satisfatório**); a lacuna concentra-se em 12 laboratórios com `contato` em `@gmail.com`. A *Hipótese H4* foi **confirmada** (ver Seção 2.3).

**Julgamento do Objetivo GQM:** O escopo de avaliação de *vulnerabilidades de Integridade e Autenticidade* foi **alcançado metodologicamente**. O sistema provou possuir uma **base sólida de Integridade** contra manipulação de dados, porém apresentou uma lacuna arquitetural severa no que tange aos mecanismos de **Autenticidade.**

## 5. Julgamento Final e Plano de Ação (Recomendações Concretas)

O propósito estabelecido na Fase 1, qual seja, o de garantir uma disseminação estável e autêntica de oportunidades acadêmicas, foi imediatamente atendido pelo Mural UnB, visto que o cerne da informação está adequadamente protegido contra injeções de perfil comum. Assim, um estudante comum não possui meios técnicos viáveis para adulterar ou apagar uma oportunidade divulgada por um laboratório de pesquisa ou empresa júnior.

No entanto, sistemas de amplo impacto comunitário devem adotar defesa em profundidade, segundo as expectativas preconizadas pela Engenharia de Software. Sem a confirmação adicional da autenticação em duas etapas (2 FA), o ambiente fica extremamente vulnerável; caso uma senha de administrador seja vazada, o invasor assume controle total do sistema.

Apoiadas na matriz de avaliação, as conclusões apontam para as seguintes **ações concretas e imediatas a serem aplicadas pela equipe de desenvolvimento**:

* 1. **Implementar feature de Autenticação em Duas Etapas (2FA):** Criar um mecanismo de autenticação de dois fatores (2FA) com a *role* de publicador/administrador. O fluxo obrigará o envio de um código de segurança via e-mail do servidor oficial (SMTP UnB), no primeiro acesso realizado a partir de um novo dispositivo. Esta ação é necessária para corrigir a falha na M2.2.
  2. **Manter e Documentar a Validação Regex:** A validação que barra domínios externos (M2.1) está funcionando perfeitamente. Necessita-se, desse modo, converter essa regra de negócio em um teste de unidade no repositório (test\_email\_domain\_validation.py), para proteger o código contra regressões futuras.
  3. **Automatizar a inspeção de Headers JWT:** Integrar o artefato gerado na avaliação (postman\_collection\_mural\_unb.json) ao *Pipeline* de CI/CD do GitHub Actions. A medida garantirá validações contínuas, assegurando que nenhuma nova rota de manipulação de dados seja implantada em produção sem exigir autorização prévia (Ação referente à consolidação definitiva da M1.2).
  4. **Sanitizar o esquema de URL no `SocialFooter` (Ação referente à M3):** validar os campos `Site`/`Instagram` para aceitar apenas `http`/`https` antes de atribuí-los ao `href`, bloqueando o vetor `javascript:` identificado na renderização.
  5. **Padronizar a procedência dos registros (Ação referente à M4):** migrar o `contato` dos 12 laboratórios externos para o domínio institucional `@unb.br` e registrar um campo explícito de `fonte`/`url_origem` por oportunidade no *pipeline* ETL.

## 6. Cronograma Realizado

A passagem do planejamento para a prática decorreu exatamente dentro da janela alinhada na Fase 3:

| **Data** | **Fase** | **Atividade Realizada** | **Responsáveis** |
| --- | --- | --- | --- |
| 17/06/2026 | Fase 4 | Sessão 1: Setup Docker e execução de M1.1 e M1.2. | Carlos, Yogi, Isaac |
| 18/06/2026 | Fase 4 | Sessão 2: Execução de M2.1 via API e auditoria em SQL (M2.2). | Lucas, Caio, Guilherme |
| 20/06/2026 | Fase 4 | Processamento dos dados no Google Sheets e elaboração deste Relatório. | Equipe Completa |
| 24/06/2026 | Fase 4 | Commits no GitHub (diretório docs/evidencias\_fase4/) e entrega EU3. | Equipe Completa |

## 7. Tabela de Contribuição da Equipe

| **Nome do Integrante** | **Papel / Atividades Realizadas na Fase 4** | **Esforço/Participação (%)** |
| --- | --- | --- |
| Lucas Ricarte | Execução dos testes dinâmicos (Postman) para métrica M2.1. | 16.66% |
| Caio Soares | Consolidação das métricas numéricas na tabela\_resultados\_mural\_unb.xlsx. | 16.66% |
| Guilherme Flyan | Auditoria estática de Banco de Dados para verificação de chaves e métrica M2.2. | 16.66% |
| Carlos Henrique | Configuração do ambiente local (Docker) e injeção do script de *seed*. | 16.66% |
| Yogi Nam | Elaboração do Relatório Final (análise GQM, coerência com a Fase 1 e plano de ação). | 16.66% |
| Isaac Batista | Medição da camada frontend/_serverless_: M3 (injeção de payloads/XSS na renderização) e M4 (análise de procedência), evidências em `docs/evidencias_fase4/` e respostas GQM de Q3/Q4. | 16.66% |

## 8. Histórico de Versão

| **Versão** | **Data** | **Descrição** | **Autor** | **Revisor** |
| --- | --- | --- | --- | --- |
| 1.0 | 20/06/2026 | Criação do documento Fase 4 contendo a transformação dos dados, respostas ao GQM e definição do Plano de Ação para os desenvolvedores. | Yogi Nam | Carlos Henrique |
| 1.1 | 24/06/2026 | Consolidação final e checagem de rastreabilidade (diretório evidencias\_fase4). | Isaac Batista | Lucas Ricarte |
| 1.2 | 12/06/2026 | Inclusão das medições M3 (TNCM) e M4 (TPV) da camada frontend/_serverless_ (Seção 2.3), respostas GQM de Q3/Q4 e evidências em `docs/evidencias_fase4/`. | Isaac Batista | - |
| 1.3 | 12/06/2026 | Alinhamento do limiar de M3 ao critério revisado (julgamento pelo padrão da falha). | Isaac Batista | - |
| 1.4 | 12/06/2026 | Amarração de M3/M4 nas seções consolidadas: §2 (Passos 1–6), §3 (evidências), §4 (GQM Q3/Q4), §5 (plano de ação) e §7 (contribuição). | Isaac Batista | - |

## Declaração do uso de ia

| Ferramenta | Tarefa | Revisão Humana |
|:--:|:---------|:------|
| Gemini 3.1 Pro | Serviu de apoio para a execução e resultados da avaliação do Mural UnB. | O texto gerado pela ia foi revisado para garantir informações válidas e relevantes para o projeto Mural UnB. |