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
        self.add_page_template('default', margins_mm = [20,20,15,15], header_mm = [10, 3], footer_mm = [10, 3])

    def px(self, mm):
        return mm * self.dpi / 25.4

    def mm(self, px):
        return px * 25.4 / self.dpi

    def add_page_template(self, id, margins_mm = [0,0,0,0], header_mm = [0, 0], footer_mm = [0, 0]):
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

    def get_page_template(self, id):
        return next((t for t in self.page_templates if t['id'] == id), None)

    def __update_page_numbers(self):
        for i in range(len(self.pages)):
            number = i - self.page_count_offset + 1
            self.pages[i].number = number

    def add_page(self, page, number = None):
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
        self.__update_page_numbers()
        return page

    def get_page(self, number):
        i = self.page_count_offset + number -1
        return self.pages[i]

    def __get_number(self, i):
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
            out += f"\n    [     | {self.__get_number(i)} ]"
            i += 1
        while i < len(self.pages):
            out += f"\n    [ {self.__get_number(i)} | {self.__get_number(i+1)} ]"
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

    def update(self):
        page_template = self.book.get_page_template(self.template_id)
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

class TestPage(BookPage):

    def __init__(self, template_id, text, func):
        super().__init__(template_id)
        self.text = text
        self.func = func

    def render(self):
        self.func(self.text, self.content)
        return


if __name__ == '__main__':
    book = Book(200, 220, 300)
    book.page_count_offset = 0
    book.add_page(BookPage('default'))
    book.add_page(BookPage('default'), number=-1)
    book.add_page(TestPage('default', "En liten text.", lambda text, book: {
        
    }), number=-1)
    book.update()
    print(book)
    #book.render_template('default')
    #print([Helpers.to_roman(i) for i in range(25)])
    #book.render_page(0)

    f = lambda text: {
        print(text)
    }
    f("text test")
