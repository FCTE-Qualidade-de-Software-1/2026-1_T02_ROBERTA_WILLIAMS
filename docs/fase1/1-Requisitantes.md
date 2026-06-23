# 1. Requisitante e Partes Interessadas

O Mural UnB` é uma plataforma digital de código aberto, desenvolvida por estudantes da Universidade de Brasília (UnB) no contexto da disciplina de Métodos de Desenvolvimento de Software (MDS) e mantida pela organização `unb-mds` no GitHub. Seu objetivo é centralizar e recomendar oportunidades acadêmicas e profissionais, tais como empresas juniores, laboratórios de pesquisa e equipes de competição, para os alunos da universidade. As demandas emergem da articulação entre diversos atores, descritos na Tabela F1-1, que relaciona suas necessidades com as características de confiabilidade e segurança.

| Papel / Stakeholder | Necessidades Principais | Influência na Avaliação |
| :--- | :--- | :--- |
| **Requisitante Principal: Equipe de Avaliação** | Aplicar conhecimentos da norma SQuaRE, produzir um diagnóstico fundamentado. | Direciona o escopo para Confiabilidade e Segurança e define a metodologia de priorização. |
| **Equipe de Desenvolvimento do Mural UnB** | Receber feedback técnico sobre vulnerabilidades e robustez da arquitetura estática (Jamstack). | Fornece os artefatos avaliáveis. Suas escolhas arquiteturais definem os limites de validação da avaliação. |
| **Usuários Finais (estudantes da UnB)** | Acesso estável e informação verídica sobre oportunidades acadêmicas. | Demandam Disponibilidade e Integridade (matriz de avaliação). |
| **Entidades Provedoras de Oportunidades (EJs, Labs)** | Garantia de que as informações sejam exibidas sem adulteração e alcancem o público-alvo. | Reforçam a importância da Autenticidade e da Integridade dos dados em JSON. |
| **Professores/Monitores de Qualidade de Software** | Avaliar a aplicação da metodologia SQuaRE. | Definem critérios de aceitação e validam a consistência da avaliação. |
| **Comunidade Open Source (GitHub)** | Código auditável, documentação clara para viabilizar a manutenção. | Reforça a relevância da Recuperabilidade e análise documental. |

*Tabela F1-1: Papéis, Necessidades e Influência na Avaliação*

Por se tratar de um projeto open source de natureza acadêmica, não existe um único requisitante que determine, de forma unilateral, as especificações do produto. As demandas emergem da articulação entre múltiplos atores: a equipe de desenvolvimento, a comunidade discente da UnB, as entidades estudantis que oferecem as oportunidades e, no contexto desta avaliação, a equipe acadêmica responsável pela análise de qualidade do software. O mapeamento a seguir relaciona as necessidades de cada parte interessada diretamente com as características priorizadas neste estudo, a `Confiabilidade` e a `Segurança`.

## Papéis e necessidades dos stakeholders
* **Equipe de Avaliação (requisitante principal - disciplina de Qualidade de Software):** Aplica a norma SQuaRE para produzir um diagnóstico de qualidade. Direciona o escopo para Confiabilidade e Segurança.
* **Equipe de Desenvolvimento do Mural UnB:** busca feedback técnico sobre vulnerabilidades e estabilidade do backend. Fornece os artefatos avaliáveis e é o principal consumidor dos resultados.
* **Usuários Finais (estudantes da UnB):** dependem de acesso estável e informação verídica em períodos críticos (matrícula, processos seletivos). Demandam Disponibilidade e Integridade.
* **Entidades Provedoras de Oportunidades (EJs, Laboratórios e Equipes de Competição da FCTE/UnB):** precisam que suas informações sejam exibidas sem adulteração. Reforçam Autenticidade e Integridade.
* **Professora e Monitores da disciplina:** avaliam a coerência metodológica do artefato. Definem os critérios de aceitação.
* **Comunidade Open Source (unb-mds e contribuidores no GitHub):** demandam código auditável e documentação clara para manutenção pós-ciclo letivo. Reforça `Recuperabilidade` e `Responsabilidade`.