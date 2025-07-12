import gradio as gr
import requests, os

from dotenv import load_dotenv
load_dotenv()

ROOT_URL = os.getenv("ROOT_URL")
ANONYM_URL = f"{ROOT_URL}/anonym/anonymize?with_entity_ids=true"
DEANONYM_URL = f"{ROOT_URL}/anonym/desanonymize"



def anonymize(text):
    try:
        response = requests.post(ANONYM_URL, json={"text": text})
        data = response.json()
        anonymized = data.get("anonymized_text", "")
        entities = data.get("entity_ids", {})
        formatted = "\n".join([f"{entity} → {label}" for entity, label in entities.items()])
        return anonymized, entities, formatted
    except Exception as e:
        return f"Erreur : {e}", {}, ""

def desanonymize(text):
    try:
        response = requests.post(DEANONYM_URL, json={"text": text})
        data = response.json()
        return data.get("text", text)
    except Exception as e:
        return f"Erreur de désanonymisation : {e}"


def process_message(message, history):
    anonymized, entities, formatted = anonymize(message)

    llm_response = f"Réponse désanonymisé: {anonymized}"

   
    deanonymized = desanonymize(llm_response)

    history = history or []
    history.append((message, deanonymized))

    side_text = (
        f"### Texte anonymisé\n{anonymized}\n\n"
        f"### Entités détectées\n{formatted}\n\n"
        f"### Texte désanonymisé\n{deanonymized}"
    )

    return history, history, side_text


example_texts = [
    "Bonjour, je m'appelle Florent et j'habite Toulouse.",
    "Je travaille chez ValSoftware depuis 2021.",
    "Mon numéro de téléphone est le 01 23 45 67 89.",
]


with gr.Blocks(title="Chatbot Anonymiseur") as gradio_ui:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Exemples")
            example_box = gr.Textbox(visible=False)
            for example in example_texts:
                btn = gr.Button(example)
                btn.click(lambda ex=example: ex, outputs=example_box)

        with gr.Column(scale=2):
            gr.Markdown("## Chatbot")
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(label="Votre message")
            send_btn = gr.Button("Envoyer")
            state = gr.State([])
            example_box.change(None, example_box, user_input, js="(i) => i")

        with gr.Column(scale=1):
            gr.Markdown("## Anonymisation")
            side_info = gr.Markdown()

    send_btn.click(
        process_message,
        [user_input, state],
        [chatbot, state, side_info],
    )

    send_btn.click(None, None, user_input, js="() => ''")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    gradio_ui.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )