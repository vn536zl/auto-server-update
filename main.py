import time
from distutils.dir_util import copy_tree

import io
import os
import re
import requests
import shutil
import zipfile
from mcstatus import BedrockServer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

webpage_url = "https://www.minecraft.net/en-us/download/server/bedrock"
server_directory = "old_server"
server = BedrockServer.lookup("localhost:19132")


def get_file_link():
    browser = webdriver.Edge()
    browser.get(webpage_url)

    browser.find_element(By.CLASS_NAME, 'form-check-input').click()

    for i in range(10):
        try:
            download_button = browser.find_element(By.XPATH, './/a[@role="button"]')
            return download_button.get_attribute('href')
        except NoSuchElementException as e:
            print('Retry element grab in 1 second')
            time.sleep(1)


def get_file(url):
    for i in range(3):
        try:
            response = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall('./updated_server')
            break
        except:
            print("Retrying file request in 3 seconds")
            time.sleep(3)


def copy_files():
    file_names = ['bedrock_server.exe', 'bedrock_server.pdb', 'release-notes.txt']
    folder_names = ['behavior_packs', 'definitions', 'resource_packs']
    for file in file_names:
        shutil.copy(f'updated_server/{file}', server_directory)
    for folder in folder_names:
        copy_tree(f'updated_server/{folder}', f'{server_directory}/{folder}')


def determine_update(download_url):
    file_version = re.search(r"(\d{1,2}[.])+zip$", download_url)
    to_version = re.search(r"(\d{1,2}[.])+", file_version[0])[0][:-1]
    try:
        server_status = server.status()
        from_version = server_status.version.name
        print(from_version)
    except TimeoutError:
        print("Server Status Timeout: Continue update")
        return True

    from_version_list = from_version.split('.')
    to_version_list = to_version.split('.')
    for i in range(len(from_version_list)):
        if from_version_list[i] != to_version_list[i]:
            print("Server Version outdated: Continue Update")
            return True

    print("Server Version Up-to-Date: Stop Update")
    return False


def kill_server():
    processes = os.popen('tasklist').readlines()
    for process in processes:
        process_name_reg = re.match(r"\w+.exe", process)
        if process_name_reg is not None:
            process_name = process_name_reg[0]
            if process_name == "bedrock_server.exe":
                os.system("taskkill /f /im bedrock_server.exe")


def restart_server():
    os.chdir(server_directory)
    os.system("bedrock_server")


def main():
    download_url = get_file_link()
    if determine_update(download_url):
        get_file(download_url)
        kill_server()
        copy_files()
        restart_server()


if __name__ == '__main__':
    main()
