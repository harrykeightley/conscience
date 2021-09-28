Feature: Simple Application Functions

    Scenario: Displays hello world at startup
        Given I start the application
         Then I see text displaying, roughly, "Hello World"
