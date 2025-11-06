# MagicSearch IT project 2A

Welcome in the promised land for players of trading card games ! By following these instructions, you will access our API where we gave our blood and tears to provide you with a diversity of searching tool !

## To access the app :
Install all modules in requirements.txt : 
- pip install -r requirements.txt 
Have the src folder as the root for executing files :
- In the .env : PYTHONPATH="/home/onyxia/work/MagicSearch/src"
- Then do : export PYTHONPATH=/home/onyxia/work/MagicSearch/src:$PYTHONPATH
Go to the module src/app.py :
- Run this python file
- At the bottom right of your screen, you should have a pop-up giving you the option to "Open in Browser", click it
 
When you want to close the API make sure to right ctrl+c in your terminal !

## To reset the database in case of need :
Download AtomicCards.json on https://mtgjson.com/downloads/all-files/
Put it in the root repository
Start reset_database.py as a main to reset the database

## To create all the cards embedding if necessary :
Execute embed_batch.py (takes approximately 30 minutes)

## To access the embed (this has to be done before starting the API):
Go on https://llm.lab.sspcloud.fr/ << Settings << Account << copy the API token
Put in the terminal : export API_TOKEN= followed by the token you just copied