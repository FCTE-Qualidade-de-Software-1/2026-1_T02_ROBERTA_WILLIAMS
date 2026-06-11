# Fase 3

## 1. Metodologia

O método consiste na execução de testes controlados de injeção de falhas em ambiente clonado (*fork*), análise retroativa de logs e monitoramento externo sintético. O processo garante repetibilidade sem exigir conhecimento interno profundo do código do Mural UnB.

### Instruções Passo a Passo para o Avaliador

#### Coleta de M1.1 (Uptime do GitHub Pages)

1. Acesse a ferramenta de monitoramento configurada (UptimeRobot).
2. Defina o filtro de visualização para as últimas 24 horas.
3. Extraia o percentual de tempo em que o servidor respondeu com status HTTP 200.
4. Aplique o valor diretamente na fórmula de M1.1.

#### Coleta de M1.2 (Taxa de Resiliência da Interface Front-end)

1. Abra o navegador Google Chrome e acesse a URL pública do painel do Mural UnB.
2. Pressione `F12` para abrir o *DevTools* e selecione a aba **Network** (Rede).
3. No campo de controle de banda (Throttling), altere de *No throttling* para **Offline**.
4. Recarregue a página (`F5`).
5. Observe o comportamento da interface: registre "Sucesso" se o React renderizou uma mensagem amigável de erro/carregamento falho; registre "Falha" se a tela apresentar um travamento completo (tela branca/quebra de DOM).
6. Repita o teste 5 vezes e aplique a fórmula de M1.2.

#### Coleta de M2.1 (Taxa de Integridade Pós-Falha do Pipeline)

1. Acesse o repositório *fork* do projeto no GitHub.
2. Navegue até o script Python responsável pelo processo de ETL.
3. Insira um erro de sintaxe intencional na primeira linha do arquivo (ex: `import erro_propositado`). Faça o commit diretamente na branch principal do *fork*.
4. Vá até a aba **Actions**, selecione o workflow correspondente (ex: `1_ejs_extrair_dados.yml`) e clique em **Run workflow** para forçar a execução.
5. Aguarde o pipeline falhar.
6. Acesse o diretório onde o arquivo JSON de produção fica armazenado. Verifique se o arquivo foi mantido intacto com os dados anteriores ou se foi limpo/corrompido. Registre o resultado para o cálculo da métrica.

#### Coleta de M2.2 (Tempo Médio de Recuperação - MTTR)

1. No repositório principal do GitHub, acesse a aba **Actions**.
2. Filtre o histórico pelas execuções que falharam nos últimos 3 meses.
3. Para cada falha encontrada: subtraia o carimbo de data/hora do primeiro disparo falho do carimbo de data/hora do commit que aplicou a correção definitiva.
4. Some todos os intervalos em horas e divida pelo número total de quebras para obter o MTTR.

---

## 2. Especificação dos Recursos e do Ambiente de Avaliação

* **Requisitos de Hardware:** Estação de trabalho com processador dual-core, mínimo de 4 GB de memória RAM e conexão estável com a internet.
* **Requisitos de Software:** Navegador web atualizado (Google Chrome ou Mozilla Firefox) com ferramentas de desenvolvedor nativas; conta ativa na plataforma GitHub.
* **Massa de Dados:** O teste exige a presença do arquivo JSON real populado com dados-exemplo de oportunidades da UnB. Essa massa é crítica para validar visualmente se a interface trata a ausência repentina de rede (M1.2) e se o pipeline impede a destruição de dados válidos pré-existentes (M2.1).
* **Perfil do Avaliador:** Usuário com conhecimento básico em informática, capacidade de navegação em sistemas web e operação básica de interfaces de repositórios (GitHub).

---

## 3. Cronograma de Avaliação

| Atividade | Responsável | Início | Término | Alinhamento com a Fase 4 |
| --- | --- | --- | --- | --- |
| Setup e ativação do UptimeRobot para o Mural UnB | - | - | - | Início do monitoramento contínuo para extração da métrica M1.1. |
| Execução dos testes de resiliência e simulações de rede offline | - | - | - | Coleta prática dos dados de comportamento da interface (M1.2). |
| Injeção de erros no script Python e checagem do estado do JSON | - | - | - | Obtenção dos resultados de integridade do pipeline pós-falha (M2.1). |
| Auditoria e varredura do histórico de execuções do Actions | - | - | - | Coleta retroativa de dados de tempo para cálculo do MTTR (M2.2). |
| Consolidação, cálculo das fórmulas e julgamento final | - | - | - | Cruzamento dos dados com os níveis de pontuação definidos na Fase 2. |

---