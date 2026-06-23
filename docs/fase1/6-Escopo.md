# 6. Escopo da Avaliação e Limites de Validade

**Delimitação do Escopo Arquitetural:** O Mural UnB não possui um backend ativo ou banco de dados transacional clássico. Ele opera estritamente sob uma `Arquitetura Jamstack (Serverless)`. O escopo da avaliação está restrito a:

1.  **Frontend / Sistema Online:** A aplicação React/TypeScript consumindo os arquivos estáticos (Tags DB.json, Oportunidades DB.json) hospedados no GitHub Pages.
2.  **Pipeline Offline (Ingestão):** O Workflow do GitHub Actions e os scripts em Python que processam e vetorizam os dados usando a API do Gemini.

**Limites de Validade:** A avaliação deve desconsiderar testes tradicionais de sobrecarga de servidor HTTP ou ataques diretos de injeção SQL, pois não refletem a realidade do produto. O sucesso da Disponibilidade dependerá unicamente da plataforma GitHub Pages. O sucesso da Integridade será avaliado com base nas permissões de acesso ao repositório, gerenciamento de chaves secretas (Gemini API Key) nas Actions e na validação de formato dos arquivos gerados pelo pipeline de ETL.

**Nível de Profundidade:** A profundidade segue a estrutura de variáveis identificadoras da qualidade proposta pela SQuaRE:

* **Nível 1 (Identificação):** Identificação do conjunto de propriedades, juntas, que cobrem a subcaracterística (ex: contagem de bugs por linha de código).
* **Nível 2 (Medição):** Obtenção de medidas de qualidade específicas para cada propriedade identificada por meio de testes e métricas estáticas.
* **Nível 3 (Integração):** Combinação computacional das medidas anteriores para chegar a uma medida de qualidade derivada correspondente à subcaracterística avaliada (ex: índice final de disponibilidade).

Logo, operaremos no `Nível 3 (Integração) da SQuaRE`, criando medidas de qualidade derivadas através da combinação de métricas estáticas focadas nos fluxos JSON e repositório.