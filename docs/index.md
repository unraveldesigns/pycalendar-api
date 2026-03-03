# Calendar API

<figure markdown="span">
    ![Calendar API Logo](assets/img/logo.webp){ width="350" }
  <figcaption>JSON API du Calendrier Marocain</figcaption>
</figure>

[![Latest Release](https://gitlab.com/ud-labs/py-calendar-api/-/badges/release.svg)](https://gitlab.com/ud-labs/py-calendar-api/-/releases)
[![pipeline status](https://gitlab.com/ud-labs/py-calendar-api/badges/main/pipeline.svg)](https://gitlab.com/ud-labs/py-calendar-api/-/commits/main)

## Présentation

Généralement les décisions d'investissement commencent par une analyse de plusieurs informations,
sur différentes périodes, pour différents instruments financiers et indices de références.
 
## Le client - SDK

Notre client est une librairie (sdk) qui simplifie l'intégration du service `Calendar API` dans les applications Python via une interface simple et intuitive.
Pour y parvenir, nous avons évité de faire un mapping 1:1 entre les services (endpoints/operations) de Calendar API et l'interface du client pycalendar_api.

Le client offre les avantages suivants:

- Construction des réponses Json en objets Python - _désérialisation_ -
- Objets basés sur les **dataclasses** (librairie standarde)
- Utilise **HTTPX** pour les requêtes http
- Configuration avancée via fichier `.toml` (timeout, proxy)
- Dépendances minimales

## Fonctionnalités


## Continuer à explorer

<div class="grid cards" markdown>

</div>

<script defer src="https://odometer.calendar-api.ma/script.js" data-website-id="3b3a9e56-7e3a-4c20-b6b4-fce013629789" data-tag="docs"></script>
