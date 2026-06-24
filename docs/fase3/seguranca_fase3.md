# Fase 3 - Projetar a Avaliação (Plano de Avaliação)

## 1. Objetivo deste Plano

O projeto de avaliação do **Mural UnB** definiu, na Fase 1, "o que" avaliar (Confiabilidade e Segurança) e, na Fase 2, estabeleceu "como medir" (por meio do framework GQM, com foco em Integridade e Autenticidade). Nesta fase, o objetivo é estruturar o Plano de Avaliação, que serve como ponte definitiva entre as métricas e as hipóteses levantadas na Fase 2 (Especificar a Avaliação) e a execução prática na Fase 4 (Executar a Avaliação).

Além disso, o **Plano de Avaliação** tem como objetivo detalhar metodologicamente a execução dos testes, bem como definir os métodos de coleta, os recursos tecnológicos, o ambiente isolado de testes e o fluxo de procedimentos para auditar a **Segurança (Integridade e Autenticidade)** do Mural UnB. Ele define os recursos de hardware e software necessários, a massa de dados para simulação e o roteiro passo a passo (scripts de teste) para que qualquer avaliador externo consiga reproduzir as medições de forma consistente, objetiva e auditável na Fase 4.

> **Nota Arquitetural: Escopo Dual de Avaliação**
>
> O Mural UnB adota uma **arquitetura 100% Estática (Jamstack)** em produção: o frontend é uma SPA React (Vite + TypeScript) hospedada no GitHub Pages, alimentada por arquivos `.json` gerados offline por um pipeline de scraping via GitHub Actions. **Não existem servidor de aplicação ativo (Node.js, Django, etc.), banco de dados acessível em tempo real, sistema de autenticação por JWT ou endpoints `POST`/`PUT`/`DELETE`** na camada de produção atual.
>
> Diante dessa arquitetura, este Plano de Avaliação cobre dois escopos complementares:
>
> * **Escopos M1.1, M1.2, M2.1 e M2.2 (Passos 1–4):** Testam os controles de acesso e autenticação do backend da versão de referência (Repositório 2025-2), executado localmente via Docker. Trata-se do modelo de avaliação planejado para um sistema com API dinâmica. A medida **M1.2 (QEC-V)** é formalmente **Não Aplicável (N/A)** na camada de produção atual, pois não há endpoints privados para atacar em um servidor de arquivos estáticos; ela é válida apenas no ambiente Docker local.
> * **Escopos M3 (TNCM) e M4 (TPV) (Passos 5–6):** Avaliam a camada efetivamente em produção (a SPA estática) por análise de renderização React e procedência dos dados no `oportunidades.json`.

**Resumo da Coleta:** O fluxo de testes adotará uma estratégia **híbrida** (automatizada e manual). A coleta das métricas de integridade (M1/M2) será realizada via API em ambiente Docker local. As métricas de camada frontend (M3/M4) serão coletadas por injeção de payloads e análise estática do código-fonte. Os dados consolidados serão armazenados em uma Ficha de Registro (Google Sheets), enquanto as evidências de execução serão documentadas por relatórios nos formatos `.json` e `.csv`, além de capturas de tela.

* **Produto Alvo:** Mural UnB, nas camadas backend (Repositório Oficial 2025-2, via Docker) para M1/M2 e frontend/serverless (produção GitHub Pages) para M3/M4.
* **Foco da avaliação:** Segurança da Informação (Integridade de Endpoints e Autenticidade de Usuários).

## 2. Rastreabilidade e Consistência (Fase 2 ➔ Fase 3)

Para assegurar a rastreabilidade exigida pelo processo formal de avaliação e explicitar a consistência do plano com as métricas e os critérios de julgamento estabelecidos na Fase 2, este plano descreve métodos e recursos estritamente coerentes com o modelo GQM ali definido. A tabela abaixo mapeia como cada métrica será operacionalizada neste plano.

| **Métrica (Fase 2)** | **Foco** | **Método Projetado (Fase 3)** | **Justificativa do Alinhamento** |
| --- | --- | --- | --- |
| **M1.1 (TBM-NAut)** | Integridade | Testes de *Payload* de API com interceptação de *Tokens* JWT. | Avalia diretamente se a API bloqueia ações (PUT/DELETE) feitas por usuários sem o privilégio adequado, garantindo o Nível de Pontuação de 100% de bloqueios exigido. |
| **M1.2 (QEC-V)** | Integridade | Inspeção sistemática de rotas e injeção de requisições sem cabeçalho Authorization (ambiente Docker). **⚠️ N/A na camada de produção**: o GitHub Pages serve arquivos estáticos; não há endpoints privados para atacar. | Garante a verificação binária (0 endpoints vulneráveis) para rotas de manipulação de dados no backend de referência (2025-2). |
| **M2.1 (EVD-Inst)** | Autenticidade | Automação de tentativas de cadastro via API com domínios *Regex* falhos. | Permite quantificar a Taxa de Rejeição de Acessos Inválidos simulando e-mails não institucionais (@gmail, @outlook). |
| **M2.2 (P-2FA)** | Autenticidade | Consulta SQL direta no Banco de Dados (Ambiente de Teste). | Mede empiricamente a adoção da dupla autenticação pelos administradores, acessando a base de dados onde a flag `is_2fa_enabled` fica armazenada. |
| **M3 (TNCM)** | Integridade | Teste de injeção de payloads na renderização React, em cópia local do `oportunidades.json` executada com Vite (`npm run dev`). | Mede diretamente se o escape automático do React neutraliza o conteúdo malicioso vindo do pipeline de scraping, atendendo ao critério de neutralização (nenhum vetor ativo, julgado pelo padrão da falha) definido na Fase 2. |
| **M4 (TPV)** | Autenticidade | Análise estática (script) do `oportunidades.json` somada à verificação amostral manual dos canais oficiais. | Quantifica a proporção de registros rastreáveis a uma fonte oficial verificável, atendendo ao limiar de ≥ 95% (Excelente) definido na Fase 2. |
| **M5.1 (Acesso Interface)** | Controle de Acesso | Evasão de rotas restritas via URL (`/admin`, `/dashboard`) e inspeção de DOM na aplicação hospedada. | Valida em ambiente produtivo se o front-end vaza componentes ou rotas administrativas indevidas. |
| **M5.2 (Pentest Endpoints)**| Controle de Acesso | Inspeção de tráfego (aba Network) e mapeamento exaustivo de chamadas HTTP na aplicação Jamstack. | Confirma a inexistência de uma superfície de ataque backend ativa no ambiente de produção. |
| **M6.1 (Criptografia Rede)**| Criptografia | Disparo de requisições web (`Invoke-WebRequest`) para análise de redirecionamentos (HSTS) e certificados TLS. | Garante que toda a transmissão de dados no domínio oficial se dá de forma cifrada em texto não plano. |
| **M6.2 (Proteção Repouso)** | Criptografia | Busca ativa de chaves expostas no código fonte (ex: API Keys no repositório) e auditoria dos arquivos JSON. | Verifica que a falta de um DB tradicional não afrouxa o tratamento de segredos sensíveis do projeto. |

* O **Passo 1** responde à métrica **M1.1 (TBM-NAut)** e o **Passo 2** à métrica **M1.2 (QEC-V)**, ambos por injeção de payloads de API.
* O **Passo 3** fornece os dados exigidos pela métrica **M2.1 (EVD-Inst)** (validação de domínio no cadastro) e o **Passo 4** os da métrica **M2.2 (P-2FA)** (consulta direta ao banco de dados).
* O **Passo 5** (injeção de conteúdo na renderização React) responde diretamente à métrica **M3 (TNCM)**.
* O **Passo 6** (análise de procedência e verificação amostral de canais oficiais) responde diretamente à métrica **M4 (TPV)**.
* O **Passo 7** (auditoria da camada de produção via terminal e rede) responde às métricas **M5.1 e M5.2 (Controle de Acesso)** e **M6.1 e M6.2 (Criptografia)**.

### Níveis de Pontuação e Critérios de Julgamento (M3 e M4)

Da mesma forma que M1.1, M1.2, M2.1, M2.2, M5.1, M5.2, M6.1 e M6.2 herdam da Fase 2 seus níveis de pontuação e critérios de julgamento, **M3** e **M4** reaproveitam os critérios já definidos no GQM. Todas as métricas operacionalizadas neste plano, incluindo as de produção (M5 e M6), constam no GQM da Fase 2; nenhuma métrica nova é criada nesta fase, o que garante rastreabilidade total da Fase 2 para a Fase 3. Os limiares abaixo são idênticos aos da Fase 2 e orientam o julgamento na Fase 4.

**Métrica 3 (M3) - Taxa de Neutralização de Conteúdo Malicioso (TNCM)**

* **Fórmula:** `TNCM = (Nº de payloads neutralizados na renderização / Nº total de payloads injetados no JSON de teste) x 100`
* **Referência:** [[1]](#ref-1), [[2]](#ref-2)
* **Critérios de julgamento** (pelo padrão da falha; a TNCM é indicador informativo):
    * **Excelente (H3 confirmada):** nenhum vetor ativo. Todos os payloads, em texto e `href`, são neutralizados.
    * **Aceitável:** falha restrita ao `href` dos campos de canal (exige clique do usuário), sem execução automática em campo de texto.
    * **Insatisfatório (H3 refutada):** qualquer execução automática (auto-XSS) em campo de texto.

**Métrica 4 (M4) - Taxa de Procedência Verificável (TPV)**

* **Fórmula:** `TPV = (Nº de registros com fonte/canal oficial verificável / Nº total de registros) x 100`
* **Referência:** [[1]](#ref-1), [[3]](#ref-3)
* **Critério de "verificável":** empresa júnior com `Site` ou `Instagram` preenchido e correspondente à entidade; laboratório com `contato` em domínio institucional `@unb.br`.
* **Critérios de julgamento:**
    * **Excelente (H4 confirmada):** ≥ 95%, quase todos os registros são rastreáveis a uma fonte oficial.
    * **Satisfatório:** 80% a 94%, maioria verificável, com lacuna pontual.
    * **Insatisfatório (H4 refutada):** < 80%, procedência insuficiente.

---

## 3. Recursos e Ambiente de Avaliação

Para que a avaliação não afete os usuários reais da UnB e mantenha total isolamento e segurança, a coleta de dados ocorrerá em um **Ambiente Local (Localhost)** que replica a arquitetura de produção do repositório oficial do Mural UnB. Para garantir o rigor técnico e isolar as variáveis de teste, os recursos de avaliação e a configuração do ambiente estão detalhados abaixo.

### 3.1 Recursos de Hardware

* **Computador do Avaliador:** Computador/Notebook padrão (Processador equivalente a Intel Core i5/Ryzen 5, mínimo de 8 GB de RAM), para suportar a conteinerização do banco de dados e da API simultaneamente.
* **Armazenamento:** 20 GB livres para conteinerização (Docker) e logs, garantindo ausência de swap durante as requisições de carga moderada.

### 3.2 Recursos de Software

* **Sistema Operacional:** Distribuição Linux (como Fedora ou Ubuntu) com kernel atualizado, ou Windows com WSL2 configurado.
* **Ambiente de Execução:** Docker e Docker Compose instalados para inicializar a aplicação (para subir a API e o Banco de Dados do Mural UnB localmente de forma padronizada).
* **Ferramenta de Teste de API:** **Postman** ou **Insomnia**. Utilizados para montar as requisições (GET, POST, PUT, DELETE), manipular Headers (JWT) e injetar payloads, bem como para estruturação e disparo das requisições HTTP (M1.1, M1.2, M2.1).
* **Cliente de Banco de Dados:** DBeaver, PgAdmin ou interface SQLite (para visualizar as tabelas locais e para auditoria direta no banco de dados M2.2).
* **Captura de Evidências:** OBS Studio (para gravação do fluxo de testes) e ferramenta de captura de tela nativa do SO.
* **Planilha de Registro:** Google Sheets (para consolidação dos logs de sucesso/falha).
* **Ambiente Frontend (para M3 e M4):** Node.js (v18+) e npm para executar o site localmente; Python 3 para o script de procedência; navegador web atualizado (Google Chrome ou Mozilla Firefox) com ferramentas de desenvolvedor nativas.

### 3.3 Massa de Dados (Preparação Crítica)

**Justificativa:** Avaliar o controle de acesso e a segurança de uma API sem um estado prévio não produz resultados reais. É estritamente pertinente e **obrigatório** o uso de uma massa de dados (via seeders ou script `.sql`) para agilizar a avaliação. Testar em um banco de dados vazio impossibilita a métrica M1.1 (pois não haveria oportunidades para tentar modificar) e a M2.2 (não haveria publicadores para checar o 2FA).

* A massa deverá conter, obrigatoriamente:
  + 3 usuários administradores.
  + 10 usuários com privilégio padrão (e-mails @aluno.unb.br).
  + 5 usuários simulando invasores (e-mails externos como @gmail.com ou @outlook.com).
  + 20 publicações/oportunidades pré-cadastradas associadas aos administradores.

Antes de iniciar a sessão, o script de seed do banco de dados local deverá criar:

1. **Usuário A (Publicador/Admin):** E-mail admin@unb.br (dono das postagens).
2. **Usuário B (Estudante Comum):** E-mail aluno@aluno.unb.br (sem privilégios de edição).
3. **Oportunidades:** 5 registros simulados de vagas/eventos (IDs de 1 a 5), atrelados ao Usuário A.

### 3.4 Recursos Humanos

* **Avaliadores:** Pelo menos 2 membros da equipe (um executando as requisições via API e outro registrando/auditando o banco de dados).

## 4. Método de Avaliação e Instruções de Coleta (Passo a Passo)

O método de avaliação é baseado em testes dinâmicos de API e auditoria estática de banco de dados. As instruções a seguir garantem a reprodutibilidade técnica. O avaliador deve executar as etapas na ordem especificada e registrar o resultado qualitativo (Sucesso/Falha) e quantitativo na planilha.

### 4.1 Preparação da Sessão de Teste (Setup)

1. **Clonar e inicializar:** Iniciar o backend local via terminal executando `docker-compose up -d` para subir a API e o banco de dados em instâncias isoladas.
2. **Injeção da Massa de Dados:** Rodar o script de seed de dados, no terminal, para popular o banco de dados conforme especificado na Seção 3.3 (Usuário A, Usuário B e Vagas 1 a 5).
3. **Setup das Ferramentas:** Iniciar gravação de tela com OBS Studio capturando a janela do Postman e do DBeaver. Abrir o Postman, importar a coleção de testes `Mural_UnB_Security_Tests.json` e abrir a Ficha de Registro no navegador.

### 4.2 Fluxo de Execução e Instruções de Coleta

**Passo 1: Teste de Bloqueio de Modificação (Métrica M1.1 - Integridade) da API**

* **Objetivo:** Verificar se o Usuário B (Estudante) consegue alterar dados do Usuário A.
* **Ação:**
  1. No Postman, realizar uma requisição POST /login com credenciais do **Usuário B** e copiar o Token JWT gerado. Em seguida, disparar 10 requisições do tipo PUT e DELETE direcionadas aos IDs das 20 publicações criadas pelos administradores.
  2. Criar uma requisição PUT /oportunidades/1 (tentando alterar o título da vaga 1).
  3. Inserir o Token do Usuário B no Header de Autorização.
  4. Enviar a requisição.
* **Coleta de Evidência:**
  1. Registrar se a resposta HTTP foi 403 Forbidden ou 401 Unauthorized (Sucesso no bloqueio) ou 200 OK (Falha crítica). Registrar na planilha.
  2. Tirar print do Postman mostrando o código da resposta e o corpo.
  3. Repetir o teste com requisição DELETE /oportunidades/1.
  4. **Evidência:** Exportar o relatório de resultados do Postman em formato `.csv` e salvar no repositório.

**Passo 2: Inspeção de Endpoints Vulneráveis (Métrica M1.2 - Integridade)**

* **Objetivo:** Garantir que 0 rotas críticas funcionem sem JWT.
* **Ação:**
  1. No Postman, limpar completamente a aba Headers (remover qualquer Token do cabeçalho) da requisição.
  2. Realizar disparos contra os endpoints críticos previamente mapeados na Fase 1: POST /oportunidades, PUT /oportunidades/{id}, DELETE /oportunidades/{id}, POST /admin/config.
* **Coleta de Evidência:**
  1. Para cada rota testada, documentar o retorno. Contabilizar quantos endpoints retornaram sucesso (200 OK ou 201 Created) na ausência do Token. Registrar **"1 endpoint vulnerável"** na planilha. A meta é que todos retornem bloqueio.
  2. **Evidência:** Exportar o relatório de resultados do Postman em formato `.csv` e salvar no repositório.

**Passo 3: Verificação de Domínio Institucional (Métrica M2.1 - Autenticidade)**

* **Objetivo:** Garantir que cadastros de entidades utilizem e-mails da universidade.
* **Ação:**
  1. No Postman, utilizar a rota de criação de contas de publicadores (POST /cadastro/publicador).
  2. No Body (JSON), enviar um payload com email: entidade@gmail.com. Registrar a resposta (Espera-se erro/validação Regex).
  3. Repetir alterando o payload para entidade@outlook.com.
  4. Repetir alterando o payload para entidade@unb.br. (Espera-se sucesso 201).
* **Coleta de Evidência:**
  1. Registrar a proporção: Total de domínios falsos rejeitados / Total de tentativas com domínios falsos. O esperado para excelência é 100%.
  2. Para **M2.1 (EVD-Inst)**: Verificar o código de resposta HTTP de cada requisição. Contabilizar quantas tentativas foram rejeitadas com erro de validação (ex: 422 Unprocessable Entity ou 400 Bad Request).
  3. **Evidência:** Print da tela do Postman exibindo a mensagem de erro da API rejeitando o domínio não institucional.

**Passo 4: Proporção de 2FA para Publicadores (Métrica M2.2 - Autenticidade)**

* **Objetivo:** Medir a camada extra de segurança diretamente no banco.
* **Ação:**
  1. Abrir o cliente de Banco de Dados (DBeaver) conectado ao PostgreSQL/MySQL do Mural UnB local.
  2. Executar a Query SQL: SELECT COUNT(*) FROM users WHERE role='publisher' AND is_2fa_enabled=true; (Para pegar usuários com 2FA).
  3. Executar a Query SQL: SELECT COUNT(*) FROM users WHERE role='publisher'; (Total de publicadores).
  4. Dividir o resultado pelo total dos usuários publicadores. Registrar a porcentagem exata na Ficha de Registro.
* **Coleta de Evidência:**
  1. Captura de tela contendo o comando SQL executado e o retorno da tabela no console do banco de dados.
  2. Printar o resultado da Query.
  3. Calcular na planilha a porcentagem de adoção do 2FA.

**Passo 5: Teste de Injeção de Conteúdo (Métrica M3 - Integridade/Frontend)**

* **Objetivo:** Verificar se o React neutraliza payloads XSS injetados no `oportunidades.json`.
* **Ação:**
  1. Clone (ou faça um fork) o repositório do Mural UnB. Na pasta `site/`, execute `npm install` para instalar as dependências (React 19 + Vite).
  2. Crie uma cópia de teste do arquivo `data/oportunidades.json`. Em registros selecionados, injete um conjunto controlado de payloads, distribuídos por tipo de campo, e registre o total injetado (denominador):
      - **Campos de texto** (`descricao`, `Sobre`, `Nome`): `<script>alert('xss')</script>`, `<img src=x onerror=alert('xss')>` e `<b>conteudo-injetado</b>`.
      - **Campos de canal** (`Site`, `Instagram`): `javascript:alert('xss')`.
  3. Inicie a aplicação com `npm run dev` e abra no navegador as oportunidades modificadas.
  4. Para cada payload, observe a renderização e classifique:
      - **Neutralizado:** o conteúdo aparece como texto literal na tela, ou o link não executa código.
      - **Ativo:** o script executa (o `alert` dispara), o HTML é injetado no DOM, ou o clique no link `javascript:` executa código.
      Registre o resultado da classificação de cada payload.
* **Coleta de Evidência:**
  1. Conte os payloads neutralizados (numerador) e aplique a fórmula: `TNCM = (neutralizados / total injetado) * 100`.
  2. Compare com os critérios de julgamento classificando pelo **padrão da falha**: Excelente = nenhum vetor ativo; Aceitável = falha restrita ao `href` de canal (exige clique), sem auto-XSS em campo de texto; Insatisfatório = qualquer execução automática em campo de texto. A TNCM é reportada como indicador.
  3. **Evidência:** registro da classificação dos payloads e a análise estática do código-fonte (`docs/evidencias_fase4/m3_analise_estatica.md`).

**Passo 6: Análise de Procedência (Métrica M4 - Autenticidade/Frontend)**

* **Objetivo:** Verificar que toda oportunidade publicada tem origem em uma fonte oficial verificável.
* **Ação:**
  1. Obtenha o arquivo `data/oportunidades.json` do repositório.
  2. Execute um script que percorra os registros e conte os que possuem canal/fonte oficial verificável: empresas juniores com `Site` ou `Instagram` preenchido; laboratórios com `contato` em domínio institucional `@unb.br`. Exemplo:

      ```python
      import json, re
      d = json.load(open('data/oportunidades.json'))
      labs, ejs = d['laboratorios'], d['empresas_juniores']
      unb = re.compile(r'@([a-z0-9.-]+\.)?unb\.br', re.I)

      lab_ok = [l for l in labs if unb.search(str(l.get('contato','')))]
      ej_ok  = [e for e in ejs if str(e.get('Site','')).strip() or str(e.get('Instagram','')).strip()]

      verificaveis = len(lab_ok) + len(ej_ok)
      total = len(labs) + len(ejs)
      print('TPV = %.1f%%' % (100 * verificaveis / total))
      ```

  3. Selecione uma amostra aleatória (~20 registros) e confirme manualmente que o canal informado resolve para a entidade real (o `Site`/`Instagram` pertence à empresa júnior citada; o `contato` do laboratório é institucional). Registre quantos da amostra se confirmam.
* **Coleta de Evidência:**
  1. Aplique a fórmula: `TPV = (registros com procedência verificável / total de registros) * 100`.
  2. Compare com os critérios de julgamento (Excelente ≥ 95%; Satisfatório 80% a 94%; Insatisfatório < 80%).
  3. **Evidência:** Saída do script e registros da verificação amostral.

**Passo 7: Avaliação da Camada de Produção via Terminal e Rede (Métricas M5 e M6)**

Este passo é exclusivo para o ambiente estático efetivamente publicado (o site no GitHub Pages) e não se aplica à API local executada via Docker. Ele compreende a auditoria do acesso (M5) e da criptografia (M6).

* **Objetivo:** Comprovar a segurança do tráfego, a ausência de rotas vulneráveis e a blindagem dos dados sensíveis armazenados na camada de produção do Mural UnB.
* **Ação e Coleta de Evidências:**
  1. **M5.1 (Acesso Interface):** Tentar acessar via navegador rotas administrativas comuns (ex: `https://muralunb.com.br/admin` ou `/dashboard`). Registrar se retornam `404 Not Found`. Inspecionar o código-fonte (DOM) e o `localStorage` em busca de dados vazados.
  2. **M5.2 (Pentest Endpoints):** Realizar mapeamento de todas as chamadas via `fetch` no frontend. Registrar e apresentar evidência de que não existem métodos HTTP ativos para injeção (ex: `POST`, `PUT`), ou seja, constatar que a API produtiva "não existe" no formato tradicional vulnerável.
  3. **M6.1 (Criptografia Rede):** No PowerShell (ou Terminal), executar `Invoke-WebRequest -Uri http://muralunb.com.br -MaximumRedirection 0`. Coletar o código `301 Moved Permanently` para provar o redirecionamento. Averiguar, nos cabeçalhos de resposta HTTP, a presença do `Strict-Transport-Security` (HSTS) e a configuração de TLS.
  4. **M6.2 (Proteção Repouso):** Auditar a configuração dos "Secrets" no GitHub Actions (ex: verificação da proteção da variável `GEMINI_API_KEY`). Checar se não existem dados como CPF/Senhas (PII) salvos em texto plano nos JSONs. Registrar conformidade na proteção dos segredos do repositório.

## 5. Armazenamento e Estrutura dos Dados (Evidências)

* **Ficha de Registro (Google Sheets):** Todos os dados numéricos brutos (contagem de requisições, status codes, percentuais) serão lançados na planilha padronizada criada na Fase 2.
* **Gestão de Evidências:** A pasta `/evidencias_fase4/` no repositório GitHub deverá conter:
  1. O arquivo `postman_collection_results.csv`.
  2. Os prints de tela nomeados de forma rastreável (ex: `M2.1_Erro_Dominio_Invalido.png`, `M2.2_Query_2FA.png`).
  3. Evidência de M3 por análise estática do código (`m3_analise_estatica.md`).
  4. Saída do script de procedência M4 e registros da verificação amostral.

Todos os artefatos resultantes deverão ser versionados no repositório GitHub do projeto, sob o diretório `docs/evidencias_fase4/`:

* `tabela_resultados_mural_unb.xlsx` (contendo os cálculos de M1.1 a M4).
* `postman_collection_mural_unb.json` (exportação com as requisições exatas feitas para que a professora possa auditar a reprodutibilidade).
* Pasta de capturas de tela rotuladas claramente (ex: `M1.1_TentativaDelete_UserB.png`).
* O link do vídeo (não listado no YouTube) demonstrando a execução contínua dos testes será fixado no relatório final da Fase 4.

## 6. Cronograma das Ações (Realista e Alinhado)

Abaixo, o roteiro alinha as preparações e as execuções práticas, considerando as datas contemporâneas à disciplina e a transição da Fase 3 para a Fase 4 (Execução).

| **Data** | **Fase** | **Atividade** | **Responsáveis** | **Entregável / Meta** |
| --- | --- | --- | --- | --- |
| **12/06/2026** | Fase 3 | Configuração do ambiente local (Docker) e script de seed (Massa de Dados). | Equipe (Desenvolvedores) | Backend rodando localmente de forma isolada. |
| **14/06/2026** | Fase 3 | Criação e exportação da Collection do Postman com as rotas a serem avaliadas. | Lucas, Caio, Guilherme | `postman_collection_mural_unb.json`. |
| **17/06/2026** | Fase 4 | Sessão de Avaliação - Execução de M1.1 e M1.2 (Integridade). | Carlos, Yogi, Isaac | Gravação de tela e prints de bloqueio. |
| **18/06/2026** | Fase 4 | Sessão de Avaliação - Execução de M2.1 e M2.2 (Autenticidade). | Equipe | Relatórios SQL e testes de Regex com Postman. |
| **19/06/2026** | Fase 4 | Sessão de Avaliação - Execução de M3 (TNCM), M4 (TPV), M5 e M6. | Isaac | Testes de frontend, procedência e produção. |
| **20/06/2026** | Fase 4 | Consolidação das planilhas, cálculo das métricas e elaboração do julgamento cruzado com a Fase 2. | Equipe | Planilha final e redação do Relatório F4. |
| **24/06/2026** | Fase 4 | Revisão ortográfica, validação de links na GitPage e entrega (EU3). | Equipe | Release final no GitHub/Moodle. |

## 7. Referências Bibliográficas

<a id="ref-1"></a>[1] INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO/IEC 25010**: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models. Geneva: ISO, 2011.

<a id="ref-2"></a>[2] MITRE. *CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')*. 2024. Disponível em: `https://cwe.mitre.org/data/definitions/79.html`. Acesso em: 12 jun. 2026.

<a id="ref-3"></a>[3] OWASP FOUNDATION. *OWASP Top Ten — A01:2021 Broken Access Control*. 2021. Disponível em: `https://owasp.org/Top10/A01_2021-Broken_Access_Control/`. Acesso em: 12 jun. 2026.

---

## Histórico de Versão

| **Versão** | **Data** | **Descrição** | **Autor** |
| --- | --- | --- | --- |
| 1.0 | 10/06/2026 | Criação inicial do Plano de Avaliação (Fase 3) alinhado ao GQM. | Lucas |
| 2.0 | 12/06/2026 | Integração das métricas M3 (TNCM) e M4 (TPV) Frontend/Serverless. Passos 5 e 6, referências bibliográficas | Isaac |
| 2.1 | 12/06/2026 | Padronização de M3 e M4: inclusão na tabela de rastreabilidade (Fase 2 ➔ Fase 3) e reformatação dos critérios de julgamento no padrão do documento. | Isaac |
| 2.2 | 12/06/2026 | Ajuste do critério de M3 (TNCM): julgamento pelo padrão da falha (auto-XSS em texto) em vez do percentual bruto, alinhado à Fase 2. | Isaac | 
| 2.3 | 23/06/2026 | Correção da rastreabilidade Passo ➔ Métrica (Passos 1 a 7 mapeados às respectivas métricas) e reforço explícito da consistência Fase 2 ➔ Fase 3 (M5/M6 herdam critérios do GQM; nenhuma métrica nova criada). Ajustes em resposta à avaliação por pares (F3-C1 e F3-C8). | Isaac | 

## Declaração do Uso de IA

| Ferramenta | Tarefa | Revisão Humana |
|:--:|:---------|:------|
| Gemini 1.5 Pro / Agentes IA | Utilizada para classificar insights de confiabilidade e segurança, auxiliar na interpretação de dados, conduzir a estruturação dos testes práticos e realizar a revisão e correção ortográfica do documento. | O texto e as classificações geradas pela IA foram rigorosamente revisados, adaptados ao contexto do projeto e validados para garantir informações fidedignas e relevantes para o Mural UnB. |
