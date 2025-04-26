import requests
import json

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "ecommerce-ner-model:latest"

def ner_query(query):
    """
    Send a NER extraction prompt to the Ollama API and return the JSON result.
    """
    prompt = (
        f"[NER] Extract entities:\n{query}"
    )
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    # Parse the JSON inside the "completion" field if that's how Ollama wraps it:
    data = response.json()
    try:
        return json.loads(data.get("completion", data.get("response", "{}")))
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw": data}

def main():
    # List your queries here:
    queries = [
        "Red t-shirt chest size 42",
        "Nike running shoe size 9 color black price < 100",
        "blue jeans waist 32 color blue",
        "men's black hoodie medium",
        # Add more queries as needed
    ]
    for q in queries:
        print(f"\nQuery: {q}")
        result = ner_query(q)
        print("NER Output:", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

