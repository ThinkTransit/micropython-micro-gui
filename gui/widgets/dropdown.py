# dropdown.py Extension to ugui providing the Dropdown class

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021 Peter Hinch

from gui.core.ugui import Widget, display, Window, Screen
from gui.core.colors import *

from gui.widgets.listbox import Listbox

dolittle = lambda *_ : None

# Next and Prev close the listbox without updating the Dropdown. This is
# handled by Screen .move bound method
class _ListDialog(Window):

    def __init__(self, writer, row, col, dropdown, textwidth):
        dd = dropdown
        elements = dd.elements
        # Need to determine Window dimensions from size of Listbox, which
        # depends on number and length of elements.
        entry_height, lb_height, textwidth = Listbox.dimensions(writer, elements)
        lb_width = textwidth + 2
        # Calculate Window dimensions
        ap_height = lb_height + 6  # Allow for listbox border
        ap_width = lb_width + 6
        super().__init__(row, col, ap_height, ap_width)
        self.listbox = Listbox(writer, row + 3, col + 3, elements = elements, width = lb_width,
                               fgcolor = dd.fgcolor, bgcolor = dd.bgcolor, bdcolor=False, 
                               fontcolor = WHITE, select_color = dd.select_color,
                               value = dd.value(), callback = self.callback)
        self.dropdown = dd

    def callback(self, obj_listbox):
        Screen.back()
        self.dropdown.value(obj_listbox.value()) # Update it


class Dropdown(Widget):
    def __init__(self, writer, row, col, *, elements, width=None, value=0,
                 fgcolor=None, bgcolor=None, bdcolor=False, fontcolor=None, select_color=DARKBLUE,
                 callback=dolittle, args=[]):

        self.entry_height = writer.height + 2 # Allow a pixel above and below text
        height = self.entry_height
        if width is None:  # Allow for square at end for arrow
            self.textwidth = max(writer.stringlen(s) for s in elements)
            width = self.textwidth + 2 + height
        else:
            self.textwidth = width
        super().__init__(writer, row, col, height, width, fgcolor, bgcolor, bdcolor, value, True)
        super()._set_callbacks(callback, args)
        self.select_color = select_color
        self.fontcolor = self.fgcolor if fontcolor is None else fontcolor
        self.elements = elements

    def show(self):
        if super().show():
            x, y = self.col, self.row
            self._draw(x, y)
            if self._value is not None:
                display.print_left(self.writer, x, y + 1, self.elements[self._value], self.fontcolor)

    def textvalue(self, text=None): # if no arg return current text
        if text is None:
            return self.elements[self._value]
        else: # set value by text
            try:
                v = self.elements.index(text)
            except ValueError:
                v = None
            else:
                if v != self._value:
                    self.value(v)
            return v

    def _draw(self, x, y):
        self.draw_border()
        display.vline(x + self.width - self.height, y, self.height, self.fgcolor)
        xcentre = x + self.width - self.height // 2 # Centre of triangle
        ycentre = y + self.height // 2
        halflength = (self.height - 8) // 2
        length = halflength * 2
        if length > 0:
            display.hline(xcentre - halflength, ycentre - halflength, length, self.fgcolor)
            display.line(xcentre - halflength, ycentre - halflength, xcentre, ycentre + halflength, self.fgcolor)
            display.line(xcentre + halflength, ycentre - halflength, xcentre, ycentre + halflength, self.fgcolor)

    def do_sel(self):  # Select was pushed
        if len(self.elements) > 1:
            args = (self.writer, self.row - 2, self.col - 2, self, self.textwidth)
            Screen.change(_ListDialog, args = args)