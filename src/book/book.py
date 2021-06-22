import math

class Book(object):

    def __init__(self, width_mm, height_mm, dpi = 300):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.dpi = dpi
        self.width_px = self.px(width_mm) 
        self.height_px = self.px(height_mm)
        self.odd_right = True

        self.pages = []
        self.page_count_offset = 0
        self.page_templates = []
        self.addPageTemplate('default', margins_mm = [15,15,15,15], header_mm = [10, 3], footer_mm = [10, 3])

    def px(self, mm):
        return mm * self.dpi / 25.4

    def mm(self, px):
        return px * 25.4 / self.dpi

    def addPageTemplate(self, id, margins_mm = [0,0,0,0], header_mm = [0, 0], footer_mm = [0, 0]):
        template = {
            'id': id,
            'margins': {
                'inner': self.px(margins_mm[0]),
                'top': self.px(margins_mm[1]),
                'outer': self.px(margins_mm[2]),
                'bottom': self.px(margins_mm[3]),
            },
            'header': {
                'height': self.px(header_mm[0]),
                'offset': self.px(header_mm[1])
            },
            'footer': {
                'height': self.px(footer_mm[0]),
                'offset': self.px(footer_mm[1])
            }
        }
        for i in range(0, len(self.page_templates), -1):
            if self.page_templates[i]['id'] == template['id']:
                self.page_templates.pop(i)
        self.page_templates.append(template)

    def getPageTemplate(self, id):
        return next((t for t in self.page_templates if t['id'] == id), None)

    def __updatePageNumbers(self):
        for i in range(len(self.pages)):
            number = i - self.page_count_offset + 1
            self.pages[i].number = number

    def addPage(self, page, number = None):
        page.book = self
        if number is None:
            number = len(self.pages) - self.page_count_offset + 1
        i = self.page_count_offset + number -1
        if i >= len(self.pages):
            self.pages.append(page)
        elif i < 0:
            self.pages.insert(len(self.pages) + i, page)
        else:
            self.pages.insert(i, page)
        self.__updatePageNumbers()
        return page

    def getPage(self, number):
        i = self.page_count_offset + number -1
        return self.pages[i]

    def __getNumber(self, i):
        if i >= len(self.pages):
            return '   '
        return f"{self.pages[i].number:03}" if self.pages[i].number > 0 else '  x'

    def update(self):
        for i in range(self.page_count_offset, len(self.pages)):
            self.pages[i].is_right = (i - self.page_count_offset + 1) % 2 != (0 if self.odd_right else 1)
        for i in range(self.page_count_offset-1, -1, -1):
            self.pages[i].is_right = (not self.pages[i+1].is_right) if (i+1 < len(self.pages)) else not self.odd_right
        for i in range(len(self.pages)):
            self.pages[i].update()


    def __str__(self) -> str:
        out = f"Book of size {self.width_mm}mm x {self.height_mm}mm @ {self.dpi} dpi"
        out += f"\n  {len(self.pages)} pages:\n  [" #{[p.number if p.number > 0 else 'x' for p in self.pages]}"
        i = 0
        if self.pages[i].is_right:
            out += f"\n    [     | {self.__getNumber(i)} ]"
            i += 1
        while i < len(self.pages):
            out += f"\n    [ {self.__getNumber(i)} | {self.__getNumber(i+1)} ]"
            i += 2
        out += f"\n  ]"
        out += f"\n  {len(self.page_templates)} page templates"
        return out


class BookPage(object):

    def __init__(self, template_id):
        self.book = None
        self.template_id = template_id
        self.number = None
        self.is_right = None
        self.header = None
        self.footer = None
        self.content = None

    def xContent(self, x_mm):
        if x_mm >= 0:
            return self.content['x'] + self.book.px(x_mm)
        return self.content['x'] + self.content['w'] + self.book.px(x_mm)
    def yContent(self, y_mm):
        if y_mm >= 0:
            return self.content['y'] + self.book.px(y_mm)
        return self.content['y'] + self.content['h'] + self.book.px(y_mm)

    def update(self):
        page_template = self.book.getPageTemplate(self.template_id)
        self.header = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': page_template['margins']['top'] - page_template['header']['height'],
            'w': self.book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': page_template['header']['height']
        },
        self.footer = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': self.book.height_px - page_template['margins']['bottom'],
            'w': self.book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': page_template['footer']['height']
        },
        self.content = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': page_template['margins']['top'],
            'w': self.book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': self.book.height_px - page_template['margins']['bottom'] - page_template['margins']['top'],
        }
    
    def render(self):
        return
        

if __name__ == '__main__':
    book = Book(200, 220, 300)
    book.page_count_offset = 0
    book.addPage(BookPage('default'))
    book.addPage(BookPage('default'), number=-1)
    book.update()
    print(book)
    #book.render_template('default')
    #print([Helpers.to_roman(i) for i in range(25)])
    #book.render_page(0)

    f = lambda text: {
        print(text)
    }
    f("text test")
