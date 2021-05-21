import logging
import json
import azure.functions as func


def main(documents: func.DocumentList, outputBlob: func.Out[str]) -> str:
    print("Its starting to take from cosmos and store on blob")
    if documents:
        print("did it even get in here?")
        x = dict(documents[0])
        logging.info('Document id: %s', documents[0]['id'])
        logging.info('Document stuff: %s', json.dumps(x))

        outputBlob.set(json.dumps(x))

    print("it finished????????")
