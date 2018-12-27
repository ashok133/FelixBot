from flask import Flask, request, make_response
import urllib.request, json
from colorama import Fore, Back, Style

import mysqlconnector as mysql_
import firebaseconnector as fb
import mailer as m

immediateHelpGuide = {
    'help': 'Let\'s see. We identified a problem with the engine\'s peak pressure. From my learnings, it usually happens if the oil pump pressure relief valve is stuck. Can you check if that\'s not the case?',
    'complex': 'Okay, I think humans can help you better. Let me place a service call for you. Someone will call you back ASAP.',
    'solved': 'Great. I\'ll take a note of thta. Glad that\'s fixed.'
}

x15Service = {
    'engine_status': 'X15 engines are performing fine. I\'m seeing an increased number of service requests though. Most of them point towards faulty oil pressure values.',
    'engine_internal_impact': 'I\'ve received around 46 service requests in last 24 hours. Our field technicians have validated the problem and it seems to have impacted 40 percent of the shipped units.' ,
    'engine_financial_impact': 'We\'re looking at an operational loss and maintenance costs that total around 0.5 million dollars per hour. Since defect validation 5 days ago, we\'ve incurred around 60 million USD in losses.',
    'engine_recommendation': 'If the engine\'s continue to operate with the defect, their time to failure will be reduced by 47%. From previous actions taken, I have two recommendations moving forward.'
}

x15previousAction = {
    'rec1':'I see excessively high RPMs in defective engines. Broadcast a notice to warn the clients about threshold RPMs and send field technicians to replace oil pressure valves.',
    'rec2':'Call back defective engines on site and replace oil pressure valves. This will lead to a planned downtime of around 48 hours for each unit.'
}

x15ChosenAction = {
    1: 'Okay, I\'ll send a broadcast notification to the clients and inform the Field Technicians team',
    2: 'Okay, I\'ll send a callback notification to the clients and place a purchase requisition for replacement valves'
}

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Flask!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # return "Fetching data..."
    req = request.get_json(silent=True, force=True)
    print("Request received: ")
    req2 = json.dumps(req, indent = 4)

    if (req['queryResult']['intent']['displayName'] == 'CumminsClients'):
        res = fetchData()
        res = json.dumps(res, indent=4)
        # print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsPurchase'):
        orderNumber = int(req['queryResult']['parameters']['number'])
        res = fetchPurchaseData(orderNumber)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsNewToken'):
        possibleProblem = req['queryResult']['parameters']['problem']
        possibleReason = req['queryResult']['parameters']['possible_reason']
        res = logNewToken(possibleProblem, possibleReason)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsImmediateHelp'):
        if (req['queryResult']['parameters']['cummins_immediate_help'] == 'help'):
            res = immediateHelp('help')
        elif (req['queryResult']['parameters']['cummins_immediate_help'] == 'complex'):
            res = immediateHelp('complex')
        else:
            res = immediateHelp('solved')
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsRecommendations'):
        res = fetchRecommendations()
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsEngineOverview'):
        if (req['queryResult']['parameters']['cummins_engine_overview'] == 'engine'):
            model = req['queryResult']['parameters']['model_number']
            res = prepareFulfillmentResponse(x15Service['engine_status'])

        if (req['queryResult']['parameters']['cummins_engine_overview'] == 'impact'):
            res = prepareFulfillmentResponse(x15Service['engine_internal_impact'])

        if (req['queryResult']['parameters']['cummins_engine_overview'] == 'financial'):
            res = prepareFulfillmentResponse(x15Service['engine_financial_impact'])

        if (req['queryResult']['parameters']['cummins_engine_overview'] == 'recommendation'):
            res = prepareFulfillmentResponse(x15Service['engine_recommendation'])
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    if (req['queryResult']['intent']['displayName'] == 'CumminsRecommendationChoice'):
        print('Entered choice')
        ordinal = req['queryResult']['parameters']['ordinal']
        print (ordinal)
        res = prepareFulfillmentResponse(x15ChosenAction[ordinal])
        m.sendMail(ordinal)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def prepareFulfillmentResponse(response):
    return {
        "fulfillmentText": response
    }

def fetchRecommendations():
    return {
        "fulfillmentText": "Sure. First, "+x15previousAction['rec1']+ ". The second recommendation would be, " +x15previousAction['rec2']
    }

def fetchData():
    return {
        "fulfillmentText": "I can't disclose my clients"
        # "displayText": "hello user"
    }

def fetchPurchaseData(orderNumber):
    orderDetails = mysql_.fetchPurchaseDetails(orderNumber)
    productOrder = orderDetails[0]
    orderAmount = orderDetails[2]
    orderStatus = orderDetails[1]
    return {
        "fulfillmentText": "Okay, checking. Found your order. Your order "+str(orderNumber)+" for "+productOrder+ " is "+orderStatus+". The order should reach you in 2 days."
    }

def logNewToken(problem, possible_reason):
    # orderDetails = mysql_.fetchPurchaseDetails(orderNumber)
    lastLog = fb.fetchVitalStats()
    print(type(lastLog))
    print ("FAULT LOG for engine ID"+str(lastLog['engineID'])+":\n \tfuelAirRatio: "+str(lastLog['fuelAirRatio'])+"\n\toilStatus: "+lastLog['oilStatus']+"\n\t"+Fore.RED+"peakPressure: "+str(lastLog['peakPressure'])+Style.RESET_ALL+"\n\tthermalEfficiency: "+str(lastLog['thermalEfficiency'])+"\n\tvolumetricEfficiency: "+str(lastLog['volumetricEfficiency']))
    lastLog.update({'problem':problem})
    serviceLog = lastLog.update({'possibleReasonDescribed':possible_reason})
    fb.push(lastLog, 'serviceLog')
    return {
        "fulfillmentText": "Okay, I'm going through your engine's vital stats. I think we have a problem with the engine's peak pressure. I've submitted a service token and someone should reach you ASAP."
    }

def fetchEngineOverview():
    pass

def immediateHelp(query):
    return {
        "fulfillmentText": immediateHelpGuide[query]
    }

if __name__ == "__main__":
    app.run()
