#!/usr/bin/env python3
"""
M4 - Taxa de Procedencia Verificavel (TPV)  -  Avaliacao Mural UnB / Fase 4

Calcula o percentual de oportunidades cuja procedencia e rastreavel a uma
fonte oficial verificavel, conforme criterio definido na Fase 2:
  - Empresa junior:  possui `Site` OU `Instagram` preenchido.
  - Laboratorio:     possui `contato` em dominio institucional `@unb.br`.

Uso:
    python3 m4_procedencia.py [caminho/para/oportunidades.json]

Por padrao espera o arquivo `data/oportunidades.json` do repositorio
oficial do Mural UnB (2025-2). Saida reproduzida em `m4_resultado.txt`.
"""
import json
import re
import sys

CAMINHO_PADRAO = "data/oportunidades.json"
DOMINIO_UNB = re.compile(r"@([a-z0-9.-]+\.)?unb\.br", re.IGNORECASE)


def main(caminho: str) -> None:
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    labs = dados["laboratorios"]
    ejs = dados["empresas_juniores"]

    labs_ok = [l for l in labs if DOMINIO_UNB.search(str(l.get("contato", "")))]
    ejs_ok = [
        e
        for e in ejs
        if str(e.get("Site", "")).strip() or str(e.get("Instagram", "")).strip()
    ]

    verificaveis = len(labs_ok) + len(ejs_ok)
    total = len(labs) + len(ejs)
    tpv = 100 * verificaveis / total

    print("=== M4 - Taxa de Procedencia Verificavel (TPV) ===")
    print(f"Empresas Juniores com Site/Instagram : {len(ejs_ok)}/{len(ejs)} "
          f"({100 * len(ejs_ok) / len(ejs):.1f}%)")
    print(f"Laboratorios com contato @unb.br     : {len(labs_ok)}/{len(labs)} "
          f"({100 * len(labs_ok) / len(labs):.1f}%)")
    print(f"TPV GLOBAL                           : {verificaveis}/{total} = {tpv:.1f}%")

    faixa = (
        "Excelente (>= 95%)"
        if tpv >= 95
        else "Satisfatorio (80% a 94%)"
        if tpv >= 80
        else "Insatisfatorio (< 80%)"
    )
    print(f"Julgamento (Fase 2)                  : {faixa}")

    fora = [str(l.get("contato", "")) for l in labs if not DOMINIO_UNB.search(str(l.get("contato", "")))]
    print(f"\nLaboratorios SEM contato @unb.br ({len(fora)}):")
    for contato in fora:
        print(f"  - {contato}")


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else CAMINHO_PADRAO
    main(caminho)
