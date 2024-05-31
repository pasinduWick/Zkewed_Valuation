from os import listdir
from os.path import isfile, join
import cv2
from numpy.core.numeric import full
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'.\Django-App\venv\Lib\site-packages\tesseract.exe'


def preprocesscrbook(image):
    scale_percent = 150 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    img = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    img = cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    return img

def readcrbook(full_img, filePath):
    results = {}
    boxes = (
        ["license_number",340,225,220],
        ["chassis_number",340,1420,220],
        ["engine_number",1680,225,110],
        ["ownership",1440,225,250],
        ["category",1770,225,110],
        ["make",1975,225,110],
        ["model",2080,225,110],
        ["year",2300,1420,110],
        ["engine_capacity",1660,1420,110],
        ["condition", 1865,225,110],
    )

    for attribute, top, left, h in boxes:
        crop_image = full_img[top:top+h, left: left+1200]
        img=preprocesscrbook(crop_image)
        text = pytesseract.image_to_string(img, lang="eng", config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        cleaned_text = text.strip().split('\n')[-1].replace(' ','').upper()
        full_img = cv2.rectangle(full_img, (left, top), (left+1200, top+h), (255, 0, 0), 5)
        full_img = cv2.putText(full_img, cleaned_text, (left+15, top+h-20), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255,0,255), thickness=5)
        results[attribute] = cleaned_text

    # cv2.imshow(filePath.split('/')[-1], full_img)
    # cv2.waitKey()
    cv2.imwrite(filePath, full_img)
    return results


#if __name__== "__main__":
    #files = [join('./input', f) for f in listdir('./input') if isfile(join('./input', f))]
    '''for filePath in files:
        print(filePath)
        img = cv2.imread(filePath)
        print(str(readcrbook(img, f'output/{filePath.split("/")[-1]}')))'''

if __name__== "__main__":
    img = cv2.imread('../userdata/OCRFILE0000301A_V1cmZFS.jpg')
    print(str(readcrbook(img, '../userdata/OCRFILE0000301A_V1cmZFS.jpg')))
    #img = cv2.imread(r'D:\zkewed\product\Valuation\Django-App\DMT\userdata\OCRFILE0000301A_V1cmZFS.jpg')
    #print(str(readcrbook(img, r'D:\zkewed\product\Valuation\Django-App\DMT\userdata\OCRFILE0000301A_V1cmZFS.jpg')))