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


# class PdfRenderer(object):

    # def render_template(self, book: Book, id):
    #     t = book.get_page_template(id)
    #     if t is None:
    #         print(f"ERROR: Page template with id '{id}' does not exist.")
    #         return
    #     s = SVG()
    #     s.create(book.width_px * 2, book.height_px)
    #     fill = '#E5D8C0'
    #     stroke = '#000000'
    #     stroke_width = 2

    #     s.rectangle(0, 0, book.width_px * 2, book.height_px, fill, None, stroke_width, 0, 0)
    #     s.line(book.width_px, 0, book.width_px, book.height_px, stroke, stroke_width)
        
    #     # left header
    #     s.rectangle(
    #         t['margins']['outer'],
    #         t['margins']['top'] - t['header']['height'] - t['header']['offset'],
    #         book.width_px - t['margins']['outer'] - t['margins']['inner'],
    #         t['header']['height'],
    #         fill, stroke, stroke_width, 0, 0)
    #     # left footer
    #     s.rectangle(
    #         t['margins']['outer'],
    #         book.height_px - t['margins']['bottom'] + t['footer']['offset'],
    #         book.width_px - t['margins']['outer'] - t['margins']['inner'],
    #         t['footer']['height'],
    #         fill, stroke, stroke_width, 0, 0)
    #     # left content
    #     s.rectangle(
    #         t['margins']['outer'],
    #         t['margins']['top'],
    #         book.width_px - t['margins']['outer'] - t['margins']['inner'],
    #         book.height_px - t['margins']['top'] - t['margins']['bottom'],
    #         fill, stroke, stroke_width, 0, 0)

    #     # right header
    #     s.rectangle(
    #         book.width_px + t['margins']['inner'],
    #         t['margins']['top'] - t['header']['height'] - t['header']['offset'],
    #         book.width_px - t['margins']['inner'] - t['margins']['outer'],
    #         t['header']['height'],
    #         fill, stroke, stroke_width, 0, 0)
    #     # right footer
    #     s.rectangle(
    #         book.width_px + t['margins']['inner'],
    #         book.height_px - t['margins']['bottom'] + t['footer']['offset'],
    #         book.width_px - t['margins']['inner'] - t['margins']['outer'],
    #         t['footer']['height'],
    #         fill, stroke, stroke_width, 0, 0)
    #     # right content
    #     s.rectangle(
    #         book.width_px + t['margins']['inner'],
    #         t['margins']['top'],
    #         book.width_px - t['margins']['inner'] - t['margins']['outer'],
    #         book.height_px - t['margins']['top'] - t['margins']['bottom'],
    #         fill, stroke, stroke_width, 0, 0)

    #     s.finalize()

    #     try:
    #         filename = f"output/template_{id}.svg"
    #         print(f"Save template rendering to {filename}")
    #         s.save(filename)
    #     except IOError as ioe:
    #         print(ioe)


    # def render_page(self, page: SvgPage, output_path, render_meta = False):
    #     s = SVG()
    #     book = page.book

    #     # https://github.com/source-foundry/font-line
        
    #     font_size = book.px(12) * 0.5
    #     line_height = font_size * 1.5
    #     line = 0
    #     lines = math.floor((page.content['h'] + (line_height - font_size)) / line_height)
    #     s.add_font('default', 'Alte Haas Grotesk', font_size, line_height)
    #     s.create(book.width_px, book.height_px)
    #     fill = '#E5D8C0'
    #     stroke = '#000000'
    #     stroke_width = 2

    #     s.rectangle(0, 0, book.width_px, book.height_px, fill, None, stroke_width, 0, 0)
    #     if render_meta:
    #         s.new_group()
    #         s.rectangle(page.content['x'], page.content['y'], page.content['w'], page.content['h'], fill, '#DD0000', stroke_width, 0, 0)
    #         for l in range(lines):
    #             y = page.content['y'] - (line_height-font_size) * 0.8 + (l+1) * (line_height - 0.1)
    #             #y = page.content['y'] + (l+1) * line_height
    #             s.line(page.content['x'], y, page.content['x'] + page.content['w'], y, '#DD0000', stroke_width, dashes = book.px(1))
    #         s.end_group()
    #     # s.text_box(page.content['x'], page.content['y'], page.content['w'], page.content['h'],
    #     #     ' '.join(["mkgÅjl"] * 100), 'default')
    #     #s.text_box(page.content['x'], page.content['y'], page.content['w'], page.content['h'],
    #     #    "En lång rackarns text, som strävar så ivrigt efter högerkanten att den förlorar fästet och, på grund av bredden, landar till vänster.", 'default')
    #     #s.text(0, 0, "Hello World", 'default')

    #     print(f"Try rende page of type: {type(page)}")
    #     page.render(s)

    #     s.finalize()

    #     try:
    #         filename = f"{output_path}/page_{page.number}.svg"
    #         print(f"Save template rendering to {filename}")
    #         s.save(filename)
    #     except IOError as ioe:
    #         print(ioe)


if __name__ == '__main__':
    book = Book(200, 220, 72)
    book.page_count_offset = 0
    book.add_page(BookPage('default'))
    book.add_page(BookPage('default'), number=-1) 

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
