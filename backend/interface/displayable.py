class Displayable:
    """
    Used to store the value of a displayable element, as well as the formatting options for that element
    To be used by the GUI to display the element
    Attributes may be left to None if the GUI should use the default formatting options
    """

    def __init__(self, value, background_color=None, font=None, font_size=None, font_style=None, alignment=None,
                 wordwrap=None, textformat=None):
        self.value = value
        if background_color is None:
            self.background_color = "#fffffff"
        else:
            self.background_color = background_color
        self.font = font
        self.font_size = font_size
        self.font_style = font_style
        self.alignment = alignment
        self.word_wrap = wordwrap
        self.text_format = textformat

    def get_text_color(self):
        """Determined black or white from the background color to avoid contrast issues"""
        r, g, b = int(self.background_color[1:3], 16), int(self.background_color[3:5], 16), int(
            self.background_color[5:7], 16)
        luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        return '#000000' if luminance > 0.5 else '#ffffff'

    def set_background_color(self, color):
        self.background_color = color

    def set_font(self, font):
        self.font = font

    def set_font_size(self, size):
        self.font_size = size

    def set_font_weight(self, weight):
        self.font_style = weight

    def set_alignment(self, alignment):
        self.alignment = alignment

    def set_word_wrap(self, wordwrap):
        self.word_wrap = wordwrap

    def set_text_format(self, textformat):
        self.text_format = textformat

    def get_background_color(self):
        return self.background_color

    def __str__(self):
        if isinstance(self.value, (list, dict)):
            return str(self.value)
        else:
            return self.value

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Category(Displayable):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def nb_of_categories(dict_of_elements):
        return len(dict_of_elements.keys())

    @staticmethod
    def get_colors():
        return ['#e6194b', '#3cb44b', '#ffe119', '#0082c8',
                '#f58231', '#911eb4', '#46f0f0', '#f032e6',
                '#d2f53c', '#fabebe', '#008080', '#e6beff',
                '#aa6e28', '#fffac8', '#800000', '#aaffc3']

    def to_dict(self):
        return {'value': self.value, 'background_color': self.background_color, 'text_color': self.get_text_color()}

