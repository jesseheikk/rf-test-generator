import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./src/")))

from confs import BASE_URL, OUTPUT_DIR
from robot_writer import append_to_robot_file, create_robot_file
from selenium_handler import (
    initialize_driver, read_js_file, inject_js_click_listener,
    log_element_info, wait_for_page_load_and_inject_js,
    get_logged_actions, clear_logged_actions
)

ACTION_LISTENER = "./src/action_listener.js"
ROBOT_TEMPLATE = "./robot_template.robot"
ROBOT_OUTPUT = os.path.join(OUTPUT_DIR, "output.robot")
ACTION_LOG = os.path.join(OUTPUT_DIR, "action_log.txt")

def main():
    driver = initialize_driver()
    driver.get(BASE_URL)

    js_script = read_js_file(ACTION_LISTENER)
    inject_js_click_listener(driver, js_script)

    create_robot_file(ROBOT_TEMPLATE, ROBOT_OUTPUT)

    try:
        while True:
            logged_actions = get_logged_actions(driver)
            if logged_actions:
                for action_info in logged_actions:
                    log_element_info(ACTION_LOG, action_info)
                    append_to_robot_file(action_info, ROBOT_OUTPUT)
                clear_logged_actions(driver)

            current_url = driver.current_url
            time.sleep(1)
            # Check if the page has been reloaded
            # TO DO: Detect reload with the same url?
            if current_url != driver.current_url:
                # Listeners needs to be re-injected when the page reloads
                wait_for_page_load_and_inject_js(driver, js_script)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
