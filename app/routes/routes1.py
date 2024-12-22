from ..app import app
from flask import Flask, render_template, request
import requests

@app.route("/retrieve_wikidata/<id>")
def retrieve_wikidata(id):
    # Construire l'URL de l'API Wikidata
    wikidata_url = f"https://www.wikidata.org/wiki/Special:EntityData/{id}.json"

    try:
        # Faire une requête à l'API Wikidata
        response = requests.get(wikidata_url)
        response.raise_for_status()  # Vérifie si le code HTTP est une erreur

        # Décoder la réponse JSON
        json_data = response.json()

        # Extraire les données
        entity_data = json_data.get("entities", {}).get(id, None)

        if entity_data:
            #Renvoyer les données trouvées
            return render_template(
            "wikidata.html", 
            id=id,
            status_code=response.status_code,  # Code HTTP
            content_type=response.headers.get('Content-Type'),  # Type de contenu
            entity_data=entity_data,  # Données de l'entité
            error_message=None  # Message d'erreur non nécessaire
            )

    except :
        # Gérer les erreurs de requête avec les entités inconnues
        return render_template(
            "wikidata.html", 
            id=id,
            status_code=response.status_code,  # Code HTTP
            content_type=response.headers.get('Content-Type'),  # Type de contenu
            entity_data=None,  # Données de l'entité
            error_message=f"Aucune donnée valide n'a été retournée pour l'ID {id}."  # Message d'erreur
            )
