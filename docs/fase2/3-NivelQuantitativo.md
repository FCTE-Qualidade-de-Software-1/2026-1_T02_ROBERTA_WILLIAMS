
# 3. Nível Quantitativo: Seleção de Métricas

Para sanar a colisão de identificadores, as métricas foram unificadas em uma sequência numérica contínua (`M01 a M18`), agrupadas por característica. Fórmulas e procedimentos foram padronizados para garantir aplicabilidade e precisão.

## Métricas de Confiabilidade

* **M01 — Uptime do Servidor (GitHub Pages):**
  * Fórmula: `(Horas sem erros HTTP 4xx ou 5xx / Total de horas monitoradas) * 100`

* **M02 — Taxa de Sucesso de Requisições:**
  * Fórmula: `(Requisições HTTP 2xx bem-sucedidas / Total de requisições enviadas sob carga) * 100`

* **M03 — Taxa de Resiliência do Front-end:**
  * Fórmula: `(Simulações sem quebra catastrófica de DOM / Total de simulações de rede falha) * 100`

* **M04 — Taxa de Integridade Pós-Falha do Pipeline:**
  * Fórmula: `(Workflows abortados sem sobrescrever JSON / Total de falhas injetadas) * 100`

* **M05 — Tempo Médio de Recuperação (MTTR):**
  * Fórmula: `Soma total de horas para correção / Total de workflows quebrados no histórico`

* **M06 — Taxa de Persistência de Dados:**
  * Fórmula: `(Total de registros íntegros após recuperação / Total de registros antes da falha) * 100`

* **M07 — Taxa de Prevenção em Testes:**
  * Fórmula: `(Falhas evitadas na suíte de testes / Casos de teste de padrão de falha executados) * 100`

* **M08 — Taxa de Prevenção no CI/CD:**
  * Fórmula: `(Workflows executados com sucesso perante falha / Total de execuções com falha forçada) * 100`

## Métricas de Segurança

* **M09 — Taxa de Bloqueio de Modificação Não Autorizada (TBM-NAut):**
  * Fórmula: `(Tentativas de modificação indevida bloqueadas / Total de tentativas) * 100`

* **M10 — Quantidade de Endpoints Vulneráveis (QEC-V):** (Substitui "Pen-test em Endpoints" para padronização)
  * Fórmula: `Contagem absoluta de rotas do backend (Docker) que permitem escrita sem JWT.`

* **M11 — Taxa de Neutralização de Conteúdo Malicioso (TNCM):**
  * Fórmula: `(Payloads neutralizados na renderização / Total de payloads injetados no JSON de teste) * 100`

* **M12 — Efetividade da Verificação Institucional (EVD-Inst):**
  * Fórmula: `(Cadastros não institucionais bloqueados / Total de tentativas com e-mail comum) * 100`

* **M13 — Proporção de Autenticação 2FA:**
  * Fórmula: `(Contas admin com 2FA ativa / Total de contas admin) * 100`

* **M14 — Taxa de Procedência Verificável (TPV):**
  * Fórmula: `(Registros com fonte ou contato oficial validado / Total de registros) * 100`

* **M15 — Auditoria de Acesso na Interface Administrativa:**
  * Fórmula: `(Tentativas de burla de rota bloqueadas / Total de tentativas de evasão) * 100`

* **M16 — Teste de Penetração em Endpoints Privados:** (Específico para injeções forjadas via rede)
  * Fórmula: `(Ataques de exaustão de token rejeitados / Total de ataques direcionados) * 100`

* **M17 — Verificação de Criptografia em Trânsito:**
  * Fórmula: `Validação binária da presença e obrigatoriedade de HTTPS/TLS nas requisições.`

* **M18 — Proteção de Dados em Repouso:**
  * Fórmula: `(Campos críticos em banco de dados armazenados com hash / Total de campos críticos avaliados) * 100`