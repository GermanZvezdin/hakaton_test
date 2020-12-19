from ftplib import FTP
import zipfile
import os
from bs4 import BeautifulSoup
import pandas as pd
import shutil

#regions = {'Adygeja_Resp': 'Адыгея'}

ftps = {
        '44': ['ftp.zakupki.gov.ru', 'free'],
        }

#folders = ['plangraphs2020', 'protocols', 'contracts']

def parse_contracts(filename, fz, region):
    with open(filename, 'r', encoding='utf8') as f:
        soup=BeautifulSoup(f.read())
        controws, custrows, supprows = [], [], []
        customer = soup.find('customer')
        supplier = soup.find('supplier')
        try:
            controws.append({
                'fz': fz,
                'purchasecode': soup.find('purchasecode').text, 
                'plannumber': soup.find('tenderplaninfo').findChildren()[0].text, 
                'positionnumber': soup.find('tenderplaninfo').findChildren()[1].text, 
                'customerinn': customer.findChildren('inn').text,
                'signdate': soup.find('signdate').text, 
                'contractregnum': soup.find_all('regnum')[2].text, 
                'contractnumber': soup.find('number').text, 
                'price': soup.find('price').text, 
                'productname': soup.find('product').findChildren('name')[0].text,
                'supplierinn': supplier.findChildren('inn').text
                })
            custrows.append({
                'region': region,
                'customerregnum': customer.findChildren('regnum').text,
                'customerfullname': customer.findChildren('fullname').text,
                'customerinn': customer.findChildren('inn').text,
                'customerkpp': customer.findChildren('kpp').text,
                })
            supprows.append({
                'supplierfullname': supplier.findChildren('fullname').text, 
                'supplierinn': supplier.findChildren('inn').text, 
                'supplierkpp': supplier.findChildren('kpp').text, 
                'supplierokpo': supplier.findChildren('okpo').text, 
                'supplieraddress': supplier.findChildren('address').text,
                'supplieremail': supplier.findChildren('contactemail').text
            })
            return pd.DataFrame(controws), pd.DataFrame(custrows), pd.DataFrame(supprows)
        except:
            return pd.DataFrame(columns=columns_cont), pd.DataFrame(columns=columns_cust),\
                pd.DataFrame(columns=columns_supp)
    
  
fz = '44'
region = 'Adygeja_Resp'

ftp = FTP(ftps[fz][0])
ftp.login(ftps[fz][1], ftps[fz][1])

ftp.cwd('fcs_regions')
ftp.cwd(region)
ftp.cwd('contracts')
ftp.cwd('currMonth') # выгрузки данных за текущий месяц
filenames = ftp.nlst()

for i in range(len(filenames)):
    with open(f'C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plan\\plan{i}.zip', 'wb') as f:
        ftp.retrbinary('RETR ' + filenames[i], f.write)
          
ftp.quit()

path = 'C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plan'
os.chdir(path)

columns_cust=['customerregnum', 'customerfullname', 'customerinn', 'customerkpp']
columns_cont=[
        'purchasecode', 'plannumber', 'positionnumber', 'customerinn',
        'signdate', 'contractregnum', 'contractnumber', 'price', 'productname',
        'supplierinn'
        ]
columns_supp=[
        'supplierfullname', 'supplierinn', 'supplierkpp', 'supplierokpo' 
        'supplieraddress', 'supplieremail'
        ]

contracts = pd.DataFrame(columns=columns_cont)
customers = pd.DataFrame(columns=columns_cust)
suppliers = pd.DataFrame(columns=columns_supp)
    

for filename in os.listdir(os.getcwd()):
    try:
        with zipfile.ZipFile(filename) as f:
            for cont in f.namelist():
                f.extract(cont, path)
    except:
        continue

for filename in os.listdir(path):
    if not filename.endswith('.xml'): 
        continue
    df1, df2, df3 = parse_contracts(filename, fz, region)
    contracts = pd.concat([contracts, df1]).drop_duplicates().reset_index(drop=True)
    customers = pd.concat([customers, df2]).drop_duplicates().reset_index(drop=True)
    suppliers = pd.concat([suppliers, df3]).drop_duplicates().reset_index(drop=True)
        
contracts.to_excel('C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\contracts.xlsx')
customers.to_excel('C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\customers_cont.xlsx') 
suppliers.to_excel('C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\suppliers.xlsx')
shutil.rmtree(path) 