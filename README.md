# MagicSearch IT project 2A

Welcome in the promised land of trading card games players! By following these instructions, you will access our API where we gave our blood and tears to provide you with a diversity of searching tools !

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

## To do a filtered search using the API
The input is a list of "filter" objects, with the following format :
{
    "variable_filtered": "string",
    "type_of_filtering": "string",
    "filtering_value": "string" or int
}

"variable_filtered" is the variable on which we apply the filter
"type_of_filtering" is the way we want to apply the filter
"filtering_value" is a value around which the filter operates

The point of the input being a list of filters is that filters can be cumulative, by listing filters you get a more precise fit to your requirements (see the example).

### Categorical filter
"variable_filtered" : str
    The filter can be applied only to the following list of categorical variables :
    -"type"
    -"color"

"type_of_filtering" : str
    A filter on categorical variables can be applied in only two ways :
    -"positive" : we select all the cards that have the "filtering_value" in the "variable_filtered"
    -"negative" : we select all the cards EXCEPT the ones that have the "filtering_value" in the "variable_filtered"

"filtering_value" :str
    Could be anything but, for your information: 
    -the variable "type" mostly has the modalities "Land", "Creature", "Enchantment", "Artifact", "Sorcerie", "Instant", "Interrupt" and "Planeswalker"
    -the variable "color" mostly refers to "B" (black), "U" (blue), "R" (red), "W" (white), "G" (green)

### Numerical filter
"variable_filtered" : str
    The filter can be applied only to the following list of numerical variables :
    -"power"
    -"toughness"
    -"manaValue"
    -"edhecRank"

"type_of_filtering" : str
    A filter on categorical variables can be applied in only two ways :
    -"higher_than" : we select all the cards that have a value in their "variable_filtered" higher than the "filtering_value"
    -"equal_to": same idea
    -"lower_than" : ditto

"filtering_value" :int
    Could be anything.

### An enlightening example

If you wish to find a card that has a high edhecRank (higher than 1000) and that has also a fairly low manaValue (equal to 1) but that's not all ! This card just HAS to be a creature and be anything but blue !
 
Your input would be :
[
  {
    "variable_filtered": "edhecRank",
    "type_of_filtering": "higher_than",
    "filtering_value": 1000
  }, 
  {
    "variable_filtered": "power",
    "type_of_filtering": "equal_to",
    "filtering_value": 1
  }, 
  {
    "variable_filtered": "type",
    "type_of_filtering": "positive",
    "filtering_value": "Creature"
  }, 
  {
    "variable_filtered": "colour",
    "type_of_filtering": "negative",
    "filtering_value": "U"
  }
]