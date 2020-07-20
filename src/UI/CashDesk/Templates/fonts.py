import Templates.references as REFS

class Fonts():
    FAMILY = "Helvetica"
    BOLD = "bold"
    ITALIC = "italic"

    SIZES = [
        "8",  # XXXXS
        "10", # XXXS
        "12", # XXS
        "14", # XS
        "16", # S
        "18", # M
        "20", # L
        "22", # XL
        "24", # XXL
        "26", # XXXL
        "32", # XXXXL
        "40"  # XXXXXL
    ]

    @staticmethod
    def xxxxsmall(bold: bool = False, italic: bool = False):
        return Fonts._get_font(0, bold, italic)

    @staticmethod
    def xxxsmall(bold: bool = False, italic: bool = False):
        return Fonts._get_font(1, bold, italic)

    @staticmethod
    def xxsmall(bold: bool = False, italic: bool = False):
        return Fonts._get_font(2, bold, italic)

    @staticmethod
    def xsmall(bold: bool = False, italic: bool = False):
        return Fonts._get_font(3, bold, italic)

    @staticmethod
    def small(bold: bool = False, italic: bool = False):
        return Fonts._get_font(4, bold, italic)

    @staticmethod
    def medium(bold: bool = False, italic: bool = False):
        return Fonts._get_font(5, bold, italic)

    @staticmethod
    def large(bold: bool = False, italic: bool = False):
        return Fonts._get_font(6, bold, italic)

    @staticmethod
    def xlarge(bold: bool = False, italic: bool = False):
        return Fonts._get_font(7, bold, italic)

    @staticmethod
    def xxlarge(bold: bool = False, italic: bool = False):
        return Fonts._get_font(8, bold, italic)

    @staticmethod
    def xxxlarge(bold: bool = False, italic: bool = False):
        return Fonts._get_font(9, bold, italic)

    @staticmethod
    def xxxxlarge(bold: bool = False, italic: bool = False):
        return Fonts._get_font(10, bold, italic)

    @staticmethod
    def xxxxxlarge(bold: bool = False, italic: bool = False):
        return Fonts._get_font(11, bold, italic)

    @staticmethod
    def _get_font(size_index: int, bold: bool = False, italic: bool = False):
        if REFS.MOBILE:
            size_index = size_index - 3

            if size_index < 0:
                size_index = 0

        style = ""

        if bold or italic:
            if bold:
                style = style + "bold"
            if italic:
                if bold:
                    style = style + " "
                style = style + "italic"

        if style == "":
            return (Fonts.FAMILY, Fonts.SIZES[size_index])
        else:
            return (Fonts.FAMILY, Fonts.SIZES[size_index], style)
