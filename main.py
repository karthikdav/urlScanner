import urllib
import configparser
import flask
from flask import Flask, Response
import dblayer

app = Flask(__name__)

# Below to read the configuration for setting up the application
config = configparser.ConfigParser()
config.read('config.ini')
FLASK_PORT = config['FLASK_APP']['port']


@app.route('/')
def hello_check():
    response_string = 'URL Scanner is running on port {}'.format(FLASK_PORT)
    return Response(response_string, status=200)


@app.route('/rest/api/v1/urlScanner/all', methods=['GET'])
def get_all_url():
    if flask.request.method == 'GET':
        # response_string = 'got all records'
        response_string = dblayer.get_all_records()
        return Response(response_string, status=200)
    else:
        response_string = 'Only GET method is supported with this endpoint'
        return Response(response_string, status=405)


# use update_url to send the updated URL in form data
@app.route('/rest/api/v1/urlScanner/<id>', methods=['GET', 'PUT', 'DELETE'])
def operate_on_url(id):
    if flask.request.method == 'GET':
        if id is not None:
            url_id = id
            # response_string = 'got the record for {}'.format(url_id)
            response_string = dblayer.get_record_by_id(url_id)
            return Response(response_string, status=200)
        else:
            return Response('Not enough values where supplied for endpoint', status=422)
    elif flask.request.method == 'PUT':
        if id is not None and flask.request.form.get('update_url') is not None:
            url_id = id
            url_string = flask.request.form.get('update_url')
            response_count = dblayer.update_record(url_id, url_string, True)
            if response_count > 0:
                response_string = 'url id with {} is updated with url string {}'.format(url_id, url_string)
            else:
                response_string = "URL update failed for id {}".format(id)
            return Response(response_string, status=200)
        else:
            return Response('Not enough values where supplied for endpoint', status=422)
    elif flask.request.method == 'DELETE':
        if id is not None:
            url_id = id
            response_count = dblayer.update_record(url_id, '', False)
            if response_count > 0:
                response_string = 'url id with {} is Deleted'.format(url_id)
            else:
                response_string = 'Deleting the record failed for id {}'.format(id)
            return Response(response_string, status=200)
        else:
            return Response('Not enough values where supplied for endpoint', status=422)
    else:
        response_string = 'Only GET, PUT and Delete method is supported with this endpoint'
        return Response(response_string, status=405)


# send the url to be inserted in insert_url in form data
@app.route('/rest/api/v1/urlScanner/add', methods=['POST'])
def add_url():
    if flask.request.method == 'POST':
        if flask.request.form.get('insert_url') is not None:
            request_url = flask.request.form.get('insert_url')
            result = dblayer.insert_record(request_url)
            if result > 0:
                response_string = 'the insert_url is {}'.format(request_url)
            else:
                response_string = 'Insertion failed for URL {}'.format(request_url)
            return Response(response_string, status=200)
        else:
            return Response('Not enough values where supplied for endpoint', status=422)
    else:
        response_string = 'Only post method is allowed with this endpoint'
        return Response(response_string, status=405)


# use originalpathquerystring to send the query string
# use hostname to send the hostname and port for sending port
# port is optional
# all these are supposed to be passed as query parameters and original path query string must be url encoded in utf-8
@app.route('/rest/api/v1/urlScanner/isSafeUrl', methods=['GET'])
def is_safe_url():
    if flask.request.method == 'GET':
        hostname = flask.request.args.get('hostname')
        port = flask.request.args.get('port')
        url = flask.request.args.get('originalpathquerystring')
        if hostname is not None and url is not None:
            url = urllib.parse.unquote(url)
            if port is not None:
                url = hostname+':'+port+url
            else:
                url = hostname+url
            db_response = dblayer.check_for_url(url)
            if len(db_response) != 0 and db_response != 0:
                return Response('The URL is unsafe', status=400)
            elif db_response == 0:
                return Response('Exception occurred in dblayer', status=200)
            else:
                return Response('The Url is clean', status=200)
    else:
        response_string = 'Only GET method is supported with this endpoint'
        return Response(response_string, status=405)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(FLASK_PORT))
