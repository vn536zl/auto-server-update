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
# Replace value with location of your server
server_directory = "old_server"
# Use IP and Port of your server
server = BedrockServer.lookup("localhost:19132")


# Use selenium to retrieve the download url of new Bedrock Server
def get_file_link():
    print('Getting Most recent Bedrock Server Release...')

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


# Use Request and zipfile to download and unzip the new version
def get_file(url):
    print('Retrieving updated files...')

    for i in range(3):
        try:
            response = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall('./updated_server')
            break
        except:
            print("Retrying file request in 3 seconds")
            time.sleep(3)


# Copy necessary files to the old servers location
def copy_files():
    print('Copying new files...')

    file_names = ['bedrock_server.exe', 'bedrock_server.pdb', 'release-notes.txt']
    folder_names = ['behavior_packs', 'definitions', 'resource_packs']
    for file in file_names:
        shutil.copy(f'updated_server/{file}', server_directory)
    for folder in folder_names:
        copy_tree(f'updated_server/{folder}', f'{server_directory}/{folder}')


# Compare the download url version to the currently running server to determine if an update is needed
def determine_update(download_url):
    print('Determining if an update is necessary...')

    file_version = re.search(r"(\d{1,2}[.])+zip$", download_url)
    to_version = re.search(r"(\d{1,2}[.])+", file_version[0])[0][:-1]
    try:
        server_status = server.status()
        from_version = server_status.version.name
    except TimeoutError:
        print("Server Status Timeout: Continue update")
        return True

    print(f"Current Server Version: {from_version}")
    from_version_list = from_version.split('.')
    to_version_list = to_version.split('.')
    for i in range(len(from_version_list)):
        if from_version_list[i] != to_version_list[i]:
            print("Server Version outdated: Continue Update")
            return True

    print("Server Version Up-to-Date: Stop Update")
    return False


# Stop the bedrock_server.exe program from running if it is
def kill_server():
    print("Stopping old server if it's running...")

    processes = os.popen('tasklist').readlines()
    for process in processes:
        process_name_reg = re.match(r"\w+.exe", process)
        if process_name_reg is not None:
            process_name = process_name_reg[0]
            if process_name == "bedrock_server.exe":
                os.system("taskkill /f /im bedrock_server.exe")


# restart the server with the new version
def restart_server():
    print('Starting Updated Server...')

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
