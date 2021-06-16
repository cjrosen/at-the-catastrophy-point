from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

def svg_to_pdf(svg_path, pdf_path):
    drawing = svg2rlg(svg_path)
    renderPDF.drawToFile(drawing, pdf_path)

if __name__ == "__main__":
    svg_to_pdf("../output/essvik/page_1.svg", "../output/essvik-pdf/page_1.pdf")