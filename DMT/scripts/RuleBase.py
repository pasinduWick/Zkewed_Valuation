#from dmtsite.utils import *
import string
from pandas import DataFrame
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.message import _EMPTY


# assigning vehicle category 

def Merge(dict1, dict2):
    return(dict2.update(dict1))


def getCategory(vehicle_category):


    search_category = vehicle_category.upper()
    # print(search_category)
    #convert df to dictionary
    #dict_from_csv = pd.read_csv('./excel/category.csv', header=None, index_col=0, squeeze=True).to_dict()
    dict_from_csv = pd.read_csv(r'C:\Users\PC\Documents\Zkewed\Product\DMT\excel\category.csv').to_dict('records')
    # print(dict_from_csv)
    for item in dict_from_csv:  
        print(item['dmt_name'])
        if item['dmt_name'] == search_category:
            new_category_name = item['given_name']
            return new_category_name

# assigning vehicle model
def getModel(vehicle_model):

    search_category = vehicle_model.upper()

    #convert df to dictionary
    #dict_from_csv = pd.read_csv('./excel/model.csv', header=None, index_col=0, squeeze=True).to_dict()
    #dict_from_csv = pd.read_csv(r'D:\zkewed\new project\Django-App\DMT\excel\model.csv', header=None, index_col=0, squeeze=True).to_dict()
    dict_from_csv = pd.read_csv(r'C:\Users\PC\Documents\Zkewed\Product\DMT\excel\model.csv').to_dict('records')
    for item in dict_from_csv:  
        if item['dmt_name'] == search_category:
           new_model_name = item['given_name']
           return new_model_name


# assigning vehicle valuation
def getRuleBaseDB(vehicle_category,vehicle_make,vehicle_model,vehicle_year,vehicle_milage=None,vehicle_gear=None,vehicle_engine_capacity=None,vehicle_fuel_type=None, isAdvanced = None):

    #client = pymongo.MongoClient('mongodb+srv://dilruksha:Abc123Aa&0@cluster0.ghtk3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',27017)
    client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority",27017)
    
    #DB = client.get_database('data_store')
    DB = client.get_database('data_store')

    collection = DB.get_collection('vehicle_data_2024_3')
    #mod_collection = DB.get_collection('moderator_data')
    #collection = DB.get_collection('vehical_data')
    print("Connected")

    getvehicle_category = vehicle_category

    getvehicle_make = vehicle_make
    getvehicle_model = vehicle_model
    getvehicle_engine_capacity = vehicle_engine_capacity
    getvehicle_year = int(vehicle_year)
    getvehicle_gear = vehicle_gear
    getvehicle_fuel_type = vehicle_fuel_type
    
    if isAdvanced is not None:
        getvehicle_milage = int(vehicle_milage)
        getvehicle_milage = int(np.ceil(getvehicle_milage/50000)*50000)


    # print(type(getvehicle_milage))
    # print(getvehicle_gear)
    # print(getvehicle_fuel_type)
    # print(getvehicle_engine_capacity)


    mydic1 = {}
    #mydic2 = {}
    getdata = collection.find({
                                'category': getvehicle_category,
                                'make': getvehicle_make,
                                'model': getvehicle_model,
                                # 'year': getvehicle_year,
                                # 'mileage': getvehicle_milage,
                                # 'gear': getvehicle_gear,
                                # 'fuel_type': getvehicle_fuel_type, 
                                # 'engine_capability': getvehicle_engine_capacity,
                                },
                                {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1, "mileage":1,"gear":1,"fuel_type":1,"engine_capability":1}
                                )
    # getdata2 = collection.find({'category': 'Cars','make': getvehicle_make, 'model': getvehicle_model,'year': getvehicle_year},
    #                             {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1})

    '''getdata_mod = mod_collection.find({'category': getvehicle_category, 'make': getvehicle_make, 'model': getvehicle_model,
                                    'year': getvehicle_year},
                                {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1})'''

    # print(list(getdata))
    df = DataFrame(list(getdata))
    print(df)


    if not df.empty:
        mileage_range = str()
        df['year'] = df['year'].astype(int)
        # year filtering
        year_filterd_df = df[df['year'] == getvehicle_year]
        # print(year_filterd_df)
        
        if len(year_filterd_df) < 3:
            around_year = [getvehicle_year+1,getvehicle_year, getvehicle_year-1]
            year_filterd_df = df[df['year'].isin(around_year)]
            # print("around year",year_filterd_df)

        if (not year_filterd_df.empty) and (isAdvanced is not None):
            
            # advance filters
            year_filterd_df.loc[:,'engine_capability'] = year_filterd_df['engine_capability'].str.replace(',','')
            adFilt = (year_filterd_df['gear'] == getvehicle_gear) & (year_filterd_df['engine_capability'] == getvehicle_engine_capacity) & (year_filterd_df['fuel_type'] == getvehicle_fuel_type)
            advance_filtered_df = year_filterd_df[adFilt]
            print("adf",advance_filtered_df)

            mileage_filtered_df = advance_filtered_df
            if not advance_filtered_df.empty:
                # mileage range filter
                advance_filtered_df.loc[:, 'mileage'] = advance_filtered_df['mileage'].str.replace(',','')
                advance_filtered_df.loc[:, 'mileage'] = advance_filtered_df['mileage'].str.replace(' km','')
                
                mileageFilt = (advance_filtered_df['mileage'].astype(int) >= (getvehicle_milage-50000)) & (advance_filtered_df['mileage'].astype(int) <= getvehicle_milage)
                mileage_filtered_df = advance_filtered_df[mileageFilt]
                mileage_range = str(getvehicle_milage-50000 )+ "Km - " + str(getvehicle_milage) + "Km"
                
                if mileage_filtered_df.empty:
                    mileageFilt = (advance_filtered_df['mileage'].astype(int) >= (getvehicle_milage-50000)) & (advance_filtered_df['mileage'].astype(int) <= (getvehicle_milage+50000))
                    mileage_filtered_df = advance_filtered_df[mileageFilt]
                    mileage_range = str(getvehicle_milage-50000) + "Km - " + str(getvehicle_milage+50000) + "Km"
                    
                print("mil fil",mileage_filtered_df)
                print("mil fil",mileage_range)
            
            final_Df = mileage_filtered_df
        
        else:
            
            final_Df = year_filterd_df
        
        if not final_Df.empty:
            
            valuvation_amount = final_Df['price'].astype(float).mean()   
            format_valuvation_amount = "{:,.2f}".format(valuvation_amount)
            #format_valuvation_amount = "{:,}".format(format_valuvation_amount)


            Maximum_amount = final_Df['price'].astype(float).max()
            format_Maximum_amount = "{:,.2f}".format(Maximum_amount)


            Minimum_amount = final_Df['price'].astype(float).min()
            format_Minimum_amount = "{:,.2f}".format(Minimum_amount)


            Mode_amount = final_Df['price'].mode(dropna=False)[0]#.astype(float)
            #format_Mode_amount = "{:.2f}".format(Mode_amount)

        
            mydic1 = {  'format_valuvation_amount':format_valuvation_amount,
                        'format_Maximum_amount' : format_Maximum_amount,
                        'format_Minimum_amount':format_Minimum_amount,
                        'Mode_amount':Mode_amount,
                        'Mileage_Range':mileage_range
                        
                        }

    else:
        print("DF is empty")


    #dict = Merge(mydic1, mydic2)
    print(mydic1)
    return mydic1

def getRuleBaseDB2(vehicle_category,vehicle_make,vehicle_model,vehicle_year,vehicle_milage=None,vehicle_gear=None,vehicle_engine_capacity=None,vehicle_fuel_type=None):

    #client = pymongo.MongoClient('mongodb+srv://dilruksha:Abc123Aa&0@cluster0.ghtk3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',27017)
    client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority",27017)
    
    #DB = client.get_database('data_store')
    DB = client.get_database('data_store')

    collection = DB.get_collection('vehicle_data_2024_1')
    #mod_collection = DB.get_collection('moderator_data')
    #collection = DB.get_collection('vehical_data')
    print("Connected")

    getvehicle_category = vehicle_category

    getvehicle_make = vehicle_make
    getvehicle_model = vehicle_model
    getvehicle_engine_capacity = vehicle_engine_capacity
    getvehicle_year = vehicle_year
    getvehicle_milage = vehicle_milage
    getvehicle_gear = vehicle_gear
    getvehicle_fuel_type = vehicle_fuel_type

    # print(getvehicle_milage)
    # print(getvehicle_gear)
    # print(getvehicle_fuel_type)
    # print(getvehicle_engine_capacity)


    mydic1 = {}
    #mydic2 = {}
    getdata = collection.find({
                                'category': getvehicle_category,
                                'make': getvehicle_make,
                                'model': getvehicle_model,
                                # 'year': getvehicle_year,
                                # 'mileage': getvehicle_milage,
                                # 'gear': getvehicle_gear,
                                # 'fuel_type': getvehicle_fuel_type, 
                                # 'engine_capability': getvehicle_engine_capacity,
                                },
                                {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1, "mileage":1,"gear":1,"fuel_type":1,"engine_capability":1}
                                )
    # getdata2 = collection.find({'category': 'Cars','make': getvehicle_make, 'model': getvehicle_model,'year': getvehicle_year},
    #                             {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1})

    '''getdata_mod = mod_collection.find({'category': getvehicle_category, 'make': getvehicle_make, 'model': getvehicle_model,
                                    'year': getvehicle_year},
                                {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1})'''

    print(list(getdata))
    df = DataFrame(list(getdata))
    # print(df)


    if not df.empty:
        valuvation_amount = df['price'].astype(float).mean()   
        format_valuvation_amount = "{:,.2f}".format(valuvation_amount)
        #format_valuvation_amount = "{:,}".format(format_valuvation_amount)


        Maximum_amount = df['price'].astype(float).max()
        format_Maximum_amount = "{:,.2f}".format(Maximum_amount)


        Minimum_amount = df['price'].astype(float).min()
        format_Minimum_amount = "{:,.2f}".format(Minimum_amount)


        Mode_amount = df['price'].mode(dropna=False)[0]#.astype(float)
        #format_Mode_amount = "{:.2f}".format(Mode_amount)

    
        mydic1 = {  'format_valuvation_amount':format_valuvation_amount,
                    'format_Maximum_amount' : format_Maximum_amount,
                    'format_Minimum_amount':format_Minimum_amount,
                    'Mode_amount':Mode_amount}

    else:
        print("DF is empty")


    #dict = Merge(mydic1, mydic2)
    return mydic1


def getModRuleBaseDB(vehicle_category,vehicle_make,vehicle_model,vehicle_year):
    client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority",27017)

    DB = client.get_database('data_store')
    mod_collection = DB.get_collection('moderator_data')

    print("Connected")
    getvehicle_category = vehicle_category

    #getvehicle_make = vehicle_make.capitalize()
    getvehicle_make = vehicle_make
    getvehicle_model = vehicle_model
    # getvehicle_engine_capacity = vehicle_engine_capacity
    getvehicle_year = vehicle_year

    print(getvehicle_category)
    print(getvehicle_make)
    print(getvehicle_model)
    mydic2 = {}
    getdata = mod_collection.find({'category': getvehicle_category, 'make': getvehicle_make, 'model': getvehicle_model,
                               'year': getvehicle_year},
                              {"_id": 0, "category": 1, "make": 1, "model": 1, "price": 1, "year": 1})

    mod_df = DataFrame(list(getdata))
    print(mod_df)
    # print(list(getdata))
    print("mod data frame loaded")


    if not mod_df.empty:
        valuvation_amount = mod_df['price'].astype(float).mean()
        format_valuvation_amount= "{:,.2f}".format(valuvation_amount)

        print(type(format_valuvation_amount))
        #format_valuvation_amount = f"{format_amount:,}"

        Maximum_amount = mod_df['price'].astype(float).max()
        format_Maximum_amount = "{:,.2f}".format(Maximum_amount)

        Minimum_amount = mod_df['price'].astype(float).min()
        format_Minimum_amount = "{:,.2f}".format(Minimum_amount)

        Mode_amount = mod_df['price'].mode(dropna=False)[0]  # .astype(float)
        #format_Mode_amount = "{:.2f}".format(Mode_amount)

        mydic2 = {'format_mod_valuvation_amount': format_valuvation_amount,
                  'format_mod_Maximum_amount': format_Maximum_amount,
                  'format_mod_Minimum_amount': format_Minimum_amount,
                  'Mode_mod_amount': Mode_amount}

    else:
        print("MOD_DF is empty")

    return mydic2

if __name__ == '__main__':
    #im1 = getCategory('motor car')
    #im2 = getModel('DBA-HA36S alto')
    #im = getRuleBaseDB(im1,'Suzuki',im2,'2017')

    # im1 = getCategory('motor car')
    # im2 = getModel('Dayz')
    im = getRuleBaseDB('Cars','Toyota','Corolla','1998','226000','Automatic','1500 cc','Petrol',True)
    print(im)
    # im = getRuleBaseDB(im1, 'Nissan', im2, '2016')

    '''print(im.get('format_mod_valuvation_amount'))
    print(im.get('format_mod_Maximum_amount'))
    print(im.get('format_mod_Minimum_amount'))
    print(im.get('Mode_mod_amount'))
'''
    # print(im.get('format_valuvation_amount'))
    # print(im.get('format_Maximum_amount'))
    # print(im.get('format_Minimum_amount'))
    # print(im.get('Mode_amount'))

# {category:'Car',make:'Suzuki',model:'Alto',year:'2017'}
