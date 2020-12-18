from ftplib import FTP
import zipfile
import os
from bs4 import BeautifulSoup
import pandas as pd

all_data = []

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
#print(ftp.retrlines('LIST'), '\n')

ftp.cwd('fcs_regions')
ftp.cwd('Adygeja_Resp')
#print(ftp.retrlines('LIST'), '\n')

ftp.cwd('plangraphs2020')
ftp.cwd('currMonth')
filenames = ftp.nlst()
#print(filenames)

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


for filename in os.listdir(path):
    if not filename.endswith('.xml'): 
        continue
    with open(filename, 'r', encoding='utf8') as f:
        soup=BeautifulSoup(f.read())
        try:
            plandata = {
    'plannumber': soup.find('ns5:plannumber').text,
    'planyear': soup.find('ns5:planyear').text,
    'firstyear': soup.find('ns5:firstyear').text,
    'secondyear': soup.find('ns5:secondyear').text,
    'publishdate': soup.find('ns5:publishdate').text,
    'customerregnum': soup.find('ns5:regnum').text,
    'customerfullname': soup.find('ns5:fullname').text,
    'customerinn': soup.find('ns5:inn').text,
    'customerkpp': soup.find('ns5:kpp').text,
    'customeraddress': soup.find('ns5:factaddress').text,
    'customeremail': soup.find('ns5:email').text,
    'OKPD': soup.find('ns4:okpdcode').text,
    'OKPD name': soup.find('ns4:okpdname').text,
    'object': soup.find('ns5:purchaseobjectinfo').text,
    'total': soup.find('ns5:total').text,
               }
            all_data.append(plandata)
        except:
            continue #пустые значения в отдельных графах?

df = pd.DataFrame(all_data)
df.to_excel('plans2.xlsx') # не забыть убрать

# ежедневные обновления - сохранять последнюю дату?
# plangraphs, contracts, protocols
# прописать удаление файлов по ходу
# проверять пустые папки
# у нас два ФЗ!
        