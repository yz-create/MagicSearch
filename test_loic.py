import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []
c = 0

for i in data['data']:
    for card in data['data'][i]:
        if "foreignData" in card:
            for url in card['foreignData']:
                c += 1


print(Counter(count))

for i in None:
    print("a")

print("b")


    def get_embedding(self, text: str) -> np.ndarray:
        """
        Embeds a text

        Parameters:
        -----------
        text: str
            The text to be embeded

        Returns:
        --------
        numpy.ndarray
            Returns the embed of the card as a vector
        """
        token = os.getenv("API_TOKEN")
        url = "https://llm.lab.sspcloud.fr/ollama/api/embed"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-type": "application/json"}

        data = {
            "model": "bge-m3:latest",
            "input": text
        }
        response = requests.post(url, headers=headers, json=data)
        return np.array(response.json()['embeddings'][0])