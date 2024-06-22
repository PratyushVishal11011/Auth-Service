from functools import wraps
import jwt
from flask import Flask, request, jsonify
from UserInfoDB import UserInfoDB
from Auth import Auth
from AuthDatabaseObject import AuthDatabaseObject
from jwt_token_generator import jwt_generator

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'auth_db'
app.config['SECRET_KEY'] = 'secret_key'


def protected_call(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        auth_db.log(request.remote_addr, "protected access")
        if not token:
            return jsonify({"message": "token is missing"}), 403
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS512")
        except:
            return jsonify({"message": "token is invalid"}), 403,
        return f(*args, **kwargs)

    return decorated


ado = AuthDatabaseObject(app)
auth_db = Auth(ado)
token_generator = jwt_generator(app)
user_db = UserInfoDB()


@app.route("/route", methods=["GET", "POST"])
@protected_call
def protected():
    token = request.args.get("token")
    return jsonify(jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS512"))


@app.route('/register/', methods=['POST', "GET"])
def register():
    auth_db.log(request.remote_addr, "register")
    data = request.get_json()
    username = data['username']
    password = data['password']
    if auth_db.check_if_exists(username):
        auth_db.signup(username, password)
        ret_val = token_generator.generate_token(username)
        ret_val["message"] = 'User registered successfully!'
        auth_db.add_log(username, request.remote_addr, ret_val["token"])
        return jsonify(ret_val), 201
    else:
        return jsonify({"message": "User already exists"}), 401


@app.route('/login/', methods=['POST'])
def login():
    ip = request.remote_addr
    auth_db.log(ip, "login")
    data = request.get_json()
    username = data['username']
    password = data['password']
    token = auth_db.check_log_in_status(username)
    if token:
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS512")
            return jsonify({"token": token})
        except jwt.exceptions.ExpiredSignatureError:
            user = auth_db.login(username, password)
            if user:
                token = token_generator.generate_token(username)
                auth_db.add_log(username, ip, token["token"])
                return jsonify(token), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
    else:
        user = auth_db.login(username, password)
        if user:
            token = token_generator.generate_token(username)
            auth_db.add_log(username, ip, token["token"])
            return jsonify(token), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/addInfo", methods=["POST"])
@protected_call
def add_info():
    data = request.get_json()
    username = jwt.decode(request.args.get("token"), app.config["SECRET_KEY"], algorithms="HS512")["username"]
    return jsonify(user_db.add_info({
        "username": username,
        "name": data['name'],
        "email": data["email"]
    }, username))


@app.route("/getInfo", methods=["GET"])
@protected_call
def get_info():
    username = jwt.decode(request.args.get("token"), app.config["SECRET_KEY"], algorithms="HS512")["username"]
    for i in user_db.get_user_info(username):
        return i


@app.route("/change_password", methods=["POST"])
@protected_call
def change_password():
    data = request.get_json()
    username = jwt.decode(request.args.get("token"), app.config["SECRET_KEY"], algorithms="HS512")["username"]
    new_password = data["newPassword"]
    old_password = data["oldPassword"]
    if auth_db.change_password(username, old_password, new_password) == 200:
        return jsonify({"message": "Password changed successfully"}), 200
    else:
        return jsonify({"message": "Enter correct password"}), 403


@app.route("/generate_reset_password/", methods=["GET"])
def generate_reset_token():
    username: str = request.get_json()["username"]
    return jsonify(token_generator.generate_token(username=username, token_type="reset"))


@app.route("/reset_password")
@protected_call
def reset_password():
    token = jwt.decode(request.args.get("token"), app.config["SECRET_KEY"], algorithms="HS512")
    new_password = request.get_json()["new_password"]
    if token["token_type"] != "reset":
        return jsonify({"message": "invalid token"}), 403
    auth_db.reset_password(token["username"], new_password)
    return jsonify({"message": "Password reset successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
