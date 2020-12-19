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
def tmp_mass2(soap, file):
    f1, f2, f3 = None, None, None
    try:
        f1 = str(soap.find("procedureinfo").findChildren("startdate")[0].text).split(sep='T', maxsplit=1) #start
    except:
        pass

    print(f"{file}   {f1}")
    try:
        f2 = soap.find("procedureinfo").findChildren("place")[0].text
    except:
        pass
    try:
        f3 = str(soap.find("procedureinfo").findChildren("enddate")[0].text).split(sep='T', maxsplit=1)
    except:
        pass
    return [f1,f2,f3]
def notif_parse(path_to_file_name):

    with open(path_to_file_name, 'r') as f:
        soap = None
        try:
            soap = BeautifulSoup(f.read())
        except:
            print("here")
            return

        try:
            tender_name = soap.find('ns2:export').findChildren("purchaseobjectinfo")[0].text
        except:
            tender_name = None


        try:
            tender_url = soap.find('ns2:export').findChildren("href")[0].text
        except:
            tender_url = None
        try:
            pub_data = soap.find('ns2:export').findChildren("docpublishdate".lower())[0].text
        except:
            try:
                pub_data = soap.find('ns8:commoninfo').findChildren("ns8:docpublishdtineis")[0].text
            except:#createDate
                try:
                    pub_data = soap.find('ns8:commoninfo').findChildren("ns8:publishdtineis")[0].text
                except:
                    try:
                        pub_data = soap.find('ns2:fcsplacementresult').findChildren("createdate")[0].text
                    except:
                        pub_data = None

        constact_info = tmp_mass(soap)
        auction_info = tmp_mass2(soap, path_to_file_name)
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
            "startdata": auction_info[0],
            "enddata": auction_info[2],
            "placingway": placinWay,
            "customerinn": inn,
            "maxprice": max_price,
            "okpdcode":category_id,
            "okpdname":category,
            "purchasobject": purObj,
            "href": tender_url,
        }
        return ans




def del_trash_not(path):
    for _, _, files in os.walk(path):
        for i in files:
            file_name, file_ext = os.path.splitext(i)
            if(re.match("\w*Clarification\w*", file_name) or file_ext != '.xml'):
                print(i)
                os.remove(f'{path}/{i}')

def del_trash_contr(path):
    for _, _, files in os.walk(path):
        for i in files:
            file_name, file_ext = os.path.splitext(i)
            if(re.match("\w*Procedure\w*", file_name) or file_ext != '.xml'):
                print(i)
                os.remove(f'{path}/{i}')
def create_ans_note():
    a = open("ans.txt", "w", encoding='utf-8')
    for _, _, files in os.walk('plan'):
        for i in files:
            file_name, file_ext = os.path.splitext(i)
            path = 'plan/' + str(i)
            if (re.match("\w*Result\w*", file_name) or re.match("\w*Cancel\w*", file_name) or re.match("\w*epProlong\w*", file_name)):
                continue
            a.write(str(notif_parse(path)) + '\n' )

def contract_parser(file_path):
    with open(file_path, 'r') as f:
        soap = None

        soap = BeautifulSoup(f.read())

        try:
            contract_sub = soap.find('contractsubject').text
        except:
            contract_sub = soap.find('product').findChildren('name')[0].text

        publish_date = soap.find('publishdate').text
        customer_name = soap.find('customer').findChildren('fullname')[0].text
        customer_inn = soap.find('customer').findChildren('inn')[0].text
        sign_date = soap.find('signdate').text
        price = soap.find('priceinfo').findChildren('price')[0].text
        url = soap.find('href').text
        try:
            conruct_num = soap.find('number').text
        except:
            conruct_num = 'без номера'
        try:
            is_ip = soap.find('supplier').findChildren('isip')[0].text
            sup_fname = soap.find('suppliers').findChildren('firstname')[0].text
            sup_lname = soap.find('suppliers').findChildren('lastname')[0].text
            sup_mname = soap.find('suppliers').findChildren('middlename')[0].text
            sup_inn = soap.find('suppliers').findChildren('inn')[0].text
            ans = {
                'contract_sub': contract_sub,
                'publish_date': publish_date,
                'customer_name': customer_name,
                'customer_inn': customer_inn,
                'sign_date': sign_date,
                'price': price,
                'sup_ip': is_ip,
                'sup_fname': sup_fname,
                'sup_lname': sup_lname,
                'sup_mname': sup_mname,
                'sup_inn': sup_inn,
                'conruct_num': conruct_num,
                'url': url
            }
            return ans
        except:
            sup_name =  soap.find('supplier').findChildren('fullname')[0].text
            sup_okpo = soap.find('supplier').findChildren('okpo')[0].text
            sup_inn = soap.find('supplier').findChildren('inn')[0].text
            sup_kpp = soap.find('supplier').findChildren('kpp')[0].text
            ans = {
                'contract_sub':contract_sub,
                'publish_date':publish_date,
                'customer_name':customer_name,
                'customer_inn':customer_inn,
                'sign_date':sign_date,
                'price':price,
                'sup_ip':False,
                'sup_name':sup_name,
                'sup_okpo':sup_okpo,
                'sup_inn':sup_inn,
                'sup_kpp':sup_kpp,
                'conruct_num':conruct_num,
                'url': url
            }
            return ans



def create_data_frame_contract():
    a = open("contract_frame.txt", "w", encoding='utf-8')
    for _,_, files in os.walk('contracts'):
        for i in files:
            if(i == '.DS_Store' or i == '.' or i == '..'):
                continue
            path = 'contracts/' + str(i)
            try:
                a.write(str(contract_parser(path)) + '\n')
            except:
                print(i)



if __name__ == '__main__':
    create_data_frame_contract()
