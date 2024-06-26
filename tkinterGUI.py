import tkinter as tk
from tkinter import ttk, Text
from tkinter.scrolledtext import ScrolledText
from tkinterQueryHelper import get_players, get_player_stats, get_teams, get_team_stats, \
                                get_top_scorers, get_player_teams, get_player_career_stats, \
                                    get_champion_data, get_all_time_scorers, get_biased_refs, \
                                    get_top_champions, get_winningest_arenas

# Define the NBA colors
NBA_BLUE = '#17408B'
NBA_RED = '#E03A3E'
NBA_GRAY = '#8A8D8F'
NBA_WHITE = '#FFFFFF'
NBA_BLACK = '#000000'

# Create the main application window
root = tk.Tk()
root.title('NBA Stats App')
root.geometry('1000x1200')
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

seasons = [str(2023-i) for i in range(2023-1945)] 
# Define the Intro Frame
class IntroFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLACK)
        header_width = 40
        header_height = 3
        subtitle_width = 40
        subtitle_height = 2
        button_width = 30
        button_height = 3
        header_font_size = 24
        subtitle_font_size = 18
        button_font_size = 18
        
        # Main title
        tk.Label(self, text='Welcome to the NBA Stats App!', font=('Helvetica', header_font_size), fg=NBA_WHITE, bg=NBA_RED, width=header_width, height=header_height).pack(pady=10)
        
        # Subtitle
        tk.Label(self, text='Providing statistics on everything NBA', font=('Helvetica', subtitle_font_size), fg=NBA_WHITE, bg=NBA_BLACK, width=subtitle_width, height=subtitle_height).pack(pady=10)
        
        # Buttons
        tk.Button(self, text='Player Season Stats', font=('Helvetica', button_font_size), command=lambda: show_frame('PlayerStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Team Season Stats', font=('Helvetica', button_font_size), command=lambda: show_frame('TeamStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Top Season Scorers', font=('Helvetica', button_font_size), command=lambda: show_frame('TopScorersFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Teams Played For', font=('Helvetica', button_font_size), command=lambda: show_frame('TeamsPlayedForFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Player Career Stats', font=('Helvetica', button_font_size), command=lambda: show_frame('PlayerCareerStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Champion Statistics', font=('Helvetica', button_font_size), command=lambda: show_frame('ChampionStatsFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='All Time Scorers', font=('Helvetica', button_font_size), command=lambda: show_frame('AllTimeScorersFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Most Biased Refs', font=('Helvetica', button_font_size), command=lambda: show_frame('BiasedRefsFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Top Champion Scorers', font=('Helvetica', button_font_size), command=lambda: show_frame('TopChampionFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)
        tk.Button(self, text='Top Arenas', font=('Helvetica', button_font_size), command=lambda: show_frame('TopArenasFrame'), bg=NBA_BLACK, fg=NBA_BLUE, width=button_width, height=button_height).pack(pady=10)

# Define the Player Stats Frame with autocomplete combobox
class PlayerStatsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Player Season Stats', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Player:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.player_combo = AutocompleteCombobox(self)
        self.player_combo.pack()
        
        ttk.Label(self, text='Select Season:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.season_combo = ttk.Combobox(self, values=seasons)
        self.season_combo.pack()
        
        tk.Button(self, text='Show Stats', command=self.show_stats, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
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
                self.results.insert(tk.END, f'Points Per Game: {stats[1]}\n')
                self.results.insert(tk.END, f'Rebounds Per Game: {stats[2]}\n')
                self.results.insert(tk.END, f'Assists Per Game: {stats[3]}\n')
                self.results.insert(tk.END, f'Steals Per Game: {stats[4]}\n')
                self.results.insert(tk.END, f'Blocks Per Game: {stats[5]}\n')
            else:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'No stats available for this player and season.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select both a player and a season.')

# Define the Player Career Stats Frame
class PlayerCareerStatsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Player Career Stats', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Player:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.player_combo = AutocompleteCombobox(self)
        self.player_combo.pack()
        
        tk.Button(self, text='Show Career Stats', command=self.show_career_stats, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = ScrolledText(self, height=12, width=60)
        self.results.pack(pady=10)
        
        self.populate_players()

    def populate_players(self):
        players = get_players()
        self.player_combo.set_completion_list(players)

    def show_career_stats(self):
        player_name = self.player_combo.get()
        
        if player_name:
            career_stats = get_player_career_stats(player_name)
            if career_stats:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, f'Total Games Played: {career_stats[0]}\n')
                self.results.insert(tk.END, f'Total Points: {career_stats[1]}\n')
                self.results.insert(tk.END, f'Total Rebounds: {career_stats[2]}\n')
                self.results.insert(tk.END, f'Total Assists: {career_stats[3]}\n')
                self.results.insert(tk.END, f'Total Steals: {career_stats[4]}\n')
                self.results.insert(tk.END, f'Total Blocks: {career_stats[5]}\n')
                self.results.insert(tk.END, f'Points Per Game: {career_stats[6]}\n')
                self.results.insert(tk.END, f'Rebounds Per Game: {career_stats[7]}\n')
                self.results.insert(tk.END, f'Assists Per Game: {career_stats[8]}\n')
                self.results.insert(tk.END, f'Steals Per Game: {career_stats[9]}\n')
                self.results.insert(tk.END, f'Blocks Per Game: {career_stats[10]}\n')
            else:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'No career stats available for this player.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select a player.')

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
        tk.Label(self, text='Team Season Stats', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Team:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.team_combo = AutocompleteCombobox(self)
        self.team_combo.pack()
        
        ttk.Label(self, text='Select Season:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.season_combo = ttk.Combobox(self, values=seasons)
        self.season_combo.pack()
        
        tk.Button(self, text='Show Stats', command=self.show_stats, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
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
                self.results.insert(tk.END, f'Wins: {stats[4]}\n')
                self.results.insert(tk.END, f'Losses: {stats[5]}\n')
                self.results.insert(tk.END, f'Points Scored Per Game: {stats[2]}\n')
                self.results.insert(tk.END, f'Points Allowed Per Game: {stats[3]}\n')
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
        tk.Label(self, text='Top Season Scorers', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Season:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.season_combo = ttk.Combobox(self, values=seasons)
        self.season_combo.pack()
        
        ttk.Label(self, text='Number of Top Scorers:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.num_top_scorers = ttk.Spinbox(self, from_=1, to=100)
        self.num_top_scorers.pack()
        
        tk.Button(self, text='Show Top Scorers', command=self.show_top_scorers, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
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

# Define the Teams Played For Frame
class TeamsPlayedForFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Teams Played For', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        ttk.Label(self, text='Select Player:', background=NBA_WHITE, foreground=NBA_BLUE).pack()
        self.player_combo = AutocompleteCombobox(self)
        self.player_combo.pack()
        
        tk.Button(self, text='Show Teams', command=self.show_teams, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=10, width=60)
        self.results.pack(pady=10)
        
        self.populate_players()

    def populate_players(self):
        players = get_players()
        self.player_combo.set_completion_list(players)

    def show_teams(self):
        player_name = self.player_combo.get()
        
        if player_name:
            teams = get_player_teams(player_name)
            if teams:
                self.results.delete('1.0', tk.END)
                for team in teams:
                    self.results.insert(tk.END, f'{team[0]}: {team[1]}\n')
            else:
                self.results.delete('1.0', tk.END)
                self.results.insert(tk.END, 'No teams found for this player.')
        else:
            self.results.delete('1.0', tk.END)
            self.results.insert(tk.END, 'Please select a player.')

# Define the Team Statistics Frame
class ChampionStatsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Champion History', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        # tk.Button(self, text='Show Statistics', command=self.show_statistics, bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=50, width=60)
        self.results.pack(pady=10)
        
        self.show_statistics()  # Automatically show statistics on load

    def show_statistics(self):
        team_stats = get_champion_data()
        
        self.results.delete('1.0', tk.END)
        if team_stats:
            for team in team_stats:
                self.results.insert(tk.END, f'{team[0]}: {team[1]} Points\n')
        else:
            self.results.insert(tk.END, 'No team statistics available.')

# Define the Team Statistics Frame
class AllTimeScorersFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='All Time Scorers', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=10, width=60)
        self.results.pack(pady=10)
        
        self.show_statistics()  # Automatically show statistics on load

    def show_statistics(self):
        team_stats = get_all_time_scorers()
        
        self.results.delete('1.0', tk.END)
        if team_stats:
            for team in team_stats:
                self.results.insert(tk.END, f'{team[0]}: {team[1]} Points\n')
        else:
            self.results.insert(tk.END, 'No team statistics available.')

# Define the Team Statistics Frame
class BiasedRefsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Most Biased Refs', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=50, width=60)
        self.results.pack(pady=10)
        
        self.show_statistics()  # Automatically show statistics on load

    def show_statistics(self):
        stats = get_biased_refs()
        
        self.results.delete('1.0', tk.END)
        if stats:
            for stat in stats:
                self.results.insert(tk.END, f'Name: {stat[0]}\n')
                self.results.insert(tk.END, f'Total Games Officiated: {stat[2]}\n')
                self.results.insert(tk.END, f'Wins Officated: {stat[1]}\n')
                self.results.insert(tk.END, f'Home Win Percentage: {stat[3]}\n\n')
        else:
            self.results.insert(tk.END, 'No ref statistics available.')

# Define the Team Statistics Frame
class TopChampionFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Top Champion Scorers', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=50, width=60)
        self.results.pack(pady=10)
        
        self.show_statistics()  # Automatically show statistics on load

    def show_statistics(self):
        stats = get_top_champions()
        
        self.results.delete('1.0', tk.END)
        if stats:
            for stat in stats:
                self.results.insert(tk.END, f'{stat[0]} {stat[1]}: {stat[2]}, {stat[3]} Points\n')
        else:
            self.results.insert(tk.END, 'No team statistics available.')

# Define the Team Statistics Frame
class TopArenasFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=NBA_BLUE)
        tk.Label(self, text='Most Winning Arenas', font=('Helvetica', 20), fg=NBA_WHITE, bg=NBA_BLUE).pack(pady=10)
        
        tk.Button(self, text='Back', command=lambda: show_frame('IntroFrame'), bg=NBA_WHITE, fg=NBA_BLUE).pack(pady=10)
        
        self.results = Text(self, height=30, width=80)
        self.results.pack(pady=10)
        
        self.show_statistics()  # Automatically show statistics on load

    def show_statistics(self):
        stats = get_winningest_arenas()
        
        self.results.delete('1.0', tk.END)
        if stats:
            for stat in stats:
                self.results.insert(tk.END, f'{stat[0]}: Games - {stat[3]}, Wins - {stat[2]}, Win Percentage - {round(stat[2] / stat[3],2)}\n')
        else:
            self.results.insert(tk.END, 'No team statistics available.')

# Add the frames to the container
for F in (IntroFrame, PlayerStatsFrame, TeamStatsFrame, TopScorersFrame, TeamsPlayedForFrame,
 PlayerCareerStatsFrame, ChampionStatsFrame, AllTimeScorersFrame, BiasedRefsFrame, 
 TopChampionFrame, TopArenasFrame):
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
