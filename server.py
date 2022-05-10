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
    return flask.redirect(
        "https://github.com/Cool-Computer-Club-v2-0-CiB-2022/server/blob/main/APIReference.md",
        code=302)


@booklist.route("/login", methods=["POST"])
def login():
    json = flask.request.json
    if "username" not in json or "password" not in json:
        return flask.abort(422)
    con, cur = db.connect()
    user = cur.execute("""
        SELECT  username,
                accessLevel
        FROM    accounts
        WHERE   LOWER(username) = :username
        AND     password = :password;
        """, {"username": json["username"].lower(),
              "password": json["password"]}).fetchone()
    con.close()
    if user:
        userInfo = {
            "username": user[0],
            "accessLevel": user[1]
        }
        response = flask.make_response(userInfo)
        sessionID = str(uuid.uuid4())
        sessions[sessionID] = userInfo
        response.set_cookie("sessionID", sessionID,
            samesite="None", secure=True)
        return response
    else:
        return flask.abort(401)


@booklist.route("/register", methods=["POST"])
def register():
    json = flask.request.json
    if not authorised(["admin", "manager"]):
        return flask.abort(401)
    if ("username" not in json or "password" not in json
        or "accessLevel" not in json):
        return flask.abort(422)
    if json["accessLevel"] not in ["admin", "manager", "serviceDesk", "technician"]:
        return flask.abort(422)
    con, cur = db.connect()
    userExists = cur.execute("""
        SELECT  username,
                accessLevel
        FROM    accounts
        WHERE   LOWER(username) = :username;
        """, {"username": json["username"].lower()}).fetchone()
    if not userExists:
        db.addUser(cur, **json)
        con.commit()
        response = flask.make_response()
    else:
        response = flask.abort(409)
    con.close()
    return response


def authorised(requiredLevel):
    # Higher number means more permissions
    try:
        return (sessions[flask.request.cookies.get(
            "sessionID")]["accessLevel"] in requiredLevel)
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
    db = database()
    db.createTables()
    sessions = {}

    # Run server
    if useWaitress:
        waitress.serve(booklist, host=host, port=port)
    else:
        booklist.run(host=host, port=port)
