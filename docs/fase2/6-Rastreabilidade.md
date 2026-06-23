# 6. Rastreabilidade (Fases 1, 2 e 3)

Esta `Tabela F2-5` conecta os requisitos prioritários (Fase 1), as métricas propostas (Fase 2) e as ferramentas que serão utilizadas para a execução prática dos testes (Fase 3).

| Prioridade / Escopo (Fase 1) | Stakeholder | Subcaracterística | Métricas Associadas | Justificativa do Alinhamento |
| :---: | :---: | :---: | :---: | :---: |
| **Disponibilidade Geral** | Alunos | Disponibilidade | M01, M02, M03 | Assegura acesso fluido e interface sem quebras (Error Boundaries). |
| **Persistência ETL** | Administradores | Recuperabilidade | M04, M05, M06 | Garante que falhas no raspador Python não deletem oportunidades ativas no JSON de produção. |
| **Garantia de Pipeline** | Desenvolvedores | Tolerância a Falhas | M07, M08 | Previne atualizações corrompidas através da suíte de testes do CI/CD. |
| **Proteção de Dados** | Alunos e Admin | Integridade | M09, M10, M11 | Previne XSS via arquivos JSON inseridos e bloqueia acesso não autorizado na API. |
| **Autenticidade Institucional** | Reitoria / Alunos | Autenticidade | M12, M13, M14 | Comprova que as vagas vêm de laboratórios/EJs oficiais (filtros de domínio e 2FA). |
| **Controle e Sigilo em Produção** | Administradores | Confidencialidade | M15, M16, M17, M18 | Isola ambiente administrativo e utiliza protocolos TLS/Hashing para blindar a aplicação real na web. |

*Tabela F2-5: Rastreabilidade*