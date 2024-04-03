import tkinter as tk
from tkinter import messagebox

"""
A model of a Hacker puzzle game where the player must collect
enough green blobs whilst destroying red blobs to win game.
"""
from typing import Tuple, Optional, Dict, List
import random


PLAYER = "P"
COLLECTABLE = "C"
DESTROYABLE = "D"
BLOCKER = "B"
BOMB = "O"

MOVE = (0, -1)
FIRE = (0, 1)
ROTATIONS = ((-1, 0), (1, 0))
SPLASH = ((0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0))
LEFT = "A"
RIGHT = "D"
DIRECTIONS = (LEFT, RIGHT)
COLLECTION_TARGET = 7
COLLECT = "RETURN"
DESTROY = "SPACE"
SHOT_TYPES = (DESTROY, COLLECT)

ENTITY_TYPES = (COLLECTABLE, DESTROYABLE)
MAP_WIDTH = MAP_HEIGHT = 400
SCORE_WIDTH = 200
BAR_HEIGHT = 150

TASK = 2
TITLE = "HACKER"
COLOURS = {
    COLLECTABLE: "#9FD7D5",
    DESTROYABLE: "#F93A3A",
    BLOCKER: "#B2B2B2",
    PLAYER: "#A482DB",
    BOMB: "#FF7324",
}

ZONE = "#2D3332"
SCORE_COLOUR = "#332027"

IMAGES = {
    COLLECTABLE: "C.png",
    DESTROYABLE: "D.png",
    BLOCKER: "B.png",
    PLAYER: "P.png",
    BOMB: "O.png",
}

GRID_SIZE = 7


class Position:
    """
    The position class represents a location in a 2D grid.

    A position is made up of an x coordinate and a y coordinate.
    The x and y coordinates are assumed to be non-negative whole numbers which
    represent a square in a 2D grid.

    Examples:
        >>> position = Position(2, 4)
        >>> position
        Position(2, 4)
        >>> position.get_x()
        2
        >>> position.get_y()
        4
    """

    def __init__(self, x: int, y: int):
        """
        The position class is constructed from the x and y coordinate which the
        position represents.

        Parameters:
            x: The x coordinate of the position
            y: The y coordinate of the position
        """
        self._x = x
        self._y = y

    def get_x(self) -> int:
        """Returns the x coordinate of the position."""
        return self._x

    def get_y(self) -> int:
        """Returns the y coordinate of the position."""
        return self._y

    def add(self, position: "Position") -> "Position":
        """
        Add a given position to this position and return a new instance of
        Position that represents the cumulative location.

        This method shouldn't modify the current position.

        Examples:
            >>> start = Position(1, 2)
            >>> offset = Position(2, 1)
            >>> end = start.add(offset)
            >>> end
            Position(3, 3)

        Parameters:
            position: Another position to add with this position.

        Returns:
            A new position representing the current position plus
            the given position.
        """
        return Position(self._x + position.get_x(), self._y + position.get_y())

    def subtract(self, position: "Position") -> "Position":
        """
        Add a given position to this position and return a new instance of
        Position that represents the cumulative location.

        This method shouldn't modify the current position.

        Examples:
            >>> start = Position(1, 2)
            >>> offset = Position(2, 1)
            >>> end = start.add(offset)
            >>> end
            Position(3, 3)

        Parameters:
            position: Another position to add with this position.

        Returns:
            A new position representing the current position plus
            the given position.
        """
        return Position(self._x - position.get_x(), self._y - position.get_y())

    def __eq__(self, other: object) -> bool:
        """
        Return whether the given other object is equal to this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are equal, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        # an __eq__ method needs to support any object for example
        # so it can handle `Position(1, 2) == 2`
        # https://www.pythontutorial.net/python-oop/python-__eq__/
        if not isinstance(other, Position):
            return False
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __hash__(self) -> int:
        """
        Calculate and return a hash code value for this position instance.

        This allows Position instances to be used as keys in dictionaries.

        A hash should be based on the unique data of a class, in the case
        of the position class, the unique data is the x and y values.
        Therefore, we can calculate an appropriate hash by hashing a tuple of
        the x and y values.

        Reference: https://stackoverflow.com/questions/17585730/what-does-hash-do-in-python
        """
        return hash((self.get_x(), self.get_y()))

    def __repr__(self) -> str:
        """
        Return the representation of a position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.

        Examples:
            >>> repr(Position(12, 21))
            'Position(12, 21)'
            >>> Position(12, 21).__repr__()
            'Position(12, 21)'
        """
        return f"Position({self.get_x()}, {self.get_y()})"

    def __str__(self) -> str:
        """
        Return a string of this position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.
        """
        return self.__repr__()

    def __lt__(self, other: object) -> bool:
        """
        Return whether the given other object is less than this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are less than the other x and y coordinates,
        return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x < other.get_x():
            return True
        if self._y < other.get_y():
            return True
        return False

    def __le__(self, other: object) -> bool:
        """
        Return whether the given other object is less than or equal to
        this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are less than or equal to the other x and y
        coordinates, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x <= other.get_x():
            return True
        if self._y <= other.get_y():
            return True
        return False

    def __gt__(self, other: object) -> bool:
        """
        Return whether the given other object is greater than this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are greater than the other x and y coordinates,
        return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x > other.get_x():
            return True
        if self._y > other.get_y():
            return True
        return False

    def __ge__(self, other: object) -> bool:
        """
        Return whether the given other object is greater than or equal to
        this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are greater than or equal to the other x and y
        coordinates, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x >= other.get_x():
            return True
        if self._y >= other.get_y():
            return True
        return False


class Entity:
    """
    Entity is an abstract class that is used to represent anything that can
    appear on the game's grid.
    """

    def display(self) -> str:
        """
        Return the character used to represent this entity in a text-based grid.

        An instance of the abstract Entity class should never be placed in the
        grid, so this method should only be implemented by subclasses of Entity.

        To indicate that this method needs to be implemented by subclasses,
        this method should raise a NotImplementedError.

        Raises:
        NotImplementedError: Whenever this method is called.
        """
        return NotImplementedError()

    def __repr__(self) -> str:
        """Return a representation of this entity."""
        return f"{self.__class__.__name__}()"


class Player(Entity):
    """
    A subclass of Entity representing a Player within the game
    """

    def display(self) -> str:
        """
        Return the character used to represent the player entity.

        A player should be represented by the 'P' character.
        """
        return PLAYER


class Collectable(Entity):
    """
    A subclass of Entity representing a Collectable within the game that
    Player's must acquire.
    """

    def display(self) -> str:
        """
        Return the character used to represent the collectable entity.

        A player should be represented by the 'C' character.
        """
        return COLLECTABLE


class Destroyable(Entity):
    """
    A subclass of Entity representing a Destroyable within the game that
    Player's must destroy before it reaches them.
    """

    def display(self) -> str:
        """
        Return the character used to represent the destroyable entity.

        A player should be represented by the 'D' character.
        """
        return DESTROYABLE


class Blocker(Entity):
    """
    A subclass of Entity representing a Blocker within the game that
    Player's cannot remove from the grid.
    """

    def display(self) -> str:
        """
        Return the character used to represent the destroyable entity.

        A player should be represented by the 'B' character.
        """
        return BLOCKER


class Grid:
    """
    The Grid class is used to represent the 2D grid of entities.

    Positions (x, y) are unique within the grid which may vary in size
    """

    def __init__(self, size: int):
        """
        A grid is constructed with a size representing the dimensions of the
        playing grid.

        Initially a grid does not contain any entities.

        Parameters:
            size: The length and width of the grid.
        """
        self._size = size
        self._entities = {}

    def get_size(self) -> int:
        """Return dimensions of the grid."""
        return self._size

    def add_entity(self, position: Position, entity: Entity) -> None:
        """
        Add a given entity into the grid at a specified position.

        This will replace any current entity at the specified position.

        Parameters:
            position: Position to place a given entity in.
            entity: Entity being added into the grid.
        """
        self._entities[position] = entity

    def get_entities(self) -> Dict[Position, Entity]:
        """
        Return the dictionary containing grid entities.

        Updating the returned dictionary should have no side-effects.
        """
        return {pos: entity for pos, entity in self._entities.items()}

    def get_entity(self, position: Position) -> Optional[Entity]:
        """
        Return a entity from the grid representing at a specific position or
        None if the position does not have a mapped entity.

        Parameters:
            position: Position to check for an entity within the grid.
        """
        return self._entities.get(position, None)

    def remove_entity(self, position: Position) -> None:
        """
        Remove an entity from the grid at a specified position.

        Parameters:
            position: Position to check for an entity within the grid.
        """
        self._entities.pop(position, None)

    def serialise(self) -> Dict[Tuple[int, int], str]:
        """
        Convert a dictionary of Positions and Entities into a simplified
        serialised dictionary mapping tuples to characters.

        Tuples are represented by the x and y coordinates of a Positions and
        Entities are represented by their `display()` character.
        """
        serial_entity = {}
        for pos, entity in self.get_entities().items():
            # Unpack x, y and display from each pos and entity before adding
            x = pos.get_x()
            y = pos.get_y()
            display = entity.display()
            serial_entity[(x, y)] = display
        return serial_entity

    def in_bounds(self, position: Position) -> bool:
        """
        Return a boolean based on whether the position is valid in terms of the
        dimensions of the grid.

        x coordinates need to be greater than 0 but less than or = to the size
        of the grid whereas y coordinates need to be between 1 and the size of
        the grid.

        Parameters:
            position: Position to be checked against valid bounds conditions
        """
        if position.get_x() < 0 or position.get_x() >= self.get_size():
            return False
        if position.get_y() < 1 or position.get_y() >= self.get_size():
            return False
        return True

    def __repr__(self) -> str:
        """Return a representation of the grid."""
        return f"Grid({self._size})"


class Game:
    """
    The Game handles the logic for controlling the actions of the entities
    within the grid.
    """

    def _create_player(self) -> Position:
        """
        Create and add a representation of a Player within a grid and return the
        Position the player's position.
        """
        # Set up player to be in the top middle of the grid
        x = self._grid.get_size() // 2
        y = 0
        player_pos = Position(x, y)
        player = Player()
        self._grid.add_entity(player_pos, player)
        return player_pos

    def __init__(self, grid_size: int):
        """
        A game is constructed with a size representing the dimensions of the
        playing grid as well as flag dictating whether the game is lost and
        variables keeping track of the number of Collectables acquired and Destroyables removed.

        Parameters:
            grid_size: The length and width of the grid.
        """
        self._grid = Grid(grid_size)
        self._collected = 0
        self._destroyed = 0
        self._shot_count = 0
        self._player_position = self._create_player()
        self._lost_flag = False

    def get_grid(self) -> Grid:
        """Return the instance of the grid held by the game."""
        return self._grid

    def get_player_position(self) -> Position:
        """Return the position of the player in the grid."""
        return self._player_position

    def get_collectable_amount(self) -> int:
        """Return the total of collectables acquired."""
        return self._collected

    def get_destroyable_amount(self) -> int:
        """Return the total of destroyables removed."""
        return self._destroyed

    def get_total_shots(self) -> int:
        """Return the total of shots taken."""
        return self._shot_count

    def rotate_grid(self, offset) -> None:
        """
        Rotate the positions of the entities within the grid depending on
        the direction they are being rotated.

        Parameters:
            offset: (x, y) position value to change each position by.
        """
        # Select the correct order of direction to traverse over x-axis by
        # this avoids entities being deleted through the rotation
        sequence = range(0, self.get_grid().get_size())
        if offset[0] > 0:
            sequence = range(self._grid.get_size() - 1, -1, -1)

        for y in range(self._grid.get_size()):
            # create buffer to hold edge position and entities
            buffer: Optional[Tuple[Position, Entity]] = None
            for x in sequence:
                pos = Position(x, y)
                entity = self._grid.get_entity(pos)

                if entity is None or isinstance(entity, Player):
                    continue

                # rotate and remove position of current entity using offset
                off_x, off_y = offset
                updated_pos = pos.add(Position(off_x, off_y))
                self._grid.remove_entity(pos)

                # Only add position back in if it is in bounds after rotation
                if not self._grid.in_bounds(updated_pos):
                    # Wrap the updated position to go to other side of grid
                    wrapped_x = updated_pos.get_x() % self.get_grid().get_size()
                    updated_pos = Position(wrapped_x, updated_pos.get_y())
                    buffer = (updated_pos, entity)
                else:
                    self._grid.add_entity(updated_pos, entity)

            # Add buffered entity back into the grid
            if buffer is not None:
                buff_pos, buff_ent = buffer
                self._grid.add_entity(buff_pos, buff_ent)

        """ ANOTHER WAY OF DOING THIS FUNCTION """
        # buffer = []
        # original = []
        # order = 1
        # if offset[0] > 0:
        #     order = -1
        # for pos in sorted(self.get_grid().get_entities())[::order]:
        #     entity = self.get_grid().get_entity(pos)
        #
        #     if isinstance(entity, Player):
        #         continue
        #
        #     updated_pos = pos.add(Position(offset[0], offset[1]))
        #     self._grid.remove_entity(pos)
        #     if not self._grid.in_bounds(updated_pos):
        #         original.append(pos)
        #         wrapped_x = updated_pos.get_x() % self.get_grid().get_size()
        #         updated_pos = Position(wrapped_x, updated_pos.get_y())
        #         buffer.append((updated_pos, entity))
        #         continue
        #     self._grid.add_entity(updated_pos, entity)
        #
        # # Add buffered entity back into the grid
        # for pos, entity in buffer:
        #     self._grid.add_entity(pos, entity)

    def _create_entity(self, display: str) -> Entity:
        """
        Uses a display character to create an Entity.

        Parameters:
            display: character dictating which entity to create.

        Raises:
            NotImplementedError: Whenever invalid display is passed.
        """
        if display == BLOCKER:
            return Blocker()
        elif display == COLLECTABLE:
            return Collectable()
        elif display == DESTROYABLE:
            return Destroyable()
        else:
            raise NotImplementedError()

    def generate_blobs(self) -> None:
        """
        Method given to the students to generate a random amount of Entities to
        add into the game after each step
        """
        # Generate amount
        blob_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=blob_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == True
        total_count = blob_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)
        entity_index = random.sample(range(self.get_grid().get_size()), total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def step(self) -> None:
        """
        The _step_ method of the game will be called after every action
        performed by the player.

        This method moves entities one step closer to the Player entity within
        the grid.
        """
        for pos in sorted(self.get_grid().get_entities()):

            # Move entities up one position
            move_x, move_y = MOVE
            update_pos = pos.add(Position(move_x, move_y))
            entity = self.get_grid().get_entity(pos)

            # Ignore for Player
            if isinstance(entity, Player):
                continue

            self.get_grid().remove_entity(pos)

            # Lose if they reach the players row
            if update_pos.get_y() == 0 and isinstance(entity, Destroyable):
                self.handle_loss()

            # Add back into the grid if entities don't go off the top of grid
            if self._grid.in_bounds(update_pos):
                self.get_grid().add_entity(update_pos, entity)

        # Create and add new blobs into the game
        self.generate_blobs()

    def fire(self, shot_type: str) -> None:
        """
        Handles the firing/collecting actions of a player towards an entity
        within the grid.

        Parameters:
            shot_type: dictates whether to collect or destroy
        """
        # Increment shot count
        self._shot_count += 1

        # Setup intial firing pos
        fire_x, fire_y = FIRE
        fire = self._player_position.add(Position(fire_x, fire_y))

        while self.get_grid().in_bounds(fire):
            entity = self.get_grid().get_entity(fire)
            # Check whether somethings hit
            if self.get_grid().get_entity(fire) is not None:

                # Block shot if it hits a blocker
                if isinstance(entity, Blocker):
                    break

                # Collect valid blobs and add to score
                if shot_type == COLLECT and isinstance(entity, Collectable):
                    self._collected += 1
                    self._grid.remove_entity(fire)

                # Destroy everything else
                if shot_type == DESTROY:
                    self._grid.remove_entity(fire)

                    # Check and update destoyable count if applicable
                    if isinstance(entity, Destroyable):
                        self._destroyed += 1
                break

            # Update firing shot position
            fire = fire.add(Position(FIRE[0], FIRE[1]))

    def has_won(self) -> bool:
        """
        Return true if the player has won the game.

        Player wins the game if they collect enough Collectable entities before
        getting hit with a Destroyable
        """
        return self._collected == COLLECTION_TARGET

    def handle_loss(self):
        self._lost_flag = True

    def has_lost(self) -> bool:
        """
        Returns true if the lost flag is set to True.
        """
        return self._lost_flag


class Bomb(Entity):
    """
    A subclass of Entity representing a Bomb within the game that
    Player's can splash damage with.
    """

    def display(self) -> str:
        """
        Return the character used to represent the destroyable entity.

        A player should be represented by the 'O' character.
        """
        return BOMB


class MastersGame(Game):

    def __init__(self, grid_size):
        super().__init__(grid_size)
        self._lives = 1

    def handle_loss(self):
        if self._lives == 0:
            super().handle_loss()
        else:
            self._lives -= 1

    def get_lives(self):
        return self._lives

    def _create_entity(self, display: str) -> Entity:
        """
        Uses a display character to create an Entity.

        Parameters:
            display: character dictating which entity to create.

        Raises:
            NotImplementedError: Whenever invalid display is passed.
        """
        if display == BOMB:
            return Bomb()
        return super()._create_entity(display)

    def generate_blobs(self) -> None:
        """
        Method given to the students to generate a random amount of Entities to
        add into the game after each step
        """
        # Generate amount
        blob_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=blob_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0
        bomb = False
        if not blocker:
            bomb = random.randint(1, 4) % 4 == 0

        total_count = blob_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        if bomb:
            total_count += 1
            entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()), total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def fire(self, shot_type: str) -> None:
        """
        Handles the firing/collecting actions of a player towards an entity
        within the grid.

        Parameters:
            shot_type: dictates whether to collect or destroy
        """
        # Increment shot count
        self._shot_count += 1

        # Setup intial firing pos
        fire_x, fire_y = FIRE
        fire = self._player_position.add(Position(fire_x, fire_y))

        while self.get_grid().in_bounds(fire):
            entity = self.get_grid().get_entity(fire)
            # Check whether somethings hit
            if self.get_grid().get_entity(fire) is not None:

                # Block shot if it hits a blocker
                if isinstance(entity, Blocker):
                    break

                # Collect valid blobs and add to score
                if shot_type == COLLECT and isinstance(entity, Collectable):
                    self._collected += 1
                    self._grid.remove_entity(fire)

                # Destroy everything else
                if shot_type == DESTROY:
                    self._grid.remove_entity(fire)

                    if isinstance(entity, Bomb):
                        offsets = (
                            (0, 1),
                            (1, 1),
                            (-1, 1),
                            (-1, -1),
                            (1, -1),
                            (0, -1),
                            (1, 0),
                            (-1, 0),
                        )

                        for x, y in offsets:
                            pos = Position(x, y)
                            current = fire.add(pos)
                            self._grid.remove_entity(current)

                    # Check and update destoyable count if applicable
                    if isinstance(entity, Destroyable):
                        self._destroyed += 1
                break

            # Update firing shot position
            fire = fire.add(Position(FIRE[0], FIRE[1]))


class AbstractField(tk.Canvas):
    """Support for creation of and annotation on Fields."""

    def __init__(self, master, rows, cols, width, height, **kwargs):
        """Constructor for AbstractGrid.
        Parameters:
            master (tk.Tk | tk.Frame): The master frame for this Canvas.
            rows (int): Number of rows.
            cols (int): Number of columns.
            width (int): The width of the Canvas in pixels.
            height (int): The height of the Canvas in pixels.
        """
        super().__init__(master, width=width, height=height, **kwargs)
        self._rows = rows
        self._cols = cols
        self._cell_width = width / cols
        self._cell_height = height / rows

    def get_bbox(self, position):
        """Returns the bounding box of the given (row, col) position.
        Parameters:
            position (tuple<int, int>): The (row, col) cell position.
        Returns:
            (tuple<int * 4>): Bounding box for this position as
                              (x_min, y_min, x_max, y_max).
        """
        row, col = position
        x_min, y_min = col * self._cell_width, row * self._cell_height
        x_max, y_max = x_min + self._cell_width, y_min + self._cell_height
        return x_min, y_min, x_max, y_max

    def pixel_to_position(self, pixel):
        """Converts the x, y pixel position to a (row, col) position.
        Parameters:
            pixel (tuple<int, int>): x, y position.
        Returns:
            (tuple<int, int): (row, col) position.
        """
        x_coord, y_coord = pixel
        return y_coord // self._cell_height, x_coord // self._cell_width

    def get_position_center(self, position):
        """Gets the graphics coordinates for the center of the cell at the
            given (row, col) position.
        Parameters:
            position (tuple<int, int>): The (row, col) cell position.
        Returns:
            tuple(int, int): The x, y pixel position of the center of the cell.
        """
        row, col = position
        x_pos = col * self._cell_width + self._cell_width // 2
        y_pos = row * self._cell_height + self._cell_height // 2
        return x_pos, y_pos

    def annotate_position(self, position, text):
        """Annotates the cell at the given (row, col) position with the
            provided text.
        Parameters:
            position (tuple<int, int>): The (row, col) cell position.
            text (str): The text to draw.
        """
        self.create_text(self.get_position_center(position), text=text)


class HackingView(AbstractField):
    """A display of the Hacker game field."""

    def __init__(self, root, size, width, height, **kwargs):
        """Constructor for HackingView.
        Parameters:
            root (tk.Tk | tk.Frame): The root frame for this Canvas.
            size (int): The number of rows (= #columns) in this map.
            width (int): Width of the entire View canvas.
            height (int): Height of the entire View canvas.
        """
        super().__init__(
            root, rows=size, cols=size, width=width, height=height, **kwargs
        )

    def draw_player_bar(self):
        """
        Draws the background bar on the same row as the Player entity.
        """
        x_min = 0
        y_min = 0
        x_max = self._rows * self._cell_width
        y_max = self._cell_width
        self.create_rectangle(x_min, y_min, x_max, y_max, fill="#8E8E8E")

    def draw_grid(self, entities):
        """
        Draws the 2D GUI representation of the game field based on dictionary
        mapping positions and entities.

        Parameters:
            entities (dict): position => entity mappings
        """
        for pos, ent in entities.items():
            x, y = pos
            bbox = self.get_bbox((y, x))
            self.create_rectangle(bbox, fill=COLOURS[ent])
            self.annotate_position((y, x), ent)


class ScoreBar(AbstractField):
    """
    A display of the amount of collectables the player has.
    """

    def __init__(self, root, rows, **kwargs):
        """Constructor for InventoryView.
        Parameters:
            root (tk.Tk | tk.Frame): The root frame for this canvas.
            rows (int): #rows to allow in this scorebar.
        """
        super().__init__(
            root,
            rows=rows,
            cols=2,
            width=SCORE_WIDTH,
            height=MAP_HEIGHT,
            bg=SCORE_COLOUR,
            **kwargs,
        )

    def generate_labels(self, current_score):
        return ["Collected:", "Destroyed:"]

    def draw(self, current_score: Tuple[int, int]):
        """
        Draws the GUI representation of the score breakdown acquired.

        Parameters:
            current_score: player stats.
        """
        # Draw header
        middle_x, *_ = self.get_bbox((0, 1))
        _, middle_y = self.get_position_center((0, 0))
        self.create_text(
            middle_x, middle_y, text="Score", fill="#FFFFFF", font=("Arial", 22)
        )

        # Iteratively display stats
        labels = self.generate_labels(current_score)
        for i, score in enumerate(current_score):
            label_pos = self.get_position_center((i + 1, 0))
            score_pos = self.get_position_center((i + 1, 1))
            self.create_text(label_pos, text=labels[i], fill="white")
            self.create_text(score_pos, text=str(score), fill="white")


class HackerController:
    """
    Controller for the Hacker game interface.
    """

    def _create_title(self):
        """Draw title visuals."""
        title_frame = tk.Frame(self._root)
        title_frame.pack(fill=tk.X)

        title = tk.Label(
            title_frame, text=TITLE, bg="#222222", fg="white", font=("Arial", 28)
        )
        title.pack(fill=tk.X)

    def draw_visuals(self):
        """Draw all visuals to display the game"""
        self._hack_view.delete("all")
        self._score_view.delete("all")
        self._hack_view.draw_player_bar()
        entities = self._model.get_grid().serialise()
        self._hack_view.draw_grid(entities)
        score = (
            self._model.get_collectable_amount(),
            self._model.get_destroyable_amount(),
        )

        self._score_view.draw(score)

    def _view_setup(self):
        """Setup Hacking and Score view components and visuals."""
        view_frame = tk.Frame(self._root)
        view_frame.pack()
        self._hack_view = HackingView(
            view_frame, self._size, MAP_WIDTH, MAP_HEIGHT, bg=ZONE
        )
        self._hack_view.pack(side=tk.LEFT)
        self._score_view = ScoreBar(view_frame, COLLECTION_TARGET)
        self._score_view.pack(side=tk.LEFT)
        self.draw_visuals()

    def _event_setup(self):
        """Bind root window to a key press event"""
        self._root.bind("<KeyPress>", self.handle_keypress)
        self._root.after(1000, self.step)

    def _game_selection(self):
        self._model = Game(self._size)

    def __init__(self, root, size):
        """Constructor for HackerController.
        Parameters:
            root (tk.Tk | tk.Frame): The master frame for this Frame.
            size (int): The number of rows (and columns) in the map.
        """
        self._root = root
        self._size = size
        self._game_selection()
        self._create_title()
        self._view_setup()
        self._event_setup()

        # Initialise the timing event variable
        self._step_event = None

    def step(self):
        """
        The step method is called two seconds. This method triggers the
            step method for in the model and updates the view accordingly.
        """
        # Destroy and redraw game after model entities have stepped
        self._model.step()
        self.draw_visuals()

        # Check for loss behavior
        if self._model.has_lost():
            self.handle_loss()
        else:
            self._step_event = self._root.after(2000, self.step)

    def handle_rotate(self, key):
        index = DIRECTIONS.index(key)
        offset = ROTATIONS[index]
        self._model.rotate_grid(offset)

    def handle_fire(self, key):
        self._model.fire(key)

    def handle_keypress(self, event):
        """Handles the event triggered from a key press by the player."""
        key = event.keysym.upper()

        # Dictate whether a firing or rotate action is to occur
        if key in DIRECTIONS:
            self.handle_rotate(key)
        elif key in SHOT_TYPES:
            self.handle_fire(key)

        self.draw_visuals()

        # Finally check for win behaviour
        if self._model.has_won():
            self.handle_win()

    def pop_up(self, msg):
        messagebox.showinfo("Game Over", f"You {msg}!")

    def show_window(self, has_won):
        if has_won:
            msg = "win"
        else:
            msg = "lost"
        self.pop_up(msg)

    def handle_win(self):
        self._root.after_cancel(self._step_event)
        self._root.update()  # For mac to update GUI before showing message
        self.show_window(True)
        self._root.destroy()

    def handle_loss(self):
        self._root.update()  # For mac to update GUI before showing message
        self.show_window(False)
        self._root.destroy()


from PIL import ImageTk, Image


class ImageHackingView(HackingView):
    """An image-based display for the game map."""

    def __init__(self, root, size, width, height, **kwargs):
        """Constructor for HackingView.
        Parameters:
            root (tk.Tk | tk.Frame): The root frame for this Canvas.
            size (int): The number of rows (= #columns) in this map.
            width (int): Width of the entire View canvas.
            height (int): Height of the entire View canvas.
        """
        super().__init__(root, size, width, height, **kwargs)
        self._images = {}

    def draw_grid(self, entities):
        """Draws the entity using a sprite image."""
        for pos, ent in entities.items():
            pixel = self.get_position_center(pos[::-1])
            self.create_image(*pixel, image=self.get_image(ent))

    def get_image(self, tile_type, angle=0):
        """Gets the image for the entity of given type. Creates a new image
            if one doesn't exist for this entity and stores a reference to it.
        Parameters:
            tile_type (str): ID of the entity.
        Returns:
            (ImageTk.PhotoImage): The image for the given tile_type.
        """
        cache_id = f"{tile_type}.png"
        if cache_id not in self._images:
            image = ImageTk.PhotoImage(
                image=Image.open("images/" + IMAGES.get(tile_type))
                .rotate(angle)
                .resize((int(self._cell_width), int(self._cell_height)))
            )
            self._images[cache_id] = image
        return self._images[cache_id]


class StatusBar(tk.Frame):

    def _setup_timer(self):
        timer_frame = tk.Frame(self)
        timer_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Label(timer_frame, text="Timer").pack()

        self._time_label = tk.Label(timer_frame)
        self._time_label.pack()

    def _setup_moves(self):
        move_frame = tk.Frame(self)
        move_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Label(move_frame, text="Total Shots").pack()

        self._shot_label = tk.Label(move_frame)
        self._shot_label.pack()

    def _setup_pause_play(self):
        """Creates the pause and play buttons."""
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self._play_button = tk.Button(buttons_frame, text="Pause")
        self._play_button.pack()

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self._setup_moves()
        self._setup_timer()
        self._setup_pause_play()

    def set_shots(self, shot_total):
        self._shot_label.config(text=f"{shot_total}")

    def set_time(self, time):
        self._time_label.config(text=f"{time // 60}m {time % 60}s")

    def setup_paused(self, func):
        self._play_button.config(command=func)

    def set_paused_text(self, text):
        self._play_button.config(text=text)


class AdvancedHackerController(HackerController):

    def _view_setup(self):
        """Setup Hacking and Score view components and visuals."""
        view_frame = tk.Frame(self._root)
        view_frame.pack()
        self._hack_view = ImageHackingView(
            view_frame, self._size, MAP_WIDTH, MAP_HEIGHT, bg="#2D3332"
        )
        self._hack_view.pack(side=tk.LEFT)
        self._score_view = ScoreBar(view_frame, COLLECTION_TARGET)
        self._score_view.pack(side=tk.LEFT)
        self.draw_visuals()

    def _set_up_file_menu(self):
        """
        Set up file menu.
        Parameters:
            game: Current game being played
        """
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save game", command=self.save_game)
        filemenu.add_command(label="Load game", command=self.load_game)
        filemenu.add_command(label="Restart game", command=self.restart_game)

        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.quit)

    def __init__(self, root, size):
        super().__init__(root, size)

        self._status_bar = StatusBar(root, height=BAR_HEIGHT, width=MAP_WIDTH)
        self._status_bar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._set_up_file_menu()

        # Initialise status bar counters
        shots = self._model.get_total_shots()
        self._status_bar.set_shots(shots)
        self._current_time = 0
        self._timer_event = None
        self.handle_timer()

        # Setup pause/play functionality
        self._paused = False
        self._status_bar.setup_paused(self.handle_pause)

    def handle_timer(self):
        self._status_bar.set_time(self._current_time)
        self._current_time += 1
        self._timer_event = self._root.after(1000, self.handle_timer)

    def handle_fire(self, key):
        super().handle_fire(key)
        shots = self._model.get_total_shots()
        self._status_bar.set_shots(shots)

    def unpause(self):
        self._timer_event = self._root.after(1000, self.handle_timer)
        self._step_event = self._root.after(2000, self.step)

    def pause(self):
        self._root.after_cancel(self._timer_event)
        self._root.after_cancel(self._step_event)

    def handle_keypress(self, event):
        """Handles the event triggered from a key press by the player."""
        if not self._paused:
            super().handle_keypress(event)

    def handle_pause(self):
        if self._paused:
            self.unpause()
            self._status_bar.set_paused_text("Pause")
        else:
            self.pause()
            self._status_bar.set_paused_text("Play")

        self._paused = not self._paused

    def save_game(self):
        """Students can implement how they please"""
        pass

    def load_game(self):
        """Students can implement how they please"""
        pass

    def quit(self):
        self.pause()
        if messagebox.askyesno("Quit?", "Do you really want to quit?"):
            self._root.destroy()
        else:
            self.unpause()

    def restart_game(self):
        self._model = Game(self._size)
        self._current_time = 0
        self.draw_visuals()
        self._paused = False
        self._status_bar.set_shots(self._model.get_total_shots())
        self._status_bar.set_time(self._current_time)

    def handle_win(self):
        self.pause()
        super().handle_win()

    def handle_loss(self):
        self.pause()
        super().handle_loss()


class MasterScoreBar(ScoreBar):

    def generate_labels(self, current_score):
        return ["Collected:", "Destroyed:", "Lives"]


class MasterHackerController(AdvancedHackerController):

    def _game_selection(self):
        self._model = MastersGame(self._size)

    def _view_setup(self):
        """Setup Hacking and Score view components and visuals."""
        view_frame = tk.Frame(self._root)
        view_frame.pack()
        self._hack_view = ImageHackingView(
            view_frame, self._size, MAP_WIDTH, MAP_HEIGHT, bg="#2D3332"
        )
        self._hack_view.pack(side=tk.LEFT)
        self._score_view = MasterScoreBar(view_frame, COLLECTION_TARGET)
        self._score_view.pack(side=tk.LEFT)
        self.draw_visuals()

    def draw_visuals(self):
        self._hack_view.delete("all")
        self._score_view.delete("all")
        self._hack_view.draw_player_bar()
        entities = self._model.get_grid().serialise()
        self._hack_view.draw_grid(entities)
        score = (
            self._model.get_collectable_amount(),
            self._model.get_destroyable_amount(),
            self._model.get_lives(),
        )

        self._score_view.draw(score)

    def __init__(self, root, size):
        super().__init__(root, size)


def start_game(root, TASK=TASK):
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app


def main():
    root = tk.Tk()
    root.title(TITLE)
    app = start_game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
