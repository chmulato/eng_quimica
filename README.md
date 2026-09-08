# Engenharia Química — Guia Vocacional (Folder PDF)

Folder A4 de 10 páginas: **"Engenharia Química — Um guia para quem sonha em transformar o mundo"**.

Preparado com carinho para **Alexandre de Lima Mulato**, de seu Pai — 2026.

## Conteúdo

| Página | Tema |
|--------|------|
| 1 | Capa com dedicatória |
| 2 | Você já parou para pensar? |
| 3 | O que um Engenheiro Químico faz? |
| 4 | Será que essa profissão é para mim? |
| 5 | Um livro que pode mudar sua visão |
| 6 | O curso e as universidades (UFPR × UTFPR) |
| 7 | Onde um Engenheiro Químico pode trabalhar? |
| 8 | Oportunidades no Paraná e faixas salariais |
| 9 | Como se preparar desde agora + profissões do futuro |
| 10 | Mensagem final ao futuro engenheiro |

## Estrutura

- `guia.txt` — texto-fonte do guia (duas versões compiladas)
- `imagem_01.jpg` … `imagem_05.jpg` — ilustrações (capa, cotidiano, estudantes, Paraná, futuro)
- `gerar_folder_pdf.py` — gerador do PDF (ReportLab)
- `revisar_ortografia.py` — varredura ortográfica pt-BR (LanguageTool)
- `folder_engenharia_quimica_alexandre.pdf` — **resultado final**

## Como gerar o PDF

Requisitos: Python 3.13+ e dependências:

```bash
pip install reportlab pypdf pymupdf
python gerar_folder_pdf.py
```

O script valida automaticamente o resultado (10 páginas, zero asteriscos residuais).

## Revisão ortográfica

```bash
pip install language-tool-python
python revisar_ortografia.py   # gera _revisao_out.txt com o relatório
```

Texto validado com LanguageTool pt-BR: sem erros de ortografia/acentuação
(ocorrências restantes são falsos positivos: nomes próprios de autores
estrangeiros, "Trainee" e artefatos de extração do PDF).
