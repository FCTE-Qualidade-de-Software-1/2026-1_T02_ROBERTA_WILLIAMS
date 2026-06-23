# 5. Seleção de características de qualidade (SQuaRE)

Como visto acima, selecionamos Confiabilidade e Segurança.

## 5.1. Justificativa de priorização
A justificativa de priorização reside no fato de o Mural UnB lidar com avisos oficiais e horários.

A **Confiabilidade** é prioritária para garantir que o serviço não fique indisponível durante períodos críticos (como a matrícula, por exemplo), para garantir acesso ininterrupto via GitHub Pages.

A **Segurança** é essencial para evitar que usuários não autorizados alterem informações públicas, o quê causaria desinformação na comunidade acadêmica. Com efeito, é essencial para evitar que processos automatizados ou terceiros alterem arquivos JSON, o que causaria desinformação.

## 5.2. Classificação de subcaracterísticas (escala 1 a 5)

1.  **Confiabilidade (Reliability):**
    * Subcaracterísticas: Maturidade, Disponibilidade, Tolerância a Falhas, Recuperabilidade.
2.  **Segurança (Security):**
    * Subcaracterísticas: Confidencialidade, Integridade, Não-repúdio, Responsabilidade, Autenticidade.

### Confiabilidade (Reliability)
**Definição:** Mede o grau em que um sistema, componente ou processo executa funções específicas sob condições estabelecidas por um período de tempo determinado.

A Tabela F1-5 detalha a classificação da Subcaracterística Confiabilidade do modelo SQuaRE (ISO/IEC 25010):

| Subcaracterística | Ênfase (1-5) | Definição Breve | Justificativa Curta |
| :--- | :---: | :--- | :--- |
| **Disponibilidade** | 5 | Grau em que o sistema está operacional e acessível. | Vital para o site no GitHub Pages estar acessível. |
| **Maturidade** | 3 | Atendimento das necessidades de confiabilidade em operação normal. | Estabilidade a longo prazo dos scripts Python ETL. |
| **Tolerância a Falhas** | 4 | Capacidade de manter a operação pretendida mesmo com falhas de HW/SW. | Manter operação do site mesmo se imagens falharem. |
| **Recuperabilidade** | 4 | Capacidade de recuperar dados e o estado operacional após interrupção. | Persistência e restauração do pipeline CI/CD em caso de falha. |

*Tabela F1-5: Classificação e Justificativa da Subcaracterística Confiabilidade*

### Segurança (Security)
**Definição:** A segurança foca na proteção das informações e dados para garantir que apenas pessoas autorizadas acessem os dados.

A Tabela F1-6 especifica a classificação da Subcaracterística Segurança do modelo SQuaRE (ISO/IEC 25010):

| Subcaracterística | Ênfase (1-5) | Definição Breve | Justificativa Curta |
| :--- | :---: | :--- | :--- |
| **Integridade** | 5 | Prevenção de acesso ou modificação não autorizada de dados. | Impedir modificação não autorizada nos arquivos JSON estáticos. |
| **Autenticidade** | 5 | Identidade de um sujeito ou recurso pode ser provada como tal. | Garantir que apenas scripts via Actions autorizados gerem dados. |
| **Confidencialidade** | 3 | Garante que os dados sejam acessíveis apenas por quem tem autorização. | Baixa, dados de editais e laboratórios são públicos. |
| **Responsabilidade** | 4 | Ações de uma entidade podem ser rastreadas exclusivamente àquela entidade. | Rastreabilidade de commits via Git. |
| **Não-repúdio** | 3 | Prova de que um evento ou ação ocorreu, para que não seja negado posteriormente. | Validade de avisos oficiais. |

*Tabela F1-6: Classificação e Justificativa da Característica Segurança*

No tocante aos Níveis de Profundidade, as Subcaracterísticas com nível 5 exigirão testes de estresse (Disponibilidade) e testes de invasão/SQL Injection (Integridade). As de Níveis 3 e 4 envolverão apenas análise documental e revisões de código. Este método avalia dois eixos fundamentais, quais sejam, o de impacto, que é a magnitude das consequências negativas para o Mural UnB e seus usuários caso a subcaracterística falhe (exemplo: desinformação em massa) e o de risco (probabilidade), que é a chance de uma ameaça explorar uma vulnerabilidade do sistema, considerando o ambiente de uso e histórico de falhas.

## 5.3. Método de priorização
O método adotado é a Priorização Quantitativa Ponderada. Este método calcula a relevância de cada subcaracterística através da fórmula.

    Prioridade = Peso da Característica X (Impacto X Risco)

O peso define a importância estratégica da característica para o negócio (Confiabilidade = 10; Segurança = 9). Enquanto o impacto (0-5) avalia a gravidade da falha para o usuário final. E o risco (0-5) avalia a probabilidade de ocorrência de falhas ou vulnerabilidades no contexto atual do sistema. Essa abordagem permite um critério de Go/No-Go fundamentado, focando os esforços de teste nos pontos de maior risco sistêmico.

## 5.4. Matriz de priorização (ponderada)
A Tabela F1-7 destaca a priorização utilizada em uma escala de 0 a 5 para Impacto e Risco, multiplicada pelo peso da característica.

| Subcaracterística | Peso | Impacto | Risco | Total (P×I×R) | Prioridade |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Integridade** | 9 | 5 | 5 | 225 | Crítica |
| **Disponibilidade** | 10 | 5 | 4 | 200 | Alta |
| **Autenticidade** | 9 | 4 | 4 | 144 | Alta |
| **Recuperabilidade** | 10 | 3 | 3 | 90 | Média |
| **Confidencialidade** | 9 | 2 | 2 | 36 | Baixa |

*Tabela F1-7: Matriz de Priorização Ponderada*