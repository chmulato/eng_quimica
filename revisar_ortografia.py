# -*- coding: utf-8 -*-
"""Varredura ortografica pt-BR do texto extraido do folder PDF."""
import sys
from pathlib import Path

import language_tool_python

OUT = Path("_revisao_out.txt")
log = OUT.open("w", encoding="utf-8")


def emit(*args):
    msg = " ".join(str(a) for a in args)
    print(msg)
    log.write(msg + "\n")
    log.flush()


text = Path("_texto_pdf.txt").read_text(encoding="utf-8")

emit("Carregando LanguageTool pt-BR...")
tool = language_tool_python.LanguageTool("pt-BR")
matches = tool.check(text)

emit(f"Total de ocorrencias: {len(matches)}\n")
for m in matches:
    ctx = m.context.replace("\n", " ").strip()
    emit(f"[{m.rule_id}] {m.message}")
    emit(f"   contexto: ...{ctx}...")
    if m.replacements:
        emit(f"   sugestoes: {m.replacements[:4]}")
    emit("")

log.close()
sys.exit(0)
