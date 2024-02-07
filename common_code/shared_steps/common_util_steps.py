from pytest_bdd import given, then, parsers, when
import glob
from lib import log
from settings import LOG_LEVEL, CONSOLE_OUT
logger = log.get_logger(__name__, LOG_LEVEL, CONSOLE_OUT)

import settings
from common_code.shared_steps.shared_steps_helpers import create_feature_file_tags_mapping, \
    update_feature_files_with_unique_test_case_ids, assign_tags_to_examples


@then("I assign unique test case id for every test case")
def print_test_case_ids():
    # collect all feature files
    features_files = glob.glob(f'{settings.FEATURE_ROOT}/**/*.feature', recursive=True)
    feature_files_tags_mapping = {}
    for feature_file in features_files:
        # read all tags and create a dict mapping
        # for scenarios and scenario outlines: key = {file_name}:{expected_tag_line_no},
        # value= testcase_id if available otherwise none
        # for example rows: key = {file_name}:{expected_scenario_outline_tag_line_no}:{example_row},
        # value= testcase_id if available otherwise none_row
        feature_files_tags_mapping.update(create_feature_file_tags_mapping(feature_file))

    # separate example rows
    scenario_and_outline_rows_mapping = {}
    example_rows_mapping = {}
    for file_line_mapping, value in feature_files_tags_mapping.items():
        line_id = len(file_line_mapping.replace('C:','').split('|'))
        if line_id == 2: scenario_and_outline_rows_mapping.update({file_line_mapping: value})
        if line_id == 3: example_rows_mapping.update({file_line_mapping: value})

    # assign/update all scenarios and scenario outlines with tags
    if scenario_and_outline_rows_mapping: update_feature_files_with_unique_test_case_ids(scenario_and_outline_rows_mapping)
    # assign/update all example rows with tags
    if example_rows_mapping: assign_tags_to_examples(example_rows_mapping)
