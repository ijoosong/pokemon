import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest, pokemonTeamDocument: func.DocumentList) -> str:
    if not pokemonTeamDocument:
        logging.warning("ToDo item not found")
    else:
        logging.info("Found ToDo item, pokemon team=%s",
                     dict(pokemonTeamDocument[0]))
        current_team = dict(pokemonTeamDocument[0])
        pokemon = req.params.get('pokemon')
        pokemon_response = requests.get(f'http://localhost:7071/api/getWeakness/{pokemon}')
        
    return 'OK'