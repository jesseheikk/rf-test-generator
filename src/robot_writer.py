import shutil
import json
import os

from confs import BROWSER_KEYWORDS, LOCATOR_ATTRIBUTES

def create_robot_file(robot_template_path, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(robot_template_path, 'r') as template_file:
        content = template_file.read()
    
    # Fix the confs path in case the output file is in a different directory
    confs_path = os.path.relpath("confs.py", os.path.dirname(output_path))
    content = content.replace("Variables    confs.py", f"Variables    {confs_path}")

    with open(output_path, 'w') as output_file:
        output_file.write(content)

def get_element_locator(element):
    attributes = element['attributes']

    for attribute in LOCATOR_ATTRIBUTES:
        if attribute in attributes:
            return f"{attribute}={attributes[attribute]}"

    return f"xpath={element['xpath']}"

def get_previous_line(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('***')]
    last_task_line = lines[-1]
    components = last_task_line.split('    ')

    last_line = {
        "keyword": components[0].strip(),
        "locator": components[1].strip() if len(components) > 1 else "",
        "argument": components[2].strip() if len(components) > 2 else ""
    }

    return last_line

def update_output_file(output_path, keyword, locator, argument):
    previous_line = get_previous_line(output_path)
    if keyword == "Press Keys":
        if previous_line["keyword"] == "Press Keys" and previous_line['locator'] == locator:
            action_line = f"    {argument}"
        else:
            action_line = f"\n    {keyword}    {locator}    {argument}"
    else:
        action_line = f"\n    {keyword}    {locator}   {argument}"

    with open(output_path, "a") as robot_file:
        robot_file.write(action_line)

def get_keyword_argument(action_data):
    action = action_data["action"]

    if action == "contextmenu":
        argument = "right"
    elif action == "keydown":
        argument = action_data["key"]
    else:
        argument = ""

    return argument

def append_to_robot_file(action_info, output_path):
    action_data = json.loads(action_info)

    keyword = BROWSER_KEYWORDS[action_data["action"]]
    locator = get_element_locator(action_data["element"])
    argument = get_keyword_argument(action_data)

    update_output_file(output_path, keyword, locator, argument)
