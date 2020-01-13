class TrackViaException(Exception):
    def __init__(self, message, method="", endpoint="", status_code=None):
        super().__init__(message)
        self.endpoint = endpoint
        self.status_code = status_code
