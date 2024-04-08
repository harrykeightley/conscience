from functools import reduce
import tkinter as tk
from typing import Any, Iterable, Optional, Set, Tuple, Union

from PIL import ImageTk

from .images import image_id_path

Position = tuple[int, int]
"""A position of the form, (row, col)"""

Item = str | int
"""Tkinter tags for canvases"""

Font = tuple[str, int, str]
"""TK font"""


class SerializedGrid:
    EMPTY = " "
    DIVIDER = "|"
    CELL_SPACING = 0

    def __init__(self, grid: tk.Canvas, dimensions: tuple[int, int]) -> None:
        self.grid = grid
        self.dimensions = dimensions

    @classmethod
    def from_cell_size(cls, grid: tk.Canvas, cell_size: tuple[int, int], **kwargs):
        dimensions = SerializedGrid.get_dimensions(grid, cell_size)
        return cls(grid, dimensions, **kwargs)

    @property
    def cell_size(self) -> tuple[int, int]:
        rows, columns = self.dimensions
        cell_width = self.grid.winfo_width() // columns
        cell_height = self.grid.winfo_height() // rows
        return cell_width, cell_height

    @staticmethod
    def get_dimensions(grid: tk.Canvas, cell_size: tuple[int, int]) -> tuple[int, int]:
        cell_width, cell_height = cell_size
        columns = int(grid.winfo_width() // cell_width)
        rows = int(grid.winfo_height() // cell_height)
        return rows, columns

    def get_items_at_position(self, position: Position) -> Tuple[Item, ...]:
        row, col = position
        cell_width, cell_height = self.cell_size
        start_x, start_y = col * cell_width, row * cell_height

        return self.grid.find_enclosed(
            start_x - self.CELL_SPACING,
            start_y - self.CELL_SPACING,
            start_x + cell_width + self.CELL_SPACING,
            start_y + cell_height + self.CELL_SPACING,
        )

    def serialize(self) -> dict[Position, tuple[Item, ...]]:
        rows, columns = self.dimensions
        return {
            (row, column): self.get_items_at_position((row, column))
            for row in range(rows)
            for column in range(columns)
        }

    def _find_item(self, position: Position) -> Optional[Item]:
        items = self.get_items_at_position(position)
        return items[0] if len(items) > 0 else None

    def get_position(self, item: Item) -> list[float]:
        return self.grid.coords(item)

    def _get_item_option(self, item: Item, option: str) -> Optional[Any]:
        try:
            return self.grid.itemcget(item, option)
        except tk.TclError:
            return None

    def get_text_at_position(self, position: Position) -> Optional[str]:
        """Gets the text contained by the first item in the position on the
        canvas, if it exists.
        """
        item = self._find_item(position)
        if item is None:
            return
        return self._get_item_option(item, "text")

    def get_font_at_position(self, position: Position) -> Optional[Font]:
        """Gets the font contained by the first item in the position on the
        canvas, if it exists.
        """
        item = self._find_item(position)
        if item is None:
            return
        return self._get_item_option(item, "font")

    def _identify_item(self, item: Item) -> Optional[str]:
        """A method to overwrite on subclasses, which returns a string which
        identifies an item.
        """
        return self._get_item_option(item, "text")

    def _render_position(self, position: Position) -> str:
        item = self._find_item(position)
        if item is None:
            return self.EMPTY

        text = self._identify_item(item)
        return text if text is not None else self.EMPTY

    def render(self) -> str:
        rows, cols = self.dimensions

        def render_row(row: int) -> str:
            inner = self.DIVIDER.join(
                (self._render_position((row, col)) for col in range(cols))
            )
            return f"{self.DIVIDER}{inner}{self.DIVIDER}\n"

        return "".join(map(render_row, range(rows)))

    def to_item_dict(self) -> dict[tuple[int, int], Any]:
        result = {}
        for item in self.grid.find_all():
            x, y = self.grid.coords(item)
            result[(x, y)] = self._identify_item(item)

        return result

    def debug(self):
        return self.to_item_dict()


class ImageGrid(SerializedGrid):
    """ImageGrid handles one layer of images over a canvas."""

    def __init__(
        self,
        grid: tk.Canvas,
        dimensions: tuple[int, int],
        cache: dict[str, ImageTk.PhotoImage],
        translations: dict[str, str],
    ) -> None:
        """Constructs a new ImageGrid for the given cache and set of translations.

        Parameters:
            grid: The canvas to inspect
            cell_size: A tuple of [rows, cols] containing the canvas dimensions.
            cache: A mapping from image paths to the corresponding images.
            translations: A mapping from image paths to their shortened symbols.
                The provided keys form a 'layer'.
        """
        super().__init__(grid, dimensions)
        self.cache = cache
        self.translations = translations

    @property
    def layer(self) -> Set[str]:
        return {path for path in self.translations}

    @property
    def layer_items(self) -> Iterable[Item]:
        items = []
        for _items in self.serialize().values():
            items.extend(_items)
        return self._layer_filter(items)

    def _identify_item(self, item) -> Optional[str]:
        image_id = self._get_item_option(item, "image")
        if image_id is None:
            return None

        path = image_id_path(self.cache, image_id)
        if path not in self.layer:
            return None

        return self.translations.get(path)

    def _layer_filter(self, items: Iterable[Item]) -> Iterable[Item]:
        return filter(lambda item: self._identify_item(item) is not None, items)

    def _find_item(self, position: Position) -> Optional[Item]:
        items = list(self._layer_filter(self.get_items_at_position(position)))
        return items[0] if len(items) > 0 else None

    def _overlaps(self, items: Iterable[Item]):
        """Returns true iff 2 items of the supplied iterable have overlapping
        images of this classes' layer.
        """
        layer_items = list(self._layer_filter(items))
        return len(layer_items) > 1

    def has_duplicates(self) -> bool:
        """Returns true iff any 2 images of the same layer overlap in the grid"""
        return any(self._overlaps(items) for items in self.serialize().values())

    def get_image_symbol_at_position(self, position: Position) -> Optional[str]:
        item = self._find_item(position)
        if item is None:
            return None
        return self._identify_item(item)

    def __len__(self) -> int:
        return len(list(self.layer_items))
