import cv2
#from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import re
from PIL import Image

def preprocessNumber(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 20, 200) #Edge detection          
    
    #print("Preprocessing for number plate is finished.\n")
    
    return edged

def createContuersNumber(edged_image):
    
    keypoints = cv2.findContours(edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        # print("cont",approx)
        # print("len",len(approx))
        if len(approx) == 4:
            location = approx
            break

    #print("Contuering for number plate is finished.\n")       
    return location, approx


def cropNumber(image, location):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(image, image, mask=mask)
    
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    
    #print("Cropping for number plate is finished.\n")
    return cropped_image


def readTextNumber (cropped_image):
    text = ''
    numberPlate = ''
    numberPlateDashed = ''
    
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(cropped_image, detail=1, paragraph=False)
    
    lenText = len(result)
    

    if lenText == 1 :
        text = result[0][-2]
    
    if lenText == 2 :
        text = result[1][-2]
    
    if lenText == 3 :
        text = result[1][-2] + result[2][-2]     

    
    text = text.replace(" ", "")
    
    
    for i in range(0, len(text)) :
        if text[i].isalpha():
            numberPlate += text[i]
        
        if text[i].isdigit():
            numberPlate += text[i]
        
        else :
            continue
    
    
    for i in range(0, len(numberPlate)) :
        if numberPlate[i-1].isalpha() and numberPlate[i].isdigit():
            numberPlateDashed += ("-" + numberPlate[i])
    
        else:
            numberPlateDashed += numberPlate[i]

    #print("number plate read and text taken\n")        
    return numberPlateDashed


def drawImageNumber (image, numberPlateDashed, approx):
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(image, text=numberPlateDashed, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(image, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    
    #print('rectangle drwaen forn the number plate\n')
    return res

def saveNumberPlate (final_image, output):
    #image = Image.fromarray(final_image.astype(np.uint8))
    #image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    cv2.imwrite(output, final_image)
    #print("Image saved")


#if __name__== "__main__":
    #files = [join('./input', f) for f in listdir('./input') if isfile(join('./input', f))]
    '''for filePath in files:
        print(filePath)
        img = cv2.imread(filePath)
        print(str(readcrbook(img, f'output/{filePath.split("/")[-1]}')))'''

if __name__== "__main__":
    img = cv2.imread('../userdata/prasad.jpg')
    edgedImg = preprocessNumber(img)
    location, approx = createContuersNumber(edgedImg)
    cropped_image = cropNumber(img, location) 
    numberPlateDashed = readTextNumber (cropped_image)
    drawedImage = drawImageNumber (img, numberPlateDashed, approx)
    
    print("\n\nNumber Plate :",numberPlateDashed)
    
