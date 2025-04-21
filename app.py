import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/anonym/anonymize?with_entity_ids=true"

def appeler_api(text):
    try:
        response = requests.post(API_URL, json={"text": text})
        data = response.json()
        anonymized = data.get("anonymized_text", "")
        entities = data.get("entity_ids", {})
        formatted = "\n".join([f"{entity} → {label}" for entity, label in entities.items()])
        return anonymized, formatted
    except Exception as e:
        return f"Erreur : {e}", ""

gradio_ui = gr.Interface(
    fn=appeler_api,
    inputs=gr.Textbox(lines=8, label="Texte à anonymiser"),
    outputs=[gr.Textbox(lines=8, label="Texte anonymisé"),
             gr.Textbox(lines=6, label="Entités détectées")],
    title="Anonymiseur de texte",
    description="Utilise l'API interne pour anonymiser un texte et détecter les entités."
)

gradio_ui.launch(server_port=8080, server_name="0.0.0.0")
