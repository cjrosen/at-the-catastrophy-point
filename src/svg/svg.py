
class SVGFont(object):

    def __init__(self, id, family, size, line_height = 1.2):
        self.id = id
        self.family = family
        self.size = size
        self.weight = 'normal'
        self.style = 'normal'
        self.stroke = None
        self.color = '#000000'
        self.line_height = line_height

    def italic(self, enabled = True):
        self.style = 'italic'
        return self

    def bold(self, enabled = True):
        self.weight = 'bold'
        return self

    def color(self, color):
        self.color = color
        return self


class SVG(object):

    """
    Provides methods for creating an empty SVG drawing, adding various
    shapes and text, and saving the finished file.
    """

    def __init__(self):

        """
        Create a few attributes with default values,
        and initialize the templates dictionary.
        """

        self.svg_list = []
        self.width = 0
        self.height = 0

        self.templates = self.__generate_templates()

        self.fonts = []
        self.current_hierarchy = []
        self.indentation = '  '

    def __add_to_svg(self, text):

        """
        Utility function to add element to drawing.
        """

        self.svg_list.append(str(text))

    def __get_indentation(self):
        
        """
        Get indentation spaces for current level
        """

        return self.indentation * len(self.current_hierarchy)

    def __generate_templates(self):

        """
        Create a set of templates for each element type for use by
        methods creating each of these types.
        """

        templates = {}

        templates["svg_begin"] = "{}<svg width='{}px' height='{}px' xmlns='http://www.w3.org/2000/svg' version='1.1' xmlns:xlink='http://www.w3.org/1999/xlink'>\n"
        templates["svg_end"] = "{}</svg>\n"
        templates["circle"] = "{}<circle stroke='{}' stroke-width='{}px' fill='{}' r='{}' cy='{}' cx='{}' />\n"
        templates["line"] = "{}<line x1='{}' y1='{}' x2='{}' y2='{}' stroke='{}' stroke-width='{}px' stroke-linecap='{}' stroke-dasharray='{}'/>\n"
        templates["rectangle"] = "{}<rect fill='{}' stroke='{}' stroke-width='{}px' width='{}' height='{}' y='{}' x='{}' ry='{}' rx='{}' />\n"
        templates["text"] = "{}<text x='{}' y = '{}' font-family='{}' font-weight='{}' font-style='{}' stroke='{}' fill='{}' font-size='{}px'>{}</text>\n"
        templates["text_box"] = "\
{indent}<foreignObject x='{x}' y='{y}' width='{width}' height='{height}' style='font-family: {font_family}; font-size: {font_size}px; font-color: {font_color}; line-height: {line_height}px;'>\n\
{indent}  <p xmlns='http://www.w3.org/1999/xhtml'>{text}</p>\n\
{indent}</foreignObject>"
        templates["ellipse"] = "{}<ellipse cx='{}' cy='{}' rx='{}' ry='{}' fill='{}' stroke='{}' stroke-width='{}' />\n"
        templates["group_begin"] = "{}<g>\n"
        templates["group_end"] = "{}</g>\n"

        return templates

    def create(self, width, height):

        """
        Adds the necessary opening element to document.
        """

        self.width = width
        self.height = height

        self.svg_list.clear()

        self.__add_to_svg(self.templates["svg_begin"].format(self.__get_indentation(), width, height))
        self.current_hierarchy.append('svg')

    def finalize(self):

        """
        Closes the SVG element.
        """

        while len(self.current_hierarchy) > 0:
            open_item = self.current_hierarchy.pop()
            self.__add_to_svg(self.templates[f"{open_item}_end"].format(self.__get_indentation()))

    def new_group(self):

        """
        Insert beginning of new group
        """

        self.__add_to_svg(self.templates["group_begin"].format(self.__get_indentation()))
        self.current_hierarchy.append('group')

    def end_group(self):

        """
        End a group
        TODO: finalize until next group item level?
        """

        open_item = self.current_hierarchy.pop()
        if open_item != 'group':
            print(f"Warning: current open item is not what you're trying to close: {open_item} != 'group")
        self.__add_to_svg(self.templates["group_end"].format(self.__get_indentation()))


    """
    Fonts
    """

    def __get_font(self, font_id):
        return next((font for font in self.fonts if font.id == font_id), None)

    def add_font(self, id, fontfamily, fontsize, line_height = 1.2, weight = 'normal', style = 'normal', color = '#000000', stroke = 'None'):
        font = SVGFont(id, fontfamily, fontsize, line_height)
        print(type(font))
        font.color = color
        font.weight = weight
        font.style = style
        font.stroke = stroke

        self.fonts.append(font)


    """
    Items
    """

    def circle(self, stroke, strokewidth, fill, r, cx, cy):

        """
        Adds a circle using the method's arguments.
        """

        self.__add_to_svg(self.templates["circle"].format(self.__get_indentation(), stroke, strokewidth, fill, r, cy, cx))

    def line(self, x1, y1, x2, y2, stroke, strokewidth, dashes = 'None', linecap = 'round'):

        """
        Adds a line using the method's arguments.
        """

        self.__add_to_svg(self.templates["line"].format(self.__get_indentation(), x1, y1, x2, y2, stroke, strokewidth, linecap, dashes))

    def rectangle(self, x, y, width, height, fill, stroke, strokewidth, radiusx, radiusy):

        """
        Adds a rectangle using the method's arguments.
        """

        self.__add_to_svg(self.templates["rectangle"].format(self.__get_indentation(), fill, stroke, strokewidth, width, height, y, x, radiusy, radiusx))

    def fill(self, Fill):

        """
        Fills the entire drawing with specified Fill.
        """

        self.rectangle(self.width, self.height, 0, 0, Fill, Fill, 0, 0, 0)

    def text_box(self, x, y, width, height, text, font_id):

        """
        Adds text using the method's arguments.
        """

        font = self.__get_font(font_id)
        if font is not None:
            self.__add_to_svg(self.templates["text_box"].format(
                indent = self.__get_indentation(), 
                x = x, y = y, width = width, height = height, 
                font_family = font.family, font_size = font.size, font_color = font.color, line_height = font.line_height, 
                text = text))
                # font.weight, font.style, font.stroke, font.fill,

    def text(self, x, y, text, font_id):

        """
        Adds text using a predefined font.
        """
        font = self.__get_font(font_id)
        if font is not None:
            self.__add_to_svg(self.templates["text"].format(self.__get_indentation(), x, y, font.family, font.weight, font.style, font.stroke, font.color, font.size, text))

    def ellipse(self, cx, cy, rx, ry, fill, stroke, strokewidth):

        """
        Adds ellipse using the method's arguments.
        """

        self.__add_to_svg(self.templates["ellipse"].format(self.__get_indentation(), cx, cy, rx, ry, fill, stroke, strokewidth))


    """
    Output stuff
    """

    def __str__(self):

        """
        Returns the entire drawing by joining list elements.
        """

        return("".join(self.svg_list))

    def save(self, path):

        """
        Saves the SVG drawing to specified path.
        Let any exceptions propagate up to calling code.
        """

        f = open(path, "w+")
        f.write(str(self))
        f.close()
