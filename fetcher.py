from flask import Flask
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/fetchData")
def fetchData():
    # return "Fetching data..."
    with urllib.request.urlopen("http://ec2-13-233-94-247.ap-south-1.compute.amazonaws.com/api/client.php") as url:
        data = json.loads(url.read().decode())
        print(data)
    return ""

if __name__ == "__main__":
    app.run()
