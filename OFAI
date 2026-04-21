import argparse
import json
import re
import urllib.parse
import urllib.request
import gradio as gr

LOGO_URL = "https://raw.githubusercontent.com/bizancio11/ort_friends/main/Hacknet.bmp"


def resolver_pregunta_matematica(sentence):
    sentence = sentence.lower().strip()
    match = re.search(r"(?:cu(á|a)nto(?: es)?|qu[eé] es|calcul[aá])(.*)", sentence)
    if not match:
        return None

    expr = match.group(2)
    expr = expr.replace("por", "*").replace("multiplicado por", "*")
    expr = expr.replace("x", "*").replace("\u00f1", "n")
    expr = expr.replace("dividido entre", "/").replace("entre", "/")
    expr = expr.replace("mas", "+").replace("más", "+")
    expr = expr.replace("menos", "-")
    expr = re.sub(r"[^0-9+\-*/(). ]", "", expr)

    if not re.search(r"[0-9]", expr):
        return None

    try:
        resultado = eval(expr, {"__builtins__": None}, {})
    except Exception:
        return None

    if isinstance(resultado, float) and resultado.is_integer():
        resultado = int(resultado)

    return f"{resultado}"


def buscar_internet(query):
    query = query.strip()
    if not query:
        return None

    url = (
        "https://api.duckduckgo.com/?"
        + urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        })
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    if data.get("AbstractText"):
        return data["AbstractText"]

    related_topics = data.get("RelatedTopics", [])
    for item in related_topics:
        if isinstance(item, dict) and item.get("Text"):
            return item["Text"]
        if isinstance(item, dict) and "Topics" in item:
            for subitem in item["Topics"]:
                if isinstance(subitem, dict) and subitem.get("Text"):
                    return subitem["Text"]

    return None


def chatbot_response(message):
    logo_html = f'<img src="{LOGO_URL}" width="50" height="50" alt="Logo" style="display: block; margin-bottom: 10px;">'
    
    if message is None:
        return f"{logo_html}<div style='font-size: 16px;'>No ingresaste ningún mensaje.</div>"

    math_answer = resolver_pregunta_matematica(message)
    if math_answer is not None:
        return f"{logo_html}<div style='font-size: 16px;'>{math_answer}</div>"

    search_answer = buscar_internet(message)
    if search_answer:
        return f"{logo_html}<div style='font-size: 16px;'>{search_answer}</div>"

    return f"{logo_html}<div style='font-size: 16px;'>Lo siento, no entiendo. ¿Puedes decirlo de otra forma?</div>"


def main():
    parser = argparse.ArgumentParser(description="Chatbot que busca respuestas en internet.")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo consola en lugar de Gradio")
    args = parser.parse_args()

    if args.cli:
        print("\n¡Bot listo! (escribe 'salir' para finalizar)")
        while True:
            message = input("Tú: ")
            if message.strip().lower() == "salir":
                print("Bot: ¡Hasta pronto!")
                break

            math_answer = resolver_pregunta_matematica(message)
            if math_answer is not None:
                print(f"Bot: {math_answer}")
                continue

            search_answer = buscar_internet(message)
            if search_answer:
                print(f"Bot: {search_answer}")
            else:
                print("Bot: Lo siento, no entiendo. ¿Puedes decirlo de otra forma?")
        return
        
    demo = gr.Interface(
        fn=chatbot_response,
        inputs=gr.Textbox(label="Escribe tu mensaje aquí"),
        outputs=gr.Markdown(label="Respuesta del Bot"),
        title="OFAI - Asistente Virtual",
        description="Hola, soy OFAI, tu asistente virtual. Puedo responder preguntas matemáticas y buscar información en internet. ¡Pruébame!",
    )

    demo.launch(share=True, inbrowser=True)


if __name__ == "__main__":
    main()
