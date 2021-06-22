
from book import Book, PdfRenderer, PdfPage
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

#from book.pdf_renderer import OutputType

from mohr import MohrCube
from mohr import Vec3, Vec2

def __clearPen(pdf_canvas: canvas.Canvas):
    pdf_canvas.setStrokeColor(Color(0,0,0))
    pdf_canvas.setLineWidth(1)
    pdf_canvas.setFillColor(Color(0,0,0,0))
    pdf_canvas.setDash([])
    pdf_canvas.setLineCap(1)

def testPage(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    pdf_canvas.setLineWidth(book.px(0.1))
    pdf_canvas.setStrokeColor(Color(0,0,0))
    pdf_canvas.rect(page.xContent(0), page.yContent(100), book.px(50), book.px(50))

    pdf_canvas.setFont("AlteHaasGrotesk", book.px(10))
    pdf_canvas.setFillColor(Color(0,0,0))
    pdf_canvas.drawString(page.xContent(0), page.yContent(10), data['text'])

    pdf_canvas.drawImage("output/original_frames/frame_0000.jpg", page.xContent(55), page.yContent(100), book.px(64), book.px(48))
    # svg.image(page.x_content(0), page.y_content(0), book.px(64), book.px(48), data['frame'])

def __drawCube(angles: Vec3, pattern, pdf_canvas: canvas.Canvas, x, y):
    pass

def __drawPattern(pattern, x, y, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    w = 3
    h = 3
    pdf_canvas.setFillColor(Color(0,0,0,1))
    for i in range(len(pattern)):
        p = pattern[i]
        pdf_canvas.roundRect(page.xContent(x + (w+1)*i), page.yContent(y), book.px(w), book.px(h), book.px(0.5), 1, 1 if p else 0)

def __drawAngles(angles, x, y, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    r = 2
    #pdf_canvas.setLineWidth(book.px(1))
    if not isinstance(angles, Vec3):
        angles = Vec3(angles[0], angles[1], angles[2])
    v = Vec2(0,-1)
    o = 0
    for a in angles:
        pdf_canvas.circle(page.xContent(x + o + r), page.yContent(y + r), book.px(r), 1, 0)
        vr = v.rotateDegrees(a)
        pdf_canvas.line(page.xContent(x + o + r), page.yContent(y + r), page.xContent(x + o + r + r*vr.x), page.yContent(y + r + r*vr.y))
        o += r*2 + r
    
def cubePage(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    cube = MohrCube()
    cube.setAngles(data['angles'][0], data['angles'][1], data['angles'][2])
    print(data['pattern'])
    cube.setPattern(data['pattern'])
    print(cube.getPattern())

    pdf_canvas.setLineWidth(book.px(0.5))
    pattern = cube.getPattern()
    __drawPattern(pattern, 4, 4, pdf_canvas, page, book)
    __drawAngles(Vec3(data['angles'][0], data['angles'][1], data['angles'][2]), 80, 3.5, pdf_canvas, page, book)

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
    #renderer.renderTemplate(book, 'default')
    for page in book.pages:
        renderer.renderPage(page, 'output/essvik', PdfRenderer.OutputType.PDF, True)

    print("main done")