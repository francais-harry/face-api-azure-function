import logging
import azure.functions as func
from urllib.parse import urlparse
from .. import face_identity

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
            logging.info(f'Input URL={input_url_string}')
            try:
                is_kid_there = face_identity.is_kid_there(input_url_string)
                if is_kid_there:
                    return func.HttpResponse("Detected")
            except Exception as e:
                logging.warning(f"Some error happens with {e.args}")
                return func.HttpResponse("Something bad happens", status_code=500)
            return func.HttpResponse("Not detected")

    return func.HttpResponse("Invalid request parameter", status_code=400)
