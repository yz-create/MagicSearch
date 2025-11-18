# MagicSearch IT project 2A

Welcome in the promised land of trading card games players! By following these instructions, you will access our API where we gave our blood and tears to provide you with a diversity of searching tool !

## To access the app :
Install all modules in requirements.txt : 
- pip install -r requirements.txt 
Have the src folder as the root for executing files :
- In the .env : PYTHONPATH="/home/onyxia/work/MagicSearch/src"
- Then do : export PYTHONPATH=/home/onyxia/work/MagicSearch/src:$PYTHONPATH
Then, you need to export an api token to use the features using embeddings :
- Go on https://llm.lab.sspcloud.fr/ << Settings << Account << copy the API token
- Put in the terminal : export API_TOKEN= followed by the token you just copied
Go to the module src/app.py :
- Run this python file
- At the bottom right of your screen, you should have a pop-up giving you the option to "Open in Browser", click it
 
When you want to close the API make sure to write ctrl+c in your terminal !

## To reset the database in case of need :
Download AtomicCards.json on https://mtgjson.com/downloads/all-files/
Put it in the root repository
Run embed_batch.py as a main to obtain all embeddings of the cards in the database
Start reset_database.py as a main to reset the database

## To create all the cards embedding if necessary :
Execute embed_batch.py (takes approximately 30 minutes)

## To create a card using the API:
The only mandatory arguments are id_card (to create a card, just keep 0, a new one is gonna get created), layout, name and type_line.

If you want to keep an argument empty :
- If it's a string or a int, you can write it as None
- If it's a list, keep the list empty
- If it's a dict, keep the dict empty

If you look at the model that should be used to create or update a card, you might notice that some arguments either are of a dict type or a list of dict.
Those arguments are : "foreign_data", "leadership_skills", "legalities", "purchase_urls" and "rulings".
None of those arguments are mandatory, therefore, 
Since the columns in those dict are fixed, you need to make sure to use the correct ones, so here's the template for each of those:

"foreignData" is a list of dict.

"foreignData": [
    {
        "language": "string",      # Mandatory
        "name": "string",          # Mandatory
        "faceName": "string",
        "flavorText": "string",
        "text": "string",
        "type": "string"
    }
]

For "leadership_skills", all of its column are mandatory.

"leadership_skills": {
    "brawl": bool,
    "commander": bool,
    "oathbreaker": bool
}

For legality, for each column, you either put "Banned", "Restricted" or "Legal". None of the columns are mandatory.

"legalities": {
    "commander": "string",
    "oathbreaker": "string",
    "duel": "string",
    "legacy": "string",
    "vintage": "string",
    "modern": "string",
    "penny": "string",
    "timeless": "string",
    "brawl": "string",
    "historic": "string",
    "gladiator": "string",
    "pioneer": "string",
    "predh": "string",
    "paupercommander": "string",
    "pauper": "string",
    "premodern": "string",
    "future": "string",
    "standardbrawl": "string",
    "standard": "string",
    "alchemy": "string",
    "oldschool": "string"
}

For "purchase_urls", none of the columns are mandatory.

"purchase_urls": {
    "tcgplayer": "string",
    "cardKingdom": "string",
    "cardmarket": "string",
    "cardKingdomFoil": "string",
    "cardKingdomEtched": "string",
    "tcgplayerEtched": "string"
}

For "rulings", it is a list of dict and all columns are mandatory. In the date column, make sure to follow the "YYYY-MM-DD" format.

"rulings": [
    {
        "date": "YYYY-MM-DD",
        "text": "string"
    }
]

## To update a card using the API
The id_card you put is the card that is gonna get updated.
You need to still write everything you don't want to get changed. If you keep a column empty, the card will get updated to have no value in that column.
Otherwise, same rules as creating a card when it comes to the dict values.