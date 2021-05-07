import logging
import azure.functions as func
from urllib.parse import urlparse

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input_url_string = req.params.get('input_url')
    if not input_url_string:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_url_string = req_body.get('input_url')

    if input_url_string:
        input_url = urlparse(input_url_string)
        if input_url.scheme == "https":
            return func.HttpResponse(f"Hello world.")

    return func.HttpResponse("Invalid request parameter", status_code=400)
