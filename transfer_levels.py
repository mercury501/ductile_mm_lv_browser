from ftplib import FTP
import os


here = os.path.dirname(os.path.abspath(__file__))

host = '192.168.1.103'
port = 5000

ftp = FTP()
ftp.connect(host,port)

i = 1

''' No need to delete, STOR overwrites files
try:
    ftp.rmd('/switch/smm2 courses')
except:
    print('no smm2 directory')

ftp.mkd('/switch/smm2 courses')
'''

try:
    while 1:    
        lfilend = './save/course_data_' + str(f'{(i):03}') + '.bcd'
        rfilend = '/switch/smm2 courses/course_data_' + str(f'{(i):03}') + '.bcd'
        lfilent = './save/course_thumb_' + str(f'{(i):03}') + '.btl'
        rfilent = '/switch/smm2 courses/course_thumb_' + str(f'{(i):03}') + '.btl'

        #upload data and thumb files
        with open(lfilend, 'rb') as f:  
            ftp.storbinary('STOR %s' % rfilend, f) 
        
        with open(lfilent, 'rb') as f:  
            ftp.storbinary('STOR %s' % rfilent, f)  
        
        # print uploaded course and remove local file
        print('Uploaded course n: ' + str(i))
        
        #increment index
        i = i + 1

        os.remove(lfilend)
        os.remove(lfilent)
        
except:
    print('done uploading!')


ftp.quit()