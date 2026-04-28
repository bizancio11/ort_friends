import argparse
import json
import re
import urllib.parse
import urllib.request
import gradio as gr


# Uso


LOGO_URL = "https://raw.githubusercontent.com/bizancio11/ort_friends/main/Hacknet.bmp"

def resolver_pregunta_matematica(sentence):
    sentence = sentence.lower().strip()
    match = re.search(r"(?:cu(á|a)nto(?: es)?|qu[eé] es|calcul[aá])(.*)", sentence)
    if not match: return None
    
    expr = match.group(2)
    replacements = {
        "por": "*", "multiplicado por": "*", "x": "*", 
        "dividido entre": "/", "entre": "/", "mas": "+", 
        "más": "+", "menos": "-"
    }
    for word, symbol in replacements.items():
        expr = expr.replace(word, symbol)
    
    expr = re.sub(r"[^0-9+\-*/(). ]", "", expr)
    if not re.search(r"[0-9]", expr): return None
    
    try:
        resultado = eval(expr, {"__builtins__": None}, {})
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)
        return f"El resultado es: {resultado}"
    except:
        return None

def buscar_internet(query):
    query = query.strip()
    if not query: return None
    
    # API de DuckDuckGo con parámetros optimizados
    params = urllib.parse.urlencode({
        "q": query,
        "lenguage": "spanish",
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
        "no_redirect": 1
    })
    url = f"https://api.duckduckgo.com/?{params}"
    
    try:
        # Añadimos un User-Agent para simular un navegador real
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            # 1. Prioridad: Texto abstracto principal
            if data.get("AbstractText"):
                return data["AbstractText"]
            
            # 2. Prioridad: Respuesta rápida (Answer)
            if data.get("Answer"):
                return data["Answer"]
            
            # 3. Prioridad: Temas relacionados (primer resultado relevante)
    except Exception as e:
        return f"Connection Error: {str(e)}"

def chatbot_response(message):
    logo_html = f'<img src="{LOGO_URL}" width="50" height="50" style="margin-bottom: 10px;">'
    if not message:
        return f"{logo_html}<div>Please, Write something.</div>"
    
    # Intentar matemáticas primero
    res = resolver_pregunta_matematica(message)
    if res:
        return f"{logo_html}<div style='font-size: 16px;'><b>Rocky:</b> {res}</div>"
    
    # Buscar en la web
    res = buscar_internet(message)
    if res:
        return f"{logo_html}<div style='font-size: 16px;'><b>Rocky:</b> {res}</div>"
    
    return f"{logo_html}<div>Sorry, I don´t founnd information.</div>"

# --- Interfaz Gradio ---
demo = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Textbox(label="Tu:"),
    outputs=gr.Markdown(),
    title="Rocky - Asistente Virtual Pro"
    
)

if __name__ == "__main__":
    demo.launch(share=True)
