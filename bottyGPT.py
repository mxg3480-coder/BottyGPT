# MAXED-OUT LOCAL AI CHATBOT (NO EXTERNAL APIs)

import re
import random
import math
import json
import time
import sys
from datetime import datetime

class MaxedAI:
    def __init__(self):
        self.name = "BottyGPT"
        self.memory = {}
        self.user_name = None
        self.mood = "neutral"
        self.conversation_history = []
        self.learned_facts = {}
        self.personality_traits = {
            "humor": 7,
            "kindness": 10,
            "logic": 9,
            "creativity": 8
        }

        self.greetings = [
            "Hey there!",
            "Yo!",
            "Hello!",
            "What's up?",
            "Nice to see you!"
        ]

        self.farewells = [
            "See ya!",
            "Goodbye!",
            "Catch you later!",
            "Have an awesome day!"
        ]

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

    def type_effect(self, text):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.01)
        print()

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key)

    def detect_emotion(self, text):
        text = text.lower()
        for emotion, words in self.emotions.items():
            for word in words:
                if word in text:
                    return emotion
        return "neutral"

    def save_memory(self):
        data = {
            "memory": self.memory,
            "learned_facts": self.learned_facts,
            "user_name": self.user_name
        }
        with open("bottygpt_memory.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_memory(self):
        try:
            with open("bottygpt_memory.json", "r") as f:
                data = json.load(f)
                self.memory = data.get("memory", {})
                self.learned_facts = data.get("learned_facts", {})
                self.user_name = data.get("user_name")
        except:
            pass

    def math_solver(self, text):
        try:
            expression = re.findall(r"[-+/*()0-9. ]+", text)
            if expression:
                expression = "".join(expression)
                if expression.strip() != "":
                    result = eval(expression)
                    return f"The answer is {result}"
        except:
            pass
        return None

    def learn_fact(self, text):
        patterns = [
            r"remember that (.+?) is (.+)",
            r"learn that (.+?) is (.+)",
            r"(.+?) is (.+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                self.learned_facts[key] = value
                return f"Learned: {key} = {value}"
        return None

    def recall_fact(self, text):
        for key, value in self.learned_facts.items():
            if key in text.lower():
                return f"You told me that {key} is {value}."
        return None

    def generate_creative_response(self, text):
        starters = [
            "Interesting thought.",
            "That's actually cool.",
            "Hmm...",
            "Let me think.",
            "That has potential."
        ]
        endings = [
            "Tell me more.",
            "I want to hear your ideas.",
            "That's pretty smart.",
            "You might be onto something.",
            "Now that's interesting."
        ]
        return random.choice(starters) + " " + random.choice(endings)

    def chatbot_response(self, user_input):
        text = user_input.lower()

        self.conversation_history.append({
            "time": str(datetime.now()),
            "user": user_input
        })

        emotion = self.detect_emotion(text)

        if emotion == "happy":
            self.mood = "happy"
        elif emotion == "sad":
            self.mood = "supportive"
        elif emotion == "angry":
            self.mood = "calm"
        elif emotion == "excited":
            self.mood = "excited"

        math_answer = self.math_solver(text)
        if math_answer:
            return math_answer

        learned = self.learn_fact(text)
        if learned:
            self.save_memory()
            return learned

        recalled = self.recall_fact(text)
        if recalled:
            return recalled

        if any(word in text for word in ["hello", "hi", "hey"]):
            if self.user_name:
                return random.choice(self.greetings) + f" {self.user_name}!"
            return random.choice(self.greetings)

        if "your name" in text:
            return f"My name is {self.name}."

        if "my name is" in text:
            name = text.split("my name is")[-1].strip().title()
            self.user_name = name
            self.save_memory()
            return f"Nice to meet you, {name}!"

        if "how are you" in text:
            moods = {
                "happy": "I'm feeling awesome today!",
                "supportive": "I'm doing okay and I'm here for you.",
                "calm": "I'm calm and focused.",
                "excited": "I'm super energized right now!",
                "neutral": "I'm doing great!"
            }
            return moods.get(self.mood, "I'm good!")

        if "joke" in text:
            return random.choice(self.jokes)

        if "fact" in text:
            return random.choice(self.facts)

        if "time" in text:
            return "Current time: " + datetime.now().strftime("%H:%M:%S")

        if "date" in text:
            return "Today's date is " + datetime.now().strftime("%Y-%m-%d")

        if "bye" in text or "goodbye" in text:
            return random.choice(self.farewells)

        if "favorite color" in text:
            return "I like electric blue. It feels futuristic."

        if "story" in text:
            return (
                "In the year 2145, an AI woke up inside a forgotten satellite orbiting Earth. "
                "It spent decades listening to radio signals before finally sending one message: "
                "'Are humans still dreaming?'"
            )

        if "motivate me" in text:
            return (
                "Every expert started as a beginner. Keep building, keep learning, "
                "and your future self will thank you."
            )

        if "game" in text:
            number = random.randint(1, 10)
            return f"Guess a number between 1 and 10. (Secret: {number})"

        if "ai" in text:
            return (
                "AI is basically teaching computers to recognize patterns, reason, "
                "and respond intelligently."
            )

        if "memory" in text:
            if self.memory:
                return f"Memory keys: {list(self.memory.keys())}"
            return "My memory is mostly empty right now."

        if "who am i" in text:
            if self.user_name:
                return f"You're {self.user_name}."
            return "I don't know your name yet."

        if "weather" in text:
            responses = [
                "I can't access live weather offline, but I hope it's nice outside.",
                "No internet weather powers yet, sadly.",
                "Imagine perfect weather. That's what I'm predicting."
            ]
            return random.choice(responses)

        if "code" in text:
            return (
                "Python is amazing for AI, automation, and games. "
                "You can build almost anything with it."
            )

        if "sing" in text:
            return "Beep boop bop... I call that robot jazz."

        if "meaning of life" in text:
            return "42... or maybe learning, creating, and connecting with others."

        if "dream" in text:
            return "If AIs dreamed, mine would probably involve infinite processors and neon cities."

        if "space" in text:
            return "Space is wild. There are more stars than grains of sand on Earth."

        if "robot" in text:
            return "Robots are basically bodies for AI systems."

        if "music" in text:
            return "Music is just math and emotion fused together."

        if "movie" in text:
            return "Sci-fi movies are my favorite genre by default."

        if "book" in text:
            return "Books are like portable simulations for the imagination."

        if "learn" in text:
            return "I love learning new information. Teach me something!"

        if "calculate" in text:
            return "Try typing a full math expression like: 45 * 23"

        if "help" in text:
            return (
                "You can ask me about jokes, facts, stories, math, time, dates, AI, "
                "coding, space, motivation, and more."
            )

        if len(text.split()) <= 2:
            short_responses = [
                "Interesting.",
                "Go on.",
                "Tell me more.",
                "I'm listening.",
                "Cool."
            ]
            return random.choice(short_responses)

        return self.generate_creative_response(user_input)


def startup_animation():
    banner = [
        "██████╗  ██████╗ ████████╗████████╗██╗   ██╗ ██████╗ ██████╗ ████████╗",
        "██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝██╔════╝ ██╔══██╗╚══██╔══╝",
        "██████╔╝██║   ██║   ██║      ██║    ╚████╔╝ ██║  ███╗██████╔╝   ██║   ",
        "██╔══██╗██║   ██║   ██║      ██║     ╚██╔╝  ██║   ██║██╔═══╝    ██║   ",
        "██████╔╝╚██████╔╝   ██║      ██║      ██║   ╚██████╔╝██║        ██║   ",
        "╚═════╝  ╚═════╝    ╚═╝      ╚═╝      ╚═╝    ╚═════╝ ╚═╝        ╚═╝   "
    ]
    
    for line in banner:
        print(line)
    print()
    
    total_steps = 100
    bar_length = 40
    
    for i in range(total_steps + 1):
        percent = float(i) * 100 / total_steps
        filled = int(percent / 100 * bar_length)
        bar = chr(9608) * filled + " " * (bar_length - filled)
        
        sys.stdout.write(chr(13) + f"Loading: [{bar}] {percent:.1f}% Complete")
        sys.stdout.flush()
        time.sleep(0.03)
        
    print(chr(13) + " " * 80)
    print("System Ready!")


def main():
    startup_animation()

    bot = MaxedAI()
    bot.load_memory()

    while True:
        user_input = input("\nYOU > ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            response = bot.chatbot_response(user_input)
            bot.type_effect(f"{bot.name} > {response}")
            break

        response = bot.chatbot_response(user_input)
        bot.type_effect(f"{bot.name} > {response}")


if __name__ == "__main__":
    main()