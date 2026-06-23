## 5. Níveis de Pontuação e Critérios de Julgamento

A `Tabela F2-4` abaixo mapeia os resultados quantitativos obtidos pelas métricas unificadas em julgamentos qualitativos (Inadequado, Satisfatório e Excelente), resolvendo a inconsistência de limiares não pré-acordados. Ademais, estabelece limites explícitos e consistentes para as 18 métricas unificadas, garantindo interpretação rigorosa na Fase 3.

| Métrica | Inadequado | Aceitável / Satisfatório | Excelente | Justificativa / Ação Recomendada |
| :---: | :---: | :---: | :---: | :---: |
| **M01** (Uptime) | < 95% | 95% - 98,9% | **≥ 99%** | Padrão GitHub Pages. Ação: Avaliar CDN se inadequado. |
| **M02** (Sucesso) | < 98% | 98% - 99,9% | **100%** | Perda de tráfego de arquivos estáticos indica gargalo. |
| **M03** (Resiliência DOM) | < 100% | Não aplicável | **100%** | Tela branca é erro fatal. Ação: Inserir Error Boundaries no React. |
| **M04** (Integridade) | < 100% | Não aplicável | **100%** | Prevenção de perda de dados. Ação: Remover `continue-on-error` no GitHub Actions. |
| **M05** (MTTR) | > 48h | 12h a 48h | **< 12h** | Agilidade na atualização de vagas. Ação: Configurar alertas. |
| **M06** (Persistência) | < 100% | Não aplicável | **100%** | Dados históricos não podem sumir. Ação: Rotina de backup do JSON. |
| **M07** (Testes pipeline) | < 90% | 90% a 95% | **> 95%** | Testes devem bloquear subidas instáveis de raspagem de dados. |
| **M08** (Actions pipeline) | < 100% | Não aplicável | **100%** | CI/CD deve replicar testes locais integralmente. |
| **M09** (TBM-NAut) | < 100% | Não aplicável | **100%** | Modificação por usuários comuns destrói a confiança. Ação: Corrigir middleware de autorização. |
| **M10** (QEC-V) | > 0 | N/A (Métrica binária) | **0 rotas expostas** | Todo endpoint do backend Docker requer JWT. |
| **M11** (TNCM Injeção) | Executa scripts em texto | Permite falha apenas no `href` | **100% Neutralizado** | Evitar auto-XSS. Ação: Sanitizar links no componente `SocialFooter`. |
| **M12** (EVD-Inst) | Aceita e-mail genérico | Não aplicável | **Bloqueio 100%** | Garante validade acadêmica. Ação: Filtro Regex para `@unb.br`. |
| **M13** (P-2FA) | 0% | 1% a 49% | **≥ 50%** | Ação: Forçar confirmação por e-mail no login admin. |
| **M14** (TPV Procedência) | < 80% | 80% a 94% | **≥ 95%** | Ação: Adicionar campo `url_origem` no banco de dados. |
| **M15** (Auditoria UI Admin) | Falha em bloquear rotas | Não aplicável | **100% bloqueados** | Rotas admin devem estar isoladas via state/localStorage validados. |
| **M16** (Pentest Exaustão) | < 100% efetividade | Não aplicável | **100% rejeição** | API não deve ceder a força bruta ou tokens inválidos. |
| **M17** (Cripto Rede) | Texto plano capturado | Cifras TLS fracas | **HTTPS Forte** | Ação: Configurar redirecionamento HTTP para HTTPS e HSTS. |
| **M18** (Cripto Repouso) | Senhas em texto plano | Segredos hardcoded | **100% com Hash forte** | Ação: Bcrypt nos dados e GitHub Secrets para chaves. |

*Tabela F2-4: Níveis de Pontuação e Critérios de Julgamento*