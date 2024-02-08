from lib.log import get_logger as log
from settings import LOG_LEVEL, CONSOLE_OUT
from collections import Counter
import re
logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)


def create_feature_file_tags_mapping(feature_file):
    feature_file_tags_mapping = {}
    with open(feature_file, 'r+') as feature:
        lines = feature.readlines()
        scenario_outline_tag_index = 0
        for index, line in enumerate(lines):
            if line.strip().startswith('Scenario:') or line.strip().startswith('Scenario Outline:'):
                scenario_tags = ''
                for scenario_tags_index in range(index - 1, 0, -1):
                    tag_line = lines[scenario_tags_index]
                    if tag_line.strip().startswith('@'):
                        scenario_tags += f'{tag_line} '
                    else:
                        break
                if line.strip().startswith('Scenario Outline:'): scenario_outline_tag_index = scenario_tags_index + 1
                if 'test_case_id' in scenario_tags:
                    id_tag = [tag.strip() for tag in scenario_tags.split() if 'test_case_id' in tag][0]
                    feature_file_tags_mapping.update({f'{feature_file}|{scenario_tags_index + 1}': id_tag})
                else:
                    # Scenario with no test_case_id
                    feature_file_tags_mapping.update({f'{feature_file}|{scenario_tags_index + 1}': 'none'})

            if line.strip().startswith('Examples:'):  # Scenario Outline Examples data table
                scenario_outline_file_tag = f'{feature_file}|{scenario_outline_tag_index}'
                if 'test_case_id' not in lines[index + 1]:
                    # Scenario Outline Header with no test_case_id column
                    feature_file_tags_mapping.update({f'{scenario_outline_file_tag}|{index + 1}': 'none_header'})
                for example_index in range(index + 2, len(lines), 1):
                    example_line_map = f'{scenario_outline_file_tag}|{example_index}'
                    example_line = lines[example_index]
                    if example_line.strip().startswith('|'):
                        cell = example_line.strip().split('|')[-2].strip()
                        if '@test_case_id' in cell:
                            feature_file_tags_mapping.update({example_line_map: cell})
                        else:
                            # Scenario Example row with no test_case_id
                            feature_file_tags_mapping.update({example_line_map: 'none_row'})
                    else:
                        break
    feature.close()
    return feature_file_tags_mapping


def update_feature_files_with_unique_test_case_ids(feature_files_tags_mapping):
    test_tag_ids = [int(tag.split('_')[-1]) for tag in list(feature_files_tags_mapping.values()) if
                    'test_case_id' in tag]
    test_tag_ids.sort()
    repeated_test_case_ids = {tag_id: count for tag_id, count in Counter(test_tag_ids).items() if count > 1}
    missing_test_case_ids = find_missing(test_tag_ids)
    last_id = 0 if not test_tag_ids else test_tag_ids[-1]

    for feature_file_with_line, tag_name in feature_files_tags_mapping.items():
        file_name, line_no = feature_file_with_line.split('|')
        with open(file_name, "r+") as feature:
            lines = feature.readlines()
            if 'test_case_id' in tag_name:
                tag_line_no = int(line_no)
                id = int(tag_name.split('_')[-1])
                if id in repeated_test_case_ids.keys() and repeated_test_case_ids[id] > 1:
                    if missing_test_case_ids:
                        missed_id = missing_test_case_ids.pop(0)
                        lines[tag_line_no] = re.sub('@test_case_id_\d+', f'@test_case_id_{missed_id}',
                                                    lines[tag_line_no])
                    else:
                        last_id += 1
                        test_tag_ids.append(last_id)
                        lines[tag_line_no] = re.sub('@test_case_id_\d+', f'@test_case_id_{last_id}',
                                                    lines[tag_line_no])
                    repeated_test_case_ids[id] = repeated_test_case_ids[id] - 1
            if tag_name == 'none':  # scenario with no test_case_id
                tag_line_no = int(line_no)
                if missing_test_case_ids:
                    missed_id = missing_test_case_ids.pop(0)
                    lines[tag_line_no] = lines[tag_line_no].strip() + f' @test_case_id_{missed_id}\n'
                else:
                    last_id += 1
                    test_tag_ids.append(last_id)
                    lines[tag_line_no] = lines[tag_line_no].rstrip() + f' @test_case_id_{last_id}\n'

            feature.seek(0)
            for line in lines:
                feature.write(line)
        feature.close()


def assign_tags_to_examples(feature_files_tags_mapping):
    so_example_index = 0
    # feature_files_tags_mapping_keys = list(feature_files_tags_mapping.keys())
    for index, (feature_file_with_line, tag_name) in enumerate(feature_files_tags_mapping.items()):
        tag_name = feature_files_tags_mapping[feature_file_with_line]
        file_name, so_line_no, line_no = feature_file_with_line.split('|')
        if tag_name in ['none_header', 'test_case_id']:
            so_example_index = 0
        else:
            so_example_index += 1

        with open(file_name, "r+") as feature:
            lines = feature.readlines()
            so_test_case_id = [tag for tag in lines[int(so_line_no)].split() if '@test_case_id' in tag][0]
            tag_line_no = int(line_no)

            if tag_name == 'none_header':  # Scenario Outline header with no 'test_case_id' column name
                lines[tag_line_no] = lines[tag_line_no].rstrip() + '@test_case_id|\n'

            if tag_name == 'none_row':  # Scenario Outline example rows with no test_case_id
                lines[tag_line_no] = lines[tag_line_no].rstrip() + f' {so_test_case_id}_{so_example_index}|\n'

            feature.seek(0)
            for line in lines:
                feature.write(line)
        feature.close()


def find_missing(lst):
    if not lst: return []
    start = lst[0]
    end = lst[-1]
    return sorted(set(range(start, end + 1)).difference(lst))


