import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"


def generate_answer_with_ollama(question: str, context: str):
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": """
                  Eres un asistente académico.

                  Responde únicamente usando el contexto proporcionado.
                  Si la respuesta no aparece en el contexto, responde:
                  "No encontré esa información en el documento."

                  Incluye citas usando el formato [Página X].
                  No inventes información.
                """
            },
            {
              "role": "user",
              "content": f"""
              Contexto del documento:

              {context}

              Pregunta del usuario:

              {question}
              """
            }
        ]
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]