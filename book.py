import math
from svg import SVG

class Book(object):

    def __init__(self, width_mm, height_mm, dpi = 300):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.dpi = dpi
        self.width_px = self.__px(width_mm) 
        self.height_px = self.__px(height_mm)

        self.pages = []
        self.page_count_offset = 0
        self.page_templates = []
        self.add_page_template('default', margins_mm = [15,15,15,15])

    def __px(self, mm):
        return mm * self.dpi / 25.4

    def __mm(self, px):
        return px * 25.4 / self.dpi

    def add_page_template(self, id, margins_mm = [0,0,0,0]):
        template = {
            'id': id,
            'margins': {
                'inner': self.__px(margins_mm[0]),
                'top': self.__px(margins_mm[1]),
                'outer': self.__px(margins_mm[2]),
                'bottom': self.__px(margins_mm[3]),
            },
            'header': {
                'height': self.__px(15)
            },
            'footer': {
                'height': self.__px(15)
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

    def add_page(self, template = 'default', number = None):
        if number is None:
            number = len(self.pages) - self.page_count_offset + 1
        i = self.page_count_offset + number -1
        page = BookPage(self, template, number, (i % 2) == 0)
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

    def render_template(self, id):
        t = self.get_page_template(id)
        if t is None:
            print(f"ERROR: Page template with id '{id}' does not exist.")
            return
        s = SVG()
        s.create(self.width_px, self.height_px)
        fill = '#DDDDDD'
        stroke = '#000000'
        stroke_width = 2
        # self.content = {
        #     'x': page_template['margins']['inner' if self.is_right else 'outer'],
        #     'y': page_template['margins']['top'],
        #     'w': book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
        #     'h': book.height_px - page_template['margins']['bottom'] - page_template['margins']['top'],
        # }

        s.rectangle(0, 0, self.width_px, self.height_px, fill, None, stroke_width, 0, 0)
        s.rectangle(
            t['margins']['inner'],
            t['margins']['top'] - t['header']['height'],
            self.width_px - t['margins']['inner'] - t['margins']['outer'],
            t['header']['height'],
            fill, stroke, stroke_width, 0, 0)
        s.rectangle(
            t['margins']['inner'],
            self.height_px - t['margins']['bottom'],
            self.width_px - t['margins']['inner'] - t['margins']['outer'],
            t['footer']['height'],
            fill, stroke, stroke_width, 0, 0)
        s.rectangle(
            t['margins']['inner'],
            t['margins']['top'],
            self.width_px - t['margins']['inner'] - t['margins']['outer'],
            self.height_px - t['margins']['top'] - t['margins']['bottom'],
            fill, stroke, stroke_width, 0, 0)
        s.finalize()

        try:
            filename = f"data/template_{id}.svg"
            print(f"Save template rendering to {filename}")
            s.save(filename)
        except IOError as ioe:
            print(ioe)

    
class BookPage(object):

    def __init__(self, book: Book, template, number, is_right):
        self.book = book
        self.template = template
        self.number = number
        self.is_right = is_right

        page_template = book.get_page_template(template)
        self.header = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': page_template['margins']['top'] - page_template['header']['height'],
            'w': book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': page_template['header']['height']
        },
        self.footer = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': book.height_px - page_template['margins']['bottom'],
            'w': book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': page_template['footer']['height']
        },
        self.content = {
            'x': page_template['margins']['inner' if self.is_right else 'outer'],
            'y': page_template['margins']['top'],
            'w': book.width_px - page_template['margins']['inner'] - page_template['margins']['outer'],
            'h': book.height_px - page_template['margins']['bottom'] - page_template['margins']['top'],
        }


class Helpers(object):

    @classmethod
    def to_roman(self, i):
        intToroman = { 1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
              50: 'L', 90: 'XC', 100: 'C', 400: 'XD', 500: 'D', 900: 'CM', 1000: 'M'}
        
        #Descending intger equivalent of seven roman numerals 
        print_order = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

        roman = ""
        for x in print_order:
            if i != 0:
                quotient= i//x

                #If quotient is not zero output the roman equivalent
                if quotient != 0:
                    for y in range(quotient):
                        roman += intToroman[x]

                #update integer with remainder
                i = i%x
        return roman.lower()


if __name__ == '__main__':
    book = Book(200, 220, 300)
    book.add_page()
    book.add_page(number=-1)
    print(book)
    book.render_template('default')
    #print([Helpers.to_roman(i) for i in range(25)])
