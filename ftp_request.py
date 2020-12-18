from ftplib import FTP

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
print(ftp.retrlines('LIST'), '\n')

ftp.cwd('fcs_regions')
#print(ftp.retrlines('LIST'), '\n')

ftp.cwd('Altaj_Resp')
print(ftp.retrlines('LIST'), '\n')

ftp.cwd('notifications')
filenames = ftp.nlst()
print(filenames[1])

with open(r'zakupka.zip', 'wb') as f:
    ftp.retrbinary('RETR ' + filenames[1], f.write)
    
ftp.quit()
