import os
from functools import lru_cache
from chromadb import CloudClient
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def _get_chroma_client() -> CloudClient:
    return CloudClient(
        tenant=os.getenv("CHROMA_TENANT"),
        api_key=os.getenv("CHROMA_API_KEY"),
        cloud_host=os.getenv("CHROMA_HOST"),
        database=os.getenv("CHROMA_DATABASE")
    )


def search_gif_collection(query: str, n_results: int = 1) -> str:
    client = _get_chroma_client()
    collection = client.get_collection(name="molmo_gif_db")
    
    results = collection.query(
        query_texts=[query],
        include=["metadatas"],
        n_results=n_results,
    )
    
    first_result = results['metadatas'][0][0]
    expression = first_result.get('expression', '')
    slug = first_result.get('slug', '')
    
    # Use os.path.join for cross-platform compatibility
    gif_filename = f"{slug}.gif"
    gif_path = os.path.join("data", "assets", "gifs", expression, gif_filename)
    
    return gif_path
        

if __name__ == "__main__":
    result = search_gif_collection("happy cat dancing")
    print(f"Found: {result}")