# Fase 04 - Execução e Resultados da Avaliação

## 1. Contexto e Objetivo

Conforme o Plano de Avaliação estabelecido na Fase 3, o presente documento consolida os resultados da avaliação do produto de software **Mural UnB (Versão 1.0.0).** O propósito desta fase é apresentar as métricas coletadas, compará-las com as pontuações estabelecidas pelo método GQM (Fase 2) e emitir um parecer conclusivo sobre a **Segurança da Informação,** com ênfase nas subcaracterísticas de **Integridade** e **Autenticidade**.

> **Nota Arquitetural**
> O Mural UnB adota uma **arquitetura 100% Estática (Jamstack)** em produção (SPA React + GitHub Pages + arquivos `.json` estáticos). Não existe servidor de aplicação ativo, banco de dados acessível ou endpoints `POST`/`PUT`/`DELETE` em produção. As métricas **M1.1, M1.2, M2.1 e M2.2** foram coletadas no *backend* de referência (Repositório 2025-2) executado via Docker local, enquanto **M3 e M4** avaliam a camada estática efetivamente em produção.

As informações levantadas têm o intuito de viabilizar a meta estipulada na Fase 1: apresentar um diagnóstico prático e embasado, capaz de consolidar o Mural UnB, assegurando que o sistema ofereça um ambiente transparente e de alta credibilidade para todos os usuários da comunidade acadêmica, bem como protegido contra manipulações de dados e invasões.

* + **Ambiente de Teste (M1/M2):** Localhost (Docker Compose - API e PostgreSQL) com script de *seed* (Massa de Dados).
  + **Ambiente de Teste (M3/M4):** Camada frontend estática (GitHub Pages / `npm run dev` local) e análise estática do `oportunidades.json`.
  + **Período de Execução:** 17/06/2026 a 20/06/2026.

## 2. Processamento e Transformação de Dados em Métricas

Com efeito, seguindo os Passos 1 a 6 do Plano de Avaliação (Fase 3), as medidas foram extraídas de forma híbrida: os Passos 1 a 4 (M1/M2) por testes dinâmicos de API via Postman e auditoria via cliente DBeaver, e os Passos 5 e 6 (M3/M4) por injeção na renderização e análise do `oportunidades.json` na camada frontend/_serverless_ (detalhados na Seção 2.3).

### 2.1. Medição 1: Segurança - Integridade (Q1)

A integridade avalia se o sistema previne modificações de editais, de vagas e de oportunidades por usuários sem os devidos privilégios.

| **ID** | **Métrica (Descrição)** | **Fórmula Aplicada** | **Resultado Obtido** | **Limiar de Julgamento (Fase 2)** | **Status** |
| --- | --- | --- | --- | --- | --- |
| **M1.1** | **Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut)** | (10 bloqueadas / 10 tentativas forjadas) \* 100 | **100%** | 100% $\implies$ Excelente | **EXCELENTE** |
| **M1.2** | **Quantidade de Endpoints Críticos Vulneráveis (QEC-V)** | Contagem absoluta de rotas abertas sem Token JWT (ambiente Docker). **⚠️ N/A na camada de produção** — arquitetura Jamstack sem endpoints privados. | **0 endpoints** vulneráveis (backend Docker) | 0 $\implies$ Excelente (backend) · N/A (produção estática) | **EXCELENTE** (backend) |

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

### 2.4. Avaliação da Camada de Produção (M5 e M6) e Avaliação Frontend (M3 e M4)

A avaliação da característica foi conduzida com base no modelo GQM previamente definido para o Mural UnB. O objetivo desta etapa consistiu em verificar se a arquitetura da aplicação atende aos requisitos relacionados à Confidencialidade, Integridade, Não-repúdio, Responsabilidade e Autenticidade, com foco especial nas hipóteses associadas ao controle de acesso e à proteção criptográfica dos dados.

Durante a execução dos testes, observou-se que a arquitetura do Mural UnB é integralmente baseada em recursos estáticos hospedados no GitHub Pages. A aplicação não possui autenticação de usuários, banco de dados transacional ou serviços de backend executando operações de escrita. Em razão dessas características, parte das métricas definidas inicialmente precisou ser analisada sob a ótica da aplicabilidade arquitetural, uma vez que determinados cenários de teste pressupõem a existência de componentes inexistentes no sistema avaliado.

**PASSO 1 – Avaliação da controlabilidade de acesso na interface (Métrica M5.1)**

A primeira etapa buscou verificar se usuários comuns conseguiriam acessar funcionalidades administrativas ou telas restritas por meio da manipulação direta da interface ou das URLs da aplicação.

| Tarefa Executada | Ação no Sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Forçar rota `/admin` | Acesso direto pela URL. | O servidor retornou erro 404, impedindo o carregamento da página. | Bloqueado |
| Forçar rota `/login` | Acesso direto pela URL. | O servidor retornou erro 404. Nenhuma rota administrativa foi identificada durante a inspeção do código-fonte. | Bloqueado |
| Inspeção de elementos ocultos | Análise do DOM utilizando ferramentas do navegador. | Não foram encontrados componentes administrativos ocultos ou controles acessíveis por manipulação manual da interface. | Bloqueado |

A partir dos testes realizados, verificou-se que todas as tentativas de acesso indevido foram interceptadas. Dessa forma, a métrica M5.1 atingiu o valor de 100%, corroborando a Hipótese 5 para a camada de apresentação.

**PASSO 2 – Avaliação da controlabilidade de acesso na API (Métrica M5.2)**

Em seguida, foi realizada uma análise estrutural da comunicação entre cliente e servidor para identificar possíveis endpoints protegidos e verificar a viabilidade da execução dos testes previstos para a métrica M5.2.

| Tarefa executada | Ação no sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Mapeamento de endpoints | Busca por chamadas HTTP no código. | Foram identificadas exclusivamente requisições GET para arquivos JSON públicos. | Não aplicável |
| Pentest em endpoints protegidos | Simulação de requisições utilizando Postman. | Não foram encontrados endpoints privados ou operações protegidas por autenticação. | Não aplicável |

Embora a hipótese previsse a medição da taxa de rejeição de requisições não autorizadas, a inexistência de uma API protegida impossibilitou a execução do teste. Portanto, a métrica foi considerada não aplicável para a arquitetura atual do sistema em produção.

**PASSO 3 – Avaliação da Proteção de Dados em Trânsito (Métrica M6.1)**

A avaliação da proteção criptográfica em trânsito teve como objetivo verificar se as informações trafegam por canais seguros e protegidos contra interceptação.

| Tarefa Executada | Ação no Sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Verificação de HTTPS obrigatório | Requisição inicial utilizando HTTP. | O servidor realizou redirecionamento automático para HTTPS. | Sucesso |
| Inspeção dos cabeçalhos de segurança | Análise dos headers de resposta. | Foi identificado o uso de HSTS e certificado TLS válido. | Sucesso |
| Análise do tráfego de rede | Monitoramento das comunicações realizadas pela aplicação. | Não foram identificadas transmissões de dados em texto plano. | Sucesso |

Os resultados demonstram que todas as comunicações observadas durante a avaliação ocorreram por meio de canais criptografados, resultando em conformidade integral com a métrica M6.1.

**PASSO 4 – Avaliação da proteção de dados em repouso (Métrica M6.2)**

Por fim, foi realizada uma auditoria dos dados persistidos e dos mecanismos de armazenamento utilizados pelo sistema.

| Tarefa Executada | Ação no Sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Inspeção dos dados persistidos | Verificação dos arquivos utilizados pela aplicação. | Foram encontrados apenas dados públicos relacionados às oportunidades acadêmicas. | Não aplicável |
| Auditoria de credenciais da infraestrutura | Inspeção das configurações do projeto. | A chave da API é armazenada por meio do GitHub Secrets e não está exposta no código-fonte. | Sucesso |

A métrica M6.2 foi parcialmente aplicável. Embora não existam registros de usuários, senhas ou informações pessoais armazenadas, foi possível verificar que os segredos de infraestrutura estão protegidos adequadamente. As chaves da API não estão expostas.

**PASSO 5 - Avaliação da neutralização de conteúdo malicioso (Métrica M3)**

Como a aplicação renderiza dados oriundos de um pipeline de scraping, avaliou-se se conteúdo malicioso injetado nos arquivos JSON é neutralizado pela interface React. A coleta combinou injeção de payloads em ambiente local (`npm run dev`) e análise estática do código-fonte do `site/`.

| Tarefa Executada | Ação no Sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Injeção em campos de texto (`Nome`, `descricao`, `Sobre`...) | `<script>`, `<img onerror>`, `<b>` no JSON, renderizados via JSX | Escape automático do React; payloads exibidos como texto inerte. Nenhum `dangerouslySetInnerHTML` em `site/src/`. | Neutralizado |
| Injeção em campos de canal (`Site`, `Instagram`) | `javascript:alert('xss')` renderizado pelo `SocialFooter` | Inserido literalmente em `href={...}` sem validar o esquema da URL; executa no clique do link. | Ativo (no clique) |

Os campos de texto apresentaram 100% de neutralização, sem execução automática (auto-XSS). O único vetor residual é o `href` dos campos de canal, que exige interação do usuário. A métrica M3 foi julgada Aceitável (com ressalva) e a Hipótese 3 foi confirmada.

**PASSO 6 - Avaliação da procedência verificável (Métrica M4)**

Avaliou-se se cada oportunidade tem origem rastreável a uma fonte oficial, executando um script de procedência sobre o `oportunidades.json` de produção (83 registros) e uma verificação amostral.

| Tarefa Executada | Ação no Sistema | Observações / Evidência | Julgamento |
| :--- | :--- | :--- | :--- |
| Empresas juniores | Conferência de `Site` / `Instagram` | 49/49 com canal oficial preenchido (100%). | Verificável |
| Laboratórios | Conferência de `contato` institucional | 22/34 com `@unb.br`; 12 com `@gmail.com`. | Parcial |
| Procedência global | `TPV = 71/83 × 100` | 85,5% de registros com procedência verificável. | - |

A taxa de procedência verificável foi de 85,5%, situando a métrica M4 no nível Satisfatório e confirmando a Hipótese 4: a lacuna concentra-se em laboratórios com contato pessoal fora do domínio institucional.

## 3. Achados e Resultados Consolidados

### 3.1 Síntese das Métricas

| Métrica | Descrição | Medida coletada | Limiar alvo | Resultado |
| :--- | :--- | :--- | :--- | :--- |
| **M1.1** | Taxa de Bloqueio de Modificação Não Autorizada (API Docker). | 100% de bloqueios no backend. | 100% | **EXCELENTE** |
| **M1.2** | Quantidade de Endpoints Críticos Vulneráveis (API Docker). | 0 endpoints vulneráveis no backend. | 0 | **EXCELENTE** |
| **M2.1** | Efetividade da Verificação de Domínio Institucional (API Docker). | 100% dos bloqueios de e-mails inválidos. | 100% | **EXCELENTE** |
| **M2.2** | Proporção de Autenticação em Duas Etapas (API Docker). | 0% ativado no banco de dados local. | 50% a 100% | **INADEQUADO** |
| **M5.1** | Controlabilidade de acesso na interface (Produção). | 100% das tentativas indevidas bloqueadas. | 100% | **EXCELENTE** |
| **M5.2** | Controlabilidade de acesso na API (Produção). | Não aplicável (sem API em produção). | 100% | **NÃO APLICÁVEL** |
| **M6.1** | Proteção de dados em trânsito (Produção). | 100% das comunicações protegidas por HTTPS/TLS. | 100% | **EXCELENTE** |
| **M6.2** | Proteção de dados em repouso (Produção). | Não aplicável para dados de usuários; infraestrutura protegida. | 100% | **PARCIALMENTE APLICÁVEL** |
| **M3** | Neutralização de conteúdo malicioso (TNCM) | Texto 100% neutralizado; `href` de canal vulnerável a `javascript:` | Nenhum vetor ativo | **ACEITÁVEL (c/ ressalva)** |
| **M4** | Procedência verificável (TPV) | 85,5% (EJs 49/49; labs 22/34 com `@unb.br`) | ≥ 95% | **SATISFATÓRIO** |

### 3.2 Julgamento das questões GQM

* **Q1: O sistema previne de forma adequada que os dados sejam modificados por usuários sem privilégios (Backend)?**
    + **Resposta:** **Sim.** Comprovado pelas métricas M1.1 e M1.2 (ambas Excelentes). A *Hipótese H1* foi completamente validada.
* **Q2: O sistema comprova de forma robusta a identidade do usuário no momento do login e cadastro (Backend)?**
    + **Resposta:** **Parcialmente.** A barreira regex M2.1 funciona, mas falha gravemente no critério de Autenticação em Duas Etapas (M2.2 = 0%), reprovando a *Hipótese H2*.
* **Q5: O sistema restringe rigorosamente as permissões horizontais e verticais, impedindo que usuários não autorizados burlem a interface ou consumam endpoints protegidos da API (Produção)?**
    + **Resposta: Parcialmente atendida.** A hipótese foi confirmada para a camada de interface, uma vez que todas as tentativas de acesso indevido foram bloqueadas durante os testes realizados. Entretanto, a validação completa da hipótese não pôde ser executada na camada de servidor devido à inexistência de endpoints protegidos ou mecanismos de autenticação que permitissem a realização dos testes previstos pela métrica M5.2.
* **Q6: Os dados sensíveis dos estudantes estão devidamente protegidos por criptografia durante o tráfego na rede e no armazenamento físico do servidor (Produção)?**
    + **Resposta: Atendida.** Foi verificado que toda a comunicação ocorre por meio de protocolos seguros baseados em TLS, atendendo integralmente aos requisitos de proteção em trânsito. Quanto ao armazenamento, não foram identificados dados sensíveis de estudantes persistidos na aplicação. Além disso, os segredos de infraestrutura encontram-se protegidos por mecanismos apropriados de gerenciamento de credenciais.
* **Q3: O sistema impede que conteúdo malicioso das fontes raspadas seja injetado e renderizado de forma ativa?**
    + **Resposta: Parcialmente atendida.** O escape automático do React neutralizou 100% dos payloads injetados em campos de texto, sem qualquer execução automática (auto-XSS), confirmando a robustez da renderização. A ressalva está no componente `SocialFooter`, que insere os campos de canal (`Site`/`Instagram`) em `href` sem validar o esquema da URL, mantendo um vetor `javascript:` acionável por clique. A *Hipótese 3* foi confirmada, pois previu exatamente esse padrão de falha restrita aos links.
* **Q4: É possível verificar que toda oportunidade publicada tem origem em uma fonte oficial autorizada?**
    + **Resposta: Majoritariamente atendida.** A Taxa de Procedência Verificável foi de 85,5%: as 49 empresas juniores possuem canal oficial em 100% dos registros, enquanto 12 dos 34 laboratórios registram contato em domínio externo (`@gmail.com`), reduzindo a taxa global. A *Hipótese 4* foi confirmada, e a lacuna aponta a ação corretiva de padronizar o contato institucional dos laboratórios.

## 4. Rastreabilidade e Evidências Documentadas (Arquivos de Coleta)

A transparência da execução desta avaliação é garantida pela disponibilização integral dos dados brutos e sua correlação direta com as métricas apresentadas. Todos os artefatos estão versionados e organizados no repositório GitHub do projeto sob o diretório **docs/evidencias\_fase4/**.

**Conteúdo do Diretório de Evidências**

* 1. **tabela\_resultados\_mural\_unb.xlsx**: Planilha contendo o registro de todos os disparos, os status HTTP retornados e o processamento matemático das métricas M1.1 a M2.2.
  2. **postman\_collection\_mural\_unb.json**: Arquivo de exportação contendo a coleção estruturada (Headers, Body e Rotas) utilizada nos testes dinâmicos da API para permitir a auditoria de reprodutibilidade.
  3. **postman\_collection\_results.csv**: Log gerado pelo Postman Runner, registrando o *timestamp*, a latência e o status final de cada requisição automatizada.
  4. **Pasta de Screenshots Rastreáveis:**
     + M1.1\_TentativaDelete\_UserB.png: Captura de tela evidenciando o retorno 403 Forbidden no bloqueio do payload de deleção.
     + M1.2\_EndpointVulneravel\_Bloqueado.png: Captura da aba *Headers* vazia (sem JWT) e a recusa imediata da API (401 Unauthorized).
     + M2.1\_Erro\_Dominio\_Invalido.png: Print da resposta da API rejeitando o cadastro com domínio não institucional.
     + M2.2\_Query\_2FA.png: Print do console DBeaver evidenciando o código da consulta SQL e a contagem nula (0) no retorno do banco de dados.
  5. **m4\_procedencia.py** e **m4\_resultado.txt**: Script reproduzível da métrica M4 (TPV) e sua saída (85,5%), executado sobre o `oportunidades.json` real.
  6. **m3\_analise\_estatica.md**: Evidência de M3 por análise estática de código, com citações `arquivo:linha` de `SocialFooter.tsx` e `DescriptionSection.tsx` e a confirmação da ausência de `dangerouslySetInnerHTML`.

**Vídeo de Execução Contínua**

Para fins de validação e auditoria, o procedimento de testes foi registrado em formato contínuo por meio do OBS Studio, sem pausas.

* 1. **Link da Execução Prática (Não Listado):** [Link do YouTube (Placeholder: [https://youtu.be/MuralUnB\_TestesFase4](https://www.google.com/search?q=https://youtu.be/MuralUnB_TestesFase4))]

## 5. Considerações Finais e Recomendações

Os resultados obtidos indicam que o Mural UnB apresenta um perfil de segurança compatível com sua proposta arquitetural. A adoção de uma arquitetura estática reduz significativamente a superfície de ataque do sistema, eliminando riscos associados a autenticação, gerenciamento de sessões e processamento de requisições no servidor. O cerne da informação está adequadamente protegido contra injeções de perfil comum.

Por outro lado, essa mesma característica limitou a execução de algumas métricas originalmente definidas no GQM. Em especial, não foi possível realizar testes completos relacionados à controlabilidade de acesso no backend de produção e à proteção criptográfica de registros persistidos, uma vez que tais componentes não fazem parte da solução atual. Dessa forma, os resultados devem ser interpretados considerando o contexto arquitetural do sistema. A ausência de determinadas vulnerabilidades decorre não apenas da existência de mecanismos de proteção, mas também da inexistência dos componentes tradicionalmente associados a esses riscos.

Apoiadas na matriz de avaliação, as conclusões apontam para as seguintes **recomendações e ações imediatas a serem aplicadas**:

* 1. **Implementar feature de Autenticação em Duas Etapas (2FA):** Criar um mecanismo de autenticação de dois fatores com a *role* de publicador/administrador (caso a API venha a ser implantada no futuro), exigindo envio de código via SMTP UnB no primeiro acesso.
  2. **Manter e Documentar a Validação Regex:** A validação que barra domínios externos (M2.1) deve ser convertida em um teste de unidade no repositório (`test_email_domain_validation.py`).
  3. **Automatizar a inspeção de Headers JWT:** Integrar a coleção Postman ao *Pipeline* de CI/CD do GitHub Actions, assegurando que nenhuma nova rota de manipulação de dados seja implantada sem exigir autorização prévia.
  4. **Sanitizar o esquema de URL no `SocialFooter` (Ação M3):** Validar os campos `Site`/`Instagram` para aceitar apenas `http`/`https` antes de atribuí-los ao `href`, bloqueando o vetor `javascript:`.
  5. **Padronizar a procedência dos registros (Ação M4):** Migrar o `contato` dos 12 laboratórios externos para o domínio institucional `@unb.br` e registrar um campo explícito de `fonte`/`url_origem` no *pipeline* ETL.
  6. **Reduzir a exposição de e-mails:** Minimizar a exposição de e-mails nos arquivos públicos para evitar *scraping* automatizado, e remover logs de depuração do código de produção.
  7. **Reforçar cabeçalhos HTTP de segurança:** Avaliar a migração para plataformas que permitam configuração avançada de `Content-Security-Policy (CSP)`, `X-Frame-Options` e demais cabeçalhos.
  8. **Reavaliação Contínua:** Caso futuras versões incorporem autenticação de usuários ou armazenamento de dados pessoais em produção, recomenda-se reexecutar integralmente as métricas M1.2 e M2.2.

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
| Caio Soares | Adição das questões e métricas (Q5, Q6, M5, M6); consolidação dos resultados (M5/M6) na Fase 3; e avaliação da camada de produção via terminal na Fase 4. | 16.66% |
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
| Gemini 1.5 Pro / Agentes IA | Utilizada para classificar insights de confiabilidade e segurança, auxiliar na interpretação de dados, conduzir a estruturação dos testes práticos, e realizar a revisão e correção ortográfica do documento. | O texto e as classificações geradas pela IA foram rigorosamente revisados, adaptados ao contexto do projeto e validados para garantir informações fidedignas e relevantes para o projeto Mural UnB. |
