import os
import json
import serpapi
import gradio as gr

LOGO_URL = "https://raw.githubusercontent.com/bizancio11/ort_friends/main/Hacknet.bmp"


def main(busqueda: str) -> str:
    if not busqueda:
        return "Por favor ingresa una consulta de búsqueda."

    api_key = os.environ.get("SERPAPI_KEY", "secret_api_key")
    client = serpapi.Client(api_key=api_key)
    params = {
        "q": busqueda,
        "location": "Buenos Aires, Argentina",
        "hl": "es",
        "gl": "ar",
        "google_domain": "google.com",
    }

    try:
        results = client.search(params)
    except Exception as error:
        return f"Error al buscar: {error}"

    organic_results = results.get("organic_results")
    if not organic_results:
        return "No se encontraron resultados."

    formatted = [
        f"### Resultado {idx + 1}\n**{item.get('title', 'Sin título')}**\n{item.get('snippet', '')}\n[{item.get('link', '')}]({item.get('link', '')})"
        for idx, item in enumerate(organic_results[:5])
    ]
    return "\n\n".join(formatted)


demo = gr.Interface(
    fn=main,
    inputs=gr.Textbox(label="Consulta de búsqueda"),
    outputs=gr.Markdown(label="Resultados"),
    title="Buscador SerpApi",
    description="Busca en Google usando SerpApi y muestra los resultados orgánicos.",
)

if __name__ == "__main__":
    demo.launch()

