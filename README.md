# CricInfo Player Statistics Management System

## Overview
The **CricInfo Player Statistics Management System** is a desktop application for managing cricket player information and their performance statistics. Built with **Python**, it uses **SQLite** for database management and **Tkinter** for the graphical user interface (GUI).  

---

## Features
1. **Player Management**:
   - Add new players with details such as name, country, age, and role.
   - Edit existing player details.
   - Delete players from the database.

2. **Batting Statistics Management**:
   - Add batting statistics for players (e.g., runs, average, strike rate).
   - Edit existing batting statistics.

3. **Bowling Statistics Management**:
   - Add bowling statistics for players (e.g., wickets, best figures, economy).
   - Edit existing bowling statistics.

4. **View Statistics**:
   - View statistics of a specific player.
   - View all players' data.

5. **Search and Sort**:
   - List players by:
     - Most runs
     - Highest score
     - Most wickets
     - Best averages
     - Best figures
   - Filter players by country.

---

## Technologies Used
- **Programming Language**: Python
- **Database**: SQLite
- **GUI Framework**: Tkinter

---

## How to Run
1. **Prerequisites**:
   - Python 3.x installed on your system.
   - SQLite3 library (comes pre-installed with Python).

2. **Steps**:
   - Clone the repository or download the project files.
   - Ensure all dependencies (Tkinter, SQLite) are satisfied.
   - Run the `code.py` file:
     ```bash
     python code.py
     ```
   - The application window will open, allowing you to interact with the system.

---

## Code Structure
- **Database Layer**: Functions to handle CRUD operations on the SQLite database.
- **Business Layer**: Classes representing players, batting stats, and bowling stats.
- **Presentation Layer**: Tkinter-based GUI providing an intuitive interface for user interaction.

---
