import cv2
import numpy as np
import urllib.request
import requests
from bs4 import BeautifulSoup
import os
#USE WIN32GUI for faster response
import pyautogui
import time
from PIL import Image, ImageGrab
from Modules import CmdCustomizer as cmd
from win32api import GetSystemMetrics

DONE = False

DATABASE = 'Database'
INVALID_ITEMS = [
'Mustache.jpg', 'Portable Table Device.jpg', 'Supply Drop.jpg',
'Brick of Cash.jpg', 'Box.jpg','GuNNER.jpg', 'Sling.jpg', 'Grasschopper.jpg'
]

def UpdateDatabase():
    invalid = ['/']
    categories = ['Guns', 'Items']
    URL = f'https://enterthegungeon.gamepedia.com/{categories[0]}'
    page = urllib.request.urlopen(URL).read()
    content = BeautifulSoup(page, 'html.parser')
    content = content.find('table', {'class':'wikitable'})

    images = content.findAll('img')

    for image in images:
        title = image['alt'].split('.')[0]
        try:title.replace('/', '_')
        except Exception as error: print(error)

        source = image['src']

        try: urllib.request.urlretrieve(source, f'{DATABASE}/{categories[0]}/{title}.jpg')
        except Exception as error: print(error)

def FindItem(threshold: float, delta: int):
    detected_items = list()

    template = cv2.imread('Template_Small.jpg')
    for folder in os.listdir(DATABASE):
        for item_id in os.listdir(f'{DATABASE}/{folder}'):
            if(item_id in INVALID_ITEMS):continue
            item = cv2.imread(f'{DATABASE}/{folder}/{item_id}')

            for i in range(1, delta + 1):
                loc = None
                # MAKE MORE VERSATILE
                item = cv2.resize(item, (item.shape[1] * 3, item.shape[0] * 3))
                h, w = item.shape[:-1]

                result = cv2.matchTemplate(template, item, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                loc = np.where(result >= threshold)

                for pt in zip(*loc[::-1]):
                    if(ContainsItem(item_id, detected_items)):continue
                    cv2.rectangle(template, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    detected_items.append((GetConfidence(result), item_id))
    print(detected_items, end='\n\n')
    DisplayInformation(detected_items)
    cv2.imwrite('result.png', template)

def MousePosition():
    position = pyautogui.position()
    return position.x, position.y

def GetImageAroundCursor(width: int, height: int):
    positionX, positionY = MousePosition()
    image = np.array(ImageGrab.grab(bbox=(positionX - width / 2, positionY - height / 2,
    positionX + height / 2, positionY + width / 2)))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('Template_Small.jpg',image)
    return image

def GetImage(width, height):
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    image = np.array(ImageGrab.grab(bbox=(
    screenWidth / 2 - width / 2, screenHeight / 2 - height / 2, screenWidth / 2 + width / 2 , screenHeight / 2 + height / 2)))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('Template_Small.jpg',image)
    return image

def GetConfidence(result):
    _, max_value, _, _ = cv2.minMaxLoc(result)
    return max_value

def FindImage(name: str):
    return cv2.imread(f'{DATABASE}/{name}')

def ContainsItem(item_id, list: list):
    for item in list:
        if(item_id in item):
            return True
    return False

def DisplayInformation(list):
    global DONE
    cmd.Window.clear()
    if(len(list) <= 0):
        print('Could not find Item :(')
        DONE = True
        return
    #item = max(list,key=lambda item:item[1])[1].strip('.jpg')

    for item in list:
        print(item[1].strip('.jpg'))
        print(FindInformation(item), end='\n\n')
    DONE = True

def FindInformation(item_id):
    global DONE
    try:
        item_id = item_id[1].replace(' ', '_')
        URL = f'https://enterthegungeon.gamepedia.com/{item_id[1]}'
        page = urllib.request.urlopen(URL).read()

        content = BeautifulSoup(page, 'html.parser')
        content = content.find('div', {'class':'mw-parser-output'})
        information = content.findAll('ul')[1]
        information = information.find('li').text
        return information
    except Exception as error:
        return error

def CreateHeadlessFirefoxBrowser():
     options = webdriver.ChromeOptions()
     options.add_argument('--headless')
     return webdriver.Chrome(options=options)

def main():
    global DONE
    while True:
        GetImage(300, 300)
        FindItem(.8, 1)
        while not DONE:
            pass



if __name__ == '__main__':
    main()
