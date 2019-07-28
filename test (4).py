# -*- coding: utf-8 -*-

from flask import Flask, request, Response, abort, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
import numpy as np
from from_spread import Get_spread,ZerotenNews

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

users = {
    1: User(1, "zeroten", "Pzeroten010"),
    2: User(2, "admin", "admin010"),
}



nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def home():
    return Response("home: <a href='/test/login'>Login</a> <a href='/test/protected'>Protected</a> <a href='/test/logout'>Logout</a>")

@app.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):

        if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):

            login_user(users.get(user_check[request.form["username"]]["id"]))
            Z=ZerotenNews()
            time1=Z.news[-3,0]
            news1=Z.news[-3,1]
            time2=Z.news[-2,0]
            news2=Z.news[-2,1]
            time3=Z.news[-1,0]
            news3=Z.news[-1,1]
            return render_template('zeroten_home.html',time1=time1,news1=news1,
time2=time2,news2=news2,time3=time3,news3=news3)
 
        else:
            return abort(401)
    else:
        return render_template("login.html")


@app.route('/protected',methods=['GET'])
@login_required
def protected():
    return render_template('member.html')

@app.route("/output", methods=['POST'])
def output():
   user_name = request.form['name']#���O
   user_id = request.form['ID']#ID
   num_id = int(user_id)
   G=Get_spread()
   if(user_name==str(G.name_list[num_id])):
        number_sales =G.result_july[num_id,34]
        sum_sales=G.result_july[num_id,25]
        user_reward=G.result_july[num_id,38]
        unsold_count=G.result_july[num_id,35]
        unsold_amount=G.result_july[num_id,27]
        transfer_amount=G.result_july[num_id,36]
        user_rank = G.result_july[num_id,23]
        return render_template('output.html', name=user_name,ID=user_id,UoRa=user_rank,NoS=number_sales,
                               SoS=sum_sales,UoR=user_reward,UoC=unsold_count,
                               UoA=unsold_amount,ToA=transfer_amount,)
   else:
        return render_template('miss.html')


 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
