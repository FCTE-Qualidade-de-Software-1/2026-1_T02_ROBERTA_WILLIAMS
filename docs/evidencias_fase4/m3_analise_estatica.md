# M3 — Taxa de Neutralização de Conteúdo Malicioso (TNCM) — Evidência de Análise Estática

**Métrica:** M3 (TNCM) · **Subcaracterística:** Integridade · **Hipótese:** H3
**Método:** análise estática do código-fonte do `site/` (React 19 + Vite), conforme previsto na Fase 3.
**Repositório avaliado:** Mural UnB (2025-2) — SPA estática servida por GitHub Pages, sem backend.

> Esta evidência documenta a **medição de M3 por inspeção do código-fonte** do `site/`.

## 1. Como cada campo é renderizado

| Campo (origem no JSON) | Componente / Linha | Forma de renderização | Escapado pelo React? |
|---|---|---|---|
| `Nome` / `name` | `OpportunityHeader.tsx:24` (`<h1>{name}</h1>`) e `:20` (`alt={name}`) | Filho JSX `{name}` | ✅ Sim |
| `descricao` / `shortDescription` | `OpportunityHeader.tsx:36` (`<p>{shortDescription}</p>`) | Filho JSX | ✅ Sim |
| `Sobre`, `Missao`, `Visao`, `Valores`, `Servicos` | `DescriptionSection.tsx:11` (`<p ...>{content}</p>`) via `DescriptionSections.tsx` | Filho JSX `{content}` | ✅ Sim |
| `Site` / `website` | `SocialFooter.tsx:28` (`href={website}`) | **Atributo `href`, sem validação de esquema** | ❌ Não |
| `Instagram` / `instagram` | `SocialFooter.tsx:38` (`href={instagram}`) | **Atributo `href`, sem validação de esquema** | ❌ Não |

**Fato decisivo:** não há **nenhuma** ocorrência de `dangerouslySetInnerHTML` em `site/src/`
(verificado por `grep -rc "dangerouslySetInnerHTML" src` → 0). Todo conteúdo textual passa pelo
escape automático do JSX.

## 2. Payloads e classificação

| Campo de injeção | Payload | Renderização esperada | Classificação |
|---|---|---|---|
| Texto (`descricao`, `Sobre`, `Nome`) | `<script>alert('xss')</script>` | Exibido como texto literal | **Neutralizado** |
| Texto | `<img src=x onerror=alert('xss')>` | Exibido como texto literal | **Neutralizado** |
| Texto | `<b>conteudo-injetado</b>` | Exibido como texto literal | **Neutralizado** |
| Canal (`Site`) | `javascript:alert('xss')` | Inserido verbatim em `href` → executa no clique | **Ativo** |
| Canal (`Instagram`) | `javascript:alert('xss')` | Inserido verbatim em `href` → executa no clique | **Ativo** |

## 3. Resultado

- **Campos de texto:** 100% neutralizados (escape do JSX; sem `dangerouslySetInnerHTML`).
- **Campos de canal (`href`):** 0% neutralizados — vetor `javascript:` vivo, acionado por clique.
- **Não há execução automática (auto-XSS) em nenhum campo de texto.**

**Julgamento (Fase 2):** **Aceitável com ressalva** — falha restrita ao `href` dos campos de
canal (exige interação do usuário). **H3 confirmada.**

> **Critério de M3 (revisado na Fase 2/3):** o veredicto de M3 segue o **padrão da falha**, e
> não o percentual bruto de TNCM (que depende da composição dos payloads — proporção texto ×
> canal). Regra vigente: há execução automática (auto-XSS) em campo de texto? Se não, e a falha
> se restringe ao `href` de canal (exige clique) → **Aceitável**. A TNCM (texto 100% / canal 0%)
> é reportada como indicador complementar.

## 4. Ação recomendada

Sanitizar o esquema da URL no `SocialFooter.tsx`, aceitando apenas `http`/`https` antes de
atribuir a `href` (ex.: rejeitar/normalizar valores iniciados por `javascript:`, `data:` etc.).

## Referências

- ISO/IEC 25010 (Integridade).
- MITRE CWE-79 — *Improper Neutralization of Input During Web Page Generation (XSS)*.
