
from book import Book, PdfRenderer, PdfPage
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

#from book.pdf_renderer import OutputType

from mohr import MohrCube

def clearPen(pdf_canvas: canvas.Canvas):
    pdf_canvas.setStrokeColor(Color(0,0,0))
    pdf_canvas.setLineWidth(1)
    pdf_canvas.setFillColor(Color(0,0,0,0))
    pdf_canvas.setDash([])
    pdf_canvas.setLineCap(1)

def testPage(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    clearPen(pdf_canvas)

    pdf_canvas.setLineWidth(book.px(0.1))
    pdf_canvas.setStrokeColor(Color(0,0,0))
    pdf_canvas.rect(page.xContent(0), page.yContent(100), book.px(50), book.px(50))

    pdf_canvas.setFont("AlteHaasGrotesk", book.px(10))
    pdf_canvas.setFillColor(Color(0,0,0))
    pdf_canvas.drawString(page.xContent(0), page.yContent(10), data['text'])

    pdf_canvas.drawImage("output/original_frames/frame_0000.jpg", page.xContent(55), page.yContent(100), book.px(64), book.px(48))
    # svg.image(page.x_content(0), page.y_content(0), book.px(64), book.px(48), data['frame'])
    
def cubePage(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    clearPen(pdf_canvas)

    cube = MohrCube()
    cube.setAngles(data['angles'][0], data['angles'][1], data['angles'][2])
    cube.setPattern(data['pattern'])

    pdf_canvas.setLineWidth(book.px(0.5))
    pattern = cube.getPattern()
    for i in range(len(pattern)):
        p = pattern[i]
        pdf_canvas.setFillColor(Color(0, 0, 0))
        pdf_canvas.roundRect(page.xContent(10 + 4*i), page.yContent(4), book.px(3), book.px(3), book.px(0.5), 1, 1 if p else 0)


if __name__ == '__main__':
    book = Book(200, 220, 300)
    

    book.addPage(PdfPage('default', {
            'frame': '../original_frames/frame_0000.jpg',
            'text': "En text till olles bok."
        }, testPage), number=None)

    book.addPage(PdfPage('default', {
            'frame': '../original_frames/frame_0000.jpg',
            'text': "En text till olles bok."
        }, testPage), number=None)

    book.addPage(PdfPage('default', {
            'angles': (34, 88, 25),
            'pattern': 2345
        }, cubePage), number=None)

    book.update()
    print(book)
    renderer = PdfRenderer()
    renderer.addFont('AlteHaasGrotesk', 'data/AlteHaasGroteskRegular.ttf')
    renderer.renderTemplate(book, 'default')
    for page in book.pages:
        renderer.renderPage(page, 'output/essvik', PdfRenderer.OutputType.PDF, True)

    print("main done")