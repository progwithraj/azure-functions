import logging
import azure.functions as func
from dotenv import load_dotenv,find_dotenv
import os

def main(req: func.HttpRequest , msg : func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    #dotenv loader
    load_dotenv(find_dotenv())
    
    #default authentication bool set to false
    is_autenticated = False

    order = req.params.get('order')
    location = req.params.get('location')

    user = req.headers.get('HTTP-USER')
    passsord = req.headers.get('HTTP-PASS')

    if user and passsord:
        if user == os.getenv('HTTP-USER') and passsord == os.getenv('HTTP-PASS'):
            is_autenticated = True


    if is_autenticated:
        if not order:
            try:
                req_body = req.get_json()
            except ValueError:
                logging.error(str(ValueError))
                return func.HttpResponse("Error occurred",status_code = 400)
            else:
                order = req_body.get('order')
                location = req_body.get('location',None)

        if order and location :
            msg.set(f"{order} at {location}")
            return func.HttpResponse(f"new order recieved , \nid : {order} \tlocation: {location}",status_code=200)
    else:
        return func.HttpResponse(
            "User Autentication Failed ! or maybe order not passed",
            status_code=400
        )
