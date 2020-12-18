from ftplib import FTP
import zipfile
import os
from bs4 import BeautifulSoup
import pandas as pd

regions = ['Adygeja_Resp', 'Altaj_Resp']

ftps = {
        '44 фз': ['ftp.zakupki.gov.ru', 'free'],
        '223 фз': ['ftp.zakupki.gov.ru/out', 'fz223free']
        }

folders = ['plangraphs2020', 'protocols', 'contracts']

def parse_plangraphs(filename):
    with open(filename, 'r', encoding='utf8') as f:
        soup=BeautifulSoup(f.read())
        try: # переписать try-except!
            plandata = {
                'plannumber': soup.find('ns5:plannumber').text,
                'planyear': soup.find('ns5:planyear').text,
                'firstyear': soup.find('ns5:firstyear').text,
                'secondyear': soup.find('ns5:secondyear').text,
                'publishdate': soup.find('ns5:publishdate').text,
                'customerinn': soup.find('ns5:inn').text,
                'OKPD': soup.find('ns4:okpdcode').text,
                'OKPD name': soup.find('ns4:okpdname').text,
                'object': soup.find('ns5:purchaseobjectinfo').text, 
                # может быть не одна позиция, может вообще не быть
                'total': soup.find('ns5:total').text,
                   }
            customerdata = {
                'customerregnum': soup.find('ns5:regnum').text,
                'customerfullname': soup.find('ns5:fullname').text,
                'customerinn': soup.find('ns5:inn').text,
                'customerkpp': soup.find('ns5:kpp').text,
                'customeraddress': soup.find('ns5:factaddress').text,
                'customeremail': soup.find('ns5:email').text,      
                   }
            all_data.append(plandata)
            customers.append(customerdata)
        except:
            os.remove(filename)
            continue
    
def parse_contracts(filename):
    
    
def parse_protocols(filename):
    

ftp = FTP(ftps['44 фз'][0])
ftp.login(ftps['44 фз'][1], ftps['44 фз'][1])

ftp.cwd('fcs_regions')
ftp.cwd(regions[0])

for folder in folders:
    ftp.cwd(folder)

    ftp.cwd('currMonth') # выгрузки данных за текущий месяц
    filenames = ftp.nlst()

    for i in range(len(filenames)):
        with open(r'C:\Users\Vladimir\Documents\GitHub\hakaton_test\plan\plan{}.zip'.format(i), 'wb') as f:
            ftp.retrbinary('RETR ' + filenames[i], f.write)
          
        ftp.quit()

    path = 'C:\\Users\\Vladimir\\Documents\\GitHub\\hakaton_test\\plan'
    os.chdir(path)

    for filename in os.listdir(os.getcwd()):
        with zipfile.ZipFile(filename) as f:
            for cont in f.namelist():
                f.extract(cont, path)
                os.remove(filename)


    for filename in os.listdir(path):
        if not filename.endswith('.xml'): 
            os.remove(filename)
            continue
        parse_plangraphs(filename)
        
             #пустые значения в отдельных графах?

df = pd.DataFrame(all_data)
df.to_excel('plans2.xlsx') # не забыть убрать

# ежедневные обновления - сохранять последнюю дату?
# plangraphs, contracts, protocols
# прописать удаление файлов по ходу
# проверять пустые папки
# у нас два ФЗ!
        