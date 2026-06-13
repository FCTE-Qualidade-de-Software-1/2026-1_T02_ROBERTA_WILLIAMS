# Fase 3

## Histórico de Versões

| Versão | Descrição                                                                                                                                                     | Autor  | Data       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------- |
| 1.0    | Criação inicial da Fase 3 com definição do método e ambiente de avaliação básico.                                                                             | Yogi   | 11/06/2026 |
| 1.1    | Inserção das métricas complementares de teste de carga (M1.2) e persistência pós-falha (M2.3).                                                                | Carlos | 11/06/2026 |
| 1.2    | Refinamento para os critérios de excelência: simplificação do texto, preenchimento do cronograma de avaliação e adição da seção de consistência com a Fase 2. | Yogi   | 12/06/2026 |

## Introdução

Nesta etapa do projeto, vamos especificar como iremos implementar e executar as métricas definidas na metodologia Goal-Question-Metric (GQM) da Fase 2 para avaliar objetivamente a Confiabilidade da arquitetura serverless do Mural UnB.
O processo de coleta e análise utilizará o próprio ambiente de hospedagem e automação do projeto (GitHub Pages e GitHub Actions) em conjunto com ferramentas externas de monitoramento e carga (como UptimeRobot e k6/Locust). A execução envolverá a aplicação de testes simulados de falha, incluindo a interrupção proposital do carregamento de arquivos JSON na interface React (via DevTools) e a injeção intencional de erros nos workflows do pipeline ETL, além da análise do histórico do repositório. O processo contará com capturas de tela e extração de logs do GitHub para evidenciar os cenários testados. Por fim, serão realizados os cálculos das fórmulas definidas anteriormente para analisar os dados gerados, garantindo a rastreabilidade e a reprodutibilidade dos resultados obtidos.

## 1. Metodologia

O método consiste na execução de testes controlados de injeção de falhas em ambiente clonado (_fork_), análise retroativa de logs e monitoramento externo sintético. O processo garante repetibilidade sem exigir conhecimento interno profundo do código do Mural UnB.

### Instruções Passo a Passo para o Avaliador

#### Coleta de M1.1 (Uptime do GitHub Pages)

1. Acesse a ferramenta de monitoramento UptimeRobot [https://dashboard.uptimerobot.com/monitors](https://dashboard.uptimerobot.com/monitors).
2. Clique em New para adicionar um monitoramento.
3. Insira o URL [https://muralunb.com.br/](https://muralunb.com.br/).
4. Anote o valor de porcentagem de uptime das últimas 24 horas, este é o resultado da métrica M1.1.

#### Coleta de M1.2 (Taxa de Sucesso de Requisições)

1. Iniciar o script de teste de carga (Locust) no terminal: `locust -f load_test.py --host=https://muralunb.com.br/ --users=500 --spawn-rate=10`
2. Disparar o script contra o servidor de produção ou endpoint JSON, mantendo a execução por 3 a 5 minutos de estresse contínuo.
3. Monitorar a taxa de sucesso das requisições via dashboard da ferramenta em tempo real.
4. Contabilizar respostas HTTP (200 OK vs 4xx/5xx) para aplicar na fórmula.

#### Coleta de M1.3 (Taxa de Resiliência da Interface Front-end)

1. Abra o site [https://muralunb.com.br/](https://muralunb.com.br/) no Chrome.
2. Aperte `F12` e clique na aba **Network** (Rede).
3. Na barra de opções da aba Network, marque a caixa **Disable cache** (Desativar cache) e clique no filtro **Fetch/XHR**.
4. **Recarregue a página (F5)** com o F12 aberto. Isso fará a lista de arquivos carregados aparecer.
5. Na coluna "Name", procure pelo arquivo de dados (geralmente com final `.json`, como `oportunidades.json`).
6. Clique com o **botão direito** no nome desse arquivo e selecione **Block request URL** (Bloquear URL da requisição). Uma gaveta inferior abrirá confirmando o bloqueio.
7. **Recarregue a página novamente (F5)**. A requisição do `.json` aparecerá em vermelho (status `(blocked:devtools)`).
8. Abra a localização onde os dados desse arquivo são renderizados. Como os dados do `oportunidades.json` aparece em [https://muralunb.com.br/feed](https://muralunb.com.br/feed), vá para essa página.
9. Olhe para a tela do site:
  * Tela totalmente em branca ou elementos sobrepostos/quebrados = Falha (0%).
  * Aviso legível informando que os dados não puderam ser carregados, mantendo o menu e o cabeçalho intactos = Sucesso (100%).
10. Para limpar o teste, vá na gaveta inferior "Network request blocking", clique com o botão direito no link bloqueado e escolha "Remove", ou desmarque a caixa "Enable network request blocking".

#### Coleta de M2.1 (Taxa de Integridade Pós-Falha do Pipeline)

1. Acesse o repositório clonado (*fork*) no GitHub.
2. Navegue até a pasta `scripts/`, abra o arquivo `extrair_empresas_juniores.py` e clique no ícone de lápis para editar.
3. Insira o código `import erro_proposital_teste` na primeira linha e faça o *commit* diretamente na *branch* principal (`main`).
4. Clique na aba **Actions**, selecione o *workflow* `1_ejs_extrair_dados.yml` que é o `Processar Empresas Juniores` na barra lateral e clique em **Run workflow** para iniciar a execução.
5. Aguarde a conclusão de todas as etapas do *job*, independentemente do status final indicado pelo GitHub Actions (verde ou vermelho).
6. Volte à aba **Code**, navegue até a pasta `data/EJs/` e abra o arquivo `empresas_juniores_consolidadas.json`.
7. Inspecione o conteúdo do arquivo e determine o resultado da métrica:
* **Sucesso (100%):** O pipeline foi interrompido antes de realizar alterações destrutivas. Os dados antigos foram integralmente preservados no repositório.
* **Falha (0%):** O erro foi ignorado ou causou um efeito colateral que sobrescreveu o arquivo anterior, deixando-o vazio, corrompido ou apenas com dados parciais/inválidos.

#### Coleta de M2.2 (Tempo Médio de Recuperação - MTTR)

1. Acesse o repositório Mural UnB no GitHub e abra o separador **Actions**.
2. No campo "Filter workflow runs", escreva `is:failure` para listar apenas as execuções que falharam.
3. Identifique uma falha ocorrida nos últimos 3 meses. Anote a data e hora exata do erro.
4. Volte à lista, remova o filtro `is:failure` e localize a primeira execução bem-sucedida (ícone verde) do mesmo *workflow* ocorrida *após* a falha identificada.
5. Se encontrar a execução de sucesso: Anote a data e hora exata, e subtraia a data/hora da falha da data/hora do sucesso para obter o tempo de recuperação (em horas).
6. Se não encontrar uma execução de sucesso (falha não corrigida): registre o tempo como incalculável e classifique a métrica diretamente como Inadequado (> 48h).
7. Repita os passos 3 a 6 para todas as falhas registadas no período de 3 meses.
8. Some todos os tempos de recuperação válidos e divida pelo número total de quebras corrigidas para obter o MTTR.

#### Coleta de M2.3 (Taxa de Persistência Pós-Falha)

1. Na estrutura do _fork_, criar a pasta `tests/mocks/` contendo `/validos/` (dados reais) e `/corrompidos/` (arquivos JSON com sintaxe malformada ou valores nulos).
2. Contar o número de registros íntegros no arquivo oficial.
3. Executar o workflow via GitHub Actions forçando a leitura dos arquivos da pasta `/corrompidos/`.
4. Observar a reação do script Python e verificar se o sistema interrompe a gravação antes de corromper o arquivo principal.
5. Analisar o arquivo .json resultante para verificar a preservação e aplicar na fórmula.

## 2. Especificação dos Recursos e do Ambiente de Avaliação

- **Sistema Operacional:** Fedora Linux 42.
- **Ambiente de Hospedagem:** Servidor de Domínio Próprio ([https://muralunb.com.br/](https://muralunb.com.br/)).
- **Requisitos de Hardware:** CPU de 4 núcleos, 20 GB de memória RAM, Armazenamento NVMe.
- **Requisitos de Software:** Navegador web atualizado (Google Chrome ou Mozilla Firefox) com ferramentas de desenvolvedor nativas (DevTools); conta configurada no UptimeRobot; ambiente Python local com as dependências do repositório (Locust); fork do repositório no GitHub.
- **Massa de Dados:** O teste exige a presença de um conjunto de dados em formato `.json` (base estruturada real) e arquivos `.json` corrompidos alocados em `tests/mocks/`. Essa massa é explicitamente justificada e crítica para agilizar a validação visual do frontend (M1.3) e atestar a persistência do pipeline sem destruir os dados da produção (M2.1 e M2.3).
- **Perfil do Avaliador:** Usuário com conhecimento básico em informática, capacidade de navegação web/DevTools e operação básica de repositórios (GitHub) e terminal.

## 3. Cronograma de Avaliação

| Atividade                                                                   | Responsável | Início | Término | Alinhamento com a Fase 4                                             |
| --------------------------------------------------------------------------- | ----------- | ------ | ------- | -------------------------------------------------------------------- |
| Setup e ativação do UptimeRobot para o Mural UnB                            | -           | -      | -       | Início do monitoramento contínuo para extração da métrica M1.1.      |
| Execução da ferramenta de carga (Locust) contra a API                       | -           | -      | -       | Coleta da taxa de requisições e estabilidade sob pressão (M1.2).     |
| Execução dos testes de resiliência e simulações de rede offline             | -           | -      | -       | Coleta prática dos dados de comportamento da interface (M1.3).       |
| Injeção de erros no script e processamento da pasta de arquivos corrompidos | -           | -      | -       | Obtenção dos resultados de integridade e persistência (M2.1 e M2.3). |
| Auditoria e varredura do histórico de execuções do Actions                  | -           | -      | -       | Coleta retroativa de dados de tempo para cálculo do MTTR (M2.2).     |
| Consolidação, cálculo das fórmulas e julgamento final                       | -           | -      | -       | Cruzamento dos dados com os níveis de pontuação definidos na Fase 2. |

## 4. Consistência com a Fase 2

Este Plano de Avaliação mantém rastreabilidade e coerência estrita com o modelo GQM definido na Fase 2. A escolha de ferramentas externas (UptimeRobot, Locust) foi especificada para extrair exatamente os dados necessários para o cálculo das métricas de Disponibilidade (M1.1, M1.2 e M1.3). Da mesma forma, o isolamento do ambiente via _fork_ e a exigência da massa de dados corrompidos garantem a repetibilidade das métricas de Recuperabilidade (M2.1, M2.2 e M2.3) estipuladas nos níveis de julgamento, sem risco de corromper o banco de dados da produção original.

## 5. Declaração de Uso de IA

**Tabela: Declaração Formal de Uso de IA**

| Ferramenta          | Tarefa Realizada                                                                                         | Conferência Humana                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Gemini 3.1 Pro** | Mesclagem de versões redundantes, formatação da tabela cronograma e checagem com consistência da fase 2. | A equipe orientou a simplificação do documento, validou as dicas dadas e aprovou as alterações estruturais. |
