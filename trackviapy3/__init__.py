import logging

from requests import Request, Session
from .trackvia_exception import TrackViaException

class TrackVia:
    def __init__(self, user_key, token="", base_url="https://go.trackvia.com:443"):
        if user_key is None or len(user_key) < 1:
            raise TrackViaException("Invalid user key. Please instantiate TrackVia object with a valid user key", endpoint=endpoint)
        self.user_key = user_key
        self.token = token
        self.base_url = base_url

    # Get all apps in an account
    def get_all_apps(self):
        METHOD = "GET"
        ENDPOINT = "/openapi/apps"
        return self.make_request(METHOD, ENDPOINT)
    # Get all views in an account
    def get_all_views(self):
        METHOD = "GET"
        ENDPOINT = "/openapi/views"
        return self.make_request(METHOD, ENDPOINT)
    # Get all views in an account
    def get_view(self, view_id=0):
        METHOD = "GET"
        ENDPOINT = "/openapi/views/{view_id}".format(view_id=view_id)
        return self.make_request(METHOD, ENDPOINT)
    # Get records in a view with pagination
    def get_all_records(self, view_id=0, start=0, max=50):
        METHOD = "GET"
        ENDPOINT = "/openapi/views/{view_id}".format(view_id=view_id)
        return self.make_request(METHOD, ENDPOINT, params={"start": start, "max": max})
        return self.make_request(METHOD, ENDPOINT)
    # Get all views in an account
    def find_records(self, view_id=0, query="", start=0, max=50):
        METHOD = "GET"
        ENDPOINT = "/openapi/views/{view_id}/find".format(view_id=view_id)
        return self.make_request(METHOD, ENDPOINT, params={"q": query, "start": start, "max": max})
     # Get record
    def get_record(self, view_id=0, record_id=0):
        METHOD = "GET"
        ENDPOINT = "/openapi/views/{view_id}/records/{record_id}".format(view_id=view_id, record_id=record_id)
        return self.make_request(METHOD, ENDPOINT)
    # Create a record
    def create_record(self, view_id=0, data={}):
        METHOD = "POST"
        ENDPOINT = "/openapi/views/{view_id}/records".format(view_id=view_id)
        return self.make_request(METHOD, ENDPOINT, json={"data": data})
    # Update a record
    def update_record(self, view_id=0, record_id=0, data={}):
        METHOD = "PUT"
        ENDPOINT = "/openapi/views/{view_id}/records/{record_id}".format(view_id=view_id, record_id=record_id)
        return self.make_request(METHOD, ENDPOINT, json={"data": data})
    # Delete record
    def delete_record(self, view_id=0, record_id=0):
        METHOD = "DELETE"
        ENDPOINT = "/openapi/views/{view_id}/records/{record_id}".format(view_id=view_id, record_id=record_id)
        return self.make_request(METHOD, ENDPOINT)
    # Get file on a record
    def get_file(self, view_id=0, record_id=0, field_name=""):
        METHOD = "GET"
        ENDPOINT = "/openapi/views/{view_id}/records/{record_id}/files/{field_name}".format(view_id=view_id, record_id=record_id, field_name=field_name)
        return self.make_request(METHOD, ENDPOINT)
    # Attach file to a record
    def attach_file(self, view_id=0, record_id=0, field_name="", files={}):
        METHOD = "POST"
        ENDPOINT = "/openapi/views/{view_id}/records/{record_id}/files/{field_name}".format(view_id=view_id, record_id=record_id, field_name=field_name)
        return self.make_request(METHOD, ENDPOINT, files=files)
    # Get users in account
    def get_users(self, start=0, max=50):
        METHOD = "GET"
        ENDPOINT = "/openapi/users"
        return self.make_request(METHOD, ENDPOINT, params={"start": start, "max": max})
    # Create users in account
    def create_user(self, email="", first_name="", last_name="", timezone=None):
        METHOD = "POST"
        ENDPOINT = "/openapi/users"
        return self.make_request(METHOD, ENDPOINT, params={"email": email, "firstName": first_name, "lastName": last_name, "timeZone": timezone})

    def login(self, username, password):
        body = {
            "grant_type": "password",
            "client_id": "TrackViaAPI",
            "username": username,
            "password": password
        }
        res = self.make_request("POST", "/oauth/token", body=body)
        self.token = res['value']
        self.refresh_token = res['refresh_token']

    def token_refresh(self):
        body = {
            "grant_type": "refresh_token",
            "client_id": "TrackViaAPI",
            "refresh_token": self.refresh_token
        }
        params = {"user_key": self.user_key}
        res = self.make_request("POST", "/oauth/token", params=params, body=body)
        self.token = res['value']
        self.refresh_token = res['refresh_token']

    def make_request(self, method, endpoint, headers={}, params={}, body=None, json=None, files=None):
        params["user_key"] = self.user_key
        if self.token is not None and len(self.token) > 0:
                headers["Authorization"] = "Bearer {token}".format(token = self.token)
        headers["Accepts"] = "application/json"
        req = Request(method, self.base_url + endpoint, headers=headers, params=params, data=body, json=json, files=files)
        resp = self.send_request(req)
        try:
            json = resp.json()
        except:
            # Delete request returns 204 status code and empty response body
            if resp.status_code == 204:
                return ""
            # File requests return 200 but not json
            if resp.status_code == 200 and len(resp.content) > 0:
                return resp.content
        if resp.status_code >= 400:
            # Attempt to refresh token if its expired
            if resp.status_code == 401 and "Access token expired" in json["error_description"]:
                self.token_refresh()
                return self.make_request(method, endpoint, headers, params, body)
            message = ""
            if "error_description" in json:
                message = json["error_description"]
            else:
                message = json["error"]
            raise TrackViaException(message, method, endpoint, resp.status_code)
        else:
            return json

    def send_request(self, req):
        s = Session()
        prepped = req.prepare()
        return s.send(prepped)