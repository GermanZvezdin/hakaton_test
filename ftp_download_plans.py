from ftplib import FTP
import zipfile
import os
from bs4 import BeautifulSoup
import pandas as pd
import shutil

regions = {'Adygeja_Resp': 'Адыгея'}

ftps = {
        '44': ['ftp.zakupki.gov.ru', 'free'],
        }

folders = ['plangraphs2020', 'protocols', 'contracts']

def parse_plangraphs(filename, fz, region):
    with open(filename, 'r', encoding='utf8') as f:
        soup=BeautifulSoup(f.read())
        positions = soup.find_all('ns5:position')
        planrows, custrows = [], []
        for position in soup.find_all('ns5:position')[1:]:
            planrows.append({
                'fz': fz,
                'plannumber': soup.find('ns5:plannumber').text,
                'planyear': soup.find('ns5:planyear').text,
                'firstyear': soup.find('ns5:firstyear').text,
                'secondyear': soup.find('ns5:secondyear').text,
                'publishdate': soup.find('ns5:publishdate').text,
                'customerinn': soup.find('ns5:inn').text,
                'positionnumber': position.find('ns5:positionnumber').text,
                'OKPD': position.find('ns4:okpdcode').text,
                'OKPD name': position.find('ns4:okpdname').text,
                'object': position.find('ns5:purchaseobjectinfo').text, 
                'total': position.find('ns5:total').text
                })
        for position in soup.find_all('ns5:specialPurchasePosition'):
            planrows.append({
                'fz': fz,
                'plannumber': soup.find('ns5:plannumber').text,
                'planyear': soup.find('ns5:planyear').text,
                'firstyear': soup.find('ns5:firstyear').text,
                'secondyear': soup.find('ns5:secondyear').text,
                'publishdate': soup.find('ns5:publishdate').text,
                'customerinn': soup.find('ns5:inn').text,
                'positionnumber': position.find('ns5:positionnumber').text,
                'OKPD': position.find('ns4:okpdcode').text,
                'OKPD name': position.find('ns4:okpdname').text,
                'object': position.find('ns5:purchaseobjectinfo').text, 
                'total': position.find('ns5:total').text
                })
        custrows.append({
                'region': regions[region],
                'customerregnum': soup.find('ns5:regnum').text,
                'customerfullname': soup.find('ns5:fullname').text,
                'customerinn': soup.find('ns5:inn').text,
                'customerkpp': soup.find('ns5:kpp').text,
                'customeraddress': soup.find('ns5:factaddress').text,
                'customeremail': soup.find('ns5:email').text
                   })
        return pd.DataFrame(planrows), pd.DataFrame(custrows)
    
  
fz = list(ftps.keys())[0]
region = list(regions.keys())[0] # это должно как-то перебираться

ftp = FTP(ftps[fz][0])
ftp.login(ftps[fz][1], ftps[fz][1])

ftp.cwd('fcs_regions')
ftp.cwd(region)
ftp.cwd('plangraphs2020')
ftp.cwd('currMonth') # выгрузки данных за текущий месяц
filenames = ftp.nlst()

for i in range(len(filenames)):
    with open(f'C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plan\\plan{i}.zip', 'wb') as f:
        ftp.retrbinary('RETR ' + filenames[i], f.write)
          
ftp.quit()

path = 'C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plan'
os.chdir(path)

customers = pd.DataFrame(
    columns=[
        'region', 'customerregnum', 'customerfullname', 'customerinn',
        'customerkpp', 'customeraddress', 'customeremail'])
plans = pd.DataFrame(
    columns=[
        'fz', 'plannumber', 'planyear', 'firstyear', 'secondyear', 'publishdate', 
        'customerinn', 'positionnumber', 'OKPD', 'OKPD name', 'object', 'total'])

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
    df1, df2 = parse_plangraphs(filename, fz, region)
    plans = pd.concat([plans, df1]).drop_duplicates().reset_index(drop=True)
    customers = pd.concat([customers, df2]).drop_duplicates().reset_index(drop=True)
        
plans.to_excel('C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plans.xlsx')
customers.to_excel('C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\customers.xlsx') 
shutil.rmtree(path) 

# ежедневные обновления - сохранять последнюю дату?
# plangraphs, contracts, protocols
# проверять пустые папки
# у нас два ФЗ!
        