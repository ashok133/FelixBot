from flask import Flask, request, make_response
import urllib.request, json

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
    # print(req['queryResult']['intent']['name'])
    if (req['queryResult']['intent']['displayName'] == 'CumminsClients'):
        res = fetchData()
        res = json.dumps(res, indent=4)
        # print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r
    # return ""

def fetchData():
    return {
        "fulfillmentText": "I can't disclose my clients"
        # "displayText": "hello user"
    }

if __name__ == "__main__":
    app.run()
