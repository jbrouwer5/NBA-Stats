import tkinter as tk
from tkinter import ttk, Text
from tkinterQueryHelper import get_players, get_player_stats, get_teams, get_team_stats, get_top_scorers

# Define the NBA colors
NBA_BLUE = '#17408B'
NBA_RED = '#E03A3E'
NBA_GRAY = '#8A8D8F'
NBA_WHITE = '#FFFFFF'
NBA_BLACK = '#000000'

# Create the main application window
root = tk.Tk()
root.title('NBA Stats App')
root.geometry('1200x800')
root.configure(bg=NBA_BLUE)

# Create a container for the different frames
container = tk.Frame(root)
container.pack(fill='both', expand=True)

# Configure the container to expand with the window
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create a dictionary to store the frames
frames = {}

def show_frame(frame_name):
    frame = frames[frame_name]
    frame.tkraise()

# Define the Intro Frame
class IntroFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLACK)
        tk.Label(self, text='Welcome to the NBA Stats App!', font=('Helvetica', 24), fg=NBA_WHITE, bg=NBA_RED).pack(pady=20)
        tk.Button(self, text='Player Stats', font=('Helvetica', 16), command=lambda: show_frame('PlayerStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Team Stats', font=('Helvetica', 16), command=lambda: show_frame('TeamStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Top Scorers', font=('Helvetica', 16), command=lambda: show_frame('TopScorersFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)

# Define the Player Stats Frame with autocomplete combobox
class PlayerStatsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Player Stats', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Player:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.player_combo = AutocompleteCombobox(self)
        self.player_combo.pack()
        
        ttk.Label(self, text='Select Season:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.season_combo = ttk.Combobox(self, values=['2023', '2022', '2021', '2020', '2019', '2018'])
        self.season_combo.pack()
        
        tk.Button(self, text='Show Stats', command=self.show_stats, bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        
        self.results = Text(self, height=10, width=60)
        self.results.pack(pady=10)
        
        self.populate_players()

    def populate_players(self):
        players = get_players()
        self.player_combo.set_completion_list(players)

    def show_stats(self):
        player_name = self.player_combo.get()
        season_year = self.season_combo.get()
        
        if player_name and season_year:
            stats = get_player_stats(player_name, season_year)
            if stats:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, f'Games Played: {stats[0]}\n')
                self.results.insert(tk.END, f'Points: {stats[1]}\n')
                self.results.insert(tk.END, f'Rebounds: {stats[2]}\n')
                self.results.insert(tk.END, f'Assists: {stats[3]}\n')
                self.results.insert(tk.END, f'Steals: {stats[4]}\n')
                self.results.insert(tk.END, f'Blocks: {stats[5]}\n')
            else:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'No stats available for this player and season.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select both a player and a season.')

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())
        
        _hits = [item for item in self._completion_list if item.lower().startswith(self.get().lower())]
        
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        
        if _hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)
            self.delete(0, tk.END)
            self.insert(0, _hits[self._hit_index])
            self.select_range(self.position, tk.END)
    
    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down'):
            return
        
        if event.keysym in ('Return', 'Tab'):
            return
        
        self.autocomplete()

# Define the Team Stats Frame with autocomplete combobox
class TeamStatsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Team Stats', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Team:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.team_combo = AutocompleteCombobox(self)
        self.team_combo.pack()
        
        ttk.Label(self, text='Select Season:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.season_combo = ttk.Combobox(self, values=['2023', '2022', '2021', '2020', '2019', '2018'])
        self.season_combo.pack()
        
        tk.Button(self, text='Show Stats', command=self.show_stats, bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        
        self.results = Text(self, height=10, width=60)
        self.results.pack(pady=10)
        
        self.populate_teams()

    def populate_teams(self):
        teams = get_teams()
        self.team_combo.set_completion_list(teams)

    def show_stats(self):
        team_name = self.team_combo.get()
        season_year = self.season_combo.get()
        
        if team_name and season_year:
            stats = get_team_stats(team_name, season_year)
            if stats:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, f'Games Played: {stats[0]}\n')
                self.results.insert(tk.END, f'Total Points: {stats[1]}\n')
                self.results.insert(tk.END, f'Points Scored Per Game: {stats[2]}\n')
                self.results.insert(tk.END, f'Points Allowed Per Game: {stats[3]}\n')
                self.results.insert(tk.END, f'Wins: {stats[4]}\n')
                self.results.insert(tk.END, f'Losses: {stats[5]}\n')
            else:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'No stats available for this team and season.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select both a team and a season.')

# Define the Top Scorers Frame
class TopScorersFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Top Scorers', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Season:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.season_combo = ttk.Combobox(self, values=['2023', '2022', '2021', '2020', '2019', '2018'])
        self.season_combo.pack()
        
        ttk.Label(self, text='Number of Top Scorers:', background=NBA_BLUE, foreground=NBA_WHITE).pack()
        self.num_top_scorers = ttk.Spinbox(self, from_=1, to=100)
        self.num_top_scorers.pack()
        
        tk.Button(self, text='Show Top Scorers', command=self.show_top_scorers, bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_RED, fg=NBA_WHITE).pack(pady=10)
        
        self.results = Text(self, height=10, width=60)
        self.results.pack(pady=10)

    def show_top_scorers(self):
        season_year = self.season_combo.get()
        num_scorers = self.num_top_scorers.get()
        
        if season_year and num_scorers:
            try:
                num_scorers = int(num_scorers)
                top_scorers = get_top_scorers(num_scorers, season_year)
                if top_scorers:
                    self.results.delete('1.0', tk.END)
                    for scorer in top_scorers:
                        self.results.insert(tk.END, f'{scorer[0]}: {scorer[1]} PPG\n')
                else:
                    self.results.delete('1.0', tk.END)
                    self.results.insert(tk.END, 'No data available for this season.')
            except ValueError:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'Please enter a valid number of top scorers.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select a season and enter the number of top scorers.')

# Add the frames to the container
for F in (IntroFrame, PlayerStatsFrame, TeamStatsFrame, TopScorersFrame):
    frame = F(container)
    frames[F.__name__] = frame
    frame.grid(row=0, column=0, sticky='nsew')

# Configure each frame to expand with the container
for frame in frames.values():
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

# Show the intro frame first
show_frame('IntroFrame')

# Run the main loop
root.mainloop()
