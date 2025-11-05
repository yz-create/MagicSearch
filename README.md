# MagicSearch
Projet info 2A 

## To use the app :
Install all modules in requirements.txt : 
- pip install -r requirements.txt 
Have the src folder as the root for executing files :
- In the .env : PYTHONPATH="/home/onyxia/work/MagicSearch/src"
- Then do : export PYTHONPATH=/home/onyxia/work/MagicSearch/src:$PYTHONPATH

## To reset the database in case of need :
Download AtomicCards.json on https://mtgjson.com/downloads/all-files/
Put it in the root repository
Start reset_database.py as a main to reset the database

## To access the embed :
Go on https://llm.lab.sspcloud.fr/ << Réglages << Compte << copier la clé d'API
Put in the terminal : API_TOKEN= followed by the token you just copied