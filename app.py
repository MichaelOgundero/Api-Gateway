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

auth_service_url = "https://security-dot-training-project-lab.appspot.com/"

game_engine_url = "https://gameengine-dot-training-project-lab.appspot.com/"

lobby_url = "https://lobbyservice-dot-training-project-lab.appspot.com/"


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


@app.route("/logIn", methods=['POST'])
def logIn(email, password):
    if not email:
        return 400
    if not password:
        return 400
    response = http.request('POST', game_engine_url, data={'email': email, 'password': password})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/logOut", methods=['GET'])
@require_authentication()
def logOut(username):
    response = http.request('GET', auth_service_url, params=username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/activeList", methods=['GET'])
def activeList():
    response = http.request('GET', auth_service_url)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/signUp", methods=['POST'])
def signUp(name, lastName, email, password, age):
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
    return response.status


@app.route("/deleteAccount", methods=['DELETE'])
def deleteAccount(userid):
    if not userid:
        return 400
    if not isinstance(userid, int):
        return 400
    response = http.request('DELETE', auth_service_url, params=userid)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/updateAccount", methods=['PUT'])
def updateAccount(updatedString):
    if not updatedString:
        return 400
    response = http.request('PUT', auth_service_url, data={'updatedString': updatedString})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/LeaveGameLobby", methods=['PUT'])
@require_authentication()
def LeaveGameLobby(username):
    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/LeaveGameLobby", data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/Ready", methods=['PUT'])
@require_authentication()
def Ready(username):
    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/Ready", data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/UnReady", methods=['PUT'])
@require_authentication()
def UnReady(username):
    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/Unready", data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/RenameLobby", methods=['PUT'])
@require_authentication()
def RenameLobby(username, newLobbyName):
    if not newLobbyName:
        return 400
    if len(newLobbyName) < 1:
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/RenameLobby", data={'username': username, 'newLobbyName': newLobbyName})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/SetSeed", methods=['PUT'])
@require_authentication()
def SetSeed(username, seed):
    if not seed:
        return 400
    if not isinstance(seed, int):
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/SetSeed", data={'username': username, 'seed': seed})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/NewGameLobby", methods=['POST'])
@require_authentication()
def NewGameLobby(username, playerNumber):
    if not isinstance(playerNumber, int):
        return 400

    response = http.request('POST', "https://lobbyservice-dot-training-project-lab.appspot.com/NewGameLobby", data={'username': username, 'playerNumber': playerNumber})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/JoinGameLobby", methods=['PUT'])
@require_authentication()
def JoinGameLobby(username, gameID):
    if not gameID:
        return 400
    if not isinstance(gameID, int):
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/JoinGameLobby", data={'username': username, 'gameID': gameID})
    if not response:
    	return 500, "Internal server error"
    return response.status


@app.route("/GetGameList", methods=['GET'])
def GetGameList():
    response = http.request('GET', "https://lobbyservice-dot-training-project-lab.appspot.com/GetGameList")
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/GetGameLobbyData", methods=['GET'])
@require_authentication()
def GetGameLobbyData(username):
    response = http.request('GET', "https://lobbyservice-dot-training-project-lab.appspot.com/GetGameLobbyData", params=username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/forfeit", methods=['PUT'])
@require_authentication()
def forfeit(username):
    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/forfeit", data={'username': username})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/endTurn", methods=['GET'])
def endTurn():
    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/end_turn")
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/upgrade", methods=['PUT'])
def upgrade(baseID):
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/upgrade", data={'baseID': baseID})
    if not response:
    	return 500, "Internal server error"
    
    return response.status


@app.route("/createUnit", methods=['POST'])
def createUnit(xCoord, yCoord, type, baseID):
    if not xCoord:
        return 400
    if not yCoord:
        return 400
    if not type:
        return 400
    if not baseID:
        return 400
    if not isinstance(xCoord, int):
        return 400
    if not isinstance(yCoord, int):
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('POST', "https://gameengine-dot-training-project-lab.appspot.com/create_unit", data={'xCoord': xCoord, 'yCoord': yCoord, 'type': type, 'basseID': baseID})
    if not response:
    	return 500, "Internal server error"

    return response.status


@app.route("/move", methods=['PUT'])
def move(xCoord, yCoord, unitID):
    if not xCoord:
        return 400
    if not yCoord:
        return 400
    if not unitID:
        return 400
    if not isinstance(xCoord, int):
        return 400
    if not isinstance(yCoord, int):
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/move", data={'xCoord': xCoord, 'yCoord': yCoord, 'unitID': unitID})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/attack", methods=['PUT'])
def attack(xCoord, yCoord, unitID):
    if not xCoord:
        return 400
    if not yCoord:
        return 400
    if not unitID:
        return 400
    if not isinstance(xCoord, int):
        return 400
    if not isinstance(yCoord, int):
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/attack", data={'xCoord': xCoord, 'yCoord': yCoord, 'unitID': unitID})
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/getMoves", methods=['GET'])
def getMoves(unitID):
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_moves", params=unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getAttacks", methods=['GET'])
def getAttacks(unitID):
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_attacks", params=unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getPlacement", methods=['GET'])
def getPlacement(baseID):
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_placement", params=baseID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getState", methods=['GET'])
@require_authentication()
def getState(username):
    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_state", params=username)
    if not response.data:
        return 500, "Internal server error"
    return response.data
