from flask import Flask
from urllib3 import PoolManager
from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox
from functools import wraps
from requests import request
from flask import abort

http = AppEngineManager() if is_appengine_sandbox() else PoolManager()
if not http:
    raise ValueError("Could not instantiate HTTTP")

app = Flask(__name__)

authorization_header = "Authorization"

token_urlparam = "token"

expected_token_length = 64

auth_service_url = "https://..."

game_engine_url = "https://..."

lobby_url = "https://..."


def require_authentication():
    def decorator(api_method):
        @wraps(api_method)
        def authenticate_user(*args, **kwargs):
            token = None
            tmp = None
            if authorization_header in request.headers:
                tmp = request.headers[authorization_header].split(" ")

            if len(tmp) < 2 or len(tmp[1]) != expected_token_length:
                return abort(401)

            else: token = tmp[1]

            username = None

            response = http.request('GET', auth_service_url, fields=token)

            username = response.data

            return api_method(username, *args, **kwargs)
        return authenticate_user
    return decorator


@app.route("/")
def test():
    return "This is our game"


@app.route("/log_in", methods=['GET'])
def log_in(email, password):
    if not email:
        return 400
    if not password:
        return 400
    response = http.request('POST', game_engine_url, data={'email': email, 'password': password})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/log_out", methods=['GET'])
@require_authentication()
def log_out(username):
    response = http.request('GET', auth_service_url, data={'username': username})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/active_list", methods=['GET'])
def active_list():
    response = http.request('GET', auth_service_url)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/sign_up", methods=['POST'])
def sign_up(name, lastName, email, password, age):
    if not name:
        return 400
    if not lastName:
        return 400
    if not email:
        return 400
    if not password:
        return 400
    if not age:
        return 400
    if not isinstance(age, int):
        raise ValueError("Age is not an INT")

    response = http.request('POST', auth_service_url, data={'name': name, 'lastName': lastName, 'password': password, 'age': age})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/delete_account", methods=['DELETE'])
def delete_account(userid):
    if not userid:
        return 400
    if not isinstance(userid, int):
        return 400
    response = http.request('DELETE', auth_service_url, fields=userid)
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/update_account", methods=['PUT'])
def update_account(updatedString):
    if not updatedString:
        return 400
    response = http.request('PUT', auth_service_url, fields=updatedString)
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/leave_game_lobby", methods=['PUT'])
@require_authentication()
def leave_game_lobby(username):
    response = http.request('PUT', lobby_url, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/ready", methods=['PUT'])
@require_authentication()
def ready(username):
    response = http.request('PUT', lobby_url, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/unready", methods=['PUT'])
@require_authentication()
def unready(username):
    response = http.request('PUT', lobby_url, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/rename_lobby", methods=['PUT'])
@require_authentication()
def rename_lobby(username, newLobbyName):
    if not new_game_lobby:
        return 400
    if len(newLobbyName) < 1:
        return 400

    response = http.request('PUT', lobby_url, fields=newLobbyName, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/set_seed", methods=['PUT'])
@require_authentication()
def set_seed(username, seed):
    if not seed:
        return 400
    if not isinstance(seed, int):
        return 400

    response = http.request('PUT', lobby_url, fields=seed, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/new_game_lobby", methods=['POST'])
@require_authentication()
def new_game_lobby(username, playerNumber):
    if not isinstance(playerNumber, int):
        return 400

    response = http.request('POST', lobby_url, fields=playerNumber, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/join_game_lobby", methods=['PUT'])
@require_authentication()
def join_game_lobby(username, gameID):
    if not gameID:
        return 400
    if not isinstance(gameID, int):
        return 400

    response = http.request('PUT', lobby_url, fields=gameID, data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_game_list", methods=['GET'])
def get_game_list():
    response = http.request('GET', lobby_url)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_game_lobby_data", methods=['GET'])
@require_authentication()
def get_game_lobby_data(username):
    response = http.request('GET', lobby_url, data={'username': username})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/forfeit", methods=['PUT'])
@require_authentication()
def forfeit(username):
    response = http.request('PUT', game_engine_url, data={'username': username})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/end_turn", methods=['GET'])
def end_turn():
    response = http.request('GET', game_engine_url)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/upgrade", methods=['PUT'])
def upgrade(baseID):
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('PUT', game_engine_url, fields=baseID)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/create_unit", methods=['POST'])
def create_unit(x, y):
    if not x:
        return 400
    if not y:
        return 400
    if not isinstance(x, int):
        return 400
    if not isinstance(y, int):
        return 400

    response = http.request('POST', game_engine_url, data={'xCoord': x, 'yCoord': y})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/move", methods=['PUT'])
def move(x, y, unitID):
    if not x:
        return 400
    if not y:
        return 400
    if not unitID:
        return 400
    if not isinstance(x, int):
        return 400
    if not isinstance(y, int):
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('PUT', game_engine_url, data={'xCoord': x, 'yCoord': y, 'unitID': unitID})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/attack", methods=['PUT'])
def attack(x, y, unitID):
    if not x:
        return 400
    if not y:
        return 400
    if not unitID:
        return 400
    if not isinstance(x, int):
        return 400
    if not isinstance(y, int):
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('PUT', game_engine_url, data={'xCoord': x, 'yCoord': y, 'unitID': unitID})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_moves", methods=['GET'])
def get_moves(unitID):
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', game_engine_url, fields=unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_attacks", methods=['GET'])
def get_attacks(unitID):
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', game_engine_url, fields=unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_placement", methods=['GET'])
def get_placement(baseID):
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('GET', game_engine_url, fields=baseID)
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data


@app.route("/get_state", methods=['GET'])
@require_authentication()
def get_state(username):
    response = http.request('GET', game_engine_url, data={'username': username})
    if not response.data:
        return 500, "Internal server error"
    return response.status, response.data
