
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

def __drawCube(cube: MohrCube, side: MohrCube.Side, center_mm: Vec2, size_mm, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    pattern = cube.getPattern()
    for i in range(12):
        if (pattern[i] is False and side == MohrCube.Side.LEFT) or (pattern[i] is True and side == MohrCube.Side.RIGHT):
            p1, p2 = cube.getLine(i)
            p1 *= size_mm * 0.5
            p2 *= size_mm * 0.5
            pdf_canvas.line(page.xContent(center_mm.x + p1.x), page.yContent(center_mm.y + p1.y), page.xContent(center_mm.x + p2.x), page.yContent(center_mm.y + p2.y))

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
    
def cubePage001(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
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

    cube.setFrame(4096)
    pdf_canvas.setLineWidth(book.px(1))
    __drawCube(cube, MohrCube.Side.LEFT, Vec2(35, 35), 17, pdf_canvas, page, book)
    __drawCube(cube, MohrCube.Side.RIGHT, Vec2(55, 35), 17, pdf_canvas, page, book)

def cubePage002(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    cube = MohrCube()

    pdf_canvas.setLineWidth(book.px(1))
    w = 17
    h = 17
    for y in range(h):
        for x in range(w):
            i = x * w + y
            cube.setFrame(520 + 5 * i)
            # __drawCube(cube, MohrCube.Side.LEFT if i % 2 == 0 else MohrCube.Side.RIGHT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)
            #__drawCube(cube, MohrCube.Side.LEFT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)
            __drawCube(cube, MohrCube.Side.RIGHT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)

def cubePage003(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    cube = MohrCube()

    pdf_canvas.setLineWidth(book.px(0.8))
    w = 17
    h = 17
    for y in range(h):
        for x in range(w):
            i = x * w + y
            cube.setPattern(200 + i*5)
            # cube.setAngles(0, x * 90.0/(w-1), (y * x) * 90.0/((h-1)*(w-1)))
            # cube.setAngles(0, x * 90.0/(w-1), y * 90.0/(h-1))
            # cube.setAngles(0, x * 90.0/(w-1), (y + x) * 90.0/((h-1)+(w-1)))
            cube.setAngles(0, (x * y) * 90.0/((w-1)*(h-1)), (x + y) * 90.0/((w-1)+(h-1)))
            __drawCube(cube, MohrCube.Side.LEFT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)

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
        }, cubePage001), number=None)

    book.addPage(PdfPage('default', {
        }, cubePage003), number=None)

    book.update()
    print(book)
    renderer = PdfRenderer()
    renderer.addFont('AlteHaasGrotesk', 'data/AlteHaasGroteskRegular.ttf')
    #renderer.renderTemplate(book, 'default')
    for page in book.pages:
        renderer.renderPage(page, 'output/essvik', PdfRenderer.OutputType.PDF, False)

    print("main done")