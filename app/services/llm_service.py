import json
import re
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


def extract_json_array(text: str):
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        raise ValueError("El modelo no devolvió un arreglo JSON válido.")

    return json.loads(match.group(0))


def generate_flashcards_with_ollama(
    context: str,
    total: int = 10
):
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": """
Eres un asistente académico experto en crear flashcards.

Genera flashcards únicamente con la información del contexto.
No inventes información.

Devuelve exclusivamente un JSON válido.
No agregues texto antes ni después.

Formato exacto:

[
  {
    "question": "Pregunta clara y breve",
    "answer": "Respuesta clara y útil"
  }
]
"""
            },
            {
                "role": "user",
                "content": f"""
Contexto del documento:

{context}

Genera {total} flashcards para estudiar este documento.
"""
            }
        ]
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()
    raw_content = data["message"]["content"]

    flashcards = extract_json_array(raw_content)

    clean_flashcards = []

    for item in flashcards:
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()

        if question and answer:
            clean_flashcards.append({
                "question": question,
                "answer": answer
            })

    if len(clean_flashcards) == 0:
        raise ValueError("No se pudieron generar flashcards válidas.")

    return clean_flashcards