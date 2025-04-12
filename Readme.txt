# 🧩 Persian Word Search Puzzle Game

A fully-featured, customizable **Persian word search game** written in Python — designed with future Unreal Engine integration in mind. This project is my first AI/game-dev crossover portfolio piece, with clean, modular design and support for language-specific logic like `آ` and `ا` equivalency.

---

## 🎯 Features

- 🧠 **Category-Based Word Selection**: Words are loaded from organized `.txt` files by category.
- 🔤 **Persian Support**: Fully supports Persian letters.
- 🔁 **All-Directional Word Placement**: Words may appear horizontally, vertically, diagonally — both forward and reversed.
- 🔒 **Overlap Rules**: Only one-character overlap between any two words is allowed.
- ☝️ **Vector-Based User Input**: Accepts input as vector start and end positions (simulating touchscreen input).
- ✅ **Dictionary Scoring**: Points awarded for valid words only, using a separate dictionary.
- ⛔ **Bad Word Filtering**: Filters out defined inappropriate words **both before** and **after** grid generation with minimal reshuffling.
- 🔧 **Customizable**: Easily update bad words, dictionary files, and categories via `.txt` files or code.

---

## 🧪 Example Use Case

This game can be integrated into a touchscreen app or game (e.g., in Unreal Engine), where users draw a line across a word to select it. The backend code checks:

- If the word exists in the dictionary.
- If it only overlaps with previously found words by **one character or less**.
- That it’s not a duplicate or a substring of a previously found word.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
