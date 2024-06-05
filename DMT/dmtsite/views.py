
import sys


from django.conf import settings

from django.core.files.storage import default_storage

from django.shortcuts import render

from django.http import HttpResponse,HttpRequest, response
from django.contrib.auth.decorators import login_required, permission_required

import pymongo


from scripts.RuleBase import *

from .models import userTransaction
from django.utils import timezone

@login_required(login_url='/login')
def valuation(request):
    
    # transaction = userTransaction(
    #     user = request.user,
    #     login_time=timezone.now(),
    #     visited_page = request.path,
    # )
    
    # transaction.save()

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

    
