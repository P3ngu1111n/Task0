import requests
import json
import http
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from http.server import BaseHTTPRequestHandler

app = FastAPI()
@app.get('/')

class SimpleCORSHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        # This sends the CORS header for every response
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello! This response is CORS-enabled.")

    def do_OPTIONS(self):
        # Browsers send an OPTIONS request (preflight) before some cross-origin requests
        self.send_response(200, "OK")
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, SimpleCORSHandler)
    print("Serving on port 8000 with CORS enabled...")
    httpd.serve_forever()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello from pure Python on Vercel!'.encode('utf-8'))
        return



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to ["*"] for Access-Control-Allow-Origin: *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def genderize():

base_url = "https://api.genderize.io?"

genderize_name = "Zenith"
def get_resource_info(name):
    url = f"{base_url}name={genderize_name}"
    response = requests.get(url)

    if response == 200:
        genderize_data = response.json()
        return genderize_data
    else:
        return f"theres an issue with the get_resource_info function"

url = f"{base_url}name={genderize_name}"
response = requests.get(url)
genderize_data = response.json()

genderize_info = get_resource_info(genderize_name)

#in case of error, checks what the api is sending
# print (f"{genderize_data["count"]}")


Name = genderize_data["name"]
Sample_size = genderize_data['count']
Gender = genderize_data["gender"]
Probability = genderize_data["probability"]
response_stat = "success"
error_message = ""
processed_at = datetime.now(timezone.utc).isoformat()


if Probability > 0.7 and Sample_size > 100:
    is_confident = True
else:
    is_confident = False


if response.status_code == 200:
    if Gender == "null" or Sample_size == 0 :
        response_stat = "error"
        error_message = "No prediction available for the provided name"

        error_data = {
            "status": response_stat,
            "error_message": error_message
        }
        error_json = json.dumps(error_data, indent=3)
        return error_json
    else:
        result_data = {
            "status": response_stat,
            "data": {
                "name": Name,
                "gender": Gender,
                "probability": Probability,
                "sample_size": Sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }
        result_json = json.dumps(result_data,  indent=4)
        return result_json

elif response.status_code == 400:
        response_stat = "error 400:Bad Request"
        error_message = "Missing or empty name parameter "

        error_data = {
            "status" : response_stat ,
            "error_message" : error_message
        }

        error_json =json.dumps(error_data, indent=3)
        return error_json

elif response.status_code == 422:
        response_stat = "error 422:Unprocessable Entity"
        error_message = "Name is not a string"

        error_data = {
            "status": response_stat,
            "error_message": error_message
        }

        error_json = json.dumps(error_data, indent=3)
        return error_json

elif response.status_code == 500:
        response_stat = "error 500:Internal Server Error "
        error_message = "Server encountered unexpected condition"

        error_data = {
            "status": response_stat,
            "error_message": error_message
        }

        error_json = json.dumps(error_data, indent=3)
        return error_json

elif response.status_code == 502:
        response_stat = "error 502:Bad Gateway"
        error_message = "Server receiving invalid or incomplete response"

        error_data = {
            "status": response_stat,
            "error_message": error_message
        }

        error_json = json.dumps(error_data, indent=3)
        return error_json

else:
        print (f"breh this is the respose its showing: {response} fix it")




