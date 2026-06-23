# 4. Hierarquia GQM (Diagramas) e Tabela de Estrutura Hierárquica GQM

O fluxograma abaixo evidencia visualmente a coesão entre as métricas e atributos em uma única estrutura GQM. A seguir, estão as representações gráficas completas e equivalentes para as duas ramificações.

## Diagrama 1: Hierarquia GQM — Confiabilidade

```mermaid
graph TD

subgraph Nivel_Conceitual [Nível Conceitual]
  O_CONF[Objetivo: Avaliar Confiabilidade Serverless do Mural UnB]
end

subgraph Nivel_Operacional [Nível Operacional - Questões]
  Q1[Q1: Frontend gerencia erros JSON sem tela branca?]
  Q2[Q2: Sistema mantém estabilidade sob picos?]
  Q3[Q3: Pipeline ETL protege arquivos contra corrupção?]
  Q4[Q4: Sistema restaura dados após falhas?]
  Q5[Q5: Suíte de testes previne falhas críticas?]
  Q6[Q6: Actions CI/CD refletem segurança contra falhas?]
end

subgraph Nivel_Quantitativo [Nível Quantitativo - Métricas]
  M01[M01: Uptime Servidor]
  M02[M02: Taxa Sucesso Req]
  M03[M03: Resiliência Frontend]
  M04[M04: Integridade Pós-Falha]
  M05[M05: MTTR Pipeline]
  M06[M06: Persistência Dados]
  M07[M07: Prevenção Testes]
  M08[M08: Prevenção CI/CD]
end

O_CONF --> Q1
O_CONF --> Q2
O_CONF --> Q3
O_CONF --> Q4
O_CONF --> Q5
O_CONF --> Q6

Q1 --> M01
Q1 --> M03
Q2 --> M02
Q3 --> M04
Q4 --> M05
Q4 --> M06
Q5 --> M07
Q6 --> M08  
```
## Diagrama 2: Hierarquia GQM — Segurança

```mermaid
graph TD

subgraph Nivel_Conceitual [Nível Conceitual]
  O_SEG[Objetivo: Avaliar Segurança de Acesso e Integridade do Mural UnB]
end

subgraph Nivel_Operacional [Nível Operacional - Questões]
  Q7[Q7: Prevenção contra modificações sem privilégio?]
  Q8[Q8: Endpoints imunes a acessos anônimos?]
  Q9[Q9: Frontend neutraliza payloads no JSON?]
  Q10[Q10: Contas garantem domínio institucional @unb.br?]
  Q11[Q11: Interface em produção resiste a evasão de rotas?]
  Q12[Q12: Dados protegidos em trânsito e repouso?]
end

subgraph Nivel_Quantitativo [Nível Quantitativo - Métricas]
  M09[M09: TBM-NAut]
  M10[M10: QEC-V]
  M11[M11: TNCM]
  M12[M12: EVD-Inst]
  M13[M13: 2FA Ativo]
  M14[M14: TPV]
  M15[M15: Auditoria Interface]
  M16[M16: Pentest Endpoints]
  M17[M17: Criptografia Rede]
  M18[M18: Hash no Repouso]
end

O_SEG --> Q7
O_SEG --> Q8
O_SEG --> Q9
O_SEG --> Q10
O_SEG --> Q11
O_SEG --> Q12

Q7 --> M09
Q8 --> M10
Q9 --> M11
Q10 --> M12
Q10 --> M13
Q10 --> M14
Q11 --> M15
Q11 --> M16
Q12 --> M17
Q12 --> M18
```

## Tabela F2-3: Estrutura Hierárquica GQM

Para garantir a precisão da avaliação, utilizamos a abordagem GQM. A `Tabela F2-3` resume a estratégia estruturada tanto para Confiabilidade quanto para Segurança.

| Característica | Objetivo (Goal) | Questão (Question) | Métrica (Metric) |
| :---: | :---: | :---: | :---: |
| **Confiabilidade** | Maximizar a disponibilidade da SPA Jamstack. | Qual a taxa de sucesso do build e deploy via GitHub Pages? | Porcentagem de Actions executadas com sucesso vs. falhas. |
| **Confiabilidade** | Assegurar tolerância a falhas na busca. | O app quebra caso falte um vetor JSON? | Quantidade de exceções não tratadas no front-end ao carregar Oportunidades DB.json. |
| **Segurança** | Proteger a Integridade dos dados de oportunidades. | O pipeline ETL possui salvaguardas contra arquivos mal formatados? | Taxa de rejeição de arquivos PDF não padronizados no Data Handler. |
| **Segurança** | Garantir Autenticidade no controle do repositório. | Apenas mantenedores aprovados podem alterar os JSONs em main? | Quantidade de regras de proteção de branch (branch protections) ativadas no repositório. |

*Tabela F2-3: Estrutura Hierárquica GQM*