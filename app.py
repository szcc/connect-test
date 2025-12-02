import os

def get():
    # Posit Connect will map HTTP GET / to this function
    return {
        "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
    }
