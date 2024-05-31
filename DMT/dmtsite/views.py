import cv2
import logging
import sys
import traceback
import json
import pandas as pd
from io import StringIO
import numpy as np
from datetime import datetime

from PIL import Image
from difflib import SequenceMatcher

from django.conf import settings

from django.core.files.storage import default_storage

from django.shortcuts import render

from django.http import HttpResponse,HttpRequest, response
from django.contrib.auth.decorators import login_required, permission_required

import pymongo


from scripts.crbook import *
from scripts.license_plate import *
from scripts.dmt_automation import *
from scripts.RuleBase import *
from scripts.chassisNumber import *
from scripts.numberPlate import *
from scripts.CRBook_new import *

from .models import userTransaction
from django.utils import timezone

@login_required(login_url='/login')
def valuation(request):
    
    transaction = userTransaction(
        user = request.user,
        login_time=timezone.now(),
        visited_page = request.path,
    )
    
    transaction.save()

    #client = pymongo.MongoClient('mongodb+srv://dilruksha:Abc123Aa&0@cluster0.ghtk3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',27017)
    client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority", 27017)

    #DB = client.get_database('data_store')
    DB = client.get_database('data_store')

    #collection = DB.get_collection('vehical_data')
    collection = DB.get_collection('vehicle_data_2024_3')
    mod_collection = DB.get_collection('moderator_data')

    vehicle_data = collection.find({})
    
    
    # print('connect DB')

    if request.method=="POST":

        try:
            vehicle_category = collection.distinct('category')
            # vehicle_make = collection.collection.find({})
            vehicle_make = collection.distinct('make')
            vehicle_model = collection.distinct('model')
            # vehicle_model = collection.distinct('model')
            vehicle_year = collection.distinct('year')

        except Exception as e :
            print('error in passing data to drop down from the data base')

            ex_type, ex_value, ex_traceback = sys.exc_info()           

            if ex_type.__name__ == 'MultiValueDictKeyError' or ex_type.__name__ == 'AttributeError':
                e = 'Select all from dropdown lists before hit the submit button.!!!'
                

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            return render(request, "valuation.html",
            {'vehicle_category': vehicle_category,
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_year': vehicle_year,
                    "alert_type":"alert-nodata",
                    "alert_msg": e       
                            
                            })

        try:

            text_vehicle_category = request.POST['name_category']
            text_vehicle_make = request.POST['name_make'].title()
            text_vehicle_model = request.POST['name_model'].title()
            text_vehicle_year = request.POST['name_year']
            text_vehicle_purpose = request.POST['purpose']
                 
            print(text_vehicle_purpose) 
            
            is_advanced = None if request.POST["is_advanced"] == 'false' else True
            is_feedback = None if request.POST["is_feedback"] == 'false' else True
            # print("is_feedback",is_feedback)
            # print(type(text_vehicle_year))
            # print(request.POST)
            # print(f'#{text_vehicle_category}#{text_vehicle_make}#{text_vehicle_model}#{text_vehicle_engine_capacity}#{text_vehicle_year}#')

        except Exception as e :
            print('error in getting data from drop down')

            ex_type, ex_value, ex_traceback = sys.exc_info()           

            if ex_type.__name__ == 'MultiValueDictKeyError' or ex_type.__name__ == 'AttributeError':
                e  = 'Select all from dropdown lists before hit the submit button.!!!'
                
            

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)

            return render(request, "valuation.html",
            {       'vehicle_category': vehicle_category,
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_year': vehicle_year,
                    "alert_type":"alert-nodata",
                    "alert_msg": e       
                            
                            })

            

        
        try:
            alert_type = str()
            alert_msg = str()
            result_status = str()
            
            if is_feedback is None:
                
                if is_advanced is not None:
                    text_vehicle_milage = request.POST['milage'] 
                    text_vehicle_gear = request.POST['gear_type'] 
                    text_vehicle_engine_capacity = request.POST['engine_capacity'] + " cc"
                    text_vehicle_fuel_type = request.POST['fuel_type']
                    
                    result_vehicle = getRuleBaseDB(text_vehicle_category,text_vehicle_make,text_vehicle_model,
                                                    text_vehicle_year,text_vehicle_milage,text_vehicle_gear,text_vehicle_engine_capacity,text_vehicle_fuel_type,True)

                    result_status = "advanced"
                else:
                
                    # print("test")
                    result_vehicle = getRuleBaseDB(text_vehicle_category,text_vehicle_make,text_vehicle_model,
                                                        text_vehicle_year)


                result_vehicle_mod = getModRuleBaseDB(text_vehicle_category,text_vehicle_make,text_vehicle_model,
                                                    text_vehicle_year)

            
                if len(result_vehicle) is 0:

                            alert_type = "alert-nodata"
                            alert_msg = "Valuation process error!"  
                            
                else:
                    # print(result_vehicle.get('Mileage_Range'))       
                    result_status = "Advanced Valuation Processed" if result_status == 'advanced' else "Valuation Processed"
                    return render(request, 'valuation.html', {'vehicle_category': vehicle_category,
                                                            'vehicle_make': vehicle_make,
                                                            'vehicle_model': vehicle_model,
                                                            'vehicle_year': vehicle_year,
                                                            
                                                            # 'vehicle_milage': text_vehicle_milage,
                                                            # 'vehicle_gear': text_vehicle_gear,
                                                            # 'vehicle_engine_capacity': text_vehicle_engine_capacity,
                                                            # 'vehicle_fuel_type': text_vehicle_fuel_type,
                                                            
                                                            'selected_Category':text_vehicle_category,
                                                            'selected_Make':text_vehicle_make,
                                                            'selected_Model':text_vehicle_model,
                                                            'selected_Year':text_vehicle_year,
                                                            'selected_purpose': text_vehicle_purpose,
                                                            
                                                            "alert_type":alert_type,
                                                            "alert_msg":alert_msg,
                                                            "result_status":result_status,
                                                            
                                                            'valuation_amount':result_vehicle.get('format_valuvation_amount'),
                                                            'Maximum_amount':result_vehicle.get('format_Maximum_amount'),
                                                            'Minimum_amount':result_vehicle.get('format_Minimum_amount'),
                                                            'Mode_amount':result_vehicle.get('Mode_amount'),
                                                            'Mileage_Range':result_vehicle.get('Mileage_Range'),
                                                            'Moderator_amount':result_vehicle_mod.get('format_mod_valuvation_amount')
                                                            })
                
                
                return render(request, "valuation.html", 
                            {
                                'vehicle_category': vehicle_category,
                                'vehicle_make': vehicle_make,
                                'vehicle_model': vehicle_model,
                                'vehicle_year': vehicle_year,
                            
                                
                                "alert_type":alert_type,
                                "alert_msg":alert_msg,
                                # "result_status":result_status,
                            })
            else:
                
                collectionfb = DB.get_collection('feedback')
                item = collectionfb.insert({'feedBack': request.POST["feedbackIn"]})
                print('feed')
                print(request.POST["feedbackIn"])
                alert_type = 'alert-matching'
                alert_msg = 'Thank You Fro Your Feedback!!!'
                # return render(request, "valuation.html")
                return render(request, 'valuation.html', {'vehicle_category': vehicle_category,
                                                            'vehicle_make': vehicle_make,
                                                            'vehicle_model': vehicle_model,
                                                            'vehicle_year': vehicle_year,
                                                            
                                                            # 'vehicle_milage': text_vehicle_milage,
                                                            # 'vehicle_gear': text_vehicle_gear,
                                                            # 'vehicle_engine_capacity': text_vehicle_engine_capacity,
                                                            # 'vehicle_fuel_type': text_vehicle_fuel_type,
                                                            
                                                            # 'selected_Category':text_vehicle_category,
                                                            # 'selected_Make':text_vehicle_make,
                                                            # 'selected_Model':text_vehicle_model,
                                                            # 'selected_Year':text_vehicle_year,
                                                            # 'selected_purpose': text_vehicle_purpose,
                                                            
                                                            "alert_type":alert_type,
                                                            "alert_msg":alert_msg,
                                                            # "result_status":result_status,
                                                            
                                                            # 'valuation_amount':result_vehicle.get('format_valuvation_amount'),
                                                            # 'Maximum_amount':result_vehicle.get('format_Maximum_amount'),
                                                            # 'Minimum_amount':result_vehicle.get('format_Minimum_amount'),
                                                            # 'Mode_amount':result_vehicle.get('Mode_amount'),
                                                            # 'Mileage_Range':result_vehicle.get('Mileage_Range'),
                                                            # 'Moderator_amount':result_vehicle_mod.get('format_mod_valuvation_amount')
                                                            })
                
                
        except Exception as e :
            print('error in passing data to drop down')
            print('here')
            ex_type, ex_value, ex_traceback = sys.exc_info()           

            if ex_type.__name__ == 'MultiValueDictKeyError' or ex_type.__name__ == 'AttributeError':
                e  = 'Select all from dropdown lists before hit the submit button.!!!'
                

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            return render(request, "valuation.html",
            {       'vehicle_category': vehicle_category,
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_year': vehicle_year,
                    "alert_type":"alert-nodata",
                    "alert_msg": e       
                            
                            })


        

    else:
        try:
            vehicle_category = collection.distinct('category')
            
            vehicle_make = collection.distinct('make')
            vehicle_model = collection.distinct('model')
            vehicle_year = collection.distinct('year')
            vehicle_full_db = list(collection.find({}))

            vehicle_list = [{'category': obj['category'], 'make': obj['make'], 'model': obj['model'], 'year': obj['year']} for obj in vehicle_full_db]
            # print(len(vehicle_list))
            
            vehicle_details = list({v["model"]:v for v in vehicle_list}.values())
            # print(vehicle_make)
            # print(len(vehicle_details))
            
        except Exception as e :
            print('error in passing data to drop down')

            ex_type, ex_value, ex_traceback = sys.exc_info()           

            if ex_type.__name__ == 'MultiValueDictKeyError' or ex_type.__name__ == 'AttributeError':
                e  = 'Select all from dropdown lists before hit the submit button.!!!'
                
            

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            return render(request, "valuation.html",
            {       'vehicle_category': vehicle_category,
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_year': vehicle_year,
                    "alert_type":"alert-nodata",
                    "alert_msg": e       
                            
                            })

        return render(request, "valuation.html",{'vehicle_category': vehicle_category,

                                                    'vehicle_make': vehicle_make,
                                                    
                                                    'vehicle_details': vehicle_details,

                                                    'vehicle_model': vehicle_model,

                                                    'vehicle_year': vehicle_year,

                                                   })

    

@login_required(login_url='/login')
def Verification(request):
    
    transaction = userTransaction(
        user = request.user,
        login_time=timezone.now(),
        visited_page = request.path,
    )
    
    transaction.save()
    
    if request.method=="POST":

        def get_data(fileName):
            file = request.FILES[fileName]
            image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            fileName = default_storage.save(file.name, file)
            fileUrl = '/userdata/'+fileName

            return (file, image, fileName, fileUrl)

        def getTheBestNumberPlate(NumberPlate1, NumberPlate2, CRBookNumberPlate):
            selected_number_plate = str()
            sel_1 = str()
            sel_2 = str()
            n1 = NumberPlate1
            n2 = NumberPlate2
            # print("np1",n1)
            # print("np2",n2)
            # n3 = CRBookNumberPlate
            
            s12 = SequenceMatcher(None, n1, n2).ratio()
            # s13 = SequenceMatcher(None, n1, n3).ratio()
            # s23 = SequenceMatcher(None, n2, n3).ratio()

            if len(n1)<7 and len(n2)>=7:
                selected_number_plate = n2

            if len(n2)<7 and len(n1)>=7 :
                selected_number_plate = n1

            if len(n1)>=7 and len(n2)>=7:
                if n1 == n2:
                    selected_number_plate = n1
                selected_number_plate = "Not match!"

            # selected_number_plate = None
            return selected_number_plate


        result_status = request.POST["result_status"]
        status = request.POST["status"]

        try:
            alert_type = str()
            alert_msg = str()
            if status == "Initial":
                
                
                # Read all 6 images
                file_FrontImage, im_FrontImage, fileName_FrontImage, fileUrl_FrontImage = get_data('imageFile_FrontImage')
                file_BackImage, im_BackImage, fileName_BackImage, fileUrl_BackImage = get_data('imageFile_BackImage')
                file_CRBookImage, im_CRBookImage, fileName_CRBookImage, fileUrl_CRBookImage = get_data('imageFile_CRBookImage')  

                # For front and back images
                edgedImg_FrontImage = preprocessNumber(im_FrontImage)
                edgedImg_BackImage = preprocessNumber(im_BackImage)


                location_FrontImage, approx_FrontImage = createContuersNumber(edgedImg_FrontImage)
                location_BackImage, approx_BackImage = createContuersNumber(edgedImg_BackImage)

                # print("location_FrontImage", location_FrontImage)
                # print("approx_FrontImage", approx_FrontImage)
                cropped_image_FrontImage = cropNumber(im_FrontImage, location_FrontImage)
                cropped_image_BackImage = cropNumber(im_BackImage, location_BackImage)

                numberPlateDashed_FrontImage = readTextNumber (cropped_image_FrontImage)
                numberPlateDashed_BackImage = readTextNumber (cropped_image_BackImage)
                print('The number plate from front image: ', numberPlateDashed_FrontImage)
                print('The number plate from back image: ', numberPlateDashed_BackImage)


                drawedImage_FrontImage = drawImageNumber (im_FrontImage, numberPlateDashed_FrontImage, approx_FrontImage)
                drawedImage_BackImage = drawImageNumber (im_BackImage, numberPlateDashed_BackImage, approx_BackImage)
                
                
                
                saveNumberPlate(drawedImage_FrontImage, './userdata/'+fileName_FrontImage)
                saveNumberPlate(drawedImage_BackImage, './userdata/'+fileName_BackImage)

                # For CR Book reading
                results_CRBook, final_CRBookImage = readcrbook_new(im_CRBookImage, fileUrl_CRBookImage)
                print("CR book readings :\n", results_CRBook)
                saveNumberPlate(final_CRBookImage, './userdata/'+fileName_CRBookImage)


                # Taking the best number plate using fron, back and CRBook number plates
                theBestNumberPlate = getTheBestNumberPlate(numberPlateDashed_FrontImage, numberPlateDashed_BackImage, results_CRBook['VehicleRegistrationNumber'])
                print("The best number plate :", theBestNumberPlate)

                theBestNumberPlate = results_CRBook['VehicleRegistrationNumber']
                # result_status = None
                if theBestNumberPlate is None :
                    alert_type = "alert-nodata"
                    alert_msg = "License plate image not clear enough to compare!"               
                    # print("test")
                elif results_CRBook['VehicleRegistrationNumber'] is None or len(results_CRBook['VehicleRegistrationNumber'])<7:
                    alert_type = "alert-nodata"
                    alert_msg = "Cr Book image not clear enough to compare!"

                elif theBestNumberPlate == "Not match!" :
                    if numberPlateDashed_FrontImage == results_CRBook['VehicleRegistrationNumber'] or numberPlateDashed_BackImage == results_CRBook['VehicleRegistrationNumber']:
                        alert_type = "alert-matching"
                        alert_msg = "License plate image number matches with CR Book number plate correctly!"
                        theBestNumberPlate = results_CRBook['VehicleRegistrationNumber']
                        result_status = 'matched'
                        
                    else:           
                        alert_type = "alert-nodata"
                        alert_msg = "License plate image Front & Back are not matching or Not clear enough!"
                    
                elif theBestNumberPlate == results_CRBook['VehicleRegistrationNumber']:

                    alert_type = "alert-matching"
                    alert_msg = "License plate image number matches with CR book license plate number correctly!"
                    result_status = 'matched'



        
                return render(request, "Verification.html", 
                {
                    # Parsing front and back images to the html
                    "fileUrl_FrontImage":fileUrl_FrontImage,
                    "license_no_FrontImage":numberPlateDashed_FrontImage,
                    "fileUrl_BackImage":fileUrl_BackImage,
                    "license_no_BackImage":numberPlateDashed_BackImage,
                    "theBestNumberPlate":theBestNumberPlate,
                    
                    "alert_type":alert_type,
                    "alert_msg":alert_msg,
                    "result_status":result_status,

                    # Parsing CR book image reading to the html
                    "fileUrl_CRBookImage":fileUrl_CRBookImage,
                    "VehicleRegistrationNumber_BackImage": results_CRBook['VehicleRegistrationNumber'],
                    "ownership_CRBookImage": results_CRBook['ownership'],
                    "engine_number_CRBookImage": results_CRBook['engine_number'],
                    "vehicle_class_CRBookImage": results_CRBook['vehicle_class'],
                    "chassis_number_CRBookImage": results_CRBook['chassis_number'],
                    "make_CRBookImage": results_CRBook['make'],
                    "model_CRBookImage": results_CRBook['model'],
                    "year_no_CRBookImage": results_CRBook['year'],
                })
                
            elif status == "DMT inprogress":
                # print("dmt")
                theBestNumberPlate = request.POST["theBestNumberPlate"]
                enginNumber = request.POST["engine_number_CRBookImage"]
                chassisNumber = request.POST["chassis_number_CRBookImage"]
                # DMT verification/ result taking
                results_Numberplate = DMTautomation(theBestNumberPlate)
                print("Readings from DMT website :\n", results_Numberplate)
                
                # #STEP2 ALERTS
                if results_Numberplate.get('errorMessage'):
                    alert_type = "alert-nodata"
                    alert_msg = "Cannot find the vehicle in the system!"
                    
                elif enginNumber == results_Numberplate.get('EngineNumber'):

                    alert_type = "alert-matching"
                    alert_msg = "Engine number matches with Motor traffic department Engine number correctly!"
                    result_status = 'DMT verified'
                else:

                    alert_type = "alert-not-matching"
                    alert_msg = "Vehicle details does not match correctly! Please cross check with the results..."
                
                return render(request, "Verification.html", 
                {
                    "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                    "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                    "theBestNumberPlate":theBestNumberPlate,
                    
                    "alert_type":alert_type,
                    "alert_msg":alert_msg,
                    "result_status":result_status,
                    
                    "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                    "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                    "engine_number_CRBookImage": enginNumber,
                    "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                    "chassis_number_CRBookImage": chassisNumber,
                    "make_CRBookImage": request.POST["make_CRBookImage"],
                    "model_CRBookImage": request.POST["model_CRBookImage"],
                    "year_no_CRBookImage": request.POST["year_no_CRBookImage"],
                    
                    # Parsing values from DMT
                    "Report_Date":results_Numberplate.get('ReportDate'),
                    "ownership":results_Numberplate.get('ownership'),
                    "EngineNumber":results_Numberplate.get('EngineNumber'),
                    "VehicleClass":results_Numberplate.get('VehicleClass'),
                    "ConditionsNotes":results_Numberplate.get('ConditionsNotes'),
                    "Make":results_Numberplate.get('Make'),
                    "Model":results_Numberplate.get('Model'),
                    "ManufacturedYear":results_Numberplate.get('ManufacturedYear'),

                })
                
            elif status == "Valuation":
                
                # print("valuation")
                VehicleClass = request.POST["vehicle_class_CRBookImage"]
                Model =  request.POST["model_CRBookImage"]
                Make = request.POST["make_CRBookImage"].title()
                ManufacturedYear = request.POST["year_no_CRBookImage"]
                # Rule-base funstions
                result_category = getCategory(VehicleClass)
                




                result_model =  getModel(Model)
                result_model =  Model if result_model is None else result_model
                result_model =  result_model.title()
                print("Model from Rule-base :", result_model)
                print("Category from Rule-base :", result_category)
                print("class :", Make)
                print("model :", result_model)
                print("year :", ManufacturedYear)

                client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority",27017)

                DB = client.get_database('data_store')

                collection = DB.get_collection('vehicle_data')

                result_vehicle_mod = []
                result_vehicle =[]
                if result_category is None:
                    alert_type = "alert-nodata"
                    alert_msg = "Incorrect category details!"  
                elif result_model is None:
                    alert_type = "alert-nodata"
                    alert_msg = "inorrect model details!" 
                elif Make=='':
                    alert_type = "alert-nodata"
                    alert_msg = "Make required!"
                elif ManufacturedYear=='':
                    alert_type = "alert-nodata"
                    alert_msg = "Manufactured year required!" 
                else:
                    result_vehicle = getRuleBaseDB(result_category,
                                                Make,
                                                result_model,
                                                ManufacturedYear)
                    
                    result_vehicle_mod = getModRuleBaseDB(result_category,
                                                Make,
                                                result_model,
                                                ManufacturedYear)

                    print("Vehicle results from Rule-base :\n", result_vehicle)
                    
                    if len(result_vehicle) is 0:

                        alert_type = "alert-nodata"
                        alert_msg = "Valuation process error!"  
                        
                    else:
                        
                        result_status = 'Valuation processed with DMT' if result_status == 'DMT verified' else 'Valuation processed'
                        print(result_status)
                        
                        if result_status == 'Valuation processed with DMT':
                            return render(request, "Verification.html", 
                            {
                                # Parsing front and back images to the html
                                "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                                "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                                "theBestNumberPlate":request.POST["theBestNumberPlate"],
                                
                                "alert_type":alert_type,
                                "alert_msg":alert_msg,
                                "result_status":result_status,

                                # Parsing CR book image reading to the html
                                "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                                "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                                "engine_number_CRBookImage": request.POST["engine_number_CRBookImage"],
                                "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                                "chassis_number_CRBookImage": request.POST["chassis_number_CRBookImage"],
                                "make_CRBookImage": request.POST["make_CRBookImage"],
                                "model_CRBookImage": request.POST["model_CRBookImage"],
                                "year_no_CRBookImage": request.POST["year_no_CRBookImage"],

                                # Parsing values from Rule-Base
                                "Report_Date":request.POST["Report_Date"],
                                "ownership":request.POST["ownership"],
                                "EngineNumber":request.POST["EngineNumber"],
                                "VehicleClass":request.POST["VehicleClass"],
                                "ConditionsNotes":request.POST["ConditionsNotes"],
                                "Make":request.POST["Make"],
                                "Model":request.POST["Model"],
                                "ManufacturedYear":request.POST["ManufacturedYear"],
                                
                                'valuation_amount':result_vehicle.get('format_valuvation_amount'),
                                'Maximum_amount':result_vehicle.get('format_Maximum_amount'),
                                'Minimum_amount':result_vehicle.get('format_Minimum_amount'),
                                'Mode_amount':result_vehicle.get('Mode_amount'),
                                'Moderator_amount':result_vehicle_mod.get('format_mod_valuvation_amount')
                            })
                        else:
                            return render(request, "Verification.html", 
                        {
                            # Parsing front and back images to the html
                            "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                            "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                            "theBestNumberPlate":request.POST["theBestNumberPlate"],
                            
                            "alert_type":alert_type,
                            "alert_msg":alert_msg,
                            "result_status":result_status,

                            # Parsing CR book image reading to the html
                            "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                            "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                            "engine_number_CRBookImage": request.POST["engine_number_CRBookImage"],
                            "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                            "chassis_number_CRBookImage": request.POST["chassis_number_CRBookImage"],
                            "make_CRBookImage": request.POST["make_CRBookImage"],
                            "model_CRBookImage": request.POST["model_CRBookImage"],
                            "year_no_CRBookImage": request.POST["year_no_CRBookImage"],
                            
                            'valuation_amount':result_vehicle.get('format_valuvation_amount'),
                            'Maximum_amount':result_vehicle.get('format_Maximum_amount'),
                            'Minimum_amount':result_vehicle.get('format_Minimum_amount'),
                            'Mode_amount':result_vehicle.get('Mode_amount'),
                            'Moderator_amount':result_vehicle_mod.get('format_mod_valuvation_amount')
                        })
                        
                return render(request, "Verification.html", 
                        {
                            "alert_type":alert_type,
                            "alert_msg":alert_msg,
                            "result_status":result_status,
                        })
        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            if ex_type.__name__ == 'MultiValueDictKeyError' :
                e  = 'Empty fields occured. Upload the vehicle images and the scanned image for the CR book correctly.!!!' 
            
            elif ex_type.__name__ == 'NoSuchElementException' :
                e  = 'Verification failed through the Motor Traffic Department website since the incorrect license plate readings from the given images. Please upload clear images and try again.!!!' 

            elif ex_type.__name__ == 'IndexError' :
                e  = 'Incorrect license plate readings from the given images. Please upload clear images and try again.!!!' 

            elif ex_type.__name__ == 'error' :
                e  = 'Insert the correct file types (jpg, png and etc) for images.!!!' 

            elif ex_type.__name__ == 'WebDriverException' or ex_type.__name__ == 'SessionNotCreatedException':
                e  = 'Time out occured while verificating through the Motor Traffic Department website. Please try again in a moment.!!!'

            else:
                e = 'Something went wrong. Please try again in a moment.!!! '

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            
            if status == "Initial":
                
                return render(request, "Verification.html",
                {
                    "alert_type":"alert-nodata",
                    "alert_msg": e,
                    "result_status":result_status,        
                                
                                })

            elif status == "DMT inprogress":
                
                return render(request, "Verification.html",
                {
                    "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                    "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                    "theBestNumberPlate":request.POST["theBestNumberPlate"],
                    
                    "alert_type":"alert-nodata",
                    "alert_msg": e,
                    "result_status":result_status,  
                    
                    "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                    "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                    "engine_number_CRBookImage": request.POST["engine_number_CRBookImage"],
                    "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                    "chassis_number_CRBookImage": request.POST["chassis_number_CRBookImage"],
                    "make_CRBookImage": request.POST["make_CRBookImage"],
                    "model_CRBookImage": request.POST["model_CRBookImage"],
                    "year_no_CRBookImage": request.POST["year_no_CRBookImage"],        
                                
                                
                                })
            
            elif status == "Valuation":
                
                if result_status == 'DMT verified':
                    
                    return render(request, "Verification.html",
                    {
                        "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                        "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                        "theBestNumberPlate":request.POST["theBestNumberPlate"],
                        
                        "alert_type":"alert-nodata",
                        "alert_msg": e,
                        "result_status":result_status,  
                            
                        "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                        "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                        "engine_number_CRBookImage": request.POST["engine_number_CRBookImage"],
                        "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                        "chassis_number_CRBookImage": request.POST["chassis_number_CRBookImage"],
                        "make_CRBookImage": request.POST["make_CRBookImage"],
                        "model_CRBookImage": request.POST["model_CRBookImage"],
                        "year_no_CRBookImage": request.POST["year_no_CRBookImage"], 
                        
                        "Report_Date":request.POST["Report_Date"],
                        "ownership":request.POST["ownership"],
                        "EngineNumber":request.POST["EngineNumber"],
                        "VehicleClass":request.POST["VehicleClass"],
                        "ConditionsNotes":request.POST["ConditionsNotes"],
                        "Make":request.POST["Make"],
                        "Model":request.POST["Model"],
                        "ManufacturedYear":request.POST["ManufacturedYear"],
                                    
                                    
                                    })
                    
                else:
                    
                    return render(request, "Verification.html",
                    {
                        "fileUrl_FrontImage":request.POST["fileUrl_FrontImage"],
                        "fileUrl_BackImage":request.POST["fileUrl_BackImage"],
                        "theBestNumberPlate":request.POST["theBestNumberPlate"],
                        
                        "alert_type":alert_type,
                        "alert_msg":alert_msg,
                        "result_status":result_status,
                        
                        "fileUrl_CRBookImage":request.POST["fileUrl_CRBookImage"],
                        "ownership_CRBookImage": request.POST["ownership_CRBookImage"],
                        "engine_number_CRBookImage": request.POST["engine_number_CRBookImage"],
                        "vehicle_class_CRBookImage": request.POST["vehicle_class_CRBookImage"],
                        "chassis_number_CRBookImage": request.POST["chassis_number_CRBookImage"],
                        "make_CRBookImage": request.POST["make_CRBookImage"],
                        "model_CRBookImage": request.POST["model_CRBookImage"],
                        "year_no_CRBookImage": request.POST["year_no_CRBookImage"], 
                                    
                                    
                                    })
    else:
        return render(request, "Verification.html")



@login_required(login_url='/login')
# @permission_required("DMT.view_log",login_url='/login',raise_exception=True)
def RPA(request):
    

    transaction = userTransaction(
        user = request.user,
        login_time=timezone.now(),
        visited_page = request.path,
    )
    
    
    transaction.save()
    
    if request.method=="POST":
        try:
            text_Numberplate = request.POST['Numberplate']
            # print("status check", request.POST)
            if text_Numberplate is not None:

                results_Numberplate = DMTautomation(text_Numberplate)


            return render(request, "RPA.html", 

            {

                "Report_Date":results_Numberplate.get('ReportDate'),
                "VehicleRegistrationNumber":results_Numberplate.get('VehicleRegistrationNumber'),
                "ownership":results_Numberplate.get('ownership'),
                "EngineNumber":results_Numberplate.get('EngineNumber'),
                "VehicleClass":results_Numberplate.get('VehicleClass'),
                "ConditionsNotes":results_Numberplate.get('ConditionsNotes'),
                "Make":results_Numberplate.get('Make'),
                "Model":results_Numberplate.get('Model'),
                "ManufacturedYear":results_Numberplate.get('ManufacturedYear')
            })

        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            if ex_type.__name__ == 'NoSuchElementException' :
                e  = 'License plate number is empty or in invalid format.!!!' 

              
            
            if ex_type.__name__ == 'WebDriverException' :
                e  = 'DMT website is busy. Try again in a moment.!!!'
            

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            return render(request, "RPA.html",
            {
                  "alert_type":"alert-nodata",
                  "alert_msg": e        
                            
                            })
    else:

        return render(request, "RPA.html") 

@login_required(login_url='/login')
def moderate(request):
    
    transaction = userTransaction(
        user = request.user,
        login_time=timezone.now(),
        visited_page = request.path,
    )
    
    transaction.save()
    
    client = pymongo.MongoClient(
        "mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority", 27017)

    DB = client.get_database('data_store')
    # collection = DB.get_collection('vehicle_data')
    collection = DB.get_collection('moderator_data')

    if request.method == "POST":
        try:
            print('connect DB')

            query = request.POST
            r = json.dumps(query)

            res = json.loads(r)
            df = pd.DataFrame([res])

            today = datetime.today().strftime('%Y-%m-%d')
            user = 'Test User'

            df = df.assign(posted_date = today)
            df = df.assign(User = user)

            dict = df.to_dict(orient='records')


            if isinstance(dict , list):
                collection.insert_many(dict)
            else:
                collection.insert_one(dict)
        except Exception as e:
            print('error in passing data to drop down from the data base')

            ex_type, ex_value, ex_traceback = sys.exc_info()

            if ex_type.__name__ == 'MultiValueDictKeyError' or ex_type.__name__ == 'AttributeError':
                e = 'Select all from dropdown lists before hit the submit button.!!!'

            print("Exception type : ", ex_type.__name__)
            print("Exception message :", ex_value)
            print("Exception traceback :", ex_traceback)
            return render(request, "moderate2.html",
                              {
                               "alert_type": "alert-nodata",
                               "alert_msg": e

                               })

    return render(request, "moderate2.html")

