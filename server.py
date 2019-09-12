from flask import Flask, render_template, redirect, request, Markup
import bleach

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'KHECTFh4ck3rMan'

@app.route("/")
def index():
	return "not authorized"

@app.route("/challenge-1")
def c1():
	if("curl" in  request.headers.get('User-Agent')):
		return "KHE{curlH3ad3rsAr3C00l}"
	else:
		return "Not Authorized"

@app.route("/challenge-2", methods=['GET', 'POST'])
def c2():
	if request.method == 'POST':
		user = request.form['user']
		if (user.lower() ==  "admin" or user.lower() ==  "administrator"):
			return "KHE{m4k3sur32DataV4lidat3}"
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
			return "KHE{XSSC4nB3D4ng3r0us}"
		
		return render_template("challenge3.html", comment=comment_html)
	return render_template("challenge3.html")

@app.route("/challenge-4")
def c4():
	return render_template("challenge4.html")
	
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=80)