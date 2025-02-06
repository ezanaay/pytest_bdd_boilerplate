# Created by ezana at 1/25/2024
Feature: Rental films in Film Categories

  @regression @test_case_id_1 @jira_NJ401
  Scenario: Verify number of films in each film category
    Given I query dvdrental_db database for list_of_films_in_category for "Action#catgory"
    Then I verify that "list_of_films_in_category" contains 64 db entries
