# -*- coding: utf-8 -*-
"""
Gera o folder A4 de 10 paginas:
"Engenharia Quimica - Um guia para quem sonha em transformar o mundo"
Dedicado a Alexandre de Lima Mulato, de seu Pai.

Uso:
    python gerar_folder_pdf.py

Saida:
    folder_engenharia_quimica_alexandre.pdf (mesmo diretorio do script)

Requisitos: reportlab, pypdf
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    PageBreak, Table, TableStyle,
)
from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "folder_engenharia_quimica_alexandre.pdf"
TOTAL_PAGES = 10

# ---------------------------------------------------------------------------
# Paleta consistente com as 5 ilustracoes (teal + laranja + creme)
# ---------------------------------------------------------------------------
TEAL = HexColor("#0E6E6B")
TEAL_DARK = HexColor("#093F3E")
ORANGE = HexColor("#E8762D")
ORANGE_SOFT = HexColor("#F5A05A")
CREAM = HexColor("#FBF5EC")
INK = HexColor("#22303A")
GRAY = HexColor("#5A6B76")
WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

IMG = {
    "capa": BASE / "imagem_01.jpg",
    "cotidiano": BASE / "imagem_02.jpg",
    "estudantes": BASE / "imagem_03.jpg",
    "parana": BASE / "imagem_04.jpg",
    "futuro": BASE / "imagem_05.jpg",
}

# ---------------------------------------------------------------------------
# Estilos (negrito SEMPRE via fontName="Helvetica-Bold", nunca com asteriscos)
# ---------------------------------------------------------------------------
st_section = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=20, leading=24,
    textColor=TEAL, spaceAfter=6,
)
st_sub = ParagraphStyle(
    "sub", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
    textColor=ORANGE, spaceBefore=10, spaceAfter=4,
)
st_body = ParagraphStyle(
    "body", fontName="Helvetica", fontSize=11.5, leading=17,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
)
st_body_bold = ParagraphStyle(
    "bodybold", parent=st_body, fontName="Helvetica-Bold",
)
st_bullet = ParagraphStyle(
    "bullet", parent=st_body, leftIndent=14, bulletIndent=4,
    spaceAfter=3, alignment=TA_JUSTIFY,
)
st_quote = ParagraphStyle(
    "quote", fontName="Helvetica-Bold", fontSize=13, leading=19,
    textColor=TEAL_DARK, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10,
)
st_img_caption = ParagraphStyle(
    "caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
    textColor=GRAY, alignment=TA_CENTER, spaceBefore=3,
)
st_table_cell = ParagraphStyle(
    "cell", fontName="Helvetica", fontSize=10.5, leading=14, textColor=INK,
)
st_table_head = ParagraphStyle(
    "cellhead", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
    textColor=WHITE,
)


def scaled_image(path: Path, max_w: float, max_h: float) -> Image:
    """Redimensiona a imagem preservando a proporcao."""
    iw, ih = ImageReader(str(path)).getSize()
    scale = min(max_w / iw, max_h / ih)
    img = Image(str(path), width=iw * scale, height=ih * scale)
    img.hAlign = "CENTER"
    return img


def bullets(items):
    return [
        Paragraph(f"{t}", ParagraphStyle(
            f"b{i}", parent=st_bullet, bulletIndent=2),
            bulletText="\u2022")  # marcador bullet (WinAnsi)
        for i, t in enumerate(items)
    ]


# ---------------------------------------------------------------------------
# Decoracoes de pagina
# ---------------------------------------------------------------------------
def draw_cover(canvas, doc):
    canvas.saveState()

    # Fundo creme
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Faixa teal no topo
    canvas.setFillColor(TEAL_DARK)
    canvas.rect(0, PAGE_H - 30 * mm, PAGE_W, 30 * mm, stroke=0, fill=1)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, PAGE_H - 31.6 * mm, PAGE_W, 1.6 * mm, stroke=0, fill=1)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 14 * mm,
                             "UM GUIA PARA QUEM SONHA EM TRANSFORMAR O MUNDO")
    canvas.setFont("Helvetica", 10.5)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 21.5 * mm,
                             "Orientação vocacional para jovens de 16 anos")

    # Imagem de capa centralizada (area util ~135 mm de altura)
    img_path = IMG["capa"]
    iw, ih = ImageReader(str(img_path)).getSize()
    max_w, max_h = PAGE_W - 30 * mm, 128 * mm
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    x = (PAGE_W - w) / 2
    y = PAGE_H - 34 * mm - h
    # Moldura teal
    canvas.setFillColor(TEAL)
    canvas.roundRect(x - 3 * mm, y - 3 * mm, w + 6 * mm, h + 6 * mm,
                     4 * mm, stroke=0, fill=1)
    canvas.drawImage(str(img_path), x, y, width=w, height=h,
                     preserveAspectRatio=True, mask="auto")

    # Titulo principal
    ty = y - 22 * mm
    canvas.setFillColor(TEAL)
    canvas.setFont("Helvetica-Bold", 40)
    canvas.drawCentredString(PAGE_W / 2, ty, "ENGENHARIA")
    canvas.drawCentredString(PAGE_W / 2, ty - 15 * mm, "QUÍMICA")

    # Linha laranja
    canvas.setStrokeColor(ORANGE)
    canvas.setLineWidth(2.5)
    canvas.line(PAGE_W / 2 - 35 * mm, ty - 20.5 * mm,
                PAGE_W / 2 + 35 * mm, ty - 20.5 * mm)

    canvas.setFillColor(INK)
    canvas.setFont("Helvetica", 12.5)
    canvas.drawCentredString(
        PAGE_W / 2, ty - 29 * mm,
        "Da ciência do laboratório aos produtos que mudam a vida das pessoas.")

    # Caixa de dedicatoria
    box_h = 34 * mm
    box_y = 22 * mm
    canvas.setFillColor(TEAL)
    canvas.roundRect(MARGIN, box_y, CONTENT_W, box_h, 5 * mm,
                     stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 11)
    canvas.drawCentredString(PAGE_W / 2, box_y + box_h - 10 * mm,
                             "Este guia foi preparado especialmente para")
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawCentredString(PAGE_W / 2, box_y + box_h - 19 * mm,
                             "ALEXANDRE DE LIMA MULATO")
    canvas.setFont("Helvetica-Oblique", 11.5)
    canvas.drawCentredString(PAGE_W / 2, box_y + box_h - 27 * mm,
                             "com carinho, de seu Pai  \u2022  2026")

    canvas.restoreState()


def draw_content(canvas, doc):
    canvas.saveState()

    # Faixa superior
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 13 * mm, PAGE_W, 13 * mm, stroke=0, fill=1)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, PAGE_H - 14.2 * mm, PAGE_W, 1.2 * mm, stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN, PAGE_H - 8.6 * mm,
                      "ENGENHARIA QUÍMICA  \u2022  UM GUIA PARA QUEM SONHA "
                      "EM TRANSFORMAR O MUNDO")

    # Rodape
    canvas.setStrokeColor(ORANGE_SOFT)
    canvas.setLineWidth(0.8)
    canvas.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(MARGIN, 8.6 * mm,
                      "Para Alexandre de Lima Mulato \u2014 de seu Pai")
    canvas.drawRightString(PAGE_W - MARGIN, 8.6 * mm,
                           f"Página {doc.page} de {TOTAL_PAGES}")

    canvas.restoreState()


def on_cover(canvas, doc):
    draw_cover(canvas, doc)


def on_content(canvas, doc):
    draw_content(canvas, doc)


# ---------------------------------------------------------------------------
# Conteudo das paginas
# ---------------------------------------------------------------------------
def build_story():
    story = []

    # PAGINA 1 - CAPA (desenhada no canvas; apenas gatilho de pagina)
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P2
    story.append(Paragraph("VOCÊ JÁ PAROU PARA PENSAR?", st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Tudo o que você usa tem <b>ciência por trás</b>.", st_body))
    story.extend(bullets([
        "O celular.", "O refrigerante.", "O shampoo.",
        "O remédio.", "A roupa.", "O combustível.",
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Alguém precisou descobrir como produzir tudo isso em "
        "<b>grande escala</b>. Esse alguém pode ser um "
        "<b>Engenheiro Químico</b>.", st_body))
    story.append(Paragraph(
        "A Engenharia Química é a profissão que transforma conhecimento "
        "científico em produtos que melhoram a vida das pessoas. Se você "
        "gosta de entender como as coisas funcionam, esta profissão pode "
        "ser para você.", st_body))
    story.append(Spacer(1, 8))
    story.append(scaled_image(IMG["cotidiano"], CONTENT_W, 92 * mm))
    story.append(Paragraph(
        "Do celular ao combustível: química presente em tudo.",
        st_img_caption))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P3
    story.append(Paragraph("O QUE UM ENGENHEIRO QUÍMICO FAZ?", st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Imagine:", st_body))
    story.extend(bullets([
        "Uma fábrica de chocolate.",
        "Uma indústria de medicamentos.",
        "Uma refinaria de petróleo.",
        "Uma fábrica de fertilizantes.",
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "O Engenheiro Químico participa da <b>criação, operação, "
        "otimização e melhoria</b> de todo o processo de produção. "
        "No dia a dia, ele pergunta:", st_body))
    story.extend(bullets([
        "Como produzir mais?",
        "Como gastar menos energia?",
        "Como reduzir desperdícios?",
        "Como proteger o meio ambiente?",
        "Como melhorar a qualidade?",
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Seu trabalho é encontrar <b>soluções inteligentes</b>: "
        "transformar matérias-primas em produtos úteis para a sociedade "
        "de forma eficiente, econômica e sustentável.", st_body))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "\u201cA missão do engenheiro químico é transformar conhecimento "
        "científico em produção industrial segura e eficiente.\u201d",
        st_quote))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P4
    story.append(Paragraph("SERÁ QUE ESSA PROFISSÃO É PARA MIM?",
                           st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Você <b>não precisa ser o melhor aluno da escola</b>. "
        "Mas é interessante gostar de:", st_body))
    story.extend(bullets([
        "Matemática", "Ciências", "Tecnologia",
        "Resolver desafios", "Aprender coisas novas",
    ]))
    story.append(Paragraph("Também ajuda ter:", st_sub))
    story.extend(bullets([
        "Curiosidade", "Disciplina", "Criatividade",
        "Raciocínio lógico", "Vontade de crescer",
        "Capacidade de trabalhar em equipe",
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A boa notícia:", st_body_bold))
    story.append(Paragraph(
        "Ninguém nasce sabendo. Tudo isso é desenvolvido com "
        "<b>estudo e prática</b>. O engenheiro químico é um profissional "
        "que combina conhecimento científico com visão prática \u2014 e "
        "essa combinação se constrói passo a passo.", st_body))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P5
    story.append(Paragraph("UM LIVRO QUE PODE MUDAR SUA VISÃO",
                           st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Um ótimo livro para começar é <b>OS BOTÕES DE NAPOLEÃO</b> "
        "(Penny Le Couteur e Jay Burreson).", st_body))
    story.append(Paragraph(
        "O livro conta histórias incríveis sobre moléculas que mudaram "
        "o mundo. Você descobrirá:", st_body))
    story.extend(bullets([
        "Como o açúcar influenciou países inteiros.",
        "Como a cafeína mudou hábitos da humanidade.",
        "Como os corantes criaram novas indústrias.",
        "Como a química alterou guerras e revoluções.",
    ]))
    story.append(Paragraph(
        "É um livro que mostra que ciência não é apenas fórmulas. "
        "<b>Ciência é história, inovação e descoberta.</b>", st_body))
    story.append(Paragraph("Outras leituras recomendadas:", st_sub))
    story.extend(bullets([
        "O Mundo Assombrado pelos Demônios \u2014 Carl Sagan.",
        "Uma Breve História da Química.",
        "Introdução à Engenharia Química \u2014 Nilo Índio do Brasil.",
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "\u201cLer sobre ciência hoje é o primeiro passo para fazer "
        "ciência amanhã.\u201d", st_quote))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P6
    story.append(Paragraph("O CURSO E AS UNIVERSIDADES", st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "O curso dura em média <b>5 anos</b>. Você aprenderá Cálculo, "
        "Física, Química Geral, Orgânica e Analítica, Termodinâmica, "
        "Fenômenos de Transporte, Operações Unitárias, Engenharia das "
        "Reações Químicas, Controle de Processos e Projeto Industrial.",
        st_body))
    story.append(Paragraph(
        "Não é um curso voltado apenas para laboratórios: grande parte "
        "do trabalho acontece em <b>processos, equipamentos e plantas "
        "industriais</b>.", st_body))
    story.append(Paragraph("No Paraná, duas referências públicas:",
                           st_sub))
    story.extend(bullets([
        "<b>UFPR</b> \u2014 mais tradicional, forte em pesquisa e "
        "ligada à petroquímica; excelente reputação nacional.",
        "<b>UTFPR</b> \u2014 forte ligação com a indústria, presença "
        "em diversas cidades e excelência em tecnologia aplicada e "
        "agronegócio.",
    ]))
    story.append(Paragraph(
        "Ambas formam excelentes profissionais \u2014 a diferença está "
        "no perfil acadêmico e industrial de cada uma.", st_body))
    story.append(Spacer(1, 6))
    story.append(scaled_image(IMG["estudantes"], CONTENT_W, 78 * mm))
    story.append(Paragraph(
        "Aprender na prática: processos, equipes e plantas industriais.",
        st_img_caption))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P7
    story.append(Paragraph("ONDE UM ENGENHEIRO QUÍMICO PODE TRABALHAR?",
                           st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Muitos jovens pensam que o Engenheiro Químico só trabalha em "
        "laboratório. <b>Não é verdade.</b> Ele pode atuar em:", st_body))

    setores = [
        ["Alimentos e bebidas", "Petróleo e energia"],
        ["Medicamentos", "Biocombustíveis"],
        ["Cosméticos", "Papel e celulose"],
        ["Fertilizantes", "Polímeros e plásticos"],
        ["Tratamento de água", "Tintas e materiais"],
        ["Meio ambiente", "Mineração"],
        ["Pesquisa e desenvolvimento", "Consultoria"],
        ["Produtos de limpeza", "Empreendedorismo"],
    ]
    tbl = Table(
        [[Paragraph(f"\u2022 {a}", st_table_cell),
          Paragraph(f"\u2022 {b}", st_table_cell)] for a, b in setores],
        colWidths=[CONTENT_W / 2, CONTENT_W / 2],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, ORANGE_SOFT),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "O mercado é muito amplo: praticamente <b>tudo o que é produzido "
        "em larga escala</b> passa por processos que envolvem Engenharia "
        "Química.", st_body))
    story.append(Paragraph(
        "E o profissional pode crescer para gestão, consultoria, "
        "pesquisa ou abrir o próprio negócio.", st_body))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P8
    story.append(Paragraph("OPORTUNIDADES NO PARANÁ E NA CARREIRA",
                           st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "O Paraná tem uma das economias mais fortes do país. A combinação "
        "entre <b>agroindústria e indústria de transformação</b> cria um "
        "excelente mercado de trabalho:", st_body))
    story.extend(bullets([
        "<b>Araucária</b> \u2014 refino de petróleo e combustíveis.",
        "<b>Paranaguá</b> \u2014 logística portuária e fertilizantes.",
        "<b>Ponta Grossa</b> \u2014 papel e celulose.",
        "<b>Londrina e Maringá</b> \u2014 agronegócio e alimentos.",
        "<b>Curitiba</b> \u2014 grande diversidade industrial.",
        "<b>Cascavel e Toledo</b> \u2014 agroindústria em expansão.",
    ]))
    story.append(Paragraph("Faixas salariais aproximadas:", st_sub))
    sal = [
        [Paragraph("Etapa", st_table_head),
         Paragraph("Faixa mensal", st_table_head)],
        ["Estágio", "R$ 1.200 a R$ 2.500"],
        ["Trainee", "R$ 4.000 a R$ 7.000"],
        ["Júnior", "R$ 6.000 a R$ 10.000"],
        ["Pleno", "R$ 10.000 a R$ 16.000"],
        ["Sênior", "R$ 15.000 a R$ 25.000"],
        ["Gerência", "R$ 20.000 a R$ 40.000 ou mais"],
    ]
    tbl_sal = Table(sal, colWidths=[CONTENT_W * 0.35, CONTENT_W * 0.65])
    tbl_sal.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.4, ORANGE_SOFT),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl_sal)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "O crescimento depende de experiência, inglês, especializações, "
        "liderança e resultados. Quem se prepara bem encontra boas "
        "oportunidades.", st_body))
    story.append(Spacer(1, 4))
    story.append(scaled_image(IMG["parana"], CONTENT_W, 62 * mm))
    story.append(PageBreak())

    # ------------------------------------------------------------------ P9
    story.append(Paragraph("COMO SE PREPARAR DESDE AGORA", st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Você não precisa esperar a faculdade. Pode começar "
        "<b>hoje</b>:", st_body))
    passos = [
        "Leia livros de divulgação científica.",
        "Fortaleça a matemática.",
        "Aprenda física.",
        "Estude química.",
        "Desenvolva o hábito de leitura.",
        "Aprenda inglês.",
        "Assista documentários sobre indústria e ciência.",
    ]
    for i, p in enumerate(passos, 1):
        story.append(Paragraph(
            f"<b>{i}.</b>  {p}",
            ParagraphStyle(f"passo{i}", parent=st_bullet, leftIndent=10)))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Um pequeno avanço por dia produz grandes resultados ao longo "
        "dos anos.", st_body_bold))
    story.append(Paragraph("E as profissões do futuro?", st_sub))
    story.append(Paragraph(
        "As próximas décadas vão precisar de engenheiros químicos em:",
        st_body))
    story.extend(bullets([
        "Hidrogênio verde e bioenergia.",
        "Química verde e economia circular.",
        "Reciclagem química e captura de carbono.",
        "Biotecnologia e novos materiais.",
        "Tratamento avançado de água e ESG.",
    ]))
    story.append(Paragraph(
        "Quem entrar nessa área estará ajudando a <b>construir o "
        "futuro</b>.", st_body))
    story.append(PageBreak())

    # ----------------------------------------------------------------- P10
    story.append(Paragraph("UMA MENSAGEM PARA VOCÊ, ALEXANDRE",
                           st_section))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Talvez hoje você tenha apenas 16 anos e ainda não saiba "
        "exatamente qual profissão seguir. Isso é normal.", st_body))
    story.append(Paragraph(
        "Mas lembre-se: <b>grandes profissionais começaram exatamente "
        "como você</b> \u2014 com dúvidas, com curiosidade e com "
        "sonhos.", st_body))
    story.append(Paragraph(
        "A Engenharia Química está no alimento que você consome, no "
        "combustível que movimenta o país, no medicamento que "
        "salva-vidas e no cuidado com o meio ambiente. Se você gosta de "
        "ciência, tecnologia, inovação e de resolver problemas reais, "
        "ela pode ser uma excelente escolha.", st_body))
    story.append(Paragraph(
        "Estude. Leia. Pergunte. Experimente. "
        "<b>Nunca pare de aprender.</b>", st_body))
    story.append(Paragraph(
        "O mundo precisa de pessoas capazes de transformar conhecimento "
        "em progresso \u2014 e talvez uma dessas pessoas seja você.",
        st_body))
    story.append(Spacer(1, 6))
    story.append(scaled_image(IMG["futuro"], CONTENT_W, 62 * mm))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "BOA JORNADA, FUTURO ENGENHEIRO!", st_quote))
    story.append(Paragraph(
        "Com todo o carinho e orgulho,<br/>\u2014 Seu Pai",
        ParagraphStyle("ass", parent=st_body, alignment=TA_CENTER,
                       fontName="Helvetica-Oblique", textColor=TEAL_DARK)))

    return story


# ---------------------------------------------------------------------------
# Montagem do documento
# ---------------------------------------------------------------------------
def build_pdf():
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=20 * mm, bottomMargin=16 * mm,
        title="Engenharia Química - Guia para Alexandre de Lima Mulato",
        author="Pai do Alexandre",
        subject="Orientação vocacional - Engenharia Química",
    )

    frame_cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
    frame_content = Frame(MARGIN, 16 * mm, CONTENT_W,
                          PAGE_H - 20 * mm - 16 * mm, id="content")

    doc.addPageTemplates([
        PageTemplate(id="Capa", frames=[frame_cover], onPage=on_cover),
        PageTemplate(id="Conteudo", frames=[frame_content],
                     onPage=on_content),
    ])

    from reportlab.platypus import NextPageTemplate
    story = [NextPageTemplate("Conteudo")] + build_story()
    doc.build(story)
    return OUTPUT


def validate_pdf(path: Path):
    reader = PdfReader(str(path))
    n = len(reader.pages)
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    stars = text.count("*")
    print(f"PDF gerado: {path.name}")
    print(f"Paginas: {n} (esperado {TOTAL_PAGES}) -> "
          f"{'OK' if n == TOTAL_PAGES else 'ERRO'}")
    print(f"Asteriscos residuais no texto: {stars} -> "
          f"{'OK' if stars == 0 else 'ERRO'}")
    print(f"Tamanho: {path.stat().st_size / 1024:.0f} KB")
    if n != TOTAL_PAGES or stars != 0:
        raise SystemExit("Validacao falhou.")


if __name__ == "__main__":
    out = build_pdf()
    validate_pdf(out)
