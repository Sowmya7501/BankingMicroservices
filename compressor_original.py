"""
from ipaddress import ip_address
from itertools import count
import pandas as pd
from datetime import datetime
import statistics

df = pd.read_csv('D:\BankLogMicroservices-main\Transaction-service\streaming.csv')       #Used to read the streaming.csv file


def diff(x,y):                                                         #function defined to find the difference between two timestamps from the csv file 
    x=x.split('+')[0]
    y=y.split('+')[0]
    if "." in x:                                                                      
        d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    else:
        d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    
    if "." in y:
        d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f")
    else:
        d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S")
    t = d2 - d1
    #x = t.split(",")  2022-09-27 18:57:48.972  2022-09-30 11:59:41.586
    # t.strftime('%d days, %H:%M:%S.%f')
    t = str(t)
    if "day" in t:
        t = t.replace(" ", "" )
        x = t.split(",")
        m = x[0].split("d")
        days = int(m[0])*24*60*60
        z = x[1].split(":")
        k = 0
        diff1 = 0
        for i in range(2,-1,-1):
            diff1 = diff1 + (float(z[i]))*(60**k)
            k = k+1
        return (diff1+days)
    else:                                                           
        z = t.split(":")
        k = 0
        diff1 = 0
    
        for i in range(2,-1,-1):
            diff1 = diff1 + (float(z[i]))*(60**k)
            k = k+1
        return diff1

#print(df)
df = df.drop(labels = 'reqType', axis=1)

df.sort_values(["timestamp"],axis=0,ascending=[True],inplace=True)              #this does sorting of the csv file based on the timestamp

df = df[["resEP","statCode","respData","timestamp","clientIP"]]

t = df.shape[0]                                                                  #used to find number of rows in the csv file

print(df)
p = []
for i in range(t):
    if df.iat[i,4] not in p:
        p.append(df.iat[i,4])

#print(p)

# for i in df.groupby(['clientIP']):
#     print(i[1])
    



count = []                                                                  #this list is used to store the two consecutive timestamp difference 
for i in range(t-1):
    count.append(diff(df.iat[i,3],df.iat[i+1,3]))


z = []
i = 0
count1 = 0
if len(count) ==0:
    max_api_call = []     
    total_calls = []     
    api_access_unique = []       
    inter_api_access = []
    num_failed = []
    data_out_rate = []
    ip_addr = []
    ip_addr.append(df.iat[0,4])
    total_calls.append(1)
    max_api_call.append(1)
    api_access_unique.append(1)
    inter_api_access.append(0)
    data_out_rate.append(df.iat[0,2])
    if df.iat[0,1] == 404:
        num_failed.append(1)
    else:
        num_failed.append(0)


if len(count)!=0:
    while i != len(count)-1:
        count1 = count1 + count[i]
        if count1 > 60:
            z.append((i))
            count1 = 0
            i = i+1
        else:
            i +=1
    z.append((i+1))
    #print(count)
    b = []                                                       #the list b contains the starting and ending index of the requests within one minute in the csv file
    for i in range(len(z)):
        if i == 0:
            b.append((0,z[i]))
        else:
            b.append((z[i-1]+1,z[i]))

    max_api_call = []     
    total_calls = []     
    api_access_unique = []       
    inter_api_access = []
    num_failed = []
    data_out_rate = []
    ip_addr = []
    for i in b:
    
        new_df = df.iloc[i[0]:(i[1]+1)]                   #this new_df contains the requests within 1 minute
        # print(new_df)
        # print("------------------------------------------------------------------------------")
        for jag in new_df.groupby(['clientIP']):
            ip_df = jag[1]
            # print(ip_df)
            # print("------------------------------------------------------------------------------")
            abc = ip_df.shape[0]
            ip_addr.append(ip_df.iat[0,4])
            total_calls.append(abc)                               #this contains the sequence_length parameter values
            d = {}
            ank = {}                                               #this contains statusCode
            ath = 0
            for j in range(abc):
                if ip_df.iat[j,1] not in ank:
                    ank[ip_df.iat[j,1]] = 0
                if ip_df.iat[j,0] not in d:
                    d[ip_df.iat[j,0]] = 0
                ank[ip_df.iat[j,1]] += 1
                d[ip_df.iat[j,0]] +=1
                ath += ip_df.iat[j,2] 
            max_api_call.append(d[max(d, key = d.get)])                        #this contains the max_api_call parameter values
            api_access_unique.append(len(d)/abc)             #this contains the api_access_unique parameter values d[max(d, key = d.get)]
            data_out_rate.append(ath)
            if 404 in ank:
                num_failed.append(ank[404])
                #matin = ank[404]
            else:
                num_failed.append(0)
                #matin = 0
            list1 = []                                  #list1 is contain to get the consecutive time difference between the requests
            c = []                                                                  #this list is used to store the two consecutive timestamp difference 
            for i in range(abc-1):
                c.append(diff(ip_df.iat[i,3],ip_df.iat[i+1,3]))                      
            list1.append(c)
            for i in list1:
                if i == []:
                    inter_api_access.append(0)
                else:
                    i.sort()
                    res = statistics.median(i)                  #used to get median
                    inter_api_access.append(res)                #this contains the inter_api_access parameter values

            #for_temp = []
            #for_temp.append([inter_api_access[0],len(d)/abc,abc,d[max(d, key = d.get)],data_out_rate[0],matin])

            #key = {}
            # if key[ip_df.iat[0,4]] not in key:
            #     key[ip_df.iat[0,4]] = []
            #key[ip_df.iat[0,4]] = for_temp


            #for_temp = []

        #print(key)



# print(inter_api_access)
# print(api_access_unique)
# print(max_api_call)
# print(data_out_rate)
# print(total_calls)
# print(ip_addr)

me = {"inter_api_access": inter_api_access ,"api_access_unique" : api_access_unique , "total_calls" : total_calls , "max_api_call" : max_api_call ,"data_out_rate" : data_out_rate, "num_failed" : num_failed, "ip_addr" : ip_addr}
one = pd.DataFrame(me)
print(one)
#one.to_csv("D:\irfan_new.csv",index = False)         

# dict = {}
# for i in range(len(inter_api_access)):
    
#         dict[ip_addr[i]] = [inter_api_access[i],api_access_unique[i],total_calls[i],max_api_call[i],data_out_rate[i],num_failed[i]]


# for i in dict:
#     print(str(i) + ":")
#     for j in dict[i]:
#         print(" "+str(j))
    

"""





























































































# def everything():
#     from ipaddress import ip_address
#     from itertools import count
#     import pandas as pd
#     from datetime import datetime
#     import statistics
#     import numpy as np
#     import sklearn
#     import pickle
#     import time
#     from sklearn.ensemble import RandomForestClassifier
#     from sklearn.tree import DecisionTreeClassifier
#     from sklearn.neighbors import KNeighborsClassifier
#     from sklearn.svm import SVC
#     df = pd.read_csv('D:\BankLogMicroservices-main\Transaction-service\streaming.csv')       #Used to read the streaming.csv file


#     def diff(x,y):                                                         #function defined to find the difference between two timestamps from the csv file 
#         x=x.split('+')[0]
#         y=y.split('+')[0]
#         if "." in x:                                                                      
#             d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
#         else:
#             d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        
#         if "." in y:
#             d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f")
#         else:
#             d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S")
#         t = d2 - d1
#         #x = t.split(",")  2022-09-27 18:57:48.972  2022-09-30 11:59:41.586
#         # t.strftime('%d days, %H:%M:%S.%f')
#         t = str(t)
#         if "day" in t:
#             t = t.replace(" ", "" )
#             x = t.split(",")
#             m = x[0].split("d")
#             days = int(m[0])*24*60*60
#             z = x[1].split(":")
#             k = 0
#             diff1 = 0
#             for i in range(2,-1,-1):
#                 diff1 = diff1 + (float(z[i]))*(60**k)
#                 k = k+1
#             return (diff1+days)
#         else:                                                           
#             z = t.split(":")
#             k = 0
#             diff1 = 0
        
#             for i in range(2,-1,-1):
#                 diff1 = diff1 + (float(z[i]))*(60**k)
#                 k = k+1
#             return diff1

#     #print(df)
#     df = df.drop(labels = 'reqType', axis=1)

#     df.sort_values(["timestamp"],axis=0,ascending=[True],inplace=True)              #this does sorting of the csv file based on the timestamp

#     df = df[["resEP","statCode","respData","timestamp","clientIP"]]

#     t = df.shape[0]                                                                  #used to find number of rows in the csv file

#     #print(df)
#     p = []
#     for i in range(t):
#         if df.iat[i,4] not in p:
#             p.append(df.iat[i,4])

#     #print(p)

#     # for i in df.groupby(['clientIP']):
#     #     print(i[1])
        



#     count = []                                                                  #this list is used to store the two consecutive timestamp difference 
#     for i in range(t-1):
#         count.append(diff(df.iat[i,3],df.iat[i+1,3]))


#     z = []
#     i = 0
#     count1 = 0
#     if len(count) ==0:
#         max_api_call = []     
#         total_calls = []     
#         api_access_unique = []       
#         inter_api_access = []
#         num_failed = []
#         data_out_rate = []
#         ip_addr = []
#         ip_addr.append(df.iat[0,4])
#         total_calls.append(1)
#         max_api_call.append(1)
#         api_access_unique.append(1)
#         inter_api_access.append(0)
#         data_out_rate.append(df.iat[0,2])
#         if df.iat[0,1] == 404:
#             num_failed.append(1)
#         else:
#             num_failed.append(0)


#     if len(count)!=0:
#         while i != len(count)-1:
#             count1 = count1 + count[i]
#             if count1 > 60:
#                 z.append((i))
#                 count1 = 0
#                 i = i+1
#             else:
#                 i +=1
#         z.append((i+1))
#         #print(count)
#         b = []                                                       #the list b contains the starting and ending index of the requests within one minute in the csv file
#         for i in range(len(z)):
#             if i == 0:
#                 b.append((0,z[i]))
#             else:
#                 b.append((z[i-1]+1,z[i]))

#         max_api_call = []     
#         total_calls = []     
#         api_access_unique = []       
#         inter_api_access = []
#         num_failed = []
#         data_out_rate = []
#         ip_addr = []
#         for i in b:
        
#             new_df = df.iloc[i[0]:(i[1]+1)]                   #this new_df contains the requests within 1 minute
#             # print(new_df)
#             # print("------------------------------------------------------------------------------")
#             for jag in new_df.groupby(['clientIP']):
#                 ip_df = jag[1]
#                 # print(ip_df)
#                 # print("------------------------------------------------------------------------------")
#                 abc = ip_df.shape[0]
#                 ip_addr.append(ip_df.iat[0,4])
#                 total_calls.append(abc)                               #this contains the sequence_length parameter values
#                 d = {}
#                 ank = {}                                               #this contains statusCode
#                 ath = 0
#                 for j in range(abc):
#                     if ip_df.iat[j,1] not in ank:
#                         ank[ip_df.iat[j,1]] = 0
#                     if ip_df.iat[j,0] not in d:
#                         d[ip_df.iat[j,0]] = 0
#                     ank[ip_df.iat[j,1]] += 1
#                     d[ip_df.iat[j,0]] +=1
#                     ath += ip_df.iat[j,2] 
#                 max_api_call.append(d[max(d, key = d.get)])                        #this contains the max_api_call parameter values
#                 api_access_unique.append(len(d)/abc)             #this contains the api_access_unique parameter values d[max(d, key = d.get)]
#                 data_out_rate.append(ath)
#                 if 404 in ank:
#                     num_failed.append(ank[404])
#                     #matin = ank[404]
#                 else:
#                     num_failed.append(0)
#                     #matin = 0
#                 list1 = []                                  #list1 is contain to get the consecutive time difference between the requests
#                 c = []                                                                  #this list is used to store the two consecutive timestamp difference 
#                 for i in range(abc-1):
#                     c.append(diff(ip_df.iat[i,3],ip_df.iat[i+1,3]))                      
#                 list1.append(c)
#                 for i in list1:
#                     if i == []:
#                         inter_api_access.append(0)
#                     else:
#                         i.sort()
#                         res = statistics.median(i)                  #used to get median
#                         inter_api_access.append(res)                #this contains the inter_api_access parameter values

#                 #for_temp = []
#                 #for_temp.append([inter_api_access[0],len(d)/abc,abc,d[max(d, key = d.get)],data_out_rate[0],matin])

#                 #key = {}
#                 # if key[ip_df.iat[0,4]] not in key:
#                 #     key[ip_df.iat[0,4]] = []
#                 #key[ip_df.iat[0,4]] = for_temp


#                 #for_temp = []

#             #print(key)



#     # print(inter_api_access)
#     # print(api_access_unique)
#     # print(max_api_call)
#     # print(data_out_rate)
#     # print(total_calls)
#     # print(ip_addr)

#     me = {"inter_api_access": inter_api_access ,"api_access_unique" : api_access_unique , "total_calls" : total_calls , "max_api_call" : max_api_call ,"data_out_rate" : data_out_rate, "num_failed" : num_failed, "ip_addr" : ip_addr}
#     one = pd.DataFrame(me)
#     print(one)
#     #one.to_csv("D:\irfan_new.csv",index = False)         

#     dict = {}
#     for i in range(len(inter_api_access)):
        
#             dict[ip_addr[i]] = [inter_api_access[i],api_access_unique[i],total_calls[i],max_api_call[i],data_out_rate[i],num_failed[i]]


#     # for i in dict:
#     #     print(str(i) + ":")
#     #     for j in dict[i]:
#     #         print(" "+str(j))

#     for i in dict:
#         ### Testing one line data
#         temp1 = dict[i][0]
#         temp2 = dict[i][1]
#         temp3 = dict[i][2]
#         my_array = np.array([[temp1,temp2,temp3]])
#         X_test = pd.DataFrame(my_array, columns = ['inter_api_access_duration(sec)','api_access_uniqueness','sequence_length(count)'])
#         ### -------------------------


#         # ### Decision Tree Model
#         # print("Decision Tree--->")
#         # dtModel = pickle.load(open('D:/capstone/final/decisionTree.pkl','rb'))

#         # st=time.time()

#         # prediction=dtModel[0].predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### ------------------------


#         # ### KNeighbours Model
#         # print("KNeighbours Model--->")
#         # knModel = pickle.load(open('D:/capstone/final/KNeigh.pkl','rb'))

#         # st=time.time()

#         # prediction=knModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### ---------------------------------



#         # ### Random Forest Model
#         # print("RandomForest Model--->")
#         # rfModel = pickle.load(open('D:/capstone/final/randomForest.pkl','rb'))

#         # st=time.time()

#         # prediction=rfModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### --------------------------


#         # ### Naive Bayes Model
#         # print("Naive Bayes Model--->")
#         # nbModel = pickle.load(open('D:/capstone/final/NaiveBayes.pkl','rb'))

#         # st=time.time()

#         # prediction=nbModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### --------------------------



#         # ### Ensemble Models
#         # ### Voting
#         # print("Voting Model--->")
#         # votingModel = pickle.load(open('D:/capstone/final/Voting.pkl','rb'))

#         # st=time.time()

#         # prediction=votingModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### --------------------------



#         # ### Bagging Model
#         # print("Bagging Model--->")
#         # baggingModel = pickle.load(open('D:/capstone/final/Bagging.pkl','rb'))

#         # st=time.time()

#         # prediction=baggingModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### --------------------------




#         # ### Boosting Model
#         # print("Boosting Model--->")
#         # boostingModel = pickle.load(open('D:/capstone/final/Boosting.pkl','rb'))

#         # st=time.time()

#         # prediction=boostingModel.predict(X_test)

#         # et = time.time()

#         # print("prediction=",prediction)
#         # print("time taken=",et-st,"s")
#         # print("************************")
#         # ### --------------------------











































































"""
def everything():
    from csv import writer
    from ipaddress import ip_address
    from itertools import count
    import pandas as pd
    from datetime import datetime
    import statistics
    import numpy as np
    import sklearn
    import pickle
    import time
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    df = pd.read_csv('D:\BankLogMicroservices-main\Transaction-service\streaming.csv')       #Used to read the streaming.csv file


    def diff(x,y):                                                         #function defined to find the difference between two timestamps from the csv file 
        x=x.split('+')[0]
        y=y.split('+')[0]
        if "." in x:                                                                      
            d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        else:
            d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        
        if "." in y:
            d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f")
        else:
            d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S")
        t = d2 - d1
        #x = t.split(",")  2022-09-27 18:57:48.972  2022-09-30 11:59:41.586
        # t.strftime('%d days, %H:%M:%S.%f')
        t = str(t)
        if "day" in t:
            t = t.replace(" ", "" )
            x = t.split(",")
            m = x[0].split("d")
            days = int(m[0])*24*60*60
            z = x[1].split(":")
            k = 0
            diff1 = 0
            for i in range(2,-1,-1):
                diff1 = diff1 + (float(z[i]))*(60**k)
                k = k+1
            return (diff1+days)
        else:                                                           
            z = t.split(":")
            k = 0
            diff1 = 0
        
            for i in range(2,-1,-1):
                diff1 = diff1 + (float(z[i]))*(60**k)
                k = k+1
            return diff1

    #print(df)
    #df = df.drop(labels = 'reqType', axis=1)

    df.sort_values(["timestamp"],axis=0,ascending=[True],inplace=True)              #this does sorting of the csv file based on the timestamp

    df = df[["resEP","statCode","respData","timestamp","clientIP","reqType"]]

    t = df.shape[0]                                                                  #used to find number of rows in the csv file

    #print(df)
    p = []
    for i in range(t):
        if df.iat[i,4] not in p:
            p.append(df.iat[i,4])

    #print(p)

    # for i in df.groupby(['clientIP']):
    #     print(i[1])
        



    count = []                                                                  #this list is used to store the two consecutive timestamp difference 
    for i in range(t-1):
        count.append(diff(df.iat[i,3],df.iat[i+1,3]))


    z = []
    i = 0
    count1 = 0
    if len(count) ==0:
        max_api_call = []     
        total_calls = []     
        api_access_unique = []       
        inter_api_access = []
        num_failed = []
        data_out_rate = []
        end_point = []
        #ip_addr = []
        #ip_addr.append(df.iat[0,4])
        total_calls.append(1)
        max_api_call.append(1)
        api_access_unique.append(1)
        inter_api_access.append(0)
        end_point.append(df.iat[0,0])
        data_out_rate.append(df.iat[0,2])
        if df.iat[0,1] == 404:
            num_failed.append(1)
        else:
            num_failed.append(0)


    if len(count)!=0:
        while i != len(count)-1:
            count1 = count1 + count[i]
            if count1 > 60:
                z.append((i))
                count1 = 0
                i = i+1
            else:
                i +=1
        z.append((i+1))
        #print(count)
        b = []                                                       #the list b contains the starting and ending index of the requests within one minute in the csv file
        for i in range(len(z)):
            if i == 0:
                b.append((0,z[i]))
            else:
                b.append((z[i-1]+1,z[i]))

        max_api_call = []     
        total_calls = []     
        api_access_unique = []       
        inter_api_access = []
        num_failed = []
        data_out_rate = []
        end_point = []
        #ip_addr = []
        for i in b:
        
            new_df = df.iloc[i[0]:(i[1]+1)]                   #this new_df contains the requests within 1 minute
            print(new_df)
            print("------------------------------------------------------------------------------")
            
            ip_df = new_df
            # print(ip_df)
            # print("------------------------------------------------------------------------------")
            abc = ip_df.shape[0]
            #ip_addr.append(ip_df.iat[0,4])
            total_calls.append(abc)                               #this contains the sequence_length parameter values
            d = {}
            ank = {}                                               #this contains statusCode
            ath = 0
            for j in range(abc):
                if ip_df.iat[j,1] not in ank:
                    ank[ip_df.iat[j,1]] = 0
                if ip_df.iat[j,0] not in d:
                    d[ip_df.iat[j,0]] = 0
                ank[ip_df.iat[j,1]] += 1
                d[ip_df.iat[j,0]] +=1
                ath += ip_df.iat[j,2] 
            max_api_call.append(d[max(d, key = d.get)])                        #this contains the max_api_call parameter values
            Keymax = max(zip(d.values(), d.keys()))[1]
            end_point.append(Keymax)
            api_access_unique.append(len(d)/abc)             #this contains the api_access_unique parameter values d[max(d, key = d.get)]
            data_out_rate.append(ath)
            if 404 in ank:
                num_failed.append(ank[404])
                #matin = ank[404]
            else:
                num_failed.append(0)
                #matin = 0
            list1 = []                                  #list1 is contain to get the consecutive time difference between the requests
            c = []                                                                  #this list is used to store the two consecutive timestamp difference 
            for i in range(abc-1):
                c.append(diff(ip_df.iat[i,3],ip_df.iat[i+1,3]))                      
            list1.append(c)
            for i in list1:
                if i == []:
                    inter_api_access.append(0)
                else:
                    i.sort()
                    res = statistics.median(i)                  #used to get median
                    inter_api_access.append(res)                #this contains the inter_api_access parameter values

            #for_temp = []
            #for_temp.append([inter_api_access[0],len(d)/abc,abc,d[max(d, key = d.get)],data_out_rate[0],matin])

            #key = {}
            # if key[ip_df.iat[0,4]] not in key:
            #     key[ip_df.iat[0,4]] = []
            #key[ip_df.iat[0,4]] = for_temp


            #for_temp = []

        #print(key)



    # print(inter_api_access)
    # print(api_access_unique)
    # print(max_api_call)
    # print(data_out_rate)
    # print(total_calls)
    # print(ip_addr)

    me = {"inter_api_access": inter_api_access ,"api_access_unique" : api_access_unique , "total_calls" : total_calls , "max_api_call" : max_api_call ,"data_out_rate" : data_out_rate, "num_failed" : num_failed, "API_endpoint" : end_point}
    # one = pd.DataFrame(me)
    # print(one)
    
    # List = [inter_api_access[0],api_access_unique[0],total_calls[0], max_api_call[0],data_out_rate[0],num_failed[0]]
    # with open('irfan_new.csv', 'a') as f_object:
    #     writer_object = writer(f_object)
    #     writer_object.writerow(List)
    #     f_object.close()
        
    
    #one.to_csv("D:\irfan_new.csv",index = False)         

    # dict = {}
    # for i in range(len(inter_api_access)):
        
    #         dict[ip_addr[i]] = [inter_api_access[i],api_access_unique[i],total_calls[i],max_api_call[i],data_out_rate[i],num_failed[i]]


    # for i in dict:
    #     print(str(i) + ":")
    #     for j in dict[i]:
    #         print(" "+str(j))

    for i in range(len(inter_api_access)):
        my_array = np.array([[inter_api_access[i],api_access_unique[i],total_calls[i]]])
        X_test = pd.DataFrame(my_array, columns = ['inter_api_access_duration(sec)','api_access_uniqueness','sequence_length(count)'])
        ## -------------------------


        ### Decision Tree Model
        print("Decision Tree--->")
        dtModel = pickle.load(open('D:/capstone/final/decisionTree.pkl','rb'))

        st=time.time()

        prediction=dtModel[0].predict(X_test)

        et = time.time()

        print("prediction=",prediction)
        print("time taken=",et-st,"s")
        print("************************")
        ### ------------------------


        # ### KNeighbours Model
        # print("KNeighbours Model--->")
        # knModel = pickle.load(open('D:/capstone/final/KNeigh.pkl','rb'))

        # st=time.time()

        # prediction=knModel.predict(X_test)

        # et = time.time()

        # print("prediction=",prediction)
        # print("time taken=",et-st,"s")
        # print("************************")
        # ### ---------------------------------



        # ### Random Forest Model
        # print("RandomForest Model--->")
        # rfModel = pickle.load(open('D:/capstone/final/randomForest.pkl','rb'))

        # st=time.time()

        # prediction=rfModel.predict(X_test)

        # et = time.time()

        # print("prediction=",prediction)
        # print("time taken=",et-st,"s")
        # print("************************")
        # ### --------------------------


        # ### Naive Bayes Model
        # print("Naive Bayes Model--->")
        # nbModel = pickle.load(open('D:/capstone/final/NaiveBayes.pkl','rb'))

        # st=time.time()

        # prediction=nbModel.predict(X_test)

        # et = time.time()

        # print("prediction=",prediction)
        # print("time taken=",et-st,"s")
        # print("************************")
        # ### --------------------------



        # ### Ensemble Models
        # ### Voting
        # print("Voting Model--->")
        # votingModel = pickle.load(open('D:/capstone/final/Voting.pkl','rb'))

        # st=time.time()

        # prediction=votingModel.predict(X_test)

        # et = time.time()

        # print("prediction=",prediction)
        # print("time taken=",et-st,"s")
        # print("************************")
        # ### --------------------------



        ### Bagging Model
        print("Bagging Model--->")
        baggingModel = pickle.load(open('D:/capstone/final/Bagging.pkl','rb'))

        st=time.time()

        prediction=baggingModel.predict(X_test)

        et = time.time()

        print("prediction=",prediction)
        print("time taken=",et-st,"s")
        print("************************")
        ### --------------------------




        # ### Boosting Model
        # print("Boosting Model--->")
        # boostingModel = pickle.load(open('D:/capstone/final/Boosting.pkl','rb'))

        # st=time.time()

        # prediction=boostingModel.predict(X_test)

        # et = time.time()

        # print("prediction=",prediction)
        # print("time taken=",et-st,"s")
        # print("************************")
        # ### --------------------------

    
    for i in range(len(inter_api_access)):
        my_array = np.array([[inter_api_access[i],api_access_unique[i],total_calls[i]],max_api_call[i],data_out_rate[i],num_failed[i]])
        X_test = pd.DataFrame(my_array, columns = ['inter_api_access','api_access_unique','total_calls',"max_api_call","data_out_rate","num_failed"])
        ### -------------------------

        ### Random Forest Model
        print("RandomForest Model--->")
        rfModel = pickle.load(open('D:/capstone/final/randomForest_d2.pkl','rb'))

        st=time.time()

        prediction=rfModel.predict(X_test)

        et = time.time()

        print("prediction=",prediction)
        print("time taken=",et-st,"s")
        print("************************")
        ### --------------------------


"""









































































































































def everything():
    from csv import writer
    from ipaddress import ip_address
    from itertools import count
    import pandas as pd
    from datetime import datetime
    import statistics
    import numpy as np
    import sklearn
    import pickle
    import time
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    import pandas as pd
    import numpy as np
    import sklearn
    import category_encoders as ce
    from sklearn.model_selection import train_test_split
    import time
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import recall_score
    from sklearn.svm import SVC
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import accuracy_score
    # import warnings
    # warnings.filterwarnings("ignore")
    df = pd.read_csv('D:\BankLogMicroservices-main\Transaction-service\streaming.csv')       #Used to read the streaming.csv file


    def diff(x,y):                                                         #function defined to find the difference between two timestamps from the csv file 
        x=x.split('+')[0]
        y=y.split('+')[0]
        if "." in x:                                                                      
            d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        else:
            d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        
        if "." in y:
            d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f")
        else:
            d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S")
        t = d2 - d1
        #x = t.split(",")  2022-09-27 18:57:48.972  2022-09-30 11:59:41.586
        # t.strftime('%d days, %H:%M:%S.%f')
        t = str(t)
        if "day" in t:
            t = t.replace(" ", "" )
            x = t.split(",")
            m = x[0].split("d")
            days = int(m[0])*24*60*60
            z = x[1].split(":")
            k = 0
            diff1 = 0
            for i in range(2,-1,-1):
                diff1 = diff1 + (float(z[i]))*(60**k)
                k = k+1
            return (diff1+days)
        else:                                                           
            z = t.split(":")
            k = 0
            diff1 = 0
        
            for i in range(2,-1,-1):
                diff1 = diff1 + (float(z[i]))*(60**k)
                k = k+1
            return diff1

    #print(df)
    #df = df.drop(labels = 'reqType', axis=1)

    df.sort_values(["timestamp"],axis=0,ascending=[True],inplace=True)              #this does sorting of the csv file based on the timestamp

    df = df[["resEP","statCode","respData","timestamp","clientIP","reqType"]]

    t = df.shape[0]                                                                  #used to find number of rows in the csv file

    #print(df)
    p = []
    for i in range(t):
        if df.iat[i,4] not in p:
            p.append(df.iat[i,4])

    #print(p)

    # for i in df.groupby(['clientIP']):
    #     print(i[1])
        



    count = []                                                                  #this list is used to store the two consecutive timestamp difference 
    for i in range(t-1):
        count.append(diff(df.iat[i,3],df.iat[i+1,3]))


    z = []
    i = 0
    count1 = 0
    if len(count) ==0:
        max_api_call = []     
        total_calls = []     
        api_access_unique = []       
        inter_api_access = []
        num_failed = []
        data_out_rate = []
        end_point = []
        #ip_addr = []
        #ip_addr.append(df.iat[0,4])
        total_calls.append(1)
        max_api_call.append(1)
        api_access_unique.append(1)
        inter_api_access.append(0)
        end_point.append(df.iat[0,0])
        data_out_rate.append(df.iat[0,2])
        if df.iat[0,1] == 404:
            num_failed.append(1)
        else:
            num_failed.append(0)


    if len(count)!=0:
        while i != len(count)-1:
            count1 = count1 + count[i]
            if count1 > 60:
                z.append((i))
                count1 = 0
                i = i+1
            else:
                i +=1
        z.append((i+1))
        #print(count)
        b = []                                                       #the list b contains the starting and ending index of the requests within one minute in the csv file
        for i in range(len(z)):
            if i == 0:
                b.append((0,z[i]))
            else:
                b.append((z[i-1]+1,z[i]))

        max_api_call = []     
        total_calls = []     
        api_access_unique = []       
        inter_api_access = []
        num_failed = []
        data_out_rate = []
        end_point = []
        #ip_addr = []
        for i in b:
            
            new_df = df.iloc[i[0]:(i[1]+1)]                   #this new_df contains the requests within 1 minute
            # print(new_df)
            # print("------------------------------------------------------------------------------")
            
            ip_df = new_df
            # print(ip_df)
            # print("------------------------------------------------------------------------------")
            abc = ip_df.shape[0]
            #ip_addr.append(ip_df.iat[0,4])
            total_calls.append(abc)                               #this contains the sequence_length parameter values
            d = {}
            ank = {}                                               #this contains statusCode
            ath = 0
            for j in range(abc):
                if ip_df.iat[j,1] not in ank:
                    ank[ip_df.iat[j,1]] = 0
                if ip_df.iat[j,0] not in d:
                    d[ip_df.iat[j,0]] = 0
                ank[ip_df.iat[j,1]] += 1
                d[ip_df.iat[j,0]] +=1
                ath += ip_df.iat[j,2] 
            max_api_call.append(d[max(d, key = d.get)])                        #this contains the max_api_call parameter values
            Keymax = max(zip(d.values(), d.keys()))[1]
            end_point.append(Keymax)
            api_access_unique.append(len(d)/abc)             #this contains the api_access_unique parameter values d[max(d, key = d.get)]
            data_out_rate.append(ath)
            if 404 in ank:
                num_failed.append(ank[404])
                #matin = ank[404]
            else:
                num_failed.append(0)
                #matin = 0
            list1 = []                                  #list1 is contain to get the consecutive time difference between the requests
            c = []                                                                  #this list is used to store the two consecutive timestamp difference 
            for i in range(abc-1):
                c.append(diff(ip_df.iat[i,3],ip_df.iat[i+1,3]))                      
            list1.append(c)
            for i in list1:
                if i == []:
                    inter_api_access.append(0)
                else:
                    i.sort()
                    res = statistics.median(i)                  #used to get median
                    inter_api_access.append(res)                #this contains the inter_api_access parameter values

    # if len(inter_api_access) == 2:
    #     inter_api_access.pop()
    #     api_access_unique.pop()
    #     total_calls.pop()
    #     max_api_call.pop()
    #     data_out_rate.pop()
    #     num_failed.pop()
    #     end_point.pop()



    me = {"inter_api_access": inter_api_access,"api_access_unique" : api_access_unique , "total_calls" : total_calls, "max_api_call" : max_api_call ,"data_out_rate" : data_out_rate, "num_failed" : num_failed, "API_endpoint" : end_point}
    one = pd.DataFrame(me)
    print(one)

    List = [inter_api_access[0],api_access_unique[0],total_calls[0], max_api_call[0],data_out_rate[0],num_failed[0]]
    with open('values_original.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(List)
        f_object.close()

    #FOR THE REALTIME DATASET PREDICTION
    my_array = np.array([[inter_api_access[0],api_access_unique[0],total_calls[0]]])
    X_test = pd.DataFrame(my_array, columns = ['inter_api_access_duration(sec)','api_access_uniqueness','sequence_length(count)'])
    
    # ### Decision Tree Model
    # dtModel = pickle.load(open('D:/capstone/final/decisionTree_synt.pkl','rb'))
    # st=time.time()
    # prediction=dtModel[0].predict(X_test)
    # print(prediction)
    # ### KNeighbours Model
    # knModel = pickle.load(open('D:/capstone/final/KNeigh_synth.pkl','rb'))
    # st=time.time()
    # prediction=knModel.predict(X_test)
    # print(prediction)

    # ### Random Forest Model
    # rfModel = pickle.load(open('D:/capstone/final/randomForest_synth.pkl','rb'))
    # st=time.time()
    # prediction=rfModel.predict(X_test)
    # print(prediction)

    # ### Naive Bayes Model
    # nbModel = pickle.load(open('D:/capstone/final/NaiveBayes_synth.pkl','rb'))
    # st=time.time()
    # prediction=nbModel.predict(X_test)
    # print(prediction)



    # Ensemble Models
    # Voting
    
    
    Bagging_syn = pickle.load(open('D:/capstone/final/Bagging_synt_new.pkl','rb'))
    randomForest = pickle.load(open('D:/capstone/final/randomForest_real.pkl','rb'))
    st=time.time()
    PRED_DB1=randomForest.predict(X_test)
    #FOR THE SYNTHETIC DATASET PREDICTION
    if PRED_DB1 == np.array([2]):
        print("THE ENDPOINT "+end_point[0]+" IS UNDER ATTACK")   
    else:
        my_array = np.array([[inter_api_access[0],api_access_unique[0],total_calls[0],max_api_call[0],data_out_rate[0],num_failed[0]]])
        X_test = pd.DataFrame(my_array, columns = ['inter_api_access','api_access_unique','total_calls','max_api_call','data_out_rate','num_failed'])
        st=time.time()
        PRED_DB2=Bagging_syn.predict(X_test)
        # print(PRED_DB2)
        if PRED_DB2 == np.array([2]):
            print("THE ENDPOINT "+end_point[0]+" IS UNDER ATTACK")
        else:
            print("NORMAL TRAFFIC")

    return total_calls[0]









































































