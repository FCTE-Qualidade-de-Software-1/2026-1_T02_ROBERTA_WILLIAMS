# 1. Nível Conceitual: Objetivo de Medição (GQM)

O objetivo de medição orienta o foco da avaliação para a arquitetura serverless do Mural UnB (React no GitHub Pages e ETL no GitHub Actions).

Para eliminar as fragilidades de trilhas paralelas e garantir consistência na auditoria, os objetivos de medição foram unificados. Ambos seguem rigorosamente o template GQM, com foco explícito na arquitetura Serverless e estática do projeto Mural UnB, para garantir rastreabilidade, visando à avaliação definida na Fase 1.

| Elemento GQM | Definição no Contexto do Projeto |
| :---: | :---: |
| **Analisar** | O sistema Mural UnB (frontend estático e pipeline de extração de dados). |
| **Com o propósito de** | Avaliar e diagnosticar falhas arquiteturais e interrupções de fluxo. |
| **Em relação à** | **Confiabilidade** (Disponibilidade, Recuperabilidade e Tolerância a Falhas). |
| **Do ponto de vista** | Da equipe avaliadora externa e dos usuários finais (alunos). |
| **No contexto do** | Projeto da disciplina de Qualidade de Software 1 (FGA0315). |

*Tabela F2-1: Objetivo GQM — Confiabilidade*

| Elemento GQM | Definição no Contexto do Projeto |
| :---: | :---: |
| **Analisar** | O sistema web e o pipeline de dados do Mural UnB. |
| **Com o propósito de** | Avaliar e diagnosticar vulnerabilidades de controle de acesso, integridade de dados e proteção criptográfica. |
| **Em relação à** | **Segurança** (Integridade, Autenticidade e Confidencialidade). |
| **Do ponto de vista** | Da equipe avaliadora, administradores e entidades provedoras de oportunidades. |
| **No contexto do** | Projeto da disciplina de Qualidade de Software 1 (FGA0315). |

*Tabela F2-2: Objetivo GQM — Segurança*

**Objetivo da Confiabilidade:** Avaliar a confiabilidade do produto de software para diagnosticar a disponibilidade da interface web, a recuperabilidade do pipeline de dados e a tolerância a falhas ao realizar web crawling ou chamadas a serviços externos como a API do Gemini, do ponto de vista de avaliadores externos e usuários, no contexto de disciplina de Qualidade de Software 1.

**Objetivo da Segurança:** O propósito é avaliar a segurança do produto de software com a finalidade de analisá-la do ponto de vista do requisitante no contexto de proteção de dados e validação de identidade de usuários.