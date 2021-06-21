import reportlab
from book import Book, BookPage
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

class PdfPage(BookPage):

    def __init__(self, template_id, data, func):
        super().__init__(template_id)
        self.data = data
        self.func = func

    def render(self, svg):
        self.func(svg, self, self.book, self.data)
        return


class PdfRenderer(object):

    def render_template(self, book: Book, id):
        t = book.get_page_template(id)
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


    def render_page(self, page: PdfPage, output_path, render_meta = False):
        
        book = page.book
        filename = f"{output_path}/page_{page.number}.pdf"
        c = canvas.Canvas(filename, (book.width_px * 2, book.height_px), 0)

        # https://github.com/source-foundry/font-line
        
        font_size = book.px(12) * 0.5
        line_height = font_size * 1.5
        line = 0
        lines = math.floor((page.content['h'] + (line_height - font_size)) / line_height)
        # s.add_font('default', 'Alte Haas Grotesk', font_size, line_height)
        # s.create(book.width_px, book.height_px)
        # fill = '#E5D8C0'
        strokeColor = Color(0,0,0)
        metaColor = Color(221,0,0)
        stroke_width = 2

        c.setStrokeColor(strokeColor)
        c.setLineWidth(stroke_width)
        c.rect(0, 0, book.width_px, book.height_px)
        if render_meta:
            c.setLineWidth(1)
            c.setStrokeColor(metaColor)
            c.rect(page.content['x'], page.content['y'], page.content['w'], page.content['h'])
            c.setDash(book.px(1), book.px(1))
            for l in range(lines):
                y = page.content['y'] - (line_height-font_size) * 0.8 + (l+1) * (line_height - 0.1)
                #y = page.content['y'] + (l+1) * line_height
                c.line(page.content['x'], y, page.content['x'] + page.content['w'], y)
        # s.text_box(page.content['x'], page.content['y'], page.content['w'], page.content['h'],
        #     ' '.join(["mkgÅjl"] * 100), 'default')
        #s.text_box(page.content['x'], page.content['y'], page.content['w'], page.content['h'],
        #    "En lång rackarns text, som strävar så ivrigt efter högerkanten att den förlorar fästet och, på grund av bredden, landar till vänster.", 'default')
        #s.text(0, 0, "Hello World", 'default')

        #print(f"Try rende page of type: {type(page)}")
        #page.render(s)

        try:
            print(f"Save template rendering to {filename}")
            c.save()
        except IOError as ioe:
            print(ioe)


if __name__ == '__main__':
    book = Book(200, 220, 72)
    book.page_count_offset = 0
    book.add_page(BookPage('default'))
    book.add_page(BookPage('default'), number=-1) 

    book.add_page(PdfPage('default', {
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
    r.render_template(book, 'default')

    # page
    page = book.get_page(3)
    print(type(page))
    r.render_page(page, 'output', True)