from difflib import ndiff
from behave import *
from .identify import *
from .formats import RelativePosition, register_formats

register_formats()


def assertEquals(expected, actual):
    assert actual == expected, "\n" + "".join(ndiff(actual.splitlines(keepends=True), expected.splitlines(keepends=True)))

@then("I see text displaying, roughly, \"{text:Text}\"")
def rough_text(context, text):
    search_for = text.lower().strip()
    widgets = find_widgets(WidgetSelector.by_rough_text(search_for), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget roughly matching the text \"{text}\", found {widgets}"
    context.last = widgets[0]


@then("I see text displaying, exactly, {text:Text}")
def exact_text(context, text):
    widgets = find_widgets(WidgetSelector.by_text(text), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget exactly matching the text \"{text}\", found {widgets}"
    context.last = widgets[0]


@then("it is {position:RelativePosition} all other widgets")
def relative_to_all(context, position):
    widgets = find_widgets(WidgetSelector.all(), context.window)
    it: tk.Widget = context.last
    its_position = it.winfo_x(), it.winfo_y()

    for widget in widgets:
        position = widget.winfo_x(), it.winfo_y()
        if position == RelativePosition.Left:
            assert its_position[0] < position[0], f"{widget} is further left than {it}"
        elif position == RelativePosition.Right:
            assert its_position[0] > position[0], f"{widget} is further right than {it}"
        elif position == RelativePosition.Above:
            assert its_position[1] < position[1], f"{widget} is above {it}"
        elif position == RelativePosition.Below:
            assert its_position[1] > position[1], f"{widget} is below {it}"


class SerializedGrid:
    CELL_SPACING = 0

    def __init__(self, grid: tk.Canvas):
        self.grid = grid

    def orient(self):
        """
        Attempt to orient the grid based on a known fixed point
        
        Fails via assert and returns None if unable to orient.
        Returns the pixel x and y size of the grid cells.
        """
        pass

    def get_cell_size(self):
        return self.orient()
    
    def get_grid_dimensions(self):
        x_size, y_size = self.orient()
        columns = int(self.grid.winfo_width() // x_size)
        rows = int(self.grid.winfo_height() // y_size)
        return columns, rows

    def get_all_at_position(self, x, y):
        x_size, y_size = self.orient()
        return self._get_all_at_position(x_size, y_size, x, y)

    def _get_all_at_position(self, x_size, y_size, x, y):
        start_x, start_y = x * x_size, y * y_size

        return self.grid.find_enclosed(
            start_x - self.CELL_SPACING,
            start_y - self.CELL_SPACING,
            start_x + x_size + self.CELL_SPACING,
            start_y + y_size + self.CELL_SPACING
        )

    def serialize(self):
        x_size, y_size = self.orient()

        columns = int(self.grid.winfo_width() // x_size)
        rows = int(self.grid.winfo_height() // y_size)

        serialized = {}
        for row in range(rows):
            for column in range(columns):
                in_position = self._get_all_at_position(x_size, y_size, column, row)

                serialized[(column, row)] = in_position

        return serialized, (rows, columns)

    def get_position(self, item):
        return self.grid.coords(item)

    def _identify_item(self, item):
        try:
            return self.grid.itemcget(item, "text")
        except tk.TclError:
            return None

    def get_at_position(self, x, y):
        serialized, _ = self.serialize()

        return self._get_at_position(serialized, x, y)

    def _get_at_position(self, serialized, x, y):
        cell_ids = serialized.get((x, y), [])
        for cell in cell_ids:
            text = self._identify_item(cell)
            if text:
                return text
        return None

    def render(self):
        output = ""

        serialized, dimensions = self.serialize()
        for row in range(dimensions[0]):
            for column in range(dimensions[1]):
                label = self._get_at_position(serialized, column, row) or " "
                output += f"|{label}"
                # output += f"{cell_id} "
            output += "|\n"
        
        return output

    def to_item_dict(self):
        result = {}

        for item in self.grid.find_all():
            x, y = self.grid.coords(item)
            result[(x, y)] = self._identify_item(item)

        return result

    def debug(self):
        return self.to_item_dict()
