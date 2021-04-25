import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pokemon = req.params.get('pokemon')

    if not pokemon:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            pokemon = req_body.get('pokemon')
    
    pokemon_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')

    body = pokemon_response.json()
    types_for_pokemon = []

    for type in body['types']:
        types_for_pokemon.append(type['type']['name'])

    types_pokemon_weak_against = []
    for type in types_for_pokemon:
        type_response = requests.get(f'https://pokeapi.co/api/v2/type/{type}')
        type_response_json = type_response.json()
        types_pokemon_weak_against.append(type_response_json['damage_relations']['double_damage_from'])
    if pokemon:
        return func.HttpResponse(f"{types_pokemon_weak_against}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized pokemon_response.",
             status_code=200
        )
