import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input_url = req.params.get('input_url')
    if not input_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_url = req_body.get('input_url')

    if input_url:
        return func.HttpResponse(f"Hello world.")
    else:
        return func.HttpResponse(
             "Invalid request parameter",
             status_code=400
        )
