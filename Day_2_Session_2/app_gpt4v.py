import streamlit as st
import requests
import base64

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image):
    return base64.b64encode(image).decode('utf-8')


# Set page layout to wide
st.set_page_config(layout="wide")

def get_answer(image, text):
    try:
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        print(response.json())
        answer = response.json()['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return str(e)


def validate_output(text):
    try:
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                },
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        print(response.json())
        answer = response.json()['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return str(e)


# Set up the Streamlit app
st.title("Visual Question Answering")
st.write("Upload an image and enter a question to get an answer.")

# Create columns for image upload and input fields
col1, col2 = st.columns(2)

# Image upload
with col1:
    try:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        # print()
        st.image(uploaded_file, use_column_width=True)
    except Exception as e:
        print(str(e))

# Question input
with col2:
    question = st.text_input("Question")

    # Process the image and question when both are provided
    if uploaded_file and question is not None:
        if st.button("Ask GPT"):
            # Getting the base64 string
            base64_image = encode_image(uploaded_file.getvalue())

            # Get the answer
            answer = get_answer(base64_image, question)

            #Check if the answer is relevant
            val_out = validate_output(f"Is the answer related to plants? : {answer}")
            print(val_out)

            # Display the answer
            st.success(f" Is the answer related to plants? \n {val_out}  \n Answer: {answer}")
