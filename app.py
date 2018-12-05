from flask import Flask
from urllib3 import PoolManager
from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox
from functools import wraps
from requests import request
from flask import abort
from flask import request
from flask import render_template

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
            tmp2 = None
            tmp3 = None
            if authorization_header in request.headers:
                tmp = request.headers[authorization_header].split(" ")

            if len(tmp) < 2 or len(tmp[1]) != expected_token_length:
                return abort(401)

            else:
                token = tmp[1]

            username = None

            response = http.request('GET',
                                    "https://security-dot-training-project-lab.appspot.com/authenticate?token=" + token)

            tmp2 = response.data.split(" ")
            tmp3 = tmp2[1].split("\"")
            username = tmp3[0]

            return api_method(username, *args, **kwargs)

        return authenticate_user

    return decorator


@app.route("/")
def test():
    return "This is our game"


def __unicode__(self):
    return unicode(self.some_field) or u''


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)


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
    lastName = request.args.get('lastName')
    password = request.args.get('password')

    response = http.request('POST',
                            "https://security-dot-training-project-lab.appspot.com/signup?name=" + name + "&last_name=" + lastName + "&email=" + email + "&password=" + password)
    return response.data


@app.route("/deleteAccount", methods=['DELETE'])
def deleteAccount():
    userid = request.args.get('userid')
    if not userid:
        return 400

    response = http.request('DELETE', auth_service_url, params=userid)
    if not response:
        return 500, "Internal server error"
    return response.data


@app.route("/updateAccount", methods=['PUT'])
def updateAccount(updatedString):
    if not updatedString:
        return 400
    response = http.request('PUT', auth_service_url, data={'updatedString': updatedString})
    if not response:
        return 500, "Internal server error"
    return response.data


@app.route("/leaveGameLobby", methods=['PUT'])
@require_authentication()
def LeaveGameLobby(username):
    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/LeaveGameLobby?username=" + username)

    return response.data


@app.route("/Ready", methods=['PUT'])
@require_authentication()
def Ready(username):
    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/Ready?username=" + username)
    return response.data


@app.route("/unReady", methods=['PUT'])
@require_authentication()
def UnReady(username):
    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/UnReady?username" + username)

    return response.data


@app.route("/renameLobby", methods=['PUT'])
@require_authentication()
def RenameLobby(username):
    newLobbyName = request.args.get('newLobbyName')
    if not newLobbyName:
        return 400
    if len(newLobbyName) < 1:
        return 400

    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/RenameLobby?newLobbyName=" + newLobbyName + "&username=" + username)

    return response.data


@app.route("/setSeed", methods=['PUT'])
@require_authentication()
def SetSeed(username):
    seed = request.args.get('seed')
    if not seed:
        return 400

    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/SetSeed?seed=" + seed + "&username=" + username)

    return response.data


@app.route("/newGameLobby", methods=['POST'])
@require_authentication()
def NewGameLobby(username):
    playerNumber = request.args.get('playerNumber')

    response = http.request('POST',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/NewGameLobby?playerNumber=" + playerNumber + "&userName=" + username)

    return response.data


@app.route("/joinGameLobby", methods=['PUT'])
@require_authentication()
def JoinGameLobby(username):
    gameID = request.args.get('GameID')

    response = http.request('PUT',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/JoinGameLobby?GameID=" + gameID + "&userName=" + username)

    return response.data


@app.route("/getGameList", methods=['GET'])
def GetGameList():
    response = http.request('GET', "https://lobbyservice-dot-training-project-lab.appspot.com/GetGameList")
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getGameLobbyData", methods=['GET'])
@require_authentication()
def GetGameLobbyData(username):
    response = http.request('GET',
                            "https://lobbyservice-dot-training-project-lab.appspot.com/GetGameLobbyData?userName=" + username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/forfeit", methods=['PUT'])
@require_authentication()
def forfeit(username):
    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/forfeit?username" + username)
    return response.data


@app.route("/endTurn", methods=['PUT'])
@require_authentication()
def endTurn(username):
    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/end_turn?username=" + username)
    return response.data


@app.route("/upgrade", methods=['PUT'])
@require_authentication()
def upgrade(username):
    baseID = request.args.get('baseID')
    if not baseID:
        return 400

    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/upgrade?baseID=" + baseID + "&username=" + username)

    return response.data


@app.route("/createUnit", methods=['PUT'])
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

    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/create_unit?xCoord=" + xCoord + "&yCoord=" + yCoord + "&type=" + type + "&baseID=" + baseID + "&username=" + username)

    return response.data


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

    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/move?xCoord=" + xCoord + "&yCoord=" + yCoord + "&unitID=" + unitID + "&username=" + username)

    return response.data


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

    response = http.request('PUT',
                            "https://gameengine-dot-training-project-lab.appspot.com/attack?xCoord=" + xCoord + "&yCoord=" + yCoord + "&unitID=" + unitID + "&username=" + username)
    return response.data


@app.route("/getMoves", methods=['GET'])
@require_authentication()
def getMoves(username):
    unitID = request.args.get('unitID')
    if not unitID:
        return 400

    response = http.request('GET',
                            "https://gameengine-dot-training-project-lab.appspot.com/get_moves?unitID=" + unitID + "&username=" + username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getAttacks", methods=['GET'])
@require_authentication()
def getAttacks(username):
    unitID = request.args.get('unitID')
    if not unitID:
        return 400

    response = http.request('GET',
                            "https://gameengine-dot-training-project-lab.appspot.com/get_attacks?unitID=" + unitID + "&username=" + username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getPlacement", methods=['GET'])
@require_authentication()
def getPlacement(username):
    baseID = request.args.get('baseID')
    if not baseID:
        return 400

    response = http.request('GET',
                            "https://gameengine-dot-training-project-lab.appspot.com/get_placement?baseID=" + baseID + "&username=" + username)
    if not response.data:
        return 500, "Internal server error"
    return response.data


@app.route("/getState", methods=['GET'])
@require_authentication()
def getState(username):
    response = http.request('GET',
                            "https://gameengine-dot-training-project-lab.appspot.com/get_state?username=" + username)
    if not response.data:
        return 500, "Internal server error"
    return response.data
