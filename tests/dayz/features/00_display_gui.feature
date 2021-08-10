Feature: Task 1: Display GUI

    Full GUI for task 1 is displayed,
    including game characters and items and inventory displays as described in specification.

    Scenario: Game title is displayed
        Given I open a task 1 game with file "maps/basic.txt"
         Then I see a title displaying roughly displaying "EndOfDayz", removing casing and whitespace

    Scenario: Game grid and inventory are displayed
        Given I open a task 1 game with file "maps/basic.txt"
         Then I can see a grid and inventory
    
    Scenario: Inventory is displayed appropriately
        Given I open a task 1 game with file "maps/basic4.txt"
        Then the inventory is displayed
        And the inventory is the same size as the map
        And the title is centred at the top

    Scenario: Empty inventory is displayed
        Given I open a task 1 game with file "maps/basic.txt"
         Then the inventory is displayed
         And the inventory has a title "Inventory"
         And the inventory title colour is "#371D33"

    Scenario: Inventory with one item is displayed
        Given I play the file "maps/basic.txt"
         And the player is holding
            | item   | quantity |
            | Garlic | 1        |
         And I open a task 1 game
        Then the inventory is displayed
         And the inventory contains "Garlic" "10" in row 2

    Scenario: Inventory with many items is displayed
        Given I play the file "maps/basic.txt"
         And the player is holding
            | item     | quantity |
            | Garlic   | 1        |
            | Crossbow | 1        |
         And I open a task 1 game
        Then the inventory is displayed
         And the inventory contains "Garlic" "10" in row 2
         And the inventory contains "Crossbow" "5" in row 3

    Scenario: Display all game characters
        Given I open a task 1 game with file "maps/basic4.txt"
        Then the player token is displayed
        And the zombie token is displayed
        And the tracking zombie token is displayed

    Scenario: Display all the game items
        Given I open a task 1 game with file "maps/basic4.txt"
        Then the hospital token is displayed
        And the crossbow token is displayed
        And the garlic token is displayed
        And the hospital token is displayed