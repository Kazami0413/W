from flask import Flask, render_template, request
import json

app = Flask(__name__)
email = None
password = None
JSON_FILE = "userdata.json"

data ={
    "email": email,
    "password": password
}

@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        with open(JSON_FILE, 'r') as json_file:
            existing_data = json.load(json_file)
            for item in existing_data:
                if item['email'] == email:
                    if item['password'] == password:
                            resp = render_template("index.html")
                            resp.set_cookie('login', email)
                            return resp
    except FileNotFoundError:
        return False
    return False

@app.route("/singin")
def singin():
    data ={
        "email": email,
        "password": password
    }
    try:
        with open(JSON_FILE, 'r') as using_json_file:
            existing_data = json.load(using_json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open(JSON_FILE, 'w') as using_json_file:
        json.dump(existing_data, using_json_file, indent=2)

@app.route('/singup', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(name, email, password)
        data ={
        "email": email,
        "password": password,
        "user": name
        }
        try:
            with open(JSON_FILE, 'r') as using_json_file:
                existing_data = json.load(using_json_file)
        except FileNotFoundError:
            existing_data = []

        existing_data.append(data)

        with open(JSON_FILE, 'w') as using_json_file:
            json.dump(existing_data, using_json_file, indent=2)
        return render_template('index.html')
    else:
        return render_template('singup.html')

if __name__ == '__main__':
    app.run(debug=True)