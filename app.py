from zeep import Client
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result=None
    data=None
    naming_string=[]
    coordonnees = {"lat": 45.86298, "lng": 5.95301}
    if request.method == 'POST':
        num1 = int(request.form['vitesse'])
        num2 = int(request.form['distance'])
        num3 = int(request.form['tempcharg'])
        client = Client('http://127.0.0.1:8000/?wsdl')
        result=client.service.calcultrajetcharg(num1, num2, num3)
        print(result)
        
        # Fetch the JSON data
    with open('response.json') as json_file:
        data = json.load(json_file)
        
    # Gather the "naming" attribute for each entry
    naming_list = []
    for entry in data['data']['vehicleList']:
        make = entry['naming']['make']
        model = entry['naming']['model']
        version = entry['naming']['version']
        naming = f"{make}, {model}, {version}"
        naming_list.append(naming)
    
    # Convert the gathered "naming" attributes to a string
    naming_string = json.dumps(naming_list)
        
    return render_template('index.html', result=result, data=data, coordonnees=coordonnees, naming_string=naming_string)
    
  
if __name__ == '__main__':
    app.run(debug=True)

