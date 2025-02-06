# Created by ezana at 1/25/2024
Feature: Countries REST api tests

  @test_case_id_1 @jira_NJ301
  Scenario Outline: Validate get countries api
    Given a <query_name> request with params <params> is sent to countries_api
    Then the response status code for <query_name> is 200
    And I verify that <query_name> query response has <count> entries
    And I verify that <query_name> query response contains <response> for key <search_key>
    Examples:
      | query_name              | params             | search_key  | count | response                      | @test_case_id     |
      | get_country_by_name_api | {"name":"aust"}    | name.common | 2     | Australia, Austria            | @test_case_id_1_1 |
      | get_country_by_name_api | {"name":"america"} | name.common | 2     | American Samoa, United States | @test_case_id_1_2 |

