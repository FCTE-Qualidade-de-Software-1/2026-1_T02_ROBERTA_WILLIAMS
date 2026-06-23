# 9. Notas Arquiteturais e Glossário

## Notas Arquiteturais Fundamentais

- **Arquitetura Serverless/Jamstack**: O Mural UnB funciona, na sua ponta final de produção, sem um backend ativo consumindo banco de dados. A aplicação hospeda no GitHub Pages lendo arquivos JSON atualizados de forma assíncrona pelo GitHub Actions.
- **N/A de Endpoints em Produção**: Devido à natureza citada acima, métricas de ataque direto a endpoints (como M10) aplicam-se exclusivamente ao backend em Docker (ambiente administrativo/cadastro planejado ou referencial de 2025), visto que arquivos estáticos no repositório final não processam rotas de POST/PUT/DELETE on-the-fly.

## Glossário

O glossário abaixo foi incluído para auxiliar na compreensão dos termos técnicos desta fase avaliativa:

- **2FA (Two-Factor Authentication)**: Mecanismo de segurança extra, exigindo verificação secundária no login.
- **API (Application Programming Interface)**: Conjunto de rotinas e padrões que permitem a comunicação entre o frontend do Mural UnB e o banco de dados.
- **DOM (Document Object Model)**: Estrutura representativa de páginas web. "Quebra de DOM" resulta em tela branca/travamento da interface React.
- **Endpoint**: Rota de acesso específica de uma API responsável por receber requisições de manipulação de dados.
- **ETL (Extract, Transform, Load)**: Pipeline de scripts (via Github Actions) que raspa dados (PDFs, sites), formata-os e cria os arquivos `Tags DB.json` e `Oportunidades DB.json`.
- **GQM (Goal, Question, Metric)**: Abordagem hierárquica focada em objetivos para orientar a medição da qualidade de software de forma sistemática.
- **HSTS (HTTP Strict Transport Security)**: Política restritiva que força a comunicação entre o cliente e o servidor através de conexões HTTPS criptografadas.
- **JWT (JSON Web Token)**: Padrão de token seguro para identificar autenticação de usuários logados.
- **MTTR (Mean Time to Recovery)**: Tempo médio necessário para que o sistema se recupere de um colapso automatizado de workflow.
- **Payload / XSS**: Dados (ou códigos injetados, como Javascript malicioso) enviados intencionalmente para manipular a página ou o servidor.
- **Regex (Expressão Regular)**: Padrão lógico de caracteres utilizado para realizar a validação de formatação, como a exigência exclusiva de domínios institucionais (@unb.br).