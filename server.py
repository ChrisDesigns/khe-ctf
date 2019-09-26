from flask import Flask, render_template, redirect, request, Markup, url_for, session
import bleach
import re
import requests

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'KHECTFh4ck3rMan'

SITE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
SITE_SECRET = '6LdtcLoUAAAAAJxdsCYTazsJrQtCjXLYveOKMTM3'

challengesName = [
	"Who run the world? Curls!",
	"Let me in",
	"Imagitive attributes",
	"Outguessing",
]
def get_key(argument):
    key_answer = {
        "1": "KHE{curlH3ad3rsAr3C00l}",
        "2": "KHE{m4k3sur32DataV4lidat3}",
        "3": "KHE{XSSC4nB3D4ng3r0us}",
        "4": "KHE{St3g0IsC00l}",
    }
    return key_answer.get(argument, "Invalid Challenge")

@app.route("/reset")
def reset():
	session.clear()
	return redirect(url_for('index'))

@app.route("/")
def index():
	notDone = []
	if (session.keys() != None):
		for i in session.keys():
			notDone.append(i)
	return render_template("check.html", challenges=challengesName, done=notDone)


@app.route('/chal/')
@app.route('/chal/<ChalNum>',  methods=['GET', 'POST'])
def hello(ChalNum=None):
	if (ChalNum and request.method == 'POST'):
		proposedToken = request.form['answer-token']
		filteredToken = re.sub('[^0-9]','', ChalNum)
		
		token = request.form['g-recaptcha-response']
		PARAMS =  {'secret': SITE_SECRET, 'response': token}
		r = requests.get(url = SITE_VERIFY_URL, params = PARAMS)
		data = r.json() 
		if (data["success"]):
			if (proposedToken == get_key(ChalNum)):
				session[filteredToken]  = True
				return "You got challenge " +  filteredToken + " correct!"
			else:
				return "You got challenge " + filteredToken + " wrong!"
		else:
			return "Please stop..."
	else:
		return redirect(url_for('index'))
	
@app.route("/challenge-1")
def c1():
	if("curl" in  request.headers.get('User-Agent')):
		return get_key("1")
	else:
		return "Not Authorized"

@app.route("/challenge-2", methods=['GET', 'POST'])
def c2():
	if request.method == 'POST':
		user = request.form['user']
		if (user.lower() ==  "admin" or user.lower() ==  "administrator"):
			return get_key("2")
		else:
			return "Welcome boring user"
	else:
		return render_template("challenge2.html")


@app.route("/challenge-3", methods=['GET', 'POST'])
def c3():
	comment_html = ""
	if request.method == 'POST':
		user = request.form['user']
		comment = request.form['comment']
		attr = {
			'img': ['rel', 'src']
		}
		attr2 = {
			'img': ['rel', 'src', 'onerror']
		}
		tags_allowed =  ['img', 'b', 'i']
		if( bleach.clean(comment, tags=tags_allowed, attributes=attr, strip=True) == bleach.clean(comment, tags=tags_allowed, attributes=attr2, strip=True) ):
			comment_html = Markup('<p id="username">User:'+ bleach.clean(user) +'</p><p id="comment">Message:'+ bleach.clean(comment, tags=tags_allowed, attributes=attr, strip=True) +'</p>')
		else:
			return get_key("3")
		
		return render_template("challenge3.html", comment=comment_html)
	return render_template("challenge3.html")

@app.route("/challenge-4")
def c4():
	return render_template("challenge4.html")
	
if __name__ == '__main__':
	app.run()