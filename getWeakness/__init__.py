import logging
import azure.functions as func
import requests

#import json; print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
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

    types_pokemon_double_damage_from = set()
    types_pokemon_half_damage_from = set()
    types_pokemon_no_damage_from = set()

    for type in types_for_pokemon:
        type_response = requests.get(f'https://pokeapi.co/api/v2/type/{type}')
        type_response_json = type_response.json()
        types_pokemon_double_damage_from.update(type['name'] for type in type_response_json['damage_relations']['double_damage_from'])
        types_pokemon_half_damage_from.update(type['name'] for type in type_response_json['damage_relations']['half_damage_from'])
        types_pokemon_no_damage_from.update(type['name'] for type in type_response_json['damage_relations']['no_damage_from'])

    types_pokemon_double_damage_from = types_pokemon_double_damage_from - types_pokemon_half_damage_from
    types_pokemon_double_damage_from = types_pokemon_double_damage_from - types_pokemon_no_damage_from
    
    output = {
        'name': pokemon,
        'weaknesses': list(types_pokemon_double_damage_from),
        'resistances': list(types_pokemon_half_damage_from),
        'no_damage_from': list(types_pokemon_no_damage_from)
    }

    if pokemon:
        doc.set(func.Document.from_dict(output))
        return func.HttpResponse(f"{output}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized pokemon_response.",
             status_code=200
        )
