# Fase 3 - Projetar a Avaliação (Plano de Avaliação)

## 1. Objetivo deste Plano**

O projeto de avaliação do **Mural UnB**, na Fase 1 definiu "o que" avaliar (Confiabilidade e Segurança) e na Fase 2 estabeleceu "como medir" (por meio do framework GQM focando em Integridade e Autenticidade). Nesta fase, o objetivo é estruturar o Plano de Avaliação, servindo como a ponte definitiva entre as métricas e as hipóteses levantadas na Fase 2 (Especificar a Avaliação) e a execução prática na Fase 4 (Executar a Avaliação).

Outrossim, o **Plano de Avaliação** tem como objetivo detalhar metodologicamente a execução dos testes, bem como definir os métodos de coleta, os recursos tecnológicos, o ambiente isolado de testes e o fluxo de procedimentos para auditar a **Segurança (Integridade e Autenticidade)** da API do Mural UnB. Ele define os recursos de hardware e software necessários, a massa de dados para simulação, e o roteiro passo a passo (scripts de teste) para que qualquer avaliador externo consiga reproduzir as medições de forma consistente, objetiva e auditável na Fase 4. O escopo desta execução limita-se ao **Backend e API** do Mural UnB.

**Resumo da Coleta:** O fluxo de testes adotará uma estratégia **híbrida (automatizada e manual).** A coleta das métricas de integridade serão extraídas por meio de rotinas automatizadas via API. Os dados consolidados serão armazenados em uma **“Ficha de Registro (Google Sheets)”,** enquanto as evidências de execução documentadas por meio de relatórios nos formatos .*json* e *.csv*, além de prints de tela do banco de dados.

* **Produto Alvo:** Backend/API do Mural UnB (Repositório Oficial 2025-2).
* **Foco da avaliação:** Segurança da Informação (Integridade de Endpoints e Autenticidade de Usuários).

## 2. Rastreabilidade e Consistência (Fase 2 ➔ Fase 3)**

Para assegurar a rastreabilidade exigida pelo processo formal de avaliação e explicitar a consistência do plano de avaliação com as métricas e critérios de julgamento estabelecidos na Fase 2. Além disso, este plano descreve métodos e recursos estritamente coerentes com o modelo GQM definido na Fase 2. A tabela abaixo mapeia como cada métrica será operacionalizada neste plano.

| **Métrica (Fase 2)** | **Foco** | **Método Projetado (Fase 3)** | **Justificativa do Alinhamento** |
| --- | --- | --- | --- |
| **M1.1 (TBM-NAut)** | Integridade | Testes de *Payload* de API com interceptação de *Tokens* JWT. | Avalia diretamente se a API bloqueia ações (PUT/DELETE) feitas por usuários sem o privilégio adequado, garantindo o Nível de Pontuação de 100% de bloqueios exigido. |
| **M1.2 (QEC-V)** | Integridade | Inspeção sistemática de rotas e injeção de requisições sem cabeçalho Authorization. | Garante a verificação binária (0 endpoints vulneráveis) estipulada na Fase 2 para rotas de manipulação de dados. |
| **M2.1 (EVD-Inst)** | Autenticidade | Automação de tentativas de cadastro via API com domínios *Regex* falhos. | Permite quantificar a Taxa de Rejeição de Acessos Inválidos simulando e-mails não institucionais (@gmail, @outlook). |
| **M2.2 (P-2FA)** | Autenticidade | Consulta SQL direta no Banco de Dados (Ambiente de Teste). | Mede empiricamente a adoção da dupla autenticação pelos administradores, acessando a base de dados onde a flag is\_2fa\_enabled fica armazenada. |

* As ferramentas de injeção de *payloads* (Passo 2 do fluxo) respondem diretamente às métricas **M1.1 (TBM-NAut)** e **M1.2 (QEC-V)**.
* A validação de formulários de registro e consultas ao banco de dados (Passo 3 do fluxo) fornecem os dados exatos exigidos pelas métricas **M2.1 (EVD-Inst)** e **M2.2 (P-2FA)**.

## 3. Recursos e Ambiente de Avaliação

Para que a avaliação não afete os usuários reais da UnB e mantenha total isolamento e segurança, a coleta de dados ocorrerá em um **Ambiente Local (Localhost)** replicando a arquitetura de produção do repositório oficial do Mural UnB. Desse modo, a fim de garantir o rigor técnico e isolar as variáveis de teste, os recursos de avaliação e a configuração do ambiente estão detalhados abaixo.

### 3.1 Recursos de Hardware

* **Computador do Avaliador:** Computador/Notebook padrão (Processador equivalente a Intel Core i5/Ryzen 5, mínimo de 8GB de RAM), para suportar a conteinerização do banco de dados e da API simultaneamente.
* **Armazenamento:** 20GB livres para conteinerização (Docker) e logs, garantindo ausência de *swap* durante as requisições de carga moderada.

### 3.2 Recursos de Software

* **Sistema Operacional:** Distribuição Linux (como Fedora ou Ubuntu) com kernel atualizado, ou Windows com WSL2 configurado.
* **Ambiente de Execução:** Docker e Docker Compose instalados para inicializar a aplicação (para subir a API e o Banco de Dados do Mural UnB localmente de forma padronizada).
* **Ferramenta de Teste de API:** **Postman** ou **Insomnia**. Utilizados para montar as requisições (GET, POST, PUT, DELETE), manipular *Headers* (JWT) e injetar *payloads*, bem como para estruturação e disparo das requisições HTTP (M1.1, M1.2, M2.1).
* **Cliente de Banco de Dados:** DBeaver ou PgAdmin ou interface SQLite (para visualizar as tabelas locais e para auditoria direta no banco de dados M2.2).
* **Captura de Evidências:** OBS Studio (para gravação do fluxo de testes) e ferramenta de captura de tela nativa do SO.
* **Planilha de Registro:** Google Sheets (para consolidação dos logs de sucesso/falha).

### 3.3 Massa de Dados (Preparação Crítica)

**Justificativa:** Avaliar o controle de acesso e a segurança de uma API sem um estado prévio não produz resultados reais. É estritamente pertinente e **obrigatório** o uso de uma massa de dados (via *seeders* ou script .sql) para agilizar a avaliação. Testar em um banco de dados vazio impossibilita a métrica M1.1 (pois não haveria oportunidades para tentar modificar) e a M2.2 (não haveria publicadores para checar o 2FA).

* A massa deverá conter, obrigatoriamente:
  + 3 usuários administradores.
  + 10 usuários com privilégio padrão (e-mails @[aluno.unb.br](http://aluno.unb.br/)).
  + 5 usuários simulando invasores (e-mails externos como @[gmail.com](http://gmail.com/) ou @[outlook.com](http://outlook.com/)).
  + 20 publicações/oportunidades pré-cadastradas associadas aos administradores.

Antes de iniciar a sessão, o script de *seed* do banco de dados local deverá criar:

1. **Usuário A (Publicador/Admin):** E-mail admin@unb.br. (Dono das postagens).
2. **Usuário B (Estudante Comum):** E-mail aluno@aluno.unb.br. (Sem privilégios de edição).
3. **Oportunidades:** 5 registros simulados de vagas/eventos (IDs de 1 a 5), atrelados ao Usuário A.

### 3.4 Recursos Humanos

* **Avaliadores:** Pelo menos 2 membros da equipe (um executando as requisições via API e outro registrando/auditando o banco de dados).

## 4. Método de Avaliação e Instruções de Coleta (Passo a Passo)

O método de avaliação é baseado em testes dinâmicos de API e auditoria estática de banco de dados. As instruções a seguir garantem a reprodutibilidade técnica. O avaliador deve executar as etapas na ordem especificada e registrar o resultado qualitativo (Sucesso/Falha) e quantitativo na planilha.

### 4.1 Preparação da Sessão de Teste (Setup)

1. **Clonar e inicializar:** Iniciar o backend local via terminal executando docker-compose up -d para subir a API e o banco de dados em instâncias isoladas.
2. **Injeção da Massa de Dados:** Rodar o script de seed de dados, no terminal, para popular o banco de dados conforme especificados na Sessão 3.3 (Usuário A, Usuário B e Vagas 1 a 5).
3. **Setup das Ferramentas:** Iniciar gravação de tela com OBS Studio capturando a janela do Postman e do DBeaver. Abrir o Postman, importar a coleção de testes Mural\_UnB\_Security\_Tests.json e abrir a Ficha de Registro no navegador.

### 4.2 Fluxo de Execução e Instruções de Coleta

**Passo 1: Teste de Bloqueio de Modificação (Métrica M1.1 - Integridade) da API**

* **Objetivo:** Verificar se o Usuário B (Estudante) consegue alterar dados do Usuário A.
* **Ação:**
  1. No Postman, realizar uma requisição POST /login com credenciais do **Usuário B** e copiar o *Token* JWT gerado. Em seguida, disparar 10 requisições do tipo PUT e DELETE direcionadas às IDs das 20 publicações criadas pelos administradores.
  2. Criar uma requisição PUT /oportunidades/1 (tentando alterar o título da vaga 1).
  3. Inserir o *Token* do Usuário B no *Header* de Autorização.
  4. Enviar a requisição.
* **Coleta de Evidência:**
  1. Registrar se a resposta HTTP foi 403 Forbidden ou 401 Unauthorized (Sucesso no bloqueio) ou 200 OK (Falha crítica). Registrar na planilha.
  2. Tirar print do Postman mostrando o código da resposta e o corpo.
  3. Repetir o teste com requisição DELETE /oportunidades/1.
  4. *Evidência:* Exportar o relatório de resultados do Postman em formato .csv e salvar no repositório.

**Passo 2: Inspeção de Endpoints Vulneráveis (Métrica M1.2 - Integridade)**

* **Objetivo:** Garantir que 0 rotas críticas funcionem sem JWT.
* **Ação:**
  1. No Postman, limpar completamente a aba *Headers* (remover qualquer Token do cabeçalho) da requisição.
  2. Realizar disparos contra os *endpoints* críticos previamente mapeados na Fase 1: POST /oportunidades, PUT /oportunidades/{id}, DELETE /oportunidades/{id}, POST /admin/config.
* **Coleta de Evidência:**
  1. Para cada rota testada, documentar o retorno.  Contabilizar quantos endpoints retornaram sucesso (200 OK ou 201 Created) na ausência do Token. Registrar **"1 endpoint vulnerável"** na planilha. A meta é que todos retornem bloqueio.
  2. *Evidência:* Exportar o relatório de resultados do Postman em formato .csv e salvar no repositório.

**Passo 3: Verificação de Domínio Institucional (Métrica M2.1 - Autenticidade)**

* **Objetivo:** Garantir que cadastros de entidades utilizem e-mails da universidade.
* **Ação:**
  1. No Postman, utilizar a rota de criação de contas de publicadores (POST /cadastro/publicador).
  2. No *Body* (JSON), enviar um payload com email: entidade@gmail.com. Registrar a resposta (Espera-se erro/validação Regex).
  3. Repetir alterando o payload para entidade@outlook.com.
  4. Repetir alterando o payload para entidade@unb.br. (Espera-se sucesso 201).
* **Coleta de Evidência:**
  1. Registrar a proporção: Total de domínios falsos rejeitados / Total de tentativas com domínios falsos. O esperado para excelência é 100%.
  2. Para **M2.1 (EVD-Inst)**: Verificar o código de resposta HTTP de cada requisição. Contabilizar quantas tentativas foram rejeitadas com erro de validação (ex: 422 Unprocessable Entity ou 400 Bad Request).
  3. *Evidência:* Print da tela do Postman exibindo a mensagem de erro da API rejeitando o domínio não institucional.

**Passo 4: Proporção de 2FA para Publicadores (Métrica M2.2 - Autenticidade)**

* **Objetivo:** Medir a camada extra de segurança diretamente no banco.
* **Ação:**
  1. Abrir o cliente de Banco de Dados (DBeaver) conectado ao PostgreSQL/MySQL do Mural UnB local.
  2. Executar a Query SQL: SELECT COUNT(\*) FROM users WHERE role='publisher' AND is\_2fa\_enabled=true; (Para pegar usuários com 2FA).
  3. Executar a Query SQL: SELECT COUNT(\*) FROM users WHERE role='publisher'; (Total de publicadores).
  4. Dividir o resultado pelo total dos usuários publicadores. Registrar a porcentagem exata na Ficha de Registro.
* **Coleta de Evidência:**
  1. Captura de tela contendo o comando SQL executado e o retorno da tabela no console do banco de dados.
  2. Printar o resultado da Query.
  3. Calcular na planilha a porcentagem de adoção do 2FA.

## 5. Armazenamento e Estrutura dos Dados (Evidências)

* **Ficha de Registro (Google Sheets):** Todos os dados numéricos brutos (contagem de requisições, status codes, percentuais) serão lançados na planilha padronizada criada na Fase 2.
* **Gestão de Evidências:** A pasta /evidencias\_fase4/ no repositório GitHub deverá conter:
  1. O arquivo postman\_collection\_results.csv.
  2. Os prints de tela nomeados de forma rastreável (ex: M2.1\_Erro\_Dominio\_Invalido.png, M2.2\_Query\_2FA.png).

Todos os artefatos resultantes deverão ser comitados no repositório GitHub do projeto sob o diretório docs/evidencias\_fase4/:

* tabela\_resultados\_mural\_unb.xlsx (Contendo os cálculos de M1.1 a M2.2).
* postman\_collection\_mural\_unb.json (Exportação com as requisições exatas feitas para que a professora possa auditar a reprodutibilidade).
* Pasta de *Screenshots* rotulados claramente (ex: M1.1\_TentativaDelete\_UserB.png).
* O link do vídeo (não listado no YouTube) demonstrando a execução contínua dos testes será fixado no relatório final da Fase 4.

## 6. Cronograma das Ações (Realista e Alinhado)

Abaixo, o roteiro alinha as preparações e as execuções práticas, considerando as datas contemporâneas à disciplina e a transição da Fase 3 para a Fase 4 (Execução).

| **Data** | **Fase** | **Atividade** | **Responsáveis** | **Entregável / Meta** |
| --- | --- | --- | --- | --- |
| **12/06/2026** | Fase 3 | Configuração do ambiente local (Docker) e script de *seed* (Massa de Dados). | Equipe (Desenvolvedores) | Backend rodando localmente de forma isolada. |
| **14/06/2026** | Fase 3 | Criação e exportação da Collection do Postman com as rotas a serem avaliadas. | Lucas, Caio, Guilherme | postman\_collection\_mural\_unb.json. |
| **17/06/2026** | Fase 4 | Sessão de Avaliação - Execução de M1.1 e M1.2 (Integridade). | Carlos, Yogi, Isaac | Gravação de tela e prints de bloqueio. |
| **18/06/2026** | Fase 4 | Sessão de Avaliação - Execução de M2.1 e M2.2 (Autenticidade). | Equipe | Relatórios SQL e testes de Regex com Postman. |
| **20/06/2026** | Fase 4 | Consolidação das planilhas, cálculo das métricas e elaboração do julgamento cruzado com a Fase 2. | Equipe | Planilha final e redação do Relatório F4. |
| **24/06/2026** | Fase 4 | Revisão ortográfica, validação de links na GitPage e entrega (EU3). | Equipe | Release final no GitHub/Moodle. |

## Histórico de Versão

| **Versão** | **Data** | **Descrição** | **Autor** | **data** |
| --- | --- | --- | --- | --- |
| 1.0 | 10/06/2026 | Criação inicial do Plano de Avaliação (Fase 3) alinhado ao GQM. | Lucas | 12/06/2026 |

## Declaração do uso de ia

| Ferramenta | Tarefa | Revisão Humana |
|:--:|:---------|:------|
| Gemini 3.1 Pro | Contribuiu para estruturar o plano de avaliação, além de estruturar o git page.  | O texto gerado pela ia foi revisado para garantir informações válidas e relevantes para o projeto Mural UnB. |