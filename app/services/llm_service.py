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


def generate_infographic_cards_with_ollama(
    context: str,
    total: int = 6
):
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": """
                    Eres un asistente académico experto en crear infografías educativas.

                    Tu tarea es convertir el contenido del documento en tarjetas informativas tipo infografía.

                    No hagas preguntas.
                    No generes formato de flashcards pregunta/respuesta.
                    No inventes información.
                    Usa únicamente la información del contexto.

                    Devuelve exclusivamente un JSON válido.
                    No agregues texto antes ni después.

                    Formato exacto:

                    [
                    {
                        "title": "Título corto del concepto",
                        "description": "Explicación breve y clara del concepto.",
                        "points": [
                        "Punto clave 1",
                        "Punto clave 2",
                        "Punto clave 3"
                        ]
                    }
                    ]
            """
            },
            {
                "role": "user",
                "content": f"""
                Contexto del documento:

                {context}

                Genera {total} tarjetas informativas tipo infografía.
                Cada tarjeta debe resumir un concepto importante del documento.
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

    cards = extract_json_array(raw_content)

    clean_cards = []

    for item in cards:
        title = str(item.get("title", "")).strip()
        description = str(item.get("description", "")).strip()
        points = item.get("points", [])

        if not isinstance(points, list):
            points = []

        clean_points = [
            str(point).strip()
            for point in points
            if str(point).strip()
        ]

        if title and description and len(clean_points) >= 2:
            clean_cards.append({
                "title": title,
                "description": description,
                "points": clean_points
            })

    if len(clean_cards) == 0:
        raise ValueError("No se pudieron generar tarjetas informativas válidas.")

    return clean_cards