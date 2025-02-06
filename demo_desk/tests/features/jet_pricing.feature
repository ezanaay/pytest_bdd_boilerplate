# Created by ezana at 6/4/2024
Feature: Jet Pricing
  Jet leasing cost calculation and fuel capacity unit conversion should work correctly

  @test_case_id_1 @jira_co200 @cost_calculation
  Scenario Outline: Jet Lease cost calculation
    Given I open "company Aircraft Lease" app
    And I open "Cost Calculation" menu item
    And based on the given <weather_condition>, <runway_condition>, <aircraft_performance>, <fuel_rate>
    Then I verify that the calculated lease cost equals <lease_cost>
    Examples:
      | weather_condition | runway_condition | aircraft_performance | fuel_rate | lease_cost |
      | 6                 | 10               | 8                    | 3         | 6          |

  @test_case_id_2 @regression @jira_co201 @capacity_conversion
  Scenario: Verify Aircraft Fuel Capacity unit conversion
    Given I open "company Aircraft Lease" app
    And I open "Aircraft Fuel Capacity" menu item
    Then I verify that "2 Gallons (US)" aircraft fuel equals "7.570824 Liters"
