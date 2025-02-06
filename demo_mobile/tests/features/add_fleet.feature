# Created by ezana at 6/6/2024
Feature: Fleet Finder
  All fleet options should be available on products page and adding a fleet to cart should make the chosen fleet option available in Carts screen.

  @test_case_id_1 @jira_NJ101 @cart
  Scenario: Verify Fleet option selection
    Given I start "company Fleet" mobile app
    And I login as a company_user
    And I should be on PRODUCTS screen
    When I add "Large Jets" to cart
    Then "Large Jets" should be available in the cart

  @test_case_id_2 @jira_NJ110 @products
  Scenario: Verify Fleet options display
    Given I start "company Fleet" mobile app
    And I login as a company_user
    And I should be on PRODUCTS screen
    And I sort fleet products based on Price (low to high)
    Then I verify that fleet product prices are sorted in increasing order
