import reportlab
from book import Book, BookPage
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPM
from enum import Enum

class PdfPage(BookPage):

    def __init__(self, template_id, data, func):
        super().__init__(template_id)
        self.data = data
        self.func = func

    def render(self, pdf_canvas: canvas.Canvas):
        if self.func is not None:
            self.func(pdf_canvas, self, self.book, self.data)

class PdfRenderer(object):

    class OutputType(Enum):
        PDF = 0,
        TIFF = 1,
        PNG = 2

    def __init__(self):
        pass

    def renderTemplate(self, book: Book, id):
        t = book.getPageTemplate(id)
        if t is None:
            print(f"ERROR: Page template with id '{id}' does not exist.")
            return
            
        filename = f"output/template_{id}.pdf"
        c = canvas.Canvas(filename, (book.width_px * 2, book.height_px), 0)
        stroke = Color(0,0,0)
        stroke_width = 2

        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_width)
        c.rect(0, 0, book.width_px * 2, book.height_px)
        c.line(book.width_px, 0, book.width_px, book.height_px)
        
        # left header
        c.rect(
            t['margins']['outer'],
            t['margins']['top'] - t['header']['height'] - t['header']['offset'],
            book.width_px - t['margins']['outer'] - t['margins']['inner'],
            t['header']['height'])
        # left footer
        c.rect(
            t['margins']['outer'],
            book.height_px - t['margins']['bottom'] + t['footer']['offset'],
            book.width_px - t['margins']['outer'] - t['margins']['inner'],
            t['footer']['height'])
        # left content
        c.rect(
            t['margins']['outer'],
            t['margins']['top'],
            book.width_px - t['margins']['outer'] - t['margins']['inner'],
            book.height_px - t['margins']['top'] - t['margins']['bottom'])

        # right header
        c.rect(
            book.width_px + t['margins']['inner'],
            t['margins']['top'] - t['header']['height'] - t['header']['offset'],
            book.width_px - t['margins']['inner'] - t['margins']['outer'],
            t['header']['height'])
        # right footer
        c.rect(
            book.width_px + t['margins']['inner'],
            book.height_px - t['margins']['bottom'] + t['footer']['offset'],
            book.width_px - t['margins']['inner'] - t['margins']['outer'],
            t['footer']['height'])
        # right content
        c.rect(
            book.width_px + t['margins']['inner'],
            t['margins']['top'],
            book.width_px - t['margins']['inner'] - t['margins']['outer'],
            book.height_px - t['margins']['top'] - t['margins']['bottom'])


        c.showPage()
        try:
            print(f"Save template rendering to {filename}")
            c.save()
        except IOError as ioe:
            print(ioe)

    def addFont(self, name, file):
        pdfmetrics.registerFont(TTFont(name, file))

    def renderPage(self, page: PdfPage, output_path, outputType: OutputType, render_meta = False):
        
        book = page.book
        filename = f"{output_path}/page_{page.number}.pdf"
        c = canvas.Canvas(filename, (book.width_px, book.height_px), 0)

        # https://github.com/source-foundry/font-line
        
        if render_meta:
            c.setStrokeColor(Color(0,0,0))
            c.setLineWidth(2)
            c.rect(0, 0, book.width_px, book.height_px)
            metaColor = Color(221,0,0)
            grid_size = book.px(10)
            c.setLineWidth(1)
            c.setStrokeColor(metaColor)
            c.rect(page.content['x'], page.content['y'], page.content['w'], page.content['h'])
            c.setDash(book.px(1), book.px(1))
            x = page.content['x'] + grid_size
            y = page.content['y'] + grid_size
            while y < page.content['y'] + page.content['h']:
                c.line(page.content['x'], y, page.content['x'] + page.content['w'], y)
                y += grid_size
            while x < page.content['x'] + page.content['w']:
                c.line(x, page.content['y'], x, page.content['y'] + page.content['h'])
                x += grid_size

        print(f"Try rende page of type: {type(page)}")
        page.render(c)

        try:
            print(f"Save template rendering to {filename}, as {outputType}")
            if outputType is self.OutputType.PDF:
                c.save()
            # elif outputType is OutputType.TIFF:
            #     renderPM.drawToFile(c, filename, 'TIFF')
            else:
                print(f"Unknown output type: {outputType}")
        except IOError as ioe:
            print(ioe)


if __name__ == '__main__':
    book = Book(200, 220, 72)
    book.page_count_offset = 0
    book.addPage(BookPage('default'))
    book.addPage(BookPage('default'), number=-1) 

    book.addPage(PdfPage('default', {
            'text': "En liten text."
        }, None), number=None)

    book.update()
    print(book)

    c = canvas.Canvas("output/hello.pdf", (book.width_px, book.height_px), 0)

    # https://www.reportlab.com/docs/reportlab-userguide.pdf

    #c.setFont("arial", 12, 1.6)
    c.drawString(100,100,"Hello World")

    # t = c.beginText(150, 150)
    # #t.setFont("Alte Haas Grotesk", 12)
    # t.textLine("En text i olles bok")
    # t.textLine("Två texter i olles bok")
    # c.drawText(t)

    color = Color(0.7,0.3,0.9)
    c.setStrokeColor(color)
    c.rect(0,0,250,200)

    c.setLineWidth(10)
    c.setLineCap(1)
    c.line(10,100,400,400)

    c.setDash(10, 50)
    c.line(10,200,400,500)

    c.drawImage("output/original_frames/frame_0000.jpg", 300, 300, 64*3, 48*3)

    c.showPage()
    c.save()

    # template
    r = PdfRenderer()
    r.renderTemplate(book, 'default')

    # page
    page = book.getPage(3)
    print(type(page))
    r.renderPage(page, 'output', True)
