from os import listdir
from os.path import isfile, join
import cv2
from numpy.core.numeric import full
import pytesseract
import numpy as np
import easyocr

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'..\shanil\Django-App\venv\Lib\site-packages\tesseract.exe'

def preprocesscrbook_new(full_img):
    gray = cv2.cvtColor(full_img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7),0)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    edged = cv2.Canny(blur, 20, 200)
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[0]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    
    
    
    for c in cnts:
        left,top,w,h = cv2.boundingRect(c)
        if h > 500 and w >600:
            
            # print("test")
            gray = gray[top:top+h , left:left+w]
            break
    
    gray = cv2.resize(gray,(870,1222))
    return gray

def cleaup_CR(img):
    crop_image = img
    blurred = cv2.GaussianBlur(crop_image, (3, 3), 0)

    thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)[1]
    aspt = cv2.adaptiveThreshold(crop_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,19,6)

    # Define Gabor filter parameters
    kernel_size = 31
    theta = np.pi / 1 # Angle of the stripes (45 degrees)
    sigma = 3
    lambda_ = 4
    gamma = 0.5

    # Create Gabor filter for detecting angled stripes
    gabor_filter = cv2.getGaborKernel((kernel_size, kernel_size), sigma, theta, lambda_, gamma, 0, ktype=cv2.CV_32F)

    filtered_image = cv2.filter2D(crop_image, cv2.CV_32F, gabor_filter)
    
    filtered_image = cv2.convertScaleAbs(filtered_image)
    
    _, mask = cv2.threshold(filtered_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = 255 - mask
    masked_final = cv2.bitwise_or(aspt, thresh)
    masked_image = cv2.bitwise_and(crop_image, crop_image, mask=masked_final)
    
    
    return masked_image

def readcrbook_new(full_img, filePath):
    full_img=preprocesscrbook_new(full_img)
    full_img=cleaup_CR(full_img)
    
    
    
    results = {}
    boxes = (
        ["VehicleRegistrationNumber",92,44,34],
        ["ownership",166,44,57],        
        ["engine_number",530,44,35],
        ["vehicle_class",573,44,21],
        ["chassis_number",96,450,34],
        ["make",644,44,21],
        ["model",680,44,21],
        ["year",754,458,22],
    )

    for attribute, top, left, h in boxes:
        
        if attribute == 'VehicleRegistrationNumber':
            crop_image = full_img[top:top+h, left: left+210]
            
            text = pytesseract.image_to_string(crop_image, lang="eng", config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            cleaned_text = text.strip().split('\n')[-1].replace(' ','').upper()
            full_img = cv2.rectangle(full_img, (left, top), (left+210, top+h), (255, 0, 0), 3)
            
                        
            license_number = ''
            for i in range(0, len(cleaned_text)) :
                if i==0:
                    if cleaned_text[i].isalpha():
                        continue
        
                if i==1:
                    if cleaned_text[i].isalpha():
                        continue
      
                license_number += cleaned_text[i]
       
            cleaned_text = license_number
            full_img = cv2.putText(full_img, cleaned_text, (left+15, top+h-20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), thickness=3)
            # print("Test num",cleaned_text)    
            
        if attribute == 'ownership':
            crop_image = full_img[top:top+h, left: left+450]
            # reader = easyocr.Reader(['en'], gpu = True)
            # text = reader.readtext(crop_image, detail = 0, paragraph=True)[0]
            text = pytesseract.image_to_string(crop_image, lang="eng", config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ- ')
            cleaned_text = text.strip().split('\n')
            # text = text[0] if len(text) > 0 else ""
            full_img = cv2.rectangle(full_img, (left, top), (left+450, top+h), (255, 0, 0), 3)
            # print("Test own",cleaned_text)
            
            count = 50
            ownership = ''
            text = ''
            for x in cleaned_text:
                text += x + ' '
            # print("cl text",text)
            for i in text:
                full_img = cv2.putText(full_img, i, (left+1350, top+count), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255,0,255), thickness=3)
                ownership += i+''
                count+=40
                
            
            cleaned_text= ownership
            
            
        if attribute == 'engine_number' or attribute == 'vehicle_class' or attribute == 'make' or attribute == 'model' :
            # print(attribute)
            crop_image = full_img[top:top+h, left: left+300]
            # img=preprocesscrbook_new(crop_image)
            # reader = easyocr.Reader(['en'], gpu = True)
            # cleaned_text = reader.readtext(crop_image, detail = 0, paragraph=False)
            # # print(len(cleaned_text))
            # if len(cleaned_text) > 0:
            #     cleaned_text = cleaned_text[0]
            # else:
            #     cleaned_text = ""
                
                
            text = pytesseract.image_to_string(crop_image, lang="eng", config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ- ')
            cleaned_text = text.strip().split('\n')[-1]
            
            print("Test rest",cleaned_text)
            full_img = cv2.rectangle(full_img, (left, top), (left+300, top+h), (255, 0, 0), 3) 
            # full_img = cv2.putText(full_img, cleaned_text, (left+400, top+h-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), thickness=3)
            # print("Test rest",cleaned_text)
            
            
        if attribute == 'year':
            crop_image = full_img[top:top+h, left: left+200]
            # img=preprocesscrbook_new(crop_image)
                    
            text = pytesseract.image_to_string(crop_image, lang="eng", config='-c tessedit_char_whitelist=0123456789')
            cleaned_text = text.strip().split('\n')[-1].replace(' ','').upper()
            # reader = easyocr.Reader(['en'], gpu = True)
            # cleaned_text = reader.readtext(crop_image, detail = 0, paragraph=False)
            full_img = cv2.rectangle(full_img, (left, top), (left+200, top+h), (255, 0, 0), 3)
            # full_img = cv2.putText(full_img, cleaned_text, (left+500, top+h-20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), thickness=3)
            # print("Test yr",cleaned_text)
            # cv2.imwrite(r'C:\Users\PC\Downloads\vehi_images_dek\final.jpg',img)
        
        
        if attribute == 'chassis_number':
            crop_image = full_img[top:top+h, left: left+250]
            # img=preprocesscrbook_new(crop_image)
            text = pytesseract.image_to_string(crop_image, lang="eng", config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            cleaned_text = text.strip().split('\n')[-1].replace(' ','').upper()
            full_img = cv2.rectangle(full_img, (left, top), (left+450, top+h), (255, 0, 0), 3)
            full_img = cv2.putText(full_img, cleaned_text, (left+25, top+h-20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), thickness=3)
            # print("Test chas",cleaned_text)
        #print('CR book reading ', attribute, 'finished\n')
    
    # cv2.imwrite(r'C:\Users\PC\Downloads\vehi_images_dek\final2.jpg',full_img)
           
        results[attribute] = cleaned_text
    print(results)    
        
        
        

    
        
    # cv2.imwrite(r'C:\Users\PC\Downloads\vehi_images_dek\final.jpg',full_img)
    # cv2.imshow('test', full_img)
    # cv2.waitKey(0)
    
    return (results, full_img)

#if __name__== "__main__":
    #files = [join('./input', f) for f in listdir('./input') if isfile(join('./input', f))]
    '''for filePath in files:
        print(filePath)
        img = cv2.imread(filePath)
        print(str(readcrbook(img, f'output/{filePath.split("/")[-1]}')))'''

if __name__== "__main__":
    #results,img = cv2.imread('../userdata/99CD2CC8A-7D4C-45C1-BA36-F7DC25D34204_1fiGFe7.jpg')
    #print(str(readcrbook_new(results, '../userdata/9CD2CC8A-7D4C-45C1-BA36-F7DC25D34204.jpg')))
    results = cv2.imread(r'C:\Users\PC\Downloads\vehi_images_dek\All\IMG-20231213-WA0070.jpg')
    # print(str(readcrbook_new(results,r'C:\Users\PC\Downloads\vehi_images_dek\KK-7767\IMG-20231213-WA0100.jpg')))
    readcrbook_new(results,r'C:\Users\PC\Downloads\vehi_images_dek\KK-7767\IMG-20231213-WA0100.jpg')