from .element import Element

class TableBody(Element):
    """Implements the <tbody> tag"""

    def __init__(self, cl=None, ident=None, style=None, attrs=None):
        super().__init__(cl=cl, ident=ident, style=style, attrs=attrs)

    def __repr__(self):
        return "<TableBody>"

    def __str__(self):
        output = [ "<tbody" ]

        if self.ident:
            output.append(" id=\"")
            output.append(self.ident)
            output.append("\"")

        if self.cl:
            output.append(" class=\"")
            output.append(self.cl)
            output.append("\"")

        if self.style:
            output.append(" style=\"")
            output.append(self.style)
            output.append("\"")

        if self.attrs:
            for k in self.attrs.keys():
                output.append(' ' + k + '="' + self.attrs[k] + '"')

        output.append(">")

        for child in self.children:
            output.append(str(child))

        output.append("</tbody>")

        return "".join(output)
