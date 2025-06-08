# az_openai.py
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file if they are not already set
load_dotenv()

# Set up Azure OpenAI Service credentials
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4o")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

# Print the OpenAI environment variables at startup
print(f"OpenAI Endpoint: {openai_endpoint}")
print(f"OpenAI Model Name: {openai_model_name}")
print(f"OpenAI API Version: {openai_api_version}")

def create_azure_openai_client():
    return AzureOpenAI(azure_endpoint=openai_endpoint,
                       api_version=openai_api_version,
                       api_key=openai_api_key)

def message_azure_openai_model(input_text):
    system_prompt = "You are a helpful assistant."
    response = client.chat.completions.create(
        model=openai_model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
    )
    return response.choices[0].message.content

# Create Azure OpenAI client
client = create_azure_openai_client()