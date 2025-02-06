# Created by ezana at 2/13/2024
Feature: Products
  Verify Inventory, Carts and Sort functionality

  @test_case_id_2 @jira_co501
  Scenario Outline: Verify all swag products are available on Inventory page
    Given a standard_user logs in
    Then the user should be on <page_name> page
    And <items type> on <page_name> page should contain <list of items>
    Examples:
      | items type       | page_name | list of items                                                                                                                                       | @test_case_id     |
      | list of products | Inventory | Sauce Labs Backpack, Sauce Labs Bike Light, Sauce Labs Bolt T-Shirt, Sauce Labs Fleece Jacket, Sauce Labs Onesie, Test.allTheThings() T-Shirt (Red) | @test_case_id_2_1 |

  @test_case_id_3 @jira_co502
  Scenario Outline: Verify Add to Cart feature
    Given a standard_user logs in
    And the user should be on Inventory page
    When the user adds <product names> to cart
    And the user navigates to Cart page
    Then <product names> should be available in cart
    Examples:
      | product names                               | @test_case_id     |
      | Sauce Labs Bolt T-Shirt                     | @test_case_id_3_1 |
      | Sauce Labs Fleece Jacket, Sauce Labs Onesie | @test_case_id_3_2 |