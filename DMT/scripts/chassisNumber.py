import cv2
import numpy as np
import imutils
import easyocr
from collections import OrderedDict
# from django.utils.encoding import smart_str, smart_unicode
# from PIL import Image

def preprocesscrChassis(image):
    # Gray scalling the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold and invert
    _,thr = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    inv   = 255 - thr

    #Perform morphological closing with square 7x7 structuring element to remove details and thin lines
    SE = np.ones((7,7),np.uint8)
    closed = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, SE)
    # DEBUG save closed image


    # Find row numbers of dark rows
    meanByRow=np.mean(closed,axis=1)
    rows = np.where(meanByRow<50)

    # Replace selected rows with those from the inverted image
    image[rows]=inv[rows]
    #print("Preprocessing part of chassis number finished \n")
    return image

def getTextChassis(preprocessImage):
    reader = easyocr.Reader(['en'], gpu = True)
    result = reader.readtext(preprocessImage)
    lenText = len(result)
    chassisNumber = ''

    if lenText == 1 :
        chassisNumber = result[0][-2]
    
    if lenText == 2 :
        if result[0][-2] > result[1][-2] :
            chassisNumber = result[0][-2]
        
        else:        
            for i in range(0, len(result)) :
                text = result[i][-2]
                chassisNumber += text
    
    chassisNumber = chassisNumber.replace(" ", "")
    #print("Chassis number text taken \n")
    
    return chassisNumber

#if __name__== "__main__":
    #files = [join('./input', f) for f in listdir('./input') if isfile(join('./input', f))]
    '''for filePath in files:
        print(filePath)
        img = cv2.imread(filePath)
        print(str(readcrbook(img, f'output/{filePath.split("/")[-1]}')))'''

if __name__== "__main__":
    img = cv2.imread('../userdata/image2.jpg')
    preproImg = preprocesscrChassis(img)
    chassisText = getTextChassis(preproImg)
    print("\n\n Chassis Number:",chassisText)
