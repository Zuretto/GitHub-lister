import requests
import json
import flask
from flask import request, jsonify
#query: here you can specify REST params that are to be send from the server to GithubAPI such as autorisation.
query = {'q': 'requests+language:python',
            'Accept': 'application/vnd.github.v3+json'
            }

app = flask.Flask(__name__)
#setting app debug mode to True so that you may see what the server is doing
app.config["DEBUG"] = True

#a function that handles GET REST command for listing repositories
@app.route('/list', methods = ['GET'])
def api_list():
    #if server's client specified the nick - get it into a variable
    if 'user' in request.args:
        nick = str(request.args['user'])
    #else return "failed" message - we can't list repos of non-existing user!
    else:
        return jsonify({'status': 'failed', 'message': 'please specify the nick'}), 400
    
    answer = []    
    #requesting data from GithubAPI
    response = requests.get('https://api.github.com/users/{0}/repos'.format(nick), params=query)

    #I have put building the answer from GHAPI response into try-catch, because if e.g. the user doesn't exist, Python will throw an exception. Therefore, the exception will be catched and server will return an error to the client.
    try:
        for i in response.json():
                answer.append({'name': i['name'], 
                            'stargazers_count': i['stargazers_count']})
        page_number = 2
        #Here I iterate through pages of GHApi while it responds me with repositories data. If it doesn't, it means I've iterated through all public repositories of an user.
        while(len(response.json())):
            response = requests.get('https://api.github.com/users/{0}/repos?page={1}'.format(nick, page_number), params=query)
            page_number += 1
            if 'message' in response.json():
                break
            for i in response.json():
                answer.append({'name': i['name'], 
                            'stargazers_count': i['stargazers_count']})
    except:
        return jsonify({'status': 'failed', 'message': response.json()['message']}), 404
    return(jsonify(answer))

#a function that handles GET REST command for counting stars of user's repos
@app.route('/star', methods = ['GET'])
def getStargazersCount():
    #if server's client specified the nick - get it into a variable
    if 'user' in request.args:
        nick = str(request.args['user'])
    #else return "failed" message - we can't list repos of non-existing user!
    else:
        return {'status': 'failed', 'message': 'please specify the nick'}, 400
        
    answer = []
    #requesting data from GithubAPI
    response = requests.get('https://api.github.com/users/{0}/repos'.format(nick), params=query)

    #I have put building the answer from GHAPI response into try-catch, because if e.g. the user doesn't exist, Python will throw an exception. Therefore, the exception will be catched and server will return an error to the client.
    try:
        answer = {'user' : nick, 'stargazers_count': 0}
        for i in response.json():
                answer['stargazers_count'] += i['stargazers_count']
        page_number = 2
        #Here I iterate through pages of GHApi while it responds me with repositories data. If it doesn't, it means I've iterated through all public repositories of an user.
        while(len(response.json())):
            response = requests.get('https://api.github.com/users/{0}/repos?page={1}'.format(nick, page_number), params=query)
            page_number += 1
            if 'message' in response.json():
                break
            for i in response.json():
                answer['stargazers_count'] += i['stargazers_count']
    except:
        return jsonify({'status': 'failed', 'message': response.json()['message']}), 404
    return(jsonify(answer))

@app.errorhandler(404)
def page_not_found(e):
    return jsonify("The resource could not been found"), 404

if __name__ == '__main__':
    app.run()