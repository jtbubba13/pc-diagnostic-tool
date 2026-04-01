# core/ai_recommender.py
import requests

def generate_recommendations(issues):
    summaries = []

    for issue in issues:
        prompt = f"""
        Issue: {issue['type']}
        Details: {issue['details']}

        Provide a short, simple fix recommendation.
        """

        # Replace with OpenAI or other LLM later
        response = requests.post(
            "http://localhost:11434/api/generate",  # Example: local LLM (Ollama)
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        try:
            summaries.append(response.json()["response"])
        finally:
            summaries.append("No recommendation available.")

    return summaries