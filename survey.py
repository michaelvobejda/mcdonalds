from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import argparse


def parse_args():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Automatically fill out McDonald\'s survey.')
    # Required positional argument
    parser.add_argument('code', help='The survey code on the receipt. Type as written with dashes.')
    return parser.parse_args()


def next_question(driver):
    driver.find_element_by_class_name('NextButton').click()


def answer_radio_question(driver):
    driver.find_element_by_class_name('radioSimpleInput').click()


def answer_all_radio_questions(driver):
    radios = driver.find_elements_by_xpath("//td[@aria-describedby='HighlySatisfiedNeitherDESC5']")
    if len(radios) == 0:
        radios = driver.find_elements_by_xpath("//td[@aria-describedby='HighlyLikelyDESC5']")
    for radio in radios:
        radio.click()


def answer_checkbox_question(driver):
    driver.find_element_by_class_name('checkboxSimpleInput').click()


def answer_no_problem(driver):
    driver.find_element_by_xpath("//td[@aria-describedby='YesNoASC2']/span[1]").click()


def validate_code_present(driver):
    val_code = driver.find_elements_by_class_name('ValCode')
    if len(val_code) == 0:
        return False
    else:
        print(val_code[0].get_attribute('innerHTML'))
        return True


def input_code(driver):
    args = parse_args()
    code_segs = args.code.split('-')
    names = ['CN1', 'CN2', 'CN3', 'CN4', 'CN5', 'CN6']
    for i in range(len(names)):
        name = names[i]
        code = code_segs[i]
        element = driver.find_element_by_name(name)
        element.send_keys(code)
    
    
    driver.find_element_by_name('NextButton').click()


def try_to(func, driver):
    try:
        return func(driver)
    except:
        return
    

def try_everything(driver):
    try_to(answer_radio_question, driver)
    try_to(answer_all_radio_questions, driver)
    try_to(answer_checkbox_question, driver)
    try_to(answer_no_problem, driver)
    try_to(next_question, driver)


def main():
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.mcdvoice.com/')

        input_code(driver)

        while not validate_code_present(driver):
            try_everything(driver)

    finally:
        driver.quit()

    return
    

if __name__ == '__main__':
    main()

