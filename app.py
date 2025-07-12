import os, gradio as gr

def echo(x): return x

demo = gr.Interface(fn=echo, inputs="text", outputs="text")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    demo.launch(server_name="0.0.0.0", server_port=port, share=False)
