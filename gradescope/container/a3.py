from a3_support import *
import tkinter as tk
import random


class Game:

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # bomb = False
        # if not blocker:
        #     bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # if bomb:
        #     total_count += 1
        #     entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()), total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)


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
