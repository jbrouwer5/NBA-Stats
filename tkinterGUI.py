import tkinter as tk
from tkinter import ttk, Text
from tkinterQueryHelper import get_players, get_player_stats

# Define the NBA colors
NBA_BLUE = '#17408B'
NBA_RED = '#E03A3E'
NBA_GRAY = '#8A8D8F'
NBA_WHITE = '#FFFFFF'
NBA_BLACK = '#000000'


# Create the main application window
root = tk.Tk()
root.title('NBA Stats App')
root.geometry('1600x1200')
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
        tk.Button(self, text='Coach Stats', font=('Helvetica', 16), command=lambda: show_frame('CoachStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Team Stats', font=('Helvetica', 16), command=lambda: show_frame('TeamStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Arena Stats', font=('Helvetica', 16), command=lambda: show_frame('ArenaStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE).pack(pady=10)

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
                self.results.insert(tk.END, f'Field Goals 2PT: {stats[1]}\n')
                self.results.insert(tk.END, f'Field Goals 3PT: {stats[2]}\n')
                self.results.insert(tk.END, f'Free Throws: {stats[3]}\n')
                self.results.insert(tk.END, f'Rebounds: {stats[4]}\n')
                self.results.insert(tk.END, f'Assists: {stats[5]}\n')
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

# Add the frames to the container
for F in (IntroFrame, PlayerStatsFrame):
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
