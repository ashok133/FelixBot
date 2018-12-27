import urllib.request, json


def fetchPurchaseDetails(orderNumber):
    with urllib.request.urlopen("http://104.196.221.75/api/client_purchase_data.php") as url:
        data = json.loads(url.read().decode())
        for i in range(0,len(data)):
            # print(data[0]['purchaseID'])
            if (int(data[i]['purchaseID']) is orderNumber):
                return [data[i]['productOrdered'], data[i]['status'], data[i]['totalAmount']]

def submitNewToken(problem, possibleReason):
    with urllib.request.urlopen("http://104.196.221.75/api/client_purchase_data.php") as url:
        data = json.loads(url.read().decode())
        for i in range(0,len(data)):
            # print(data[0]['purchaseID'])
            if (int(data[i]['purchaseID']) is orderNumber):
                return [data[i]['productOrdered'], data[i]['status'], data[i]['totalAmount']]

def setConnection(hostIP, username, passwd, mysqlDB):
    mariadb_connection = mariadb.connect(host=hostIP,user=username, password=passwd, database=mysqlDB)
    return mariadb_connection.cursor()
    # connection = pymysql.connect(host=hostIP,user=username, password = passwd, db = mysqlDB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    # return connection
