import gradio as gr
import openai
import time
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Setting up API keys from the .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            video_html = '<div style="display: flex; justify-content: center; align-items: center;">' \
                         '<video autoplay controls height="360" width="480">' \
                         '<source src="VIDEO URL HERE" type="video/webm">' \
                         '</video>' \
                         '</div>'
            gr.HTML(video_html)
        with gr.Column():
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(label="Enter your message:")  # Changed the label
            
            # Create a row for buttons
            with gr.Row():
                clear = gr.Button("Clear")

            messages = ["You are an advisor. Please respond to all input in 50 words or less."]

            def user(user_message, history):
                messages.append(f"\nUser: {user_message}")
                return "", history + [[user_message, None]]

            def bot(history):
                # Generating a response using OpenAI GPT
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=messages[-1],
                    max_tokens=80,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                bot_message = response["choices"][0]["text"]
                messages.append(f"System: {bot_message}")
                history[-1][1] = ""
                for character in bot_message:
                    history[-1][1] += character
                    time.sleep(0.05)
                    yield history

            user_input.submit(user, [user_input, chatbot], [user_input, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )

demo.queue()
demo.launch()
