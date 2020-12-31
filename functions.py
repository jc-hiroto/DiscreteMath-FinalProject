import pandas as pd
import datetime

buys = pd.DataFrame()
lastid = -1
lastClickData = pd.DataFrame()
PARTITION = 128
PATH = "parts\\clicks_p"

sChunk = 10000  # default chunk size of searching.


def initDataB():
    global buys
    # Read and sort buy session data
    buys = pd.read_csv("yoochoose-data\yoochoose-buys.dat",parse_dates = [1], date_parser = dateparse)
    buys = buys.sort_values(by='session')


def dateparse(dt_str):
    return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def getSessionData(sid):
    global PARTITION
    sres = pd.DataFrame()
    filep = PATH + str(sid % PARTITION) + ".csv"
    s = pd.read_csv(filep, parse_dates=[1], date_parser=dateparse)
    sres = s.loc[s['session'] == sid]
    if sres.empty:
        print("Session not found!")
    return sres


def parseSession(session,time,item_id):
    print("======== Session "+str(session)+" ========")
    print("# Product:",item_id)
    print("# Purchase time:",time)
    global lastid, lastClickData
    counter = 0
    clickTime = []
    tgap = datetime.datetime.now()
    if session != lastid:
        lastid = session
        temp = getSessionData(session)
        lastClickData=temp.loc[temp['item_id'] == item_id]
    for index, srow in lastClickData.iterrows():
        if srow['timestamp'] < time:
            counter+=1
        clickTime.append(srow['timestamp'])
    print("Clicks before buy: "+str(counter)+"  |  First click: "+str(clickTime[0])+"  |  Last click: "+str(clickTime[-1]))
    print("First click until buy: "+str((time - clickTime[0]).total_seconds())+
          " sec.  |  Last click until buy: "+str((time - clickTime[-1]).total_seconds())+" sec.",end="\n\n")


# iterate through all buy sessions.
def getPurchaseDataA(length=-1):
    loop = 0
    for index,row in buys.iterrows():
        if loop >= length and length != -1:
            break;
        parseSession(row['session'],row['timestamp'],row['item_id'])
        loop += 1
        

# get data by item_id
def getPurchaseDataI(itemSID,length=-1):
    loop = 0
    df = buys.loc[buys['item_id'] == itemSID]
    if df.empty:
        print("Find by Item ID: No Result!")
    else:
        for index,row in df.iterrows():
            if loop >= length and length != -1:
                break;
            parseSession(row['session'],row['timestamp'],row['item_id'])
            loop += 1


# get data by session ID
def getPurchaseDataS(sessionSID,length=-1):
    loop = 0
    df = buys.loc[buys['session'] == sessionSID]
    if df.empty:
        print("Find by Session: No Result!")
    else:
        for index,row in df.iterrows():
            if loop >= length and length != -1:
                break;
            parseSession(row['session'],row['timestamp'],row['item_id'])
            loop += 1
          

def extractSession(sessionSID,sess,isTest=False):
    df1=sess[['item_id']].groupby('item_id')
    res = []
    if not isTest:
        sessBuys = buys.loc[buys['session'] == sessionSID]
        doBuy = not sessBuys.empty
        for id, group in df1:
            clicks = group.count()[0]
            if doBuy:
                if sessBuys.loc[sessBuys['item_id'] == id].empty:
                    buyI=0
                else:
                    buyI=1
            else:
                buyI = 0
            print("[Train Data] Parsing Session: "+str(sessionSID),end='\r')
            dict = {'session':sessionSID,'item_id':id,'clicks':clicks,'buy':buyI}
            res.append(dict)
    else:
        for id, group in df1:
            clicks = group.count()[0]
            print("[Test Data] Parsing Session: "+str(sessionSID),end='\r')
            dict = {'session':sessionSID,'item_id':id,'clicks':clicks}
            res.append(dict)
    return res


def extractTrainData(sessionSID,sess,isTest=False):
    gbyI=sess[['item_id']].groupby('item_id')
    catS = sess['category'].loc[sess['category'] == "S"]
    sales = catS.count()
    sess = sess.sort_values(by='timestamp')
    #print(sess)
    dur = sess['timestamp'].iloc[-1]-sess['timestamp'].iloc[0]
    numGroups = gbyI.ngroups
    clicks=sess.count()[0]
    res = []
    #print("Sales:",sales)
    #print("Duration:",dur.ptotal_seconds(),"sec.")
    #print("clicks:",clicks)
    #print("different items:",numGroups)
    if not isTest:
        print("[TRAIN DATA] session: "+str(sessionSID),end='\r')
        sessBuys = buys.loc[buys['session'] == sessionSID]
        doBuy = 0 if (sessBuys.empty) else 1
        saleSum=0
        #print("Puchased?:",doBuy)
        dict = {'session':sessionSID,'sales':sales,'duration':dur.total_seconds(),'clicks':clicks,'items':numGroups,'buy':doBuy}
        res.append(dict)
    return res