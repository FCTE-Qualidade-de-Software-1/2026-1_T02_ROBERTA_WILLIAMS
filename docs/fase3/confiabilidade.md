# Fase 3

## Introdução

Nesta etapa do projeto, vamos especificar como iremos implementar e executar as métricas definidas na metodologia Goal-Question-Metric (GQM) da Fase 2 para avaliar objetivamente a Confiabilidade da arquitetura serverless do Mural UnB.
O processo de coleta e análise utilizará o próprio ambiente de hospedagem e automação do projeto (GitHub Pages e GitHub Actions) em conjunto com ferramentas externas de monitoramento e carga (como UptimeRobot e k6/Locust). A execução envolverá a aplicação de testes simulados de falha, incluindo a interrupção proposital do carregamento de arquivos JSON na interface React (via DevTools) e a injeção intencional de erros nos workflows do pipeline ETL, além da análise do histórico do repositório. O processo contará com capturas de tela e extração de logs do GitHub para evidenciar os cenários testados. Por fim, serão realizados os cálculos das fórmulas definidas anteriormente para analisar os dados gerados, garantindo a rastreabilidade e a reprodutibilidade dos resultados obtidos.

## 1. Metodologia

O método consiste na execução de testes controlados de injeção de falhas em ambiente clonado (_fork_), análise retroativa de logs e monitoramento externo sintético. O processo garante repetibilidade sem exigir conhecimento interno profundo do código do Mural UnB.

### Instruções Passo a Passo para o Avaliador

#### Coleta de M1.1 (Uptime do GitHub Pages)

1. Acesse a ferramenta de monitoramento configurada (UptimeRobot).
2. Defina o filtro de visualização para as últimas 24 horas.
3. Extraia o percentual de tempo em que o servidor respondeu com status HTTP 200.
4. Aplique o valor diretamente na fórmula de M1.1.

#### Coleta de M1.2 (Taxa de Sucesso de Requisições)

1. Iniciar o script de teste de carga (Locust) no terminal: `locust -f load_test.py --host=https://muralunb.com.br/ --users=500 --spawn-rate=10`
2. Disparar o script contra o servidor de produção ou endpoint JSON, mantendo a execução por 3 a 5 minutos de estresse contínuo.
3. Monitorar a taxa de sucesso das requisições via dashboard da ferramenta em tempo real.
4. Contabilizar respostas HTTP (200 OK vs 4xx/5xx) para aplicar na fórmula.

#### Coleta de M1.3 (Taxa de Resiliência da Interface Front-end)

1. Abra o navegador Google Chrome e acesse a URL pública do painel do Mural UnB.
2. Pressione `F12` para abrir o _DevTools_ e selecione a aba **Network** (Rede).
3. No campo de controle de banda (Throttling), altere de _No throttling_ para **Offline**.
4. Recarregue a página (`F5`).
5. Observe o comportamento da interface: registre "Sucesso" se o React renderizou uma mensagem amigável de erro/carregamento falho; registre "Falha" se a tela apresentar um travamento completo (tela branca/quebra de DOM).
6. Repita o teste 5 vezes e aplique a fórmula de M1.3.

#### Coleta de M2.1 (Taxa de Integridade Pós-Falha do Pipeline)

1. Acesse o repositório _fork_ do projeto no GitHub.
2. Navegue até o script Python responsável pelo processo de ETL.
3. Insira um erro de sintaxe intencional na primeira linha do arquivo (ex: `import erro_propositado`). Faça o commit diretamente na branch principal do _fork_.
4. Vá até a aba **Actions**, selecione o workflow correspondente (ex: `1_ejs_extrair_dados.yml`) e clique em **Run workflow** para forçar a execução.
5. Aguarde o pipeline falhar.
6. Acesse o diretório onde o arquivo JSON de produção fica armazenado. Verifique se o arquivo foi mantido intacto com os dados anteriores ou se foi limpo/corrompido. Registre o resultado para o cálculo.

#### Coleta de M2.2 (Tempo Médio de Recuperação - MTTR)

1. No repositório principal do GitHub, acesse a aba **Actions**.
2. Filtre o histórico pelas execuções que falharam nos últimos 3 meses.
3. Para cada falha encontrada: subtraia o carimbo de data/hora do primeiro disparo falho do carimbo de data/hora do commit que aplicou a correção definitiva.
4. Some todos os intervalos em horas e divida pelo número total de quebras para obter o MTTR.

#### Coleta de M2.3 (Taxa de Persistência Pós-Falha)

1. Na estrutura do _fork_, criar a pasta `tests/mocks/` contendo `/validos/` (dados reais) e `/corrompidos/` (arquivos JSON com sintaxe malformada ou valores nulos).
2. Contar o número de registros íntegros no arquivo oficial.
3. Executar o workflow via GitHub Actions forçando a leitura dos arquivos da pasta `/corrompidos/`.
4. Observar a reação do script Python e verificar se o sistema interrompe a gravação antes de corromper o arquivo principal.
5. Analisar o arquivo .json resultante para verificar a preservação e aplicar na fórmula.

---

## 2. Especificação dos Recursos e do Ambiente de Avaliação

- **Sistema Operacional:** Fedora Linux 42.
- **Ambiente de Hospedagem:** Servidor de Domínio Próprio ([https://muralunb.com.br/](https://muralunb.com.br/)).
- **Requisitos de Hardware:** CPU de 4 núcleos, 20 GB de memória RAM, Armazenamento NVMe.
- **Requisitos de Software:** Navegador web atualizado (Google Chrome ou Mozilla Firefox) com ferramentas de desenvolvedor nativas (DevTools); conta configurada no UptimeRobot; ambiente Python local com as dependências do repositório (Locust); fork do repositório no GitHub.
- **Massa de Dados:** O teste exige a presença de um conjunto de dados em formato `.json` (base estruturada real) e arquivos `.json` corrompidos alocados em `tests/mocks/`. Essa massa é explicitamente justificada e crítica para agilizar a validação visual do frontend (M1.3) e atestar a persistência do pipeline sem destruir os dados da produção (M2.1 e M2.3).
- **Perfil do Avaliador:** Usuário com conhecimento básico em informática, capacidade de navegação web/DevTools e operação básica de repositórios (GitHub) e terminal.

---

## 3. Cronograma de Avaliação

| Atividade                                                                   | Responsável | Início | Término | Alinhamento com a Fase 4                                             |
| --------------------------------------------------------------------------- | ----------- | ------ | ------- | -------------------------------------------------------------------- |
| Setup e ativação do UptimeRobot para o Mural UnB                            | -           | -      | -       | Início do monitoramento contínuo para extração da métrica M1.1.      |
| Execução da ferramenta de carga (Locust) contra a API                       | -           | -      | -       | Coleta da taxa de requisições e estabilidade sob pressão (M1.2).     |
| Execução dos testes de resiliência e simulações de rede offline             | -           | -      | -       | Coleta prática dos dados de comportamento da interface (M1.3).       |
| Injeção de erros no script e processamento da pasta de arquivos corrompidos | -           | -      | -       | Obtenção dos resultados de integridade e persistência (M2.1 e M2.3). |
| Auditoria e varredura do histórico de execuções do Actions                  | -           | -      | -       | Coleta retroativa de dados de tempo para cálculo do MTTR (M2.2).     |
| Consolidação, cálculo das fórmulas e julgamento final                       | -           | -      | -       | Cruzamento dos dados com os níveis de pontuação definidos na Fase 2. |

---

## 4. Consistência com a Fase 2

Este Plano de Avaliação mantém rastreabilidade e coerência estrita com o modelo GQM definido na Fase 2. A escolha de ferramentas externas (UptimeRobot, Locust) foi especificada para extrair exatamente os dados necessários para o cálculo das métricas de Disponibilidade (M1.1, M1.2 e M1.3). Da mesma forma, o isolamento do ambiente via _fork_ e a exigência da massa de dados corrompidos garantem a repetibilidade das métricas de Recuperabilidade (M2.1, M2.2 e M2.3) estipuladas nos níveis de julgamento, sem risco de corromper o banco de dados da produção original.
