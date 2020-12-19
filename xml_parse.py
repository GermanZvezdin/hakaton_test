import os
import sys
import re
from bs4 import BeautifulSoup
#import pandas as pd
#Clarification,
def tmp_mass(soap):
    f1, f2, f3, f4,f5, f6 = None, None, None, None, None, None
    try:
        f1 = soap.find('responsibleinfo').findChildren("lastname")[0].text
    except:
        pass
    try:
        f2 = soap.find('responsibleinfo').findChildren("firstname")[0].text
    except:
        pass
    try:
        f3 = soap.find('responsibleinfo').findChildren("middlename")[0].text
    except:
        pass
    try:
        f4 = soap.find('responsibleinfo').findChildren("contactemail")[0].text
    except:
        pass
    try:
        f5 = soap.find('responsibleinfo').findChildren("contactphone")[0].text
    except:
        pass
    try:
        f6 = soap.find('responsibleinfo').findChildren("contactfax")[0].text
    except:
        pass
    return [f1,f2,f3,f4,f5,f6]
def tmp_mass2(soap):
    f1, f2, f3 = None, None, None
    try:
        f1 = str(soap.find("procedureinfo").findChildren("startdate")[0].text).split(sep='T', maxsplit=1) #start
    except:
        pass
    try:
        f2 = soap.find("procedureinfo").findChildren("place")[0].text
    except:
        pass
    try:
        f3 = str(soap.find("procedureinfo").findChildren("enddate")[0].text).split(sep='T', maxsplit=1)
    except:
        pass
    return [f1,f2,f3]
def create_table(path_to_file_name):

    with open(path_to_file_name, 'r', encoding='utf-8') as f:
        soap = BeautifulSoup(f.read())

        try:
            tender_name = soap.find('ns2:export').findChildren("purchaseobjectinfo")[0].text
        except:
            tender_name = None


        try:
            tender_url = soap.find('ns2:export').findChildren("href")[0].text
        except:
            tender_url = None
        try:
            pub_data = soap.find('ns2:export').findChildren("docPublishDate".lower())[0].text
        except:
            pub_data = None

        constact_info = tmp_mass(soap)
        auction_info = tmp_mass2(soap)
        try:
            max_price = str(soap.find("lot").findChildren("maxprice")[0].text)
        except:
            max_price = None
        try:
            category_id = soap.find("okpd2info").findChildren("ns4:okpdcode")[0].text
        except:
            category_id = None

        try:
            category = soap.find("okpd2info").findChildren("ns4:okpdname")[0].text
        except:
            category = None

        try:
            global_category_id = soap.find("kvrinfo").findChildren("ns4:code")[0].text
        except:
            global_category_id = None
        try:
            global_category = soap.find("kvrinfo").findChildren("ns4:name")[0].text
        except:
            global_category = None
        try:
            customer_info =  global_category = soap.find("customerrequirements").findChildren("fullname")[0].text
        except:
            customer_info = None
        try:
            purNumber = soap.find("purchasenumber").text
        except:
            purNumber = None
        try:
            placinWay = soap.find("placingway").findChildren('name')[0].text
        except:
            placinWay = None
        try:
            inn = soap.find("purchaseresponsible").findChildren('inn')[0].text
        except:
            inn = None
        try:
            purObj = soap.find("customerrequirement").findChildren('purchaseobjectdescription')[0].text
        except:
            purObj = None
        ans = {
            "fz": "44",
            "purchasenumber": purNumber,
            "publishdate": pub_data,
            "startdata": auction_info[0][0],
            "enddata": auction_info[2][0],
            "placingway": placinWay,
            "customerinn": inn,
            "maxprice": max_price,
            "okpdcode":category_id,
            "okpdname":category,
            "purchasobject": purObj,
            "href": tender_url,
        }
        return ans

def del_trash(path):
    for _, _, files in os.walk(path):
        for i in files:
            file_name, file_ext = os.path.splitext(i)
            if(re.match("\w*Clarification\w*", file_name) or file_ext != '.xml'):
                print(i)
                os.remove(f'{path}/{i}')



if __name__ == '__main__':
    #del_trash('/Users/germanzvezdin/Desktop/hack/XML_parse/venv/plan')
    create_table("/Users/germanzvezdin/Desktop/hack/XML_parse/venv/plan/fcsNotificationEA44_0176200005520001726_25267246.xml")