import serpapi
import gradio as gr
LOGO_URL = "https:///github/bizancio11/ort_friends/main/Hacknet.bmp"
def main(results):
    busqueda = gr.Textbox()
    client = serpapi.Client(api_key="secret_api_key")
    results = client.search({
    "q": f"{busqueda}",
    "location": "Buenos Aires, Argentina",
    "hl": "es",
    "gl": "ar",
    "google_domain": "google.com"
    })
    print(results)

demo = gr.Interface(
    fn = main,
    busqueda = gr.Textbox(),
    respuesta = gr.Markdown(f"{gr.Image(LOGO_URL)}Bot: {results}")
    
)

