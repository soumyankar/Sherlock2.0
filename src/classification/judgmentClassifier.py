import requests
import json

api_key = "49af15c9be3d4a5f927bc4a85d9511fa" # You could use your own API key here but ok.
input_claim = "The sky is blue."

def textJudge(text):   
        # Define the endpoint (url), payload (sentence to be scored), api-key (api-key is sent as an extra header)
        api_endpoint = "https://idir.uta.edu/claimbuster/api/v2/score/text/"
        request_headers = {"x-api-key": api_key}
        payload = {"input_text": text}

        # Send the POST request to the API and store the api response
        api_response = requests.post(url=api_endpoint, json=payload, headers=request_headers)

        # Print out the JSON payload the API sent back
        json_response = api_response.json()
        response = {"score": json_response['results'][0]['score'], "result": json_response['results'][0]['result']}
        return response
                    