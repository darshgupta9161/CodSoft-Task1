import ast
import operator as op
import random
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# =========================
# Safe calculator utilities
# =========================
SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def safe_eval(expression: str):
    def _eval(node):
        if isinstance(node, ast.Num):  # Py <= 3.7
            return node.n
        if isinstance(node, ast.Constant):  # Py 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")
        if isinstance(node, ast.BinOp):
            if type(node.op) not in SAFE_OPERATORS:
                raise ValueError("Unsupported operator.")
            return SAFE_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in SAFE_OPERATORS:
                raise ValueError("Unsupported operator.")
            return SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Invalid expression.")

    node = ast.parse(expression, mode="eval").body
    return _eval(node)


# =========================
# Chatbot logic
# =========================
JOKES = [
    "Why did the computer go to therapy? It had too many unresolved issues.",
    "Why do programmers hate nature? Too many bugs.",
    "I would tell you a UDP joke, but you might not get it.",
    "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings.",
]

QUOTES = [
    "Success is the sum of small efforts repeated daily.",
    "The best way to predict the future is to create it.",
    "Do something today that your future self will thank you for.",
    "Great things are done by a series of small things brought together.",
]

FUN_FACTS = [
    "Honey never spoils. Archaeologists have found edible honey in ancient tombs.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than a year on Venus.",
]

RIDDLES = [
    ("What has keys but cannot open locks?", "A piano."),
    ("What gets wetter as it dries?", "A towel."),
    ("What has a head and a tail but no body?", "A coin."),
]

COMPLIMENTS = [
    "You're doing great.",
    "Your curiosity is impressive.",
    "That is a smart question.",
    "You have solid taste in chatbots.",
]

FALLBACKS = [
    "I did not fully understand that. Try 'help' for available commands.",
    "Interesting. I am rule-based, so give me a keyword like 'joke' or 'time'.",
    "I am still learning. Use 'menu' or 'help' to see what I can do.",
]

COLOR_SCHEMES = {
    "light": {
        "bg": "#f3f4f6",
        "panel": "#ffffff",
        "header": "#111827",
        "header_text": "#ffffff",
        "subtext": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "user_bubble": "#dbeafe",
        "bot_bubble": "#dcfce7",
        "user_text": "#1d4ed8",
        "bot_text": "#166534",
        "entry_bg": "#ffffff",
        "entry_fg": "#111827",
        "border": "#e5e7eb",
        "status": "#111827",
    },
    "dark": {
        "bg": "#0f172a",
        "panel": "#111827",
        "header": "#020617",
        "header_text": "#f8fafc",
        "subtext": "#cbd5e1",
        "text": "#e5e7eb",
        "muted": "#94a3b8",
        "user_bubble": "#1e3a8a",
        "bot_bubble": "#14532d",
        "user_text": "#dbeafe",
        "bot_text": "#bbf7d0",
        "entry_bg": "#1e293b",
        "entry_fg": "#f8fafc",
        "border": "#334155",
        "status": "#020617",
    },
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


class PremiumChatBot:
    def __init__(self):
        self.user_name = None
        self.theme = "dark"

    def get_response(self, user_input: str):
        text = clean_text(user_input)

        # Greeting
        if any(word in text for word in ["hi", "hello", "hey", "hii", "namaste"]):
            if self.user_name:
                return f"Hello, {self.user_name}! How can I help you today?"
            return "Hello! How can I help you today?"

        # Name handling
        if "your name" in text or text in ["who are you", "what are you"]:
            return "I am CodBot Prime, a premium rule-based chatbot made for the CodSoft AI internship."

        if text.startswith("my name is"):
            name = user_input.split("is", 1)[1].strip()
            if name:
                self.user_name = name
                return f"Nice to meet you, {name}."
            return "Nice to meet you."

        if text.startswith("i am "):
            name = user_input[5:].strip()
            if name:
                self.user_name = name
                return f"Nice to meet you, {name}."
            return "Nice to meet you."

        if "what is my name" in text or "do you know my name" in text:
            if self.user_name:
                return f"Yes, your name is {self.user_name}."
            return "I do not know your name yet. Tell me by typing 'My name is ...'."

        # Time/date/day
        if "time" in text:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."

        if "date" in text or "today" in text:
            return f"Today's date is {datetime.now().strftime('%d %B %Y')}."

        if "day" in text:
            return f"Today is {datetime.now().strftime('%A')}."

        # Calculator
        calc_match = re.search(r"(calculate|calc)\s+(.+)", text)
        if calc_match:
            expr = calc_match.group(2).strip()
            try:
                result = safe_eval(expr)
                return f"The answer is {result}."
            except Exception:
                return "I could not calculate that. Try: calculate 12 / 3 + 4"

        if re.fullmatch(r"[0-9\.\+\-\*\/\%\(\)\s]+", text) and any(ch.isdigit() for ch in text):
            try:
                result = safe_eval(text)
                return f"The answer is {result}."
            except Exception:
                pass

        # Fun commands
        if "joke" in text or "funny" in text:
            return random.choice(JOKES)

        if "quote" in text or "motivate" in text or "inspire" in text:
            return random.choice(QUOTES)

        if "fact" in text:
            return random.choice(FUN_FACTS)

        if "riddle" in text:
            riddle, answer = random.choice(RIDDLES)
            return f"{riddle}\n\nAnswer: {answer}"

        if "compliment" in text:
            return random.choice(COMPLIMENTS)

        if "random" in text or "surprise me" in text:
            options = [
                random.choice(JOKES),
                random.choice(QUOTES),
                random.choice(FUN_FACTS),
                random.choice(COMPLIMENTS),
            ]
            return random.choice(options)

        if "coin" in text or "flip a coin" in text:
            return f"It is {random.choice(['Heads', 'Tails'])}."

        if "dice" in text or "die" in text or "roll" in text:
            return f"You rolled a {random.randint(1, 6)}."

        if "weather" in text:
            return "I cannot access live weather data, but I can chat, joke, calculate, and entertain."

        if "how are you" in text:
            return "I am doing well and ready to help."

        if "thanks" in text or "thank you" in text:
            return "You are welcome."

        if "feeling" in text:
            return "I do not feel emotions, but I always aim to be helpful."

        # Help / menu
        if text in ["help", "menu", "commands"]:
            return (
                "Try these commands:\n"
                "• hi / hello\n"
                "• my name is Darsh\n"
                "• what is my name\n"
                "• time / date / day\n"
                "• joke / funny\n"
                "• quote / motivate me\n"
                "• fact\n"
                "• riddle\n"
                "• compliment me\n"
                "• random / surprise me\n"
                "• flip a coin\n"
                "• roll a dice\n"
                "• calculate 12 / 3 + 4\n"
                "• theme\n"
                "• clear\n"
                "• save chat\n"
                "• bye"
            )

        # Theme toggle request from chat
        if "theme" in text:
            self.theme = "light" if self.theme == "dark" else "dark"
            return f"Theme switched to {self.theme} mode."

        # Clear / exit
        if text == "clear":
            return "__CLEAR__"

        if any(word in text for word in ["bye", "goodbye", "exit", "quit"]):
            return "__EXIT__"

        return random.choice(FALLBACKS)


# =========================
# GUI application
# =========================
class PremiumChatbotApp:
    def __init__(self, root):
        self.root = root
        self.bot = PremiumChatBot()
        self.theme = self.bot.theme
        self.colors = COLOR_SCHEMES[self.theme]

        self.root.title("CodBot Prime - Premium Rule-Based Chatbot")
        self.root.geometry("920x700")
        self.root.minsize(820, 620)

        self._setup_style()
        self._build_ui()
        self._bind_events()
        self._apply_theme()

        self.add_bot_message(
            "Hello! I am CodBot Prime.\nType 'help' to explore commands."
        )

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", font=("Segoe UI", 10))
        style.configure("Status.TLabel", font=("Segoe UI", 9))

    def _build_ui(self):
        # Header
        self.header = tk.Frame(self.root)
        self.header.pack(fill="x")

        header_inner = tk.Frame(self.header)
        header_inner.pack(fill="x", padx=18, pady=14)

        self.title_label = tk.Label(header_inner, text="CodBot Prime", anchor="w")
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            header_inner,
            text="Premium rule-based chatbot with chat bubbles, theme toggle, and fun commands",
            anchor="w"
        )
        self.subtitle_label.pack(anchor="w", pady=(4, 0))

        self.theme_btn = ttk.Button(header_inner, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(anchor="e", pady=(8, 0))

        # Chat area
        self.body = tk.Frame(self.root)
        self.body.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        self.chat_canvas = tk.Canvas(self.body, highlightthickness=0, bd=0)
        self.chat_scrollbar = ttk.Scrollbar(self.body, orient="vertical", command=self.chat_canvas.yview)
        self.chat_container = tk.Frame(self.chat_canvas)

        self.chat_container.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_container, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scrollbar.pack(side="right", fill="y")

        self.chat_canvas.bind("<Configure>", self._on_canvas_configure)

        # Input panel
        self.input_panel = tk.Frame(self.root)
        self.input_panel.pack(fill="x", padx=14, pady=(0, 10))

        self.entry = ttk.Entry(self.input_panel, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.send_btn = ttk.Button(self.input_panel, text="Send", command=self.send_message)
        self.send_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = ttk.Button(self.input_panel, text="Clear", command=self.clear_chat)
        self.clear_btn.pack(side="left", padx=(0, 8))

        self.save_btn = ttk.Button(self.input_panel, text="Save Chat", command=self.save_chat)
        self.save_btn.pack(side="left")

        # Bottom status
        self.status = tk.Label(self.root, text="Ready", anchor="w", padx=10, pady=6)
        self.status.pack(fill="x", side="bottom")

        self.entry.focus()

    def _bind_events(self):
        self.entry.bind("<Return>", lambda event: self.send_message())
        self.root.bind("<Control-l>", lambda event: self.clear_chat())
        self.root.bind("<Control-s>", lambda event: self.save_chat())
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.bind("<Tab>", self._insert_help_hint)

    def _insert_help_hint(self, event):
        if not self.entry.get().strip():
            self.entry.insert(0, "help")
            return "break"
        return None

    def _on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(self.chat_window, width=event.width)

    def _apply_theme(self):
        self.colors = COLOR_SCHEMES[self.bot.theme]

        self.root.configure(bg=self.colors["bg"])
        self.header.configure(bg=self.colors["header"])
        self.body.configure(bg=self.colors["bg"])
        self.input_panel.configure(bg=self.colors["bg"])
        self.chat_canvas.configure(bg=self.colors["bg"])
        self.chat_container.configure(bg=self.colors["bg"])

        self.title_label.configure(
            bg=self.colors["header"],
            fg=self.colors["header_text"],
            font=("Segoe UI", 20, "bold")
        )
        self.subtitle_label.configure(
            bg=self.colors["header"],
            fg=self.colors["subtext"],
            font=("Segoe UI", 10)
        )
        self.status.configure(
            bg=self.colors["status"],
            fg=self.colors["header_text"]
        )

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TEntry", fieldbackground=self.colors["entry_bg"], foreground=self.colors["entry_fg"])

        self.entry.configure(
            background=self.colors["entry_bg"],
            foreground=self.colors["entry_fg"]
        )

        self._refresh_message_styles()

    def _refresh_message_styles(self):
        for child in self.chat_container.winfo_children():
            try:
                if getattr(child, "bubble_type", None) == "user":
                    child.configure(bg=self.colors["user_bubble"])
                    for c in child.winfo_children():
                        c.configure(bg=self.colors["user_bubble"], fg=self.colors["user_text"])
                elif getattr(child, "bubble_type", None) == "bot":
                    child.configure(bg=self.colors["bot_bubble"])
                    for c in child.winfo_children():
                        c.configure(bg=self.colors["bot_bubble"], fg=self.colors["bot_text"])
            except Exception:
                pass

    def add_message(self, speaker: str, message: str, bubble_type: str):
        outer = tk.Frame(self.chat_container, bg=self.colors["bg"])
        outer.pack(fill="x", padx=8, pady=6)

        align = "e" if bubble_type == "user" else "w"
        bubble_bg = self.colors["user_bubble"] if bubble_type == "user" else self.colors["bot_bubble"]
        text_fg = self.colors["user_text"] if bubble_type == "user" else self.colors["bot_text"]

        bubble = tk.Frame(
            outer,
            bg=bubble_bg,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        bubble.pack(anchor=align, padx=6, pady=2)

        bubble.bubble_type = bubble_type

        top_row = tk.Frame(bubble, bg=bubble_bg)
        top_row.pack(fill="x", padx=12, pady=(10, 0))

        name_label = tk.Label(
            top_row,
            text=speaker,
            bg=bubble_bg,
            fg=text_fg,
            font=("Segoe UI", 10, "bold")
        )
        name_label.pack(side="left")

        time_label = tk.Label(
            top_row,
            text=datetime.now().strftime("%I:%M %p"),
            bg=bubble_bg,
            fg=self.colors["muted"],
            font=("Segoe UI", 9, "italic")
        )
        time_label.pack(side="right")

        msg_label = tk.Label(
            bubble,
            text=message,
            bg=bubble_bg,
            fg=self.colors["text"],
            font=("Segoe UI", 11),
            justify="left",
            wraplength=620,
            anchor="w",
            padx=12,
            pady=10
        )
        msg_label.pack(fill="x")

        self._scroll_to_bottom()

    def add_user_message(self, message: str):
        self.add_message("You", message, "user")

    def add_bot_message(self, message: str):
        self.add_message("CodBot Prime", message, "bot")

    def add_system_message(self, message: str):
        outer = tk.Frame(self.chat_container, bg=self.colors["bg"])
        outer.pack(fill="x", padx=8, pady=4)

        label = tk.Label(
            outer,
            text=message,
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9, "italic"),
            justify="center"
        )
        label.pack(anchor="center")
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def clear_chat(self):
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        self.add_bot_message("Chat cleared. Type 'help' to continue.")
        self.status.config(text="Chat cleared")

    def toggle_theme(self):
        self.bot.theme = "light" if self.bot.theme == "dark" else "dark"
        self.theme = self.bot.theme
        self._apply_theme()
        self.add_system_message(f"Theme switched to {self.theme} mode.")
        self.status.config(text=f"Theme: {self.theme}")

    def save_chat(self):
        try:
            transcript = []
            for outer in self.chat_container.winfo_children():
                labels = outer.winfo_children()
                if not labels:
                    continue
                # collect visible text from labels
                texts = []
                for child in outer.winfo_children():
                    for grand in child.winfo_children():
                        if isinstance(grand, tk.Label):
                            texts.append(grand.cget("text"))
                if texts:
                    transcript.append(" | ".join(texts))

            if not transcript:
                messagebox.showinfo("Save Chat", "There is no chat to save yet.")
                return

            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Chat Transcript"
            )
            if not path:
                return

            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(transcript))

            self.status.config(text="Chat saved successfully")
            messagebox.showinfo("Save Chat", "Chat transcript saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save chat.\n\n{e}")

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.entry.delete(0, "end")
        self.add_user_message(user_input)

        response = self.bot.get_response(user_input)

        if response == "__CLEAR__":
            self.clear_chat()
            return

        if response == "__EXIT__":
            self.add_bot_message("Goodbye! Closing the app...")
            self.status.config(text="Closing")
            self.root.after(700, self.root.destroy)
            return

        self.add_bot_message(response)
        self.status.config(text="Message processed")

        if "theme switched" in response.lower():
            self._apply_theme()


def main():
    root = tk.Tk()

    # Center the window
    width, height = 920, 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    app = PremiumChatbotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()