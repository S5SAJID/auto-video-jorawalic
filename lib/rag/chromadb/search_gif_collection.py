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
    
    logger.info(f"Searching GIF collection for: '{query}'")
    
    results = collection.query(
        query_texts=[query],
        include=["metadatas"],
        n_results=n_results,
    )
    
    # Validate results
    if not results or not results.get('metadatas') or not results['metadatas'][0]:
        logger.warning(f"No GIF found for query: '{query}'")
        raise ValueError(f"No matching GIF found for: {query}")
    
    first_result = results['metadatas'][0][0]
    expression = first_result.get('expression', '')
    slug = first_result.get('slug', '')
    
    if not expression or not slug:
        raise ValueError("Invalid metadata in search result")
    
    # Use os.path.join for cross-platform compatibility
    gif_filename = f"{slug}.gif"
    gif_path = os.path.join("data", "assets", "gifs", expression, gif_filename)
    
    # Verify file exists
    if not os.path.exists(gif_path):
        logger.error(f"GIF file not found at: {gif_path}")
        raise FileNotFoundError(f"GIF file not found: {gif_path}")
    
    logger.info(f"Found GIF: {gif_path}")
    return gif_path
        

if __name__ == "__main__":
    result = search_gif_collection("happy cat dancing")
    print(f"Found: {result}")