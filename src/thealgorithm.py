
from hashlib import pbkdf2_hmac
from typing import Collection
from book import Book, PdfRenderer, PdfPage
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

#from book.pdf_renderer import OutputType

from mohr import MohrCube
from mohr import Vec3, Vec2

import math
import random
import collections

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

def __drawFilledLine(p1: Vec2, p2: Vec2, width, radius, pdf_canvas: canvas.Canvas):
    if radius * 2 > width:
        radius = width * 0.5
    v = p2 - p1
    right = Vec2(1,0)
    up = Vec2(0,-1)
    angle = right.angleDegrees(v) # compared to right
    angle = -angle if up.dot(v) > 0 else angle
    pdf_canvas.saveState()
    pdf_canvas.translate(p1.x, p1.y)
    pdf_canvas.rotate(angle)
    pdf_canvas.translate(-radius, 0)
    pdf_canvas.roundRect(0, -0.5*width, v.length()+2*radius, width, radius, 0, 1)
    pdf_canvas.restoreState()

def __drawCube(cube: MohrCube, side: MohrCube.Side, center_mm: Vec2, size_mm, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    pattern = cube.getPattern()
    for i in range(12):
        if (pattern[i] is False and side == MohrCube.Side.LEFT) or (pattern[i] is True and side == MohrCube.Side.RIGHT):
            p1, p2 = cube.getLine(i)
            p1 *= size_mm * 0.5
            p2 *= size_mm * 0.5
            pdf_canvas.line(page.xContent(center_mm.x + p1.x), page.yContent(center_mm.y + p1.y), page.xContent(center_mm.x + p2.x), page.yContent(center_mm.y + p2.y))

def __drawPattern(pattern, x, y, w, dw, h, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    if pattern is None:
        pattern = [False] * 12
    ps = len(pattern)
    space = w / ps - dw
    for i in range(ps):
        p = pattern[-1-i]
        #pdf_canvas.roundRect(page.xContent(x + (w+1)*i), page.yContent(y), book.px(w), book.px(h), book.px(0.5), 1, 1 if p else 0)
        pdf_canvas.roundRect(page.xContent(x + (dw+space)*i), page.yContent(y), book.px(dw), book.px(h), book.px(dw*0.1), 1, 1 if p else 0)

def inversePattern(pattern):
    if pattern is None:
        return pattern
    return [not p for p in pattern]

def __drawPatterns(patterns, x, y, w, h, pdf_canvas: canvas.Canvas, page: PdfPage, book: Book):
    ps = len(patterns[0])
    dw = w / ps
    dh = h / len(patterns)
    f = 1.0
    pdf_canvas.rect(page.xContent(x), page.yContent(y), book.px(w), book.px(h), 1, 0)
    for i in range(ps):
        #pdf_canvas.rect(page.xContent(x + dw*i), page.yContent(y), book.px(dw*0.8), book.px(h), 1, 0)
        for j in range(len(patterns)):
            p = patterns[j][-1-i]
            if p:
                pdf_canvas.rect(page.xContent(x + dw*i), page.yContent(y+dh*j), book.px(dw*f*1.1), book.px(dh*1.1), 0, 1)

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
    
# def cubePage001(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
#     __clearPen(pdf_canvas)

#     cube = MohrCube()
#     cube.setAngles(data['angles'][0], data['angles'][1], data['angles'][2])
#     print(data['pattern'])
#     cube.setPattern(data['pattern'])
#     print(cube.getPattern())

#     pdf_canvas.setLineWidth(book.px(0.5))
#     pattern = cube.getPattern()
#     __drawPattern(pattern, 4, 4, pdf_canvas, page, book)
#     __drawAngles(Vec3(data['angles'][0], data['angles'][1], data['angles'][2]), 80, 3.5, pdf_canvas, page, book)

#     cube.setFrame(4096)
#     pdf_canvas.setLineWidth(book.px(1))
#     __drawCube(cube, MohrCube.Side.LEFT, Vec2(35, 35), 17, pdf_canvas, page, book)
#     __drawCube(cube, MohrCube.Side.RIGHT, Vec2(55, 35), 17, pdf_canvas, page, book)

# def cubePage002(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
#     __clearPen(pdf_canvas)

#     cube = MohrCube()

#     pdf_canvas.setLineWidth(book.px(1))
#     w = 17
#     h = 17
#     for y in range(h):
#         for x in range(w):
#             i = x * w + y
#             cube.setFrame(520 + 5 * i)
#             # __drawCube(cube, MohrCube.Side.LEFT if i % 2 == 0 else MohrCube.Side.RIGHT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)
#             #__drawCube(cube, MohrCube.Side.LEFT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)
#             __drawCube(cube, MohrCube.Side.RIGHT, Vec2(5+x*10, 5+y*10), 7, pdf_canvas, page, book)

# def cubePage003(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
#     __clearPen(pdf_canvas)

#     cube = MohrCube()

#     pdf_canvas.setLineWidth(book.px(0.8))
#     w = 17
#     h = 17
#     cube.setPattern(3 << 0)
#     for y in range(h):
#         for x in range(w):
#             i = x * w + y
#             #cube.setPattern(200 + i*5)
#             # cube.setAngles(0, x * 90.0/(w-1), (y * x) * 90.0/((h-1)*(w-1)))
#             # cube.setAngles(0, x * 90.0/(w-1), y * 90.0/(h-1))
#             # cube.setAngles(0, x * 90.0/(w-1), (y + x) * 90.0/((h-1)+(w-1)))
#             #cube.setAngles(0, (x * y) * 90.0/((w-1)*(h-1)), (x + y) * 90.0/((w-1)+(h-1)))
#             cube.setAngles(random.randint(0, 359), random.randint(0, 359), random.randint(0, 359))
#             __drawCube(cube, MohrCube.Side.RIGHT, Vec2(5+x*10, 5+y*10), 4, pdf_canvas, page, book)
            
def cubePagePatterns(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    cube = MohrCube()

    pdf_canvas.setFillColor(Color(0,0,0))
    pdf_canvas.setStrokeColor(Color(0,0,0,0))
    pdf_canvas.setLineWidth(book.px(0.7))

    if 'end' not in data['frame']:
        if data['angle'] == 0:
            data['frame']['end'] = data['frame']['begin'] + 200
        else:
            data['frame']['end'] = data['frame']['begin'] + int((book.mm(page.content['w'])-2*35)/v.y)
    print(f"Frame range: {data['frame']['begin']} -- {data['frame']['end']}")

    patterns = []
    for f in range(data['frame']['begin'], data['frame']['end']+1, 1):
        cube.setFrame(cube.clampFrame(f))
        pattern = cube.getPattern()
        if len(patterns) == 0 or pattern != patterns[-1]:
            patterns.append(pattern)
    
    s = 2.5
    w = 40
    xLeft = 25
    xRight = book.mm(page.widthContent()) - xLeft - w
    y = s + 50
    ds = w / 12 #s + (w - 12 * s) / 11
    print(ds)
    for pattern in patterns:
        inv_pattern = inversePattern(pattern)
        __drawPattern(inv_pattern, xLeft, y-s, w, s, s, pdf_canvas, page, book)
        __drawPattern(pattern, xRight, y-s, w, s, s, pdf_canvas, page, book)
        y += ds

    drawText(pdf_canvas, cube, patterns, data)


def cubePageSideTransparent(pdf_canvas: canvas.Canvas, page: PdfPage, book: Book, data):
    __clearPen(pdf_canvas)

    cube = MohrCube()

    pdf_canvas.setLineWidth(book.px(2.2))
    pdf_canvas.setFillColor(Color(0,0,0,data['alpha']))
    # s = 40

    v = Vec2(1,0).rotateDegrees(data['angle'])
    if 'end' not in data['frame']:
        if data['angle'] == 0:
            data['frame']['end'] = data['frame']['begin'] + (data['frame']['limit'] if 'limit' in data['frame'] else 200)
        else:
            n = int((book.mm(page.content['w'])-2*35)/v.y)
            if 'limit' in data['frame'] and n > data['frame']['limit']:
                n = data['frame']['limit']
            data['frame']['end'] = data['frame']['begin'] + n

    print(f"Frame range: {data['frame']['begin']} -- {data['frame']['end']}")
    center = Vec2((book.mm(page.content['w']) - (data['frame']['end'] - data['frame']['begin']) * v.y)/2, 70)
    if data['meta']:
        pdf_canvas.setStrokeColor(Color(1,0,0,1))
        pdf_canvas.setLineWidth(book.px(0.3))
        # pdf_canvas.rect(page.xContent(40-20), page.yContent(70-20), book.px(40*v.x), book.px(40), 1, 0)
    patterns = []
    for f in range(data['frame']['begin'], data['frame']['end']+1, 1):
        cube.setFrame(cube.clampFrame(f))
        pattern = cube.getPattern()
        if len(patterns) == 0 or pattern != patterns[-1]:
            patterns.append(pattern)
        try:
            for i in range(12):
                if pattern[i] == data['right']:
                    p1, p2 =  cube.getLine(i)
                    p1 *= 20
                    p2 *= 20
                    p1.x *= v.x
                    p2.x *= v.x
                    
                    xo = center.x + v.y*(f-data['frame']['begin'])
                    if data['meta']:
                        pdf_canvas.line(
                            page.xContent(center.x + v.y*(f-data['frame']['begin']-1)), page.yContent(center.y),
                            page.xContent(center.x + v.y*(f-data['frame']['begin'])), page.yContent(center.y))
                    __drawFilledLine(
                        Vec2(page.xContent(xo + p1.x), page.yContent(center.y + p1.y)),
                        Vec2(page.xContent(xo + p2.x), page.yContent(center.y + p2.y)),
                        book.px(3), book.px(1.5), pdf_canvas)
        except:
            print(f"Empty pattern for frame: {f}")
    
    drawText(pdf_canvas, cube, patterns, data)


def drawText(pdf_canvas: canvas.Canvas, cube: MohrCube, patterns, data):
    # text
    pdf_canvas.setFont("AlteHaasGrotesk-Bold", book.px(5))
    pdf_canvas.setFillColor(Color(0,0,0))
    pdf_canvas.setStrokeColor(Color(0,0,0))
    pdf_canvas.setLineWidth(book.px(0.7))
    cube.setFrame(cube.clampFrame(data['frame']['begin']))
    cube.setPattern(0)
    s = 3
    x = 3
    y = 190
    l = 9
    __drawCube(cube, MohrCube.Side.LEFT, Vec2(x+s, y-s/2), s, pdf_canvas, page, book)
    pdf_canvas.line(page.xContent(x+s*2+1), page.yContent(y-s/2), page.xContent(x+s*2+1+l), page.yContent(y-s/2))
    cube.setFrame(cube.clampFrame(data['frame']['end']))
    cube.setPattern(0)
    __drawCube(cube, MohrCube.Side.LEFT, Vec2(x+s*2+1+l+1+s, y-s/2), s, pdf_canvas, page, book)
    x += s*2+1+l+1+s*2+1 + 1
    pdf_canvas.drawString(page.xContent(x), page.yContent(y), f"/ {data['frame']['begin']:04}")
    x += 16
    pdf_canvas.line(page.xContent(x), page.yContent(y-s/2), page.xContent(x+l), page.yContent(y-s/2))
    x += l + 2
    pdf_canvas.drawString(page.xContent(x), page.yContent(y), f"{cube.clampFrame(data['frame']['end']):04} /")
    x += 16
    pdf_canvas.line(page.xContent(x), page.yContent(y-s/2), page.xContent(x+l), page.yContent(y-s/2))
    if data['right']:
        pdf_canvas.line(page.xContent(x+l), page.yContent(y-s/2), page.xContent(x+l-s/2), page.yContent(y-s))
        pdf_canvas.line(page.xContent(x+l), page.yContent(y-s/2), page.xContent(x+l-s/2), page.yContent(y))
    else:
        pdf_canvas.line(page.xContent(x), page.yContent(y-s/2), page.xContent(x+s/2), page.yContent(y-s))
        pdf_canvas.line(page.xContent(x), page.yContent(y-s/2), page.xContent(x+s/2), page.yContent(y))
    x += l+2
    pdf_canvas.drawString(page.xContent(x), page.yContent(y), "/")
    x += 4
    pdf_canvas.setLineWidth(book.px(0.5))
    #__drawPatterns(patterns, 0, 170, 50, 10, pdf_canvas, page, book)
    r = 1.5
    patternBegin = patterns[0] if data['right'] else inversePattern(patterns[0])
    __drawPattern(patternBegin, x, y-((s-r)/2+r), 28, 1.5, r, pdf_canvas, page, book)
    x += 30
    pdf_canvas.line(page.xContent(x), page.yContent(y-s/2), page.xContent(x+l), page.yContent(y-s/2))
    x += l + 3
    patternEnd = patterns[-1] if data['right'] else inversePattern(patterns[-1])
    __drawPattern(patternEnd, x, y-((s-r)/2+r), 28, 1.5, r, pdf_canvas, page, book)
    x += 30
    if 'angle' in data:
        pdf_canvas.drawString(page.xContent(x), page.yContent(y), f"/ {data['angle']}°")
    else:
        pdf_canvas.drawString(page.xContent(x), page.yContent(y), f"/ ---")


if __name__ == '__main__':
    book = Book(200, 220, 72)

    #angles = [0, 0, 0, 4, 8, 8, 10, 16, 16, 30]
    n = 400
    angles = [0] * n + [4] * n + [8] * n + [10] * n + [16] * n + [30] * n

    print(f"Will generate {len(angles)} images")
    count = collections.Counter(angles)
    for angle in count:
        print(f"  {angle:2}°: {count[angle]} pages")
    
    #random.shuffle(angles)
    for angle in angles:
        f = int(random.uniform(518, 4000))
        angle = angle
        book.addPage(PdfPage('default', {
            'angle': angle,
            'alpha': 0.03,
            'right': random.random() >= 0.5,
            'frame': {
                'begin': f,
                'limit': 518
            },
            'meta': False
        }, cubePageSideTransparent), number=None)

    if False:

        f = int(random.uniform(518, 4000))
        #f = 4000

        book.addPage(PdfPage('default', {
                'angle': 10,
                'alpha': 0.03,
                'right': True,
                'frame': {
                    'begin': f
                },
                'meta': False
            }, cubePageSideTransparent), number=None)

        book.addPage(PdfPage('default', {
                'angle': 0,
                'alpha': 0.03,
                'right': False,
                'frame': {
                    'begin': f
                },
                'meta': False
            }, cubePageSideTransparent), number=None)

        book.addPage(PdfPage('default', {
                'angle': 0,
                'alpha': 0.03,
                'right': True,
                'frame': {
                    'begin': f,
                    'end': f + int(random.uniform(160, 600))
                },
                'meta': False
            }, cubePageSideTransparent), number=None)

        book.addPage(PdfPage('default', {
                'angle': 5,
                'alpha': 0.03,
                'right': False,
                'frame': {
                    'begin': f
                },
                'meta': False
            }, cubePageSideTransparent), number=None)

        book.addPage(PdfPage('default', {
                'angle': 5,
                'alpha': 0.03,
                'right': True,
                'frame': {
                    'begin': f
                },
                'meta': False
            }, cubePageSideTransparent), number=None)
        
        # book.addPage(PdfPage('default', {
        #         'right': True,
        #         'frame': {
        #             'begin': f,
        #             'end': f + int(random.uniform(160, 600))    
        #         },
        #         'meta': False
        #     }, cubePagePatterns), number=None)

        book.addPage(PdfPage('default', {
                'angle': 15,
                'alpha': 0.03,
                'right': True,
                'frame': {
                    'begin': f
                },
                'meta': False
            }, cubePageSideTransparent), number=None)

    book.update()
    print(book)
    renderer = PdfRenderer()
    renderer.addFont('AlteHaasGrotesk', 'data/AlteHaasGroteskRegular.ttf')
    renderer.addFont('AlteHaasGrotesk-Bold', 'data/AlteHaasGroteskBold.ttf')
    #renderer.renderTemplate(book, 'default')
    for page in book.pages:
        renderer.renderPage(page, 'output/pdf', PdfRenderer.OutputType.PDF, False)

    print("main done")