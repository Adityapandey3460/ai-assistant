import json
import webbrowser
import cohere
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load API key from config file
with open("static\config.json", "r") as file:
    config = json.load(file)
    # api_key = config['api_key']
    api_key="6IgJF11748bKzPEcswK2ZZN3mXerGUcaaK971klb"  # Replace with your API key

# Initialize Cohere AI client
cohere_client = cohere.Client(api_key=api_key)

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
        
        try:
            response = cohere_client.chat(
                model='c4ai-aya-expanse-32b',
                message=command,
                temperature=0.3,
                prompt_truncation='AUTO'
            )
            chatbot_response = response.text
        except Exception as e:
            chatbot_response = f"API Error: {e}"
        
        return chatbot_response

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            command = data.get("command", "")
            response = process_command(command)
            return JsonResponse({"response": response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Render the main UI
def index(request):
    return render(request, "index.html")
