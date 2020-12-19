from ftplib import FTP
import os
import zipfile

class FtpRequest():
    def __init__(self):
        pass
        
    def download(self, path, region, folder='notifications', period='currMonth'):
        ftp = FTP('ftp.zakupki.gov.ru')
        ftp.login('free', 'free')
        ftp.cwd('fcs_regions')
        ftp.cwd(region)
        ftp.cwd(folder)
        ftp.cwd(period)
        filenames = ftp.nlst()

        for i in range(len(filenames)):
            with open(path + f'\plan{i}.zip', 'wb') as f:
                ftp.retrbinary('RETR ' + filenames[i], f.write)
        
        ftp.quit()
        
        os.chdir(path)
        
        for filename in os.listdir(os.getcwd()):
            try:
                with zipfile.ZipFile(filename) as f:
                    for cont in f.namelist():
                        f.extract(cont, path)
            except:
                continue
