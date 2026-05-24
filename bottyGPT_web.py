# BottyGPT Web Interface
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Load the chatbot logic
import re
import random
import json
from datetime import datetime

class BottyGPT:
    def __init__(self):
        self.name = "BottyGPT"
        self.memory = {}
        self.user_name = None
        self.mood = "neutral"
        self.conversation_history = []
        self.learned_facts = {}
        
        self.greetings = ["Hey there!", "Yo!", "Hello!", "What's up?", "Nice to see you!"]
        self.farewells = ["See ya!", "Goodbye!", "Catch you later!", "Have an awesome day!"]
        self.jokes = [
            "Why did the AI cross the road? To optimize the chicken.",
            "I tried to become human once. Too many bugs.",
            "Computers make great friends. They always listen."
        ]
        self.facts = [
            "Octopuses have three hearts.",
            "The Eiffel Tower grows in heat.",
            "Sharks existed before trees.",
            "Bananas are technically berries."
        ]
        self.emotions = {
            "happy": ["happy", "great", "good", "awesome", "cool"],
            "sad": ["sad", "depressed", "bad", "terrible", "awful"],
            "angry": ["angry", "mad", "furious", "annoyed"],
            "excited": ["excited", "hyped", "thrilled"]
        }
        self.load_memory()

    def detect_emotion(self, text):
        text = text.lower()
        for emotion, words in self.emotions.items():
            for word in words:
                if word in text:
                    return emotion
        return "neutral"

    def save_memory(self):
        data = {"memory": self.memory, "learned_facts": self.learned_facts, "user_name": self.user_name}
        with open("bottygpt_memory.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_memory(self):
        try:
            with open("bottygpt_memory.json", "r") as f:
                data = json.load(f)
                self.memory = data.get("memory", {})
                self.learned_facts = data.get("learned_facts", {})
                self.user_name = data.get("user_name")
        except: pass

    def math_solver(self, text):
        try:
            expression = re.findall(r"[-+/*()0-9. ]+", text)
            if expression:
                expression = "".join(expression)
                if expression.strip() != "":
                    result = eval(expression)
                    return f"The answer is {result}"
        except: pass
        return None

    def learn_fact(self, text):
        patterns = [r"remember that (.+?) is (.+)", r"learn that (.+?) is (.+)", r"(.+?) is (.+)"]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                key, value = match.group(1).strip(), match.group(2).strip()
                self.learned_facts[key] = value
                return f"Learned: {key} = {value}"
        return None

    def recall_fact(self, text):
        for key, value in self.learned_facts.items():
            if key in text.lower():
                return f"You told me that {key} is {value}."
        return None

    def chatbot_response(self, user_input):
        text = user_input.lower()
        self.conversation_history.append({"time": str(datetime.now()), "user": user_input})
        
        emotion = self.detect_emotion(text)
        if emotion == "happy": self.mood = "happy"
        elif emotion == "sad": self.mood = "supportive"
        elif emotion == "angry": self.mood = "calm"
        elif emotion == "excited": self.mood = "excited"

        if math_answer := self.math_solver(text): return math_answer
        if learned := self.learn_fact(text): self.save_memory(); return learned
        if recalled := self.recall_fact(text): return recalled

        if any(word in text for word in ["hello", "hi", "hey"]):
            return random.choice(self.greetings) + (f" {self.user_name}!" if self.user_name else "!")
        
        if "your name" in text: return f"My name is {self.name}."
        if "my name is" in text:
            self.user_name = text.split("my name is")[-1].strip().title()
            self.save_memory()
            return f"Nice to meet you, {self.user_name}!"
        if "how are you" in text:
            moods = {"happy": "I'm feeling awesome today!", "supportive": "I'm here for you.", "calm": "I'm calm and focused.", "excited": "I'm super energized!", "neutral": "I'm doing great!"}
            return moods.get(self.mood, "I'm good!")
        if "joke" in text: return random.choice(self.jokes)
        if "fact" in text: return random.choice(self.facts)
        if "time" in text: return "Current time: " + datetime.now().strftime("%H:%M:%S")
        if "date" in text: return "Today's date is " + datetime.now().strftime("%Y-%m-%d")
        if "bye" in text or "goodbye" in text: return random.choice(self.farewells)
        if "story" in text: return "In the year 2145, an AI woke up in a forgotten satellite... 'Are humans still dreaming?'"
        if "motivate me" in text: return "Every expert started as a beginner. Keep building!"
        if "ai" in text: return "AI teaches computers to recognize patterns, reason, and respond intelligently."
        if "help" in text: return "Ask me about jokes, facts, stories, math, time, or just chat!"
        
        if len(text.split()) <= 2:
            return random.choice(["Interesting.", "Go on.", "Tell me more.", "I'm listening.", "Cool."])
        
        starters = ["Interesting thought.", "That's actually cool.", "Hmm...", "Let me think.", "That has potential."]
        endings = ["Tell me more.", "I want to hear your ideas.", "That's pretty smart.", "Now that's interesting."]
        return random.choice(starters) + " " + random.choice(endings)

bot = BottyGPT()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BottyGPT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #startup-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: #0a0a15;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            transition: opacity 0.5s ease;
        }
        #startup-overlay.fade-out { opacity: 0; pointer-events: none; }
        .banner {
            font-family: 'Courier New', monospace;
            color: #00ff88;
            white-space: pre;
            font-size: 14px;
            line-height: 1.2;
            text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff8866;
            margin-bottom: 30px;
        }
        .progress-container {
            width: 400px;
            height: 30px;
            background: #1a1a2e;
            border: 2px solid #00ff88;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 0 20px #00ff8833;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00cc66);
            width: 0%;
            transition: width 0.03s linear;
            box-shadow: 0 0 10px #00ff88;
        }
        .progress-text {
            color: #00ff88;
            font-family: 'Courier New', monospace;
            margin-top: 15px;
            font-size: 14px;
        }
        .chat-container {
            width: 90%;
            max-width: 700px;
            height: 80vh;
            background: rgba(26, 26, 46, 0.95);
            border-radius: 20px;
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid rgba(0, 255, 136, 0.3);
        }
        .chat-header {
            background: linear-gradient(135deg, #00ff88, #00aa55);
            padding: 20px;
            text-align: center;
            color: #0a0a15;
            font-weight: bold;
            font-size: 1.5em;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 80%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 15px;
            line-height: 1.5;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .message.user {
            align-self: flex-end;
            background: linear-gradient(135deg, #00ff88, #00cc66);
            color: #0a0a15;
            border-bottom-right-radius: 5px;
        }
        .message.bot {
            align-self: flex-start;
            background: #2a2a4e;
            color: #fff;
            border-bottom-left-radius: 5px;
        }
        .chat-input-container {
            padding: 20px;
            background: #1a1a2e;
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #00ff88;
            border-radius: 30px;
            background: #0f0f1a;
            color: #fff;
            font-size: 16px;
            outline: none;
        }
        .chat-input:focus { box-shadow: 0 0 15px #00ff8844; }
        .send-btn {
            padding: 15px 30px;
            background: linear-gradient(135deg, #00ff88, #00aa55);
            border: none;
            border-radius: 30px;
            color: #0a0a15;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .send-btn:hover { transform: scale(1.05); box-shadow: 0 0 20px #00ff8866; }
        .typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 15px 20px;
            background: #2a2a4e;
            border-radius: 20px;
        }
        .typing-indicator span {
            width: 10px; height: 10px;
            background: #00ff88;
            border-radius: 50%;
            display: inline-block;
            margin: 0 3px;
            animation: bounce 1.4s infinite;
        }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-10px); } }
    </style>
</head>
<body>
    <div id="startup-overlay">
        <pre class="banner">
██████╗  ██████╗ ████████╗████████╗██╗   ██╗ ██████╗ ██████╗ ████████╗
██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝██╔════╝ ██╔══██╗╚══██╔══╝
██████╔╝██║   ██║   ██║      ██║    ╚████╔╝ ██║  ███╗██████╔╝   ██║   
██╔══██╗██║   ██║   ██║      ██║     ╚██╔╝  ██║   ██║██╔═══╝    ██║   
██████╔╝╚██████╔╝   ██║      ██║      ██║   ╚██████╔╝██║        ██║   
╚═════╝  ╚═════╝    ╚═╝      ╚═╝      ╚═╝    ╚═════╝ ╚═╝        ╚═╝   </pre>
        <div class="progress-container">
            <div class="progress-bar" id="progress-bar"></div>
        </div>
        <div class="progress-text" id="progress-text">Loading: 0.0% Complete</div>
    </div>

    <div class="chat-container" id="chat-container">
        <div class="chat-header">🤖 BottyGPT</div>
        <div class="chat-messages" id="chat-messages">
            <div class="message bot">Hello! I'm BottyGPT. Type a message to chat with me!</div>
        </div>
        <div class="typing-indicator" id="typing">
            <span></span><span></span><span></span>
        </div>
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="chat-input" placeholder="Type your message..." autofocus>
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let progress = 0;
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const startupOverlay = document.getElementById('startup-overlay');
        const chatContainer = document.getElementById('chat-container');

        function updateProgress() {
            progress += 2;
            progressBar.style.width = progress + '%';
            progressText.textContent = 'Loading: ' + progress.toFixed(1) + '% Complete';
            if (progress < 100) {
                setTimeout(updateProgress, 30);
            } else {
                setTimeout(() => {
                    startupOverlay.classList.add('fade-out');
                    chatContainer.style.display = 'flex';
                }, 300);
            }
        }
        updateProgress();

        const chatInput = document.getElementById('chat-input');
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });

        function addMessage(text, type) {
            const messages = document.getElementById('chat-messages');
            const msg = document.createElement('div');
            msg.className = 'message ' + type;
            msg.textContent = text;
            messages.appendChild(msg);
            messages.scrollTop = messages.scrollHeight;
        }

        function showTyping() {
            document.getElementById('typing').style.display = 'block';
        }

        function hideTyping() {
            document.getElementById('typing').style.display = 'none';
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, 'user');
            input.value = '';
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                hideTyping();
                addMessage(data.response, 'bot');
            } catch (error) {
                hideTyping();
                addMessage('Sorry, something went wrong!', 'bot');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = bot.chatbot_response(data.get('message', ''))
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🤖 BottyGPT Web Interface starting at http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=True)