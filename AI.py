from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
ROBOT_ID = os.getenv("ROBOT_ID")

if not API_KEY or not ROBOT_ID:
    raise RuntimeError("Missing API_KEY or ROBOT_ID in .env")

def fetch_browseai_data():
    url = f"https://api.browse.ai/v2/robots/{ROBOT_ID}/tasks"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_text(data):
    """
    Extracts readable text from Browse AI task output.
    Adjust this if your robot structure differs.
    """
    texts = []

    result = data.get("result", {})
    tasks = result.get("robotTasks") or result.get("tasks") or []

    for task in tasks:
        for key, value in task.items():
            if isinstance(value, str):
                texts.append(value)
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, str):
                        texts.append(v)
            elif isinstance(value, dict):
                for v in value.values():
                    if isinstance(v, str):
                        texts.append(v)

    return "\n".join(texts)

def answer_prompt(prompt, context):
    """
    Very simple local reasoning over scraped context.
    Replace this with an actual LLM call if desired.
    """
    if not context.strip():
        return "No data available from Browse AI."

    # Naive example: return context snippet + prompt
    return f"Prompt: {prompt}\n\nContext:\n{context[:2000]}"

def main():
    print("Fetching Browse AI data...")
    data = fetch_browseai_data()
    context = extract_text(data)

    print("Ready. Enter a prompt (Ctrl+C to exit):")
    while True:
        prompt = input("\n> ")
        if not prompt.strip():
            continue

        response = answer_prompt(prompt, context)
        print("\n--- Response ---")
        print(response)
        print("----------------")

if __name__ == "__main__":
    main()
