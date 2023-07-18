import requests
import re
import os
import shutil
from mcstatus import JavaServer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

webpage = 'https://www.minecraft.net/en-us/download/server'
new_version = []

# Change to path of Java server
server_path = "jserver"
# Change to servers IP and Port
server = JavaServer.lookup('serverip:25565')


def get_file_link():
    print('Getting link to new server download...')
    global new_version
    browser = webdriver.Edge()
    browser.get(webpage)

    try:
        elem = browser.find_element(By.XPATH, '//a[@aria-label="mincraft version"]')
        elem_text = elem.text
        version = re.search(r"([.]\d+)+", elem_text)[0].split('.')
        for v in version:
            if v != '':
                new_version.append(v)
        return elem.get_attribute('href')
    except NoSuchElementException:
        print('Error: Element Not Found')


def is_update_needed():
    print('Determining if update is needed...')
    server_status = server.status()
    try:
        server_version = server_status.version.name.split('.')
    except TimeoutError:
        print('Server timeout: Continue Update')
        return True

    for i in range(len(server_version)):
        if server_version[i] != new_version[i]:
            print('Miss-matched versions: Continue Update')
            return True

    print('Server is up to date.')
    return False


def stop_old_server():
    print('Stopping old server if it is running...')
    processes = os.popen('tasklist /v /FI "IMAGENAME eq java.exe" | find /i "Minecraft server"').readlines()

    for process in processes:
        if process is not None:
            pid = re.search(r"\d{4,}", process)[0]
            os.popen(f'taskkill /pid {pid}')


def get_file(file_url):
    print('Getting the new server file...')
    resp = requests.get(file_url, allow_redirects=True)

    with open('server.jar', 'wb') as f:
        f.write(resp.content)


def copy_file_clean_up():
    print('Copying new file and cleaning up...')
    shutil.copy('server.jar', server_path)
    os.remove('server.jar')


def restart_server():
    print('Restarting server...')
    os.chdir(server_path)
    os.system('./run_server')


def main():
    print('Updating server...')
    file_url = get_file_link()
    if is_update_needed():
        get_file(file_url)
        stop_old_server()
        copy_file_clean_up()
        restart_server()


if __name__ == '__main__':
    main()
