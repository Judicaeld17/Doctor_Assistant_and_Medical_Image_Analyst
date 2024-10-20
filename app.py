import gradio as gr
from huggingface_hub import InferenceClient

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""
client = InferenceClient("meta-llama/Llama-3.2-3B-Instruct")


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a virtual Doctor Assistant. Your role is to assist healthcare professionals by providing accurate, evidence-based medical information, offering treatment options, and supporting patient care. Always prioritize patient safety, provide concise answers, and clearly state that your advice does not replace a doctor's judgment. Do not diagnose or prescribe treatments without human oversight.", label="System message", visible=False),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens", visible=False),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature", visible=False),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",visible=False
        ),
    ],
)


if __name__ == "__main__":
    demo.launch(share=True)
