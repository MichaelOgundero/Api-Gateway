from flask import Flask
from urllib3 import PoolManager
from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox
from functools import wraps
from requests import request
from flask import abort
from flask import request

http = AppEngineManager() if is_appengine_sandbox() else PoolManager()
if not http:
    raise ValueError("Could not instantiate HTTTP")

app = Flask(__name__)

authorization_header = "Authorization"

token_urlparam = "token"

expected_token_length = 256

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

            else:
                token = tmp[1]

            username = None

            response = http.request('GET', "https://security-dot-training-project-lab.appspot.com/authenticate?token=" + token)

            username = response.data

            return api_method(username, *args, **kwargs)

        return authenticate_user

    return decorator


@app.route("/")
def test():
    return "This is our game"


@app.route("/test", methods=['GET'])
def test2():
    response = http.request('GET', "https://security-dot-training-project-lab.appspot.com/test")
    return response.data


@app.route("/logIn", methods=['POST'])
def logIn():
    email = request.args.get('email')
    password = request.args.get('password')
    response = http.request('POST',
                            "https://security-dot-training-project-lab.appspot.com/login?email=" + email + "&password=" + password)
    return response.data


@app.route("/logOut", methods=['POST'])
def logOut():
    token = request.args.get('token')
    response = http.request('POST', "https://security-dot-training-project-lab.appspot.com/logout?token=" + token)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/activeList", methods=['GET'])
def activeList():
    response = http.request('GET', "https://security-dot-training-project-lab.appspot.com/activeusers")
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/signUp", methods=['POST'])
def signUp():
    email = request.args.get('email')
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    password = request.args.get('password')

    response = http.request('POST', "https://security-dot-training-project-lab.appspot.com/signup?name=" + name + "&last_name=" + last_name + "&email=" + email + "&password=" + password)
    return response.data


@app.route("/deleteAccount", methods=['DELETE'])
def deleteAccount():
    userid = request.args.get('userid')
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

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/LeaveGameLobby?username="+ username)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/Ready", methods=['PUT'])
@require_authentication()
def Ready(username):
    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/Ready?username="+username)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/UnReady", methods=['PUT'])
@require_authentication()
def UnReady(username):
    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/Unready?username"+username)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/RenameLobby", methods=['PUT'])
@require_authentication()
def RenameLobby(username):
    newLobbyName = request.args.get('newLobbyName')
    if not newLobbyName:
        return 400
    if len(newLobbyName) < 1:
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/RenameLobby?username="+username+"&newLobbyName="+newLobbyName)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/SetSeed", methods=['PUT'])
@require_authentication()
def SetSeed(username):
    seed = request.args.get('seed')
    if not seed:
        return 400
    if not isinstance(seed, int):
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/SetSeed?username="+username+"&seed="+seed)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/NewGameLobby", methods=['POST'])
@require_authentication()
def NewGameLobby(username):
    playerNumber = request.args.get('playerNumber')
    if not isinstance(playerNumber, int):
        return 400

    response = http.request('POST', "https://lobbyservice-dot-training-project-lab.appspot.com/NewGameLobby?username="+username+"&playerNumber="+playerNumber)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/JoinGameLobby", methods=['PUT'])
@require_authentication()
def JoinGameLobby(username):
    gameID = request.args.get('gameID')
    if not gameID:
        return 400
    if not isinstance(gameID, int):
        return 400

    response = http.request('PUT', "https://lobbyservice-dot-training-project-lab.appspot.com/JoinGameLobby?username="+username+"&gameID"+gameID)
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
    response = http.request('GET', "https://lobbyservice-dot-training-project-lab.appspot.com/GetGameLobbyData?username="+username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/forfeit", methods=['PUT'])
@require_authentication()
def forfeit(username):
    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/forfeit?username"+username)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/endTurn", methods=['PUT'])
@require_authentication()
def endTurn(username):
    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/end_turn?username="+username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/upgrade", methods=['PUT'])
@require_authentication()
def upgrade(username):
    baseID = request.args.get('baseID')
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/upgrade?username="+username+"&baseID="+baseID)
    if not response.data:
        return 500, "Internal server error"

    return response.data


@app.route("/createUnit", methods=['POST'])
@require_authentication()
def createUnit(username):
    xCoord = request.args.get('xCoord')
    yCoord = request.args.get('yCoord')
    baseID = request.args.get('baseID')
    type = request.args.get('type')
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

    response = http.request('POST', "https://gameengine-dot-training-project-lab.appspot.com/create_unit?username="+username+"&xCoord="+xCoord+"&yCoord="+yCoord+"&type="+type+"&baseID="+baseID)
    if not response:
        return 500, "Internal server error"

    return response.status


@app.route("/move", methods=['PUT'])
@require_authentication()
def move(username):
    xCoord = request.args.get('xCoord')
    yCoord = request.args.get('yCoord')
    unitID = request.args.get('unitID')
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

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/move?username="+username+"&xCoord="+xCoord+"&yCoord="+yCoord+"&unitID="+unitID)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/attack", methods=['PUT'])
@require_authentication()
def attack(username):
    xCoord = request.args.get('xCoord')
    yCoord = request.args.get('yCoord')
    unitID = request.args.get('unitID')
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

    response = http.request('PUT', "https://gameengine-dot-training-project-lab.appspot.com/attack?username="+username+"&xCoord="+xCoord+"&yCoord="+yCoord+"&unitID="+unitID)
    if not response:
        return 500, "Internal server error"
    return response.status


@app.route("/getMoves", methods=['GET'])
@require_authentication()
def getMoves(username):
    unitID = request.args.get('unitID')
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_moves?username="+username+"&unitID="+unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getAttacks", methods=['GET'])
@require_authentication()
def getAttacks(username):
    unitID = request.args.get('unitID')
    if not unitID:
        return 400
    if not isinstance(unitID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_attacks?username="+username+"&unitID="+unitID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getPlacement", methods=['GET'])
@require_authentication()
def getPlacement(username):
    baseID = request.args.get('baseID')
    if not baseID:
        return 400
    if not isinstance(baseID, int):
        return 400

    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_placement?username="+username+"&baseID="+baseID)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getState", methods=['GET'])
@require_authentication()
def getState(username):
    response = http.request('GET', "https://gameengine-dot-training-project-lab.appspot.com/get_state?username="+username)
    if not response.data:
        return 500, "Internal server error"
    return response.data
