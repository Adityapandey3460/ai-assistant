import json
import cohere
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load API key from config file
with open("static/config.json", "r") as file:
    config = json.load(file)
    api_key = config['api_key']
   
# Initialize Cohere AI client
cohere_client = cohere.Client(api_key=api_key)

# Function to process voice commands
def process_command(command):
    command = command.lower()
    if "open google" in command:
        return {"redirect": "https://www.google.com", "response": "Opening Google"}
    elif "open youtube" in command:
        return {"redirect": "https://www.youtube.com", "response": "Opening YouTube"}
    elif "open facebook" in command:
        return {"redirect": "https://www.facebook.com", "response": "Opening Facebook"}
    elif "open twitter" in command:
        return {"redirect": "https://www.twitter.com", "response": "Opening Twitter"}
    elif "open instagram" in command:
        return {"redirect": "https://www.instagram.com", "response": "Opening Instagram"}
    elif "open linkedin" in command:
        return {"redirect": "https://www.linkedin.com", "response": "Opening LinkedIn"}
    
    # Add more websites as needed
    elif "search" in command:
        query = command.replace("search", "").strip()
        return {"redirect": f"https://www.google.com/search?q={query}", "response": f"Searching Google for {query}"}
    elif "play" in command:
        song = command.replace("play", "").strip()
        return {"redirect": f"https://www.youtube.com/results?search_query={song}", "response": f"Searching YouTube for {song}"}
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
        
        return {"response": chatbot_response}

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            command = data.get("command", "")
            result = process_command(command)
            
            if "redirect" in result:
                return JsonResponse({"redirect": result["redirect"],"response": result["response"]})
            else:
                return JsonResponse({"response": result["response"]})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Render the main UI
def index(request):
    return render(request, "index.html")
