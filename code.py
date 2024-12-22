import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

######CREATING DATABASE##################
conn = sqlite3.connect('cricinfo.db')
cursor = conn.cursor()

##########################################################################################################################################################################################################################################################################################
####MAIN DATA LAYER CONTAINS FUNCTIONS TO MANAGE DATA IN DATABASE###########################

cursor.execute("CREATE TABLE IF NOT EXISTS PlayerInfo (player_id INTEGER PRIMARY KEY,name TEXT NOT NULL,country TEXT NOT NULL,age INTEGER NOT NULL,role TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS BattingStats (player_id INTEGER NOT NULL,innings INTEGER NOT NULL,runs INTEGER NOT NULL,average REAL NOT NULL,strike_rate REAL NOT NULL,highest_score INTEGER NOT NULL,FOREIGN KEY (player_id) REFERENCES PlayerInfo (player_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS BowlingStats (player_id INTEGER NOT NULL,innings INTEGER NOT NULL,wickets INTEGER NOT NULL,best_figures TEXT NOT NULL,average REAL NOT NULL,economy REAL NOT NULL,FOREIGN KEY (player_id) REFERENCES PlayerInfo (player_id))")

conn.commit()

def add_player(obj):
    cursor.execute('''
        SELECT * FROM PlayerInfo WHERE player_id = ?
    ''', (obj.player_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showerror("Error", "Player Record Already Exists for this ID")
    else:
        cursor.execute('INSERT INTO PlayerInfo (player_id,name, country, age, role) VALUES (?,?, ?, ?, ?)', (obj.player_id,obj.name, obj.country, obj.age, obj.role))
        conn.commit()

def add_batting_stats(obj):
    cursor.execute('''
        SELECT * FROM BattingStats WHERE player_id = ?
    ''', (obj.player_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showerror("Error", "Batting stats record already exists for this player ID.")
    else:
        cursor.execute('''
            INSERT INTO BattingStats (player_id, innings, runs, average, strike_rate, highest_score) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (obj.player_id, obj.innings, obj.runs, obj.average, obj.strike_rate, obj.highest_score))
        conn.commit()
        messagebox.showinfo("Success", "Batting stats added successfully!")

def add_bowling_stats(obj):
    cursor.execute('''
        SELECT * FROM BowlingStats WHERE player_id = ?
    ''', (obj.player_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showerror("Error", "Bowling stats record already exists for this player ID.")
    else:
        cursor.execute('''
            INSERT INTO BowlingStats (player_id, innings, wickets, best_figures, average, economy) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (obj.player_id, obj.innings, obj.wickets, obj.best_figures, obj.average, obj.economy))
        conn.commit()
        messagebox.showinfo("Success", "Bowling stats added successfully!")

def view_stats(player_id):
    cursor.execute('''
        SELECT 
            PlayerInfo.name, PlayerInfo.country, PlayerInfo.age, PlayerInfo.role,
            BattingStats.innings, BattingStats.runs, BattingStats.average, 
            BattingStats.strike_rate, BattingStats.highest_score, 
            BowlingStats.innings, BowlingStats.wickets, BowlingStats.best_figures, 
            BowlingStats.average, BowlingStats.economy
        FROM PlayerInfo
        LEFT JOIN BattingStats ON PlayerInfo.player_id = BattingStats.player_id
        LEFT JOIN BowlingStats ON PlayerInfo.player_id = BowlingStats.player_id
        WHERE PlayerInfo.player_id = ?
    ''', (player_id,))
    result = cursor.fetchone()
    return result

def view_all_players():
        cursor.execute('''
            SELECT PlayerInfo.player_id,PlayerInfo.name, PlayerInfo.country, PlayerInfo.age, PlayerInfo.role,
            BattingStats.runs, BattingStats.average, BattingStats.highest_score,
            BowlingStats.wickets, BowlingStats.best_figures, BowlingStats.average
            FROM PlayerInfo
            LEFT JOIN BattingStats ON PlayerInfo.player_id = BattingStats.player_id
            LEFT JOIN BowlingStats ON PlayerInfo.player_id = BowlingStats.player_id
        ''')
        result = cursor.fetchall()
        return result

def list_by_highest_score():
    cursor.execute('''
        SELECT PlayerInfo.player_id,PlayerInfo.name, BattingStats.highest_score 
        FROM PlayerInfo 
        JOIN BattingStats ON PlayerInfo.player_id = BattingStats.player_id
        ORDER BY BattingStats.highest_score DESC
    ''')
    result = cursor.fetchall()
    return result

def list_by_most_runs():
    cursor.execute('''
        SELECT PlayerInfo.player_id,PlayerInfo.name, BattingStats.runs 
        FROM PlayerInfo 
        JOIN BattingStats ON PlayerInfo.player_id = BattingStats.player_id
        ORDER BY BattingStats.runs DESC
    ''')
    result = cursor.fetchall()
    return result

def list_by_most_wickets():
    cursor.execute('''
        SELECT PlayerInfo.player_id,PlayerInfo.name, BowlingStats.wickets 
        FROM PlayerInfo 
        JOIN BowlingStats ON PlayerInfo.player_id = BowlingStats.player_id
        ORDER BY BowlingStats.wickets DESC
    ''')
    result = cursor.fetchall()
    return result

def list_by_average():
    cursor.execute('''
        SELECT PlayerInfo.player_id,PlayerInfo.name, BattingStats.average 
        FROM PlayerInfo 
        JOIN BattingStats ON PlayerInfo.player_id = BattingStats.player_id
        ORDER BY BattingStats.average DESC
    ''')
    result = cursor.fetchall()
    return result

def list_by_best_figures():
    cursor.execute('''
        SELECT PlayerInfo.player_id,PlayerInfo.name, BowlingStats.best_figures 
        FROM PlayerInfo 
        JOIN BowlingStats ON PlayerInfo.player_id = BowlingStats.player_id
        ORDER BY BowlingStats.best_figures DESC
    ''')
    result = cursor.fetchall()
    return result

def list_by_country(country):
    cursor.execute('''
        SELECT PlayerInfo.player_id, PlayerInfo.name 
        FROM PlayerInfo 
        WHERE PlayerInfo.country = ?
    ''', (country,))
    result = cursor.fetchall()
    return result

def delete_player(player_id):
    cursor.execute('''
        SELECT * FROM PlayerInfo WHERE player_id = ?
    ''', (player_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        cursor.execute('DELETE FROM PlayerInfo WHERE player_id = ?', (player_id,))
        cursor.execute('DELETE FROM BattingStats WHERE player_id = ?', (player_id,))
        cursor.execute('DELETE FROM BowlingStats WHERE player_id = ?', (player_id,))
        conn.commit()
        messagebox.showinfo("Success", "Player Deleted successfully!")
    
    else:
        messagebox.showerror("Error", "No Record Found Against this ID.")

def fetch_player_details(player_id):
    cursor.execute('''
        SELECT * FROM PlayerInfo WHERE player_id = ?
    ''', (player_id,))
    return cursor.fetchone()

def update_player(player_id, name, country, age, role):
    cursor.execute('''
        UPDATE PlayerInfo 
        SET name=?, country=?, age=?, role=?
        WHERE player_id=?
    ''', (name, country, age, role, player_id))
    conn.commit()


def fetch_batting_stats(player_id):
        connection = sqlite3.connect('cricinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM BattingStats WHERE player_id=?", (player_id,))
        batting_stats = cursor.fetchone()

        connection.close()

        return batting_stats

def update_batting_stats(player_id, innings, runs, average, strike_rate,highest_score):
        connection = sqlite3.connect('cricinfo.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE BattingStats SET innings=?, runs=?, average=?, strike_rate=?, highest_score=? WHERE player_id=?",
                       (innings, runs, average, strike_rate,highest_score, player_id))

        connection.commit()
        connection.close()

def fetch_bowling_stats(player_id):
        connection = sqlite3.connect('cricinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM BowlingStats WHERE player_id=?", (player_id,))
        batting_stats = cursor.fetchone()

        connection.close()

        return batting_stats

def update_bowling_stats(player_id, innings, wickets,best_figures,average,economy):
        connection = sqlite3.connect('cricinfo.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE BowlingStats SET innings=?, wickets=?, best_figures=?, average=?, economy=? WHERE player_id=?",
                       (innings, wickets,best_figures,average,economy, player_id))

        connection.commit()
        connection.close()

##########################################################################################################################################################################################################################################################################################
####BUSINESS LAYER CONTAINING CLASSES AND BUSINESS LOGIC###########################
class Player :
    def __init__ (self,player_id,name,country,age,role):
        self.player_id = player_id
        self.name = name
        self.country = country
        self.age = age
        self.role = role

class BattingStats :
    def __init__ (self,player_id, innings, runs, average, strike_rate, highest_score):
        self.player_id = player_id
        self.innings = innings
        self.runs = runs
        self.average = average
        self.strike_rate = strike_rate
        self.highest_score = highest_score

class BowlingStats:
    def __init__ (self,player_id, innings, wickets, best_figures, average, economy):
        self.player_id = player_id
        self.innings = innings
        self.wickets = wickets
        self.best_figures = best_figures
        self.average = average
        self.economy = economy

class CricInfo:
    def __init__(self, master):
        self.master = master
        self.selected_player_id = None
        master.title("Cricinfo")

        welcome_label = tk.Label(master, text="Welcome to Cricinfo", font=("Helvetica", 16))
        welcome_label.pack(pady=10)

        add_player_button = tk.Button(master, text="Add Player", command=self.show_add_player_window,font=('Verdana',12),relief='groove')
        add_player_button.pack(pady=5)

        add_batting_stats_button = tk.Button(master, text="Add Batting Stats", command=self.show_add_batting_stats_window,font=('Verdana',12),relief='groove')
        add_batting_stats_button.pack(pady=5)

        add_bowling_stats_button = tk.Button(master, text="Add Bowling Stats", command=self.show_add_bowling_stats_window,font=('Verdana',12),relief='groove')
        add_bowling_stats_button.pack(pady=5)

        view_stats_button = tk.Button(master, text="View Stats", command=self.show_view_stats_window,font=('Verdana',12),relief='groove')
        view_stats_button.pack(pady=5)

        view_all_button = tk.Button(master, text="View All Players", command=self.show_view_all_window,font=('Verdana',12),relief='groove')
        view_all_button.pack(pady=5)
    
        edit_player_button = tk.Button(master, text="Edit Player", command=self.input_id, font=('Verdana', 12), relief='groove')
        edit_player_button.pack(pady=5)

        edit_batting_stats_button = tk.Button(master, text="Edit Batting Stats", command=self.input_id_batting, font=('Verdana', 12), relief='groove')
        edit_batting_stats_button.pack(pady=5)

        edit_bowling_stats_button = tk.Button(master, text="Edit Bowling Stats", command=self.input_id_bowling, font=('Verdana', 12), relief='groove')
        edit_bowling_stats_button.pack(pady=5)

        list_most_runs_button = tk.Button(master, text="List by Most Runs", command=self.show_list_most_runs_window,font=('Verdana',12),relief='groove')
        list_most_runs_button.pack(pady=5)

        list_highest_score_button = tk.Button(master, text="List by Highest Score", command=self.show_list_highest_score_window,font=('Verdana',12),relief='groove')
        list_highest_score_button.pack(pady=5)

        list_average_button = tk.Button(master, text="List by Average", command=self.show_list_average_window,font=('Verdana',12),relief='groove')
        list_average_button.pack(pady=5)

        list_most_wickets_button = tk.Button(master, text="List by Most Wickets", command=self.show_list_most_wickets_window,font=('Verdana',12),relief='groove')
        list_most_wickets_button.pack(pady=5)

        

        list_best_figures_button = tk.Button(master, text="List by Best Figures", command=self.show_list_best_figures_window,font=('Verdana',12),relief='groove')
        list_best_figures_button.pack(pady=5)

        list_by_country_button = tk.Button(master, text="List by Country", command=self.show_list_by_country_window,font=('Verdana',12),relief='groove')
        list_by_country_button.pack(pady=5)

        delete_player_button = tk.Button(master, text="Delete Player", command=self.show_delete_player_window,font=('Verdana',12),relief='groove')
        delete_player_button.pack(pady=5)





    def show_add_player_window(self):
        add_player_window = tk.Toplevel(self.master)
        add_player_window.title("Add Player")

        frame = tk.Frame(add_player_window, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text="Player ID:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        player_id_entry = tk.Entry(frame)
        player_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Name:", font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Country:", font=('Helvetica', 12)).grid(row=2, column=0, sticky='w', pady=5)
        country_entry = tk.Entry(frame)
        country_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Age:", font=('Helvetica', 12)).grid(row=3, column=0, sticky='w', pady=5)
        age_entry = tk.Entry(frame)
        age_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Role:", font=('Helvetica', 12)).grid(row=4, column=0, sticky='w', pady=5)
        role_options = ["Batsman", "Bowler", "All-Rounder"]
        role_var = tk.StringVar(add_player_window)
        role_dropdown = tk.OptionMenu(frame, role_var, *role_options)
        role_dropdown.grid(row=4, column=1, pady=5)

        add_player_button = tk.Button(frame, text="Add Player", font=('Helvetica', 12), command=lambda: self.add_player(
            player_id_entry.get(), name_entry.get(), country_entry.get(), age_entry.get(), role_var.get(), add_player_window))
        add_player_button.grid(row=5, columnspan=2, pady=10)


    def add_player(self, player_id,name, country, age, role, window):
        try:
            player_id = int(player_id)
            age = int(age)
            if age < 15:
                raise ValueError("Age must be 15 or above.")
            
            if not all(entry.strip() for entry in [name, country, role]):
                raise ValueError("Name, Country, and Role are mandatory fields.")

            player = Player(player_id, name.upper(), country.upper(), age, role)
            add_player(player)
            messagebox.showinfo("Success","Player Added Succesfully.")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            window.destroy()

    def show_add_batting_stats_window(self):
        add_batting_stats_window = tk.Toplevel(self.master)
        add_batting_stats_window.title("Add Batting Stats")

        frame = tk.Frame(add_batting_stats_window, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text="Player ID:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        player_id_entry = tk.Entry(frame, font=('Helvetica', 12))
        player_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Innings:", font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        innings_entry = tk.Entry(frame, font=('Helvetica', 12))
        innings_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Runs:", font=('Helvetica', 12)).grid(row=2, column=0, sticky='w', pady=5)
        runs_entry = tk.Entry(frame, font=('Helvetica', 12))
        runs_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Average:", font=('Helvetica', 12)).grid(row=3, column=0, sticky='w', pady=5)
        average_entry = tk.Entry(frame, font=('Helvetica', 12))
        average_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Strike Rate:", font=('Helvetica', 12)).grid(row=4, column=0, sticky='w', pady=5)
        strike_rate_entry = tk.Entry(frame, font=('Helvetica', 12))
        strike_rate_entry.grid(row=4, column=1, pady=5)

        tk.Label(frame, text="Highest Score:", font=('Helvetica', 12)).grid(row=5, column=0, sticky='w', pady=5)
        highest_score_entry = tk.Entry(frame, font=('Helvetica', 12))
        highest_score_entry.grid(row=5, column=1, pady=5)

        add_batting_stats_button = tk.Button(frame, text="Add Batting Stats", font=('Helvetica', 12), command=lambda: self.add_batting_stats(
            player_id_entry.get(), innings_entry.get(), runs_entry.get(), average_entry.get(), strike_rate_entry.get(), highest_score_entry.get(), add_batting_stats_window))
        add_batting_stats_button.grid(row=6, columnspan=2, pady=10)

    def add_batting_stats(self, player_id, innings, runs, average, strike_rate, highest_score, window):
        try:
            player_id = int(player_id)
            innings = int(innings)
            runs = int(runs)
            average = float(average)
            strike_rate = float(strike_rate)
            highest_score = int(highest_score)
            batting_stats = BattingStats (player_id,innings,runs,average,strike_rate,highest_score)
            add_batting_stats(batting_stats)
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")

    def show_add_bowling_stats_window(self):
        add_bowling_stats_window = tk.Toplevel(self.master)
        add_bowling_stats_window.title("Add Bowling Stats")

        frame = tk.Frame(add_bowling_stats_window, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text="Player ID:",font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        player_id_entry = tk.Entry(frame)
        player_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Innings:",font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        innings_entry = tk.Entry(frame)
        innings_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Wickets:",font=('Helvetica', 12)).grid(row=2, column=0, sticky='w', pady=5)
        wickets_entry = tk.Entry(frame)
        wickets_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Best Figures:",font=('Helvetica', 12)).grid(row=3, column=0, sticky='w', pady=5)
        best_figures_entry = tk.Entry(frame)
        best_figures_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Average:",font=('Helvetica', 12)).grid(row=4, column=0, sticky='w', pady=5)
        average_entry = tk.Entry(frame)
        average_entry.grid(row=4, column=1, pady=5)

        tk.Label(frame, text="Economy:",font=('Helvetica', 12)).grid(row=5, column=0, sticky='w', pady=5)
        economy_entry = tk.Entry(frame)
        economy_entry.grid(row=5, column=1, pady=5)

        add_bowling_stats_button = tk.Button(frame, text="Add Bowling Stats",font=('Helvetica', 12), command=lambda: self.add_bowling_stats(
            player_id_entry.get(), innings_entry.get(), wickets_entry.get(), best_figures_entry.get(), average_entry.get(), economy_entry.get(), add_bowling_stats_window))
        add_bowling_stats_button.grid(row=6, columnspan=2, pady=10)


    def add_bowling_stats(self, player_id, innings, wickets, best_figures, average, economy, window):
        try:
            player_id = int(player_id)
            innings = int(innings)
            wickets = int(wickets)
            average = float(average)
            economy = float(economy)
            bowling_stats = BowlingStats (player_id,innings,wickets,best_figures,average,economy)
            add_bowling_stats(bowling_stats)
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")

    def show_view_stats_window(self):
        view_stats_window = tk.Toplevel(self.master)
        view_stats_window.title("View Stats")

        frame = tk.Frame(view_stats_window, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text="Player ID:",font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        player_id_entry = tk.Entry(frame)
        player_id_entry.grid(row=0, column=1, pady=5)

        view_stats_button = tk.Button(frame, text="View Stats",font=('Helvetica', 12), command=lambda: self.view_stats(
            player_id_entry.get(), view_stats_window))
        view_stats_button.grid(row=1, columnspan=2, pady=10)


    def view_stats(self, player_id, window):
        try:
            player_id = int(player_id)
            data = view_stats(player_id)
            if data[5]== None and data [12] == None:
                messagebox.showerror ("Error","No Record Found for this ID")
                window.destroy()
            else:
                output_text = "\n".join([f"Name: {data[0]}",f"Country: {data[1]}",f"Age: {data[2]}",f"Role: {data[3]}",f"Innings: {data[4]}",f"Runs: {data[5]}",f"Average: {data[6]}",f"Strike Rate: {data[7]}",f"Highest Score: {data[8]}",f"Innings (Bowling): {data[9]}",f"Wickets: {data[10]}",f"Best Figures: {data[11]}",f"Average (Bowling): {data[12]}",f"Economy: {data[13]}"])
                window.destroy()
                view_output_window = tk.Toplevel(self.master)
                view_output_window.title("View Stats Output")

                output_label = tk.Label(view_output_window, text=output_text, justify="left")
                output_label.pack(pady=10)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid Player ID.")

    def input_id (self):
        edit_player_id = simpledialog.askinteger("Edit Player", "Enter the ID of the player you want to edit:")
    
        if edit_player_id is not None:
                self.selected_player_id = edit_player_id
                self.show_edit_player_window()
        if self.selected_player_id is None:
                messagebox.showwarning("Warning", "Please select a player before editing.")
                return
    def input_id_batting(self):
        edit_player_id = simpledialog.askinteger("Edit Player", "Enter the ID of the player you want to edit:")
    
        if edit_player_id is not None:
                self.selected_player_id = edit_player_id
                self.show_edit_batting_stats_window()
        if self.selected_player_id is None:
                messagebox.showwarning("Warning", "Please select a player before editing.")
                return
    def input_id_bowling(self):
        edit_player_id = simpledialog.askinteger("Edit Player", "Enter the ID of the player you want to edit:")
    
        if edit_player_id is not None:
                self.selected_player_id = edit_player_id
                self.show_edit_bowling_stats_window()
        if self.selected_player_id is None:
                messagebox.showwarning("Warning", "Please select a player before editing.")
                return
        
    def show_edit_player_window(self):

        edit_player_window = tk.Toplevel(self.master)
        edit_player_window.title("Edit Player")

        player_details = fetch_player_details(self.selected_player_id)
        if player_details == None:
            messagebox.showerror("Error","No Record Found for this ID.")
        else:
            tk.Label(edit_player_window, text="Player ID:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5)
            player_id_label = tk.Label(edit_player_window, text=player_details[0])
            player_id_label.grid(row=0, column=1, pady=5)

            tk.Label(edit_player_window, text="Name:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5)
            name_entry = tk.Entry(edit_player_window)
            name_entry.insert(0, player_details[1])
            name_entry.grid(row=1, column=1, pady=5)

            tk.Label(edit_player_window, text="Country:", font=('Helvetica', 12)).grid(row=2, column=0, pady=5)
            country_entry = tk.Entry(edit_player_window)
            country_entry.insert(0, player_details[2])
            country_entry.grid(row=2, column=1, pady=5)

            tk.Label(edit_player_window, text="Age:", font=('Helvetica', 12)).grid(row=3, column=0, pady=5)
            age_entry = tk.Entry(edit_player_window)
            age_entry.insert(0, player_details[3])
            age_entry.grid(row=3, column=1, pady=5)

            tk.Label(edit_player_window, text="Role:", font=('Helvetica', 12)).grid(row=4, column=0, pady=5)
            role_options = ["Batsman", "Bowler", "All-Rounder"]
            role_var = tk.StringVar(edit_player_window)
            role_dropdown = tk.OptionMenu(edit_player_window, role_var, *role_options)
            role_dropdown.grid(row=4, column=1, pady=5)
            role_var.set(player_details[4])

            update_button = tk.Button(edit_player_window, text="Update Player", font=('Helvetica', 12), command=lambda: self.edit_player(
                player_details[0], name_entry.get(), country_entry.get(), age_entry.get(), role_var.get(), edit_player_window))
            update_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_player(self, player_id, name, country, age, role, window):
        try:
            age = int(age)
            if age < 15:
                raise ValueError("Age must be 15 or above.")

            if not all(entry.strip() for entry in [name, country, role]):
                raise ValueError("Name, Country, and Role are mandatory fields.")

            update_player(player_id, name.upper(), country.upper(), age, role)
            messagebox.showinfo("Success", "Player details updated successfully!")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            window.destroy()

    def show_edit_batting_stats_window(self):
        if self.selected_player_id is not None:
            player_id = int(self.selected_player_id)
            batting_stats = fetch_batting_stats(player_id)
            edit_batting_stats_window = tk.Toplevel(self.master)
            edit_batting_stats_window.title("Edit Batting Stats")
            print(batting_stats)
            if batting_stats == None:
                messagebox.showerror("Error","No Record Found for this ID.")
            else:
                tk.Label(edit_batting_stats_window, text="Player ID:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5)
                player_id_label = tk.Label(edit_batting_stats_window, text=batting_stats[0])
                player_id_label.grid(row=0, column=1, pady=5)

                tk.Label(edit_batting_stats_window, text="Matches:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5)
                innings_entry = tk.Entry(edit_batting_stats_window)
                innings_entry.insert(0, batting_stats[1])
                innings_entry.grid(row=1, column=1, pady=5)

                tk.Label(edit_batting_stats_window, text="Runs:", font=('Helvetica', 12)).grid(row=2, column=0, pady=5)
                runs_entry = tk.Entry(edit_batting_stats_window)
                runs_entry.insert(0, batting_stats[2])
                runs_entry.grid(row=2, column=1, pady=5)

                tk.Label(edit_batting_stats_window, text="Average:", font=('Helvetica', 12)).grid(row=3, column=0, pady=5)
                average_entry = tk.Entry(edit_batting_stats_window)
                average_entry.insert(0, batting_stats[3])
                average_entry.grid(row=3, column=1, pady=5)

                tk.Label(edit_batting_stats_window, text="Strike Rate:", font=('Helvetica', 12)).grid(row=4, column=0, pady=5)
                strike_rate_entry = tk.Entry(edit_batting_stats_window)
                strike_rate_entry.insert(0, batting_stats[4])
                strike_rate_entry.grid(row=4, column=1, pady=5)

                tk.Label(edit_batting_stats_window, text="Highest Score:", font=('Helvetica', 12)).grid(row=5, column=0, pady=5)
                highest_score_entry = tk.Entry(edit_batting_stats_window)
                highest_score_entry.insert(0, batting_stats[5])
                highest_score_entry.grid(row=5, column=1, pady=5)

                update_button = tk.Button(edit_batting_stats_window, font=('Helvetica', 12),text="Update Batting Stats", command=lambda: self.edit_batting_stats(
                    batting_stats[0], innings_entry.get(), runs_entry.get(), average_entry.get(), strike_rate_entry.get(), highest_score_entry.get(), edit_batting_stats_window))
                update_button.grid(row=6, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error","No Record Exists for this ID")

    def edit_batting_stats(self, player_id, innings, runs, average, strike_rate,high_score,  window):
        try:
            player_id = int(player_id)
            innings = int(innings)
            runs = int(runs)
            highest_score = high_score
            average = float(average)
            strike_rate = float(strike_rate)
            update_batting_stats(player_id, innings, runs, average, strike_rate,highest_score)

            messagebox.showinfo("Success", "Batting stats updated successfully!")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", "Invalid Input")
            window.destroy()

    def show_edit_bowling_stats_window(self):
        if self.selected_player_id is not None:
            player_id = int(self.selected_player_id)
            bowling_stats = fetch_bowling_stats(player_id)
            edit_bowling_stats_window = tk.Toplevel(self.master)
            edit_bowling_stats_window.title("Edit Bowling Stats")
            if bowling_stats == None:
                messagebox.showerror("Error","No Record Found for this ID.")
            else:
                tk.Label(edit_bowling_stats_window, text="Player ID:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5)
                player_id_label = tk.Label(edit_bowling_stats_window, text=bowling_stats[0])
                player_id_label.grid(row=0, column=1, pady=5)

                tk.Label(edit_bowling_stats_window, text="Innings:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5)
                innings_entry = tk.Entry(edit_bowling_stats_window)
                innings_entry.insert(0, bowling_stats[1])
                innings_entry.grid(row=1, column=1, pady=5)

                tk.Label(edit_bowling_stats_window, text="Wickets:", font=('Helvetica', 12)).grid(row=2, column=0, pady=5)
                wickets_entry = tk.Entry(edit_bowling_stats_window)
                wickets_entry.insert(0, bowling_stats[2])
                wickets_entry.grid(row=2, column=1, pady=5)

                tk.Label(edit_bowling_stats_window, text="Best Figures:", font=('Helvetica', 12)).grid(row=3, column=0, pady=5)
                best_figures_entry = tk.Entry(edit_bowling_stats_window)
                best_figures_entry.insert(0, bowling_stats[3])
                best_figures_entry.grid(row=3, column=1, pady=5)

                tk.Label(edit_bowling_stats_window, text="Average:", font=('Helvetica', 12)).grid(row=4, column=0, pady=5)
                average_entry = tk.Entry(edit_bowling_stats_window)
                average_entry.insert(0, bowling_stats[4])
                average_entry.grid(row=4, column=1, pady=5)

                tk.Label(edit_bowling_stats_window, text="Economy:", font=('Helvetica', 12)).grid(row=5, column=0, pady=5)
                economy_entry = tk.Entry(edit_bowling_stats_window)
                economy_entry.insert(0, bowling_stats[5])
                economy_entry.grid(row=5, column=1, pady=5)

                update_button = tk.Button(edit_bowling_stats_window, text="Update Bowling Stats", font=('Helvetica', 12), command=lambda: self.edit_bowling_stats(
                    bowling_stats[0], innings_entry.get(), wickets_entry.get(), best_figures_entry.get(), average_entry.get(), economy_entry.get(), edit_bowling_stats_window))
                update_button.grid(row=6, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error","No Record Exists for this ID")

    def edit_bowling_stats(self, player_id, innings, wickets, best_figures, average,economy,  window):
        try:
            player_id = int(player_id)
            innings = int(innings)
            wickets = int(wickets)
            best_figures = best_figures
            average = float(average)
            economy = float(economy)
            update_bowling_stats(player_id, innings, wickets,best_figures,average,economy)

            messagebox.showinfo("Success", "Bowling stats updated successfully!")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", "Invalid Input")
            window.destroy()
    
    def show_view_all_window(self):
        data = view_all_players()
        if data != []:
            view_all_window = tk.Toplevel(self.master)
            view_all_window.title("View All Players")

            output_text = tk.Text(view_all_window, height=80, width=80)
            output_text.pack()
            for item in data:
                output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Country: {item[2]} Age: {item[3]} Role: {item[4]}\n")
        else:
            messagebox.showerror ("Error","Empty Record. Add to view.")
    
    def show_list_most_runs_window(self):
        list_by_most_runs_window = tk.Toplevel(self.master)
        list_by_most_runs_window.title("List by Most Runs")

        output_text = tk.Text(list_by_most_runs_window, height=10, width=40)
        output_text.pack()

        data = list_by_most_runs()
        for item in data:
            output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Runs: {item[2]}\n")

    def show_list_highest_score_window(self):
        list_highest_score_window = tk.Toplevel(self.master)
        list_highest_score_window.title("List by Highest Score")

        output_text = tk.Text(list_highest_score_window, height=10, width=40)
        output_text.pack()

        data = list_by_highest_score()
        for item in data:
            output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Score: {item[2]}\n")

    def show_list_most_wickets_window(self):
        list_most_wickets_window = tk.Toplevel(self.master)
        list_most_wickets_window.title("List by Most Wickets")

        output_text = tk.Text(list_most_wickets_window, height=10, width=40)
        output_text.pack()

        data = list_by_most_wickets()
        for item in data:
            output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Wickets: {item[2]}\n")

    def show_list_average_window(self):
        list_average_window = tk.Toplevel(self.master)
        list_average_window.title("List by Average")

        output_text = tk.Text(list_average_window, height=10, width=40)
        output_text.pack()

        data = list_by_average()
        for item in data:
            output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Average: {item[2]}\n")

    def show_list_best_figures_window(self):
        list_best_figures_window = tk.Toplevel(self.master)
        list_best_figures_window.title("List by Best Figures")

        output_text = tk.Text(list_best_figures_window)
        output_text.pack()

        data = list_by_best_figures()
        for item in data:
            output_text.insert(tk.END, f"ID: {item[0]} Name: {item[1]} Figures: {item[2]}\n")

    def show_list_by_country_window(self):
        list_by_country_window = tk.Toplevel(self.master)
        list_by_country_window.title("List by Country")

        frame = tk.Frame(list_by_country_window, padx=20, pady=10)
        frame.pack()
        tk.Label(frame, text="Country:",font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        country_entry = tk.Entry(frame)
        country_entry.grid(row=0, column=1, pady=5)

        list_by_country_button = tk.Button(frame, text="List by Country",font=('Helvetica', 12) ,command=lambda: self.list_by_country(
            country_entry.get(), list_by_country_window))
        list_by_country_button.grid(row=1, columnspan=2, pady=10)


    def list_by_country(self, country, window):
        data = list_by_country(country.upper())

        window.destroy()

        view_output_window = tk.Toplevel(self.master)
        view_output_window.title("List by Country Output")

        output_label = tk.Label(view_output_window, text="", justify="left")
        output_label.pack(pady=10)

        if data:
            output_text = "\n".join([f"ID: {item[0]}\t Name: {item[1]}" for item in data])
            output_label.config(text=output_text)
        else:
            output_label.config(text="No players found for the given country.")

    def show_delete_player_window(self):
        delete_player_window = tk.Toplevel(self.master)
        delete_player_window.title("Delete Player")

        frame = tk.Frame(delete_player_window, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text="Player ID:",font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        player_id_entry = tk.Entry(frame)
        player_id_entry.grid(row=0, column=1, pady=5)

        delete_player_button = tk.Button(frame, text="Delete Player",font=('Helvetica', 12), command=lambda: self.delete_player(
            player_id_entry.get(), delete_player_window))
        delete_player_button.grid(row=1, columnspan=2, pady=10)

    def delete_player(self, player_id, window):
        try:
            player_id = int(player_id)
            delete_player(player_id)
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid Player ID.")

#######################################################################################################################################################
#############PRESENTATION LAYER##########################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = CricInfo(root)
    root.geometry("1280x720")
    root.resizable(width=False, height=False)
    root.mainloop()