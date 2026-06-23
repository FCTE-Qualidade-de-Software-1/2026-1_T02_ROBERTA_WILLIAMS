# 2. Nível Operacional: Questões e Hipóteses

As questões investigam aspectos reais da aplicação, e suas respectivas hipóteses foram estabelecidas para facilitar a interpretação dos resultados (comportamento esperado), permitindo avaliação binária e inequívoca.

## 2.1. Confiabilidade (Disponibilidade, Recuperabilidade, Tolerância)

* **Q1:** O frontend hospedado no GitHub Pages gerencia interrupções no carregamento dos dados JSON sem causar falha fatal (tela branca)?
    * **H1:** O GitHub Pages garantirá uptime superior a 99%, e a aplicação React possui componentes nativos que previnem a quebra do DOM em falhas assíncronas.

* **Q2:** O sistema mantém operação estável e acessível sob picos de acesso de estudantes da UnB?
    * **H2:** A infraestrutura suportará a carga de acessos simultâneos, com taxa de sucesso de requisições próxima a 100%.

* **Q3:** O pipeline ETL protege os arquivos JSON em produção contra corrupção em caso de erro nos scripts?
    * **H3:** O pipeline interromperá a execução de workflows em caso de erro no script, prevenindo a sobrescrita nula dos dados e garantindo integridade.

* **Q4:** O sistema restaura suas funções e consistência automaticamente após falhas no serviço?
    * **H4:** Em caso de quebra de workflow, o sistema preserva os dados legados, e o tempo médio de recuperação (MTTR) será inferior a 24 horas.

* **Q5:** Qual é a eficácia do pipeline em tratar falhas críticas segundo a suíte de testes existente?
    * **H5:** A suíte de testes existente cobre e previne as falhas críticas conhecidas, garantindo que o pipeline funcione adequadamente. (Nota: O framing da hipótese foi corrigido para refletir o comportamento desejado, evitando a contradição de invalidar a hipótese quando os testes passam em 100%).

* **Q6:** O pipeline evidencia resiliência na esteira CI/CD do GitHub Actions?
    * **H6:** As Actions do GitHub refletem com precisão a cobertura de testes locais, evitando discrepâncias em produção.

## 2.2. Segurança (Integridade, Autenticidade, Confidencialidade)

* **Q7:** O sistema previne que registros sejam modificados por usuários sem privilégios?
    * **H7:** O sistema bloqueará 100% das tentativas de manipulação forjadas via validação rigorosa de tokens em todos os métodos de escrita.

* **Q8:** Há proteção em todos os endpoints de manipulação de dados contra requisições anônimas?
    * **H8:** O backend Docker exigirá JWT válido em 100% das rotas de edição de oportunidades.

* **Q9:** A renderização da aplicação neutraliza payloads maliciosos injetados pelo pipeline de scraping?
    * **H9:** O escape automático do React impedirá execuções automáticas (auto-XSS) em campos de texto e restringirá esquemas de URL nos campos de contato.

* **Q10:** O sistema garante a autenticidade institucional de publicadores (cadastro/login)?
    * **H10:** O sistema bloqueará cadastros que não utilizem o domínio oficial `@unb.br` ou `@aluno.unb.br`.

* **Q11:** O sistema valida rigorosamente a camada estática de produção contra evasão de rotas?
    * **H11:** A interface administrativa estática ocultará ou bloqueará 100% das rotas protegidas se acessadas sem autorização (retornando erro de bloqueio ou 404).

* **Q12:** Os dados trafegam e repousam protegidos por protocolos fortes?
    * **H12:** Toda a transferência ocorrerá via HTTPS forte e eventuais dados sensíveis (senhas) utilizarão funções de hash na persistência.