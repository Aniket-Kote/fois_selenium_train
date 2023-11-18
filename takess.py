
import pyautogui # for ss
from PIL import Image # to crop
import sys
import time

ss_file_name='ss.png'
captcha_name='cap.png'


def take_ss():
    time.sleep(5)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(ss_file_name)


def crop_ss():    
    # Opens a image in RGB mode
    im = Image.open(ss_file_name)

    # Size of the image in pixels (size of original image)

    # Setting the points for cropped image
    # left = 1000
    # top =650
    # right = 1185
    # bottom = 700
    
    # left = 554
    # top = 845
    # right = 780
    # bottom = 965 
    
    
    # left = 1055
    # top = 483
    # right = 1185
    # bottom = 521
    
    # left = 1070
    # top = 565
    # right = 1230
    # bottom = 610
    
    
    left = 1090
    top = 585
    right = 1230
    bottom = 630
    
    
    # pos={"top":376,"bottom":409,"left":725,"right":836}
    # left = pos['left']
    # top = pos['top']
    # right = pos['right']
    # bottom = pos['bottom']
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))

    # Shows the image in image viewer
    # im1.show()
    im1.save(captcha_name)
    
# take_ss()
# crop_ss()
