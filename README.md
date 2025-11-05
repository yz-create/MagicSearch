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

## To create all the cards embedding if necessary :
Execute embed.py

## To access the embed (this has to be done before starting the API):
Go on https://llm.lab.sspcloud.fr/ << Settings << Account << copy the API token
Put in the terminal : export API_TOKEN= followed by the token you just copied