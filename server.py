#!/usr/bin/env python3

import flask
import os
import sys
import subprocess
import time
import uuid

from database import database

booklist = flask.Flask(__name__)
booklist.url_map.strict_slashes = False

# Get commit count and set server string in header
try:
    commitCount = str(int(subprocess.check_output(
        "git rev-list --count HEAD", shell=True, stderr=subprocess.STDOUT)))
    if (len(str(subprocess.check_output(
            "git diff", shell=True, stderr=subprocess.STDOUT)))) > 256:
        commitCount += "-dev"
except subprocess.CalledProcessError:
    commitCount = 0
serverString = f"CoolComputerClubCiBServer/{commitCount} \
Python/{sys.version.split()[0]}"


@booklist.after_request
def afterRequest(response):
    response.headers["Server"] = serverString
    return response


@booklist.route("/", methods=["GET"])
def helloWorld():
    return "Hello, world!"


## Creating accounts is not implemented
# new accounts must be added to the db manually
# {username: {"password": password, "accessLevel": int}}
# accessLevel 1-5, 5 highest, 1 lowest


@booklist.route("/login", methods=["POST"])
def login():
    json = flask.request.json
    if json in [None, {}]:
        return flask.abort(422)
    if json["username"].lower() not in accounts.data:
        return flask.abort(401)
    user = accounts.data[json["username"]]
    if user["password"] == json["password"]:
        response = flask.make_response()
        sessionID = str(uuid.uuid4())
        accounts.sessions[sessionID] = {
            "username": json["username"].lower(),
            "accessLevel": user["accessLevel"]
        }
        response.set_cookie("sessionID", sessionID,
            samesite="None", secure=True)
        return response
    else:
        return flask.abort(401)


def authorised(requiredLevel):
    try:
        return (requiredLevel <= 
        accounts.sessions[flask.request.cookies.get("sessionID")]["accessLevel"])
    except:
        return False


if __name__ == "__main__":
    if "--help" in sys.argv:
        print("Cool Computer Club v2.0 CiB Prototype Server")
        print("Usage: ./server.py [options]")
        print("Options:")
        print("  --help            Display this help and exit")
        print("  --host HOST       Set the servers host IP")
        print("  --port PORT       Set the servers port")
        print("  --werkzeug        Use werkzeug instead of waitress")
        print("  --data-dir DIR    Set the directory where data is stored")
        exit()

    # Get host and port from argv or use the defaults
    host = "0.0.0.0"
    port = 80
    if "--host" in sys.argv:
        host = sys.argv[sys.argv.index("--host") + 1]
    if "--port" in sys.argv:
        port = sys.argv[sys.argv.index("--port") + 1]

    # Use waitress as the WSGI server if it is installed,
    # but use built-in if it isnt, or if --werkzeug argument.
    useWaitress = False
    if not "--werkzeug" in sys.argv:
        try:
            import waitress
            useWaitress = True
        except:
            print("Waitress is not installed, using built-in WSGI server (werkzeug).")

    # Startup
    print("Loading database")
    accounts = database("accounts.json")
    accounts.load()
    accounts.sessions = {}

    # Run server
    print("Starting server")
    if useWaitress:
        waitress.serve(booklist, host=host, port=port)
    else:
        booklist.run(host=host, port=port)

    # Shut down
    print("Saving database")
    accounts.save()
