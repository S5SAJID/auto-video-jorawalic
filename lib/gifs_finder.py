from main_classes.giphy_client import GiphyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = GiphyClient(api_key=os.getenv("GIPHY_API_KEY"))

def find_gifs(query: str):
  return client.search(q=query, limit=50)