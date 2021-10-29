from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,url_for
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


def on_message(client, userdata, msg):
   print(msg.payload.decode("utf-8"))




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

client.username_pw_set("admin", "password")

client.connect("broker", 8883)
client.loop_start()

client.subscribe("mydevice")


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

@app.route("/" )
def index():

   return render_template("index.html")

@app.route("/register.html")
def register():

   return render_template("register.html")


@app.route("/main" , methods = ["POST","GET"])
def second():


   return render_template("main.html")


@app.route("/start" , methods = ["POST","GET"])
def start():

   client.publish("mydevice", "start")

   return render_template("main.html")


@app.route("/stop" , methods = ["POST","GET"])
def stop():
   client.publish("mydevice", "stop")

   return render_template("main.html",user = user)


@app.route("/submit" , methods = ["POST"])
def submit():

   name = request.form.get("username")
   passw = request.form.get("password")

   try:
      admin = User.query.filter_by(username=name).first()

      if name == admin.username and passw == admin.password :

         global user
         user = admin.username

         user = user
         return render_template("main.html",user = user)
      else:
         return redirect(url_for("index"))

   except:
      return redirect(url_for("index"))


@app.route("/save" , methods = ["POST","GET"])
def save():

   username = request.form.get("regname")
   password = request.form.get("regpassword")

   admin = User(username=username, password=password)
   db.session.add(admin)
   db.session.commit()

   return redirect(url_for("index"))


class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=False, nullable=False)
   password = db.Column(db.String(120), unique=False, nullable=False)

   def __repr__(self):
      return '<User %r>' % self.username


if __name__ == "__main__" :
   app.run(debug=True)
