import json
import webbrowser
import pyttsx3
from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load API key from config file
with open("D:\\Django\\New_Project\\ai_assistant\\static\\config.json", "r") as file:
    config = json.load(file)
    api_key = config['api_key']

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepinfra.com/v1/openai",
)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to process voice commands
def process_command(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "relax" in command:
        return "Okay, I'm going to relax now."
    elif "search" in command:
        query = command.replace("search", "").strip()
        
        known_websites = {
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
        }
        
        if query in known_websites:
            webbrowser.open(known_websites[query])
            return f"Opening {query}."
        else:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for {query}."
    
    elif "play" in command:
        song = command.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return f"Searching YouTube for {song}."
    
    else:
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": command}]
        
        chat_completion = openai_client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages,
        )
        
        chatbot_response = chat_completion.choices[0].message.content
        return chatbot_response

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        data = json.loads(request.body)
        command = data.get("command", "")
        response = process_command(command)
        return JsonResponse({"response": response})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Render the main UI
def index(request):
    return render(request, "index.html")
