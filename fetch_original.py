# from time import time
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import pandas as pd
# import json
# import csv
# import itertools
# import sys
# from datetime import datetime
# from datetime import timedelta
# import nothing as t

# cred = credentials.Certificate("./serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db=firestore.client()
# batch=db.batch()

# docs = db.collection(u'API-LOGS').stream()




# dd = db.collection("API-LOGS")

# #Subtracting current time with one minute to get the latest miniute records.
# now = datetime.now()
# one_minute = timedelta(minutes=1)
# add_value = timedelta(hours=5,minutes=30)
# now = now - add_value
# print(one_minute)
# check = now - one_minute
# print(now)

# st = '2022-10-19 06:53:17.894000+00:00'
# l = st.split('+')
# di = dict()
# dt = datetime.strptime(l[0],"%Y-%m-%d %H:%M:%S.%f")
# #query to fetch all the data with timestamp greater than check.
# query = dd.where(
#     u'timestamp', u'>', check).order_by(u'timestamp')

# results = query.get()

# #printing it
# for d in results:
#     #d.reference.delete()
#     print(d)
#     di[d.id] = d.to_dict()
#     di[d.id]['timestamp'] =str(di[d.id]['timestamp'])
    
# print(di)

# d = dict()
# """
# for doc in docs:
#     #if doc.timestamp == 'com.corebankingservice.service.AccountService@6850b758':
    
#     d[doc.id]=doc.to_dict()
#     d[doc.id]['timestamp'] =str(d[doc.id]['timestamp'])
#     #print(d[doc.id]['timestamp'])

# print(d)
# """
# #out_file = open("./myfile.json", "w")
# """
# fields = [ 'id','resEP', 'respData', 'statCode', 'timestamp','clientIP','reqType' ]

# with open("streaming.csv", "w",newline='') as f:
#     w = csv.DictWriter( f, fields )
#     #w.writerow(fields)
#     for key,val in sorted(d.items()):
#         row = {'id': key}
#         row.update(val)
#         w.writerow(row)
# """


# #-------------------------
# j1 = json.dumps(di)
# #print(j1)
# out_file = open("./myfile.json", "w")
  
# json.dump(di, out_file, indent = 6)
  
# out_file.close()

# pdObj = pd.read_json('./myfile.json', orient='index')
# pdObj.to_csv('./streaming.csv', index=False)

# #print(check)
# try:
#     t.everything()
# except:
#     print("No Requests")













import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np
import json
import csv
import itertools
import sys
from datetime import datetime
from datetime import timedelta
import compressor_original as t
from csv import writer
#import change_point as cp
import multiprocessing

def dos_detect(index):
    
    time.sleep(1200)
    df = pd.read_csv('D:/BankLogMicroservices-main/Transaction-service/values_original.csv')
    df = df.dropna(axis = 0)
    z = df.iloc[index:(index+20)].dropna(axis = 0)
    #print(z)
    t =(z['total_calls']*z['data_out_rate'])/z['inter_api_access']
    temp = np.array(t)
    import ruptures as rpt
    import matplotlib.pyplot as plt
    model="rbf"
    algo = rpt.Pelt(model=model).fit(temp)
    result = algo.predict(pen=7)
    #print("result=",result)
    if(len(result)>1):
        print("-------------------------------------------------------------------------------------------------------------")
        print("ALERT : DOS ATTACK DETECTED")
        print("-------------------------------------------------------------------------------------------------------------")
        exit
    else:
        pass

if __name__ == '__main__':
    count = 0
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db=firestore.client()
    batch=db.batch()
    print("-------------------------------------------------------------------------------------------------------------")
    print("M O N I T O R I N G")
    print("-------------------------------------------------------------------------------------------------------------")
    while 1:
        start = time.time()
        docs = db.collection(u'API-LOGS').stream()




        dd = db.collection("API-LOGS")

        #Subtracting current time with one minute to get the latest miniute records.
        now = datetime.now()
        one_minute = timedelta(minutes=1)
        add_value = timedelta(hours=5,minutes=30)
        now = now - add_value
        #print(one_minute)
        check = now - one_minute
        #print(now)

        st = '2022-10-19 06:53:17.894000+00:00'
        l = st.split('+')
        di = dict()
        dt = datetime.strptime(l[0],"%Y-%m-%d %H:%M:%S.%f")
        #query to fetch all the data with timestamp greater than check.
        query = dd.where(
            u'timestamp', u'>', check).order_by(u'timestamp')

        results = query.get()

        #printing it
        for d in results:
            #d.reference.delete()
            #print(d)
            di[d.id] = d.to_dict()
            di[d.id]['timestamp'] =str(di[d.id]['timestamp'])
            
        #print(di)

        d = dict()
        """
        for doc in docs:
            #if doc.timestamp == 'com.corebankingservice.service.AccountService@6850b758':
            
            d[doc.id]=doc.to_dict()
            d[doc.id]['timestamp'] =str(d[doc.id]['timestamp'])
            #print(d[doc.id]['timestamp'])

        print(d)
        """
        #out_file = open("./myfile.json", "w")
        """
        fields = [ 'id','resEP', 'respData', 'statCode', 'timestamp','clientIP','reqType' ]

        with open("streaming.csv", "w",newline='') as f:
            w = csv.DictWriter( f, fields )
            #w.writerow(fields)
            for key,val in sorted(d.items()):
                row = {'id': key}
                row.update(val)
                w.writerow(row)
        """


        #-------------------------
        j1 = json.dumps(di)
        #print(j1)
        out_file = open("./myfile.json", "w")
        
        json.dump(di, out_file, indent = 6)
        
        out_file.close()

        pdObj = pd.read_json('./myfile.json', orient='index')
        pdObj.to_csv('./streaming.csv', index=False)

        #print(check)
        try:
            temp = t.everything()
            if temp > 1000 and count == 0:
                count += 1
                df = pd.read_csv('D:/BankLogMicroservices-main/Transaction-service/values_original.csv')
                for i in range(df.shape[0]):
                    if df.iat[i,2] == temp:
                        note = i
                p1 = multiprocessing.Process(target=dos_detect,args=[note])
                p1.start()
                # detection = dos_detect(note)
                        
        except:
            print("No more Requests")
            List = [0,0,0,0,0,0]
            with open('values_original.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()

        end = time.time()
        temp_num = end - start
        print("waiting")
        print("-------------------------------------------------------------------------------------------------------------")
        time.sleep(60-temp_num)
    