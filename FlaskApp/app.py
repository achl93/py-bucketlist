from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = MY_DB_PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
	return render_template('signup.html')

@app.route("/signUp", methods=['POST', 'GET'])
def signUp():
	try:
		# read posted values from UI
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		# validate the recieved values
		if _name and _email and _password:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_createUser', (_name, _email, _password))
			data = cursor.fetchall

			if (data):
				conn.commit()
				cursor.close()
				conn.close()
				return json.dumps({'Message': 'User created'})
			else:
				cursor.close()
				conn.close()
				return json.dumps({'Error': str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'Error':str(e)})

if __name__ == "__main__":
	app.run()
