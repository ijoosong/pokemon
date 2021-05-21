import azure.functions as func
import requests

def main(req: func.HttpRequest, pokemonTeamDocument: func.Out[func.Document]) -> func.HttpResponse:

    request_body = req.get_json()
    # body = {'pokemon': [{'name': 'pikachu'}.....etc.]}
    
    pokemon_team = {}

    for pokemon in request_body['pokemon']:
        pokemon_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}').json()
        pokemon_types = [type['type']['name'] for type in pokemon_response['types']]
        pokemon_team[pokemon] = {'types': pokemon_types}

    pokemonTeamDocument.set(func.Document.from_dict(pokemon_team))

    return 'OK'

#{"pokemon": ["pikachu", "squirtle", "gastly", "scyther", "moltres", "articuno"]}