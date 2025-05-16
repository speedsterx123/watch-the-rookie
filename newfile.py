from flask import Flask, render_template_string, request
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

seasons = {
    "Season 1 (2018–2019)": [
        "Pilot", "Crash Course", "The Good, the Bad and the Ugly", "The Switch", "The Roundup", "The Hawke",
        "The Ride Along", "Time of Death", "Standoff", "Flesh and Blood", "Redwood", "Heartbreak", "Caught Stealing",
        "Plain Clothes Day", "Manhunt", "Greenlight", "The Shake Up", "Homefront", "The Checklist", "Free Fall",
    ],
    "Season 2 (2019–2020)": [
        "Impact", "The Night General", "The Bet", "Warriors and Guardians", "Tough Love", "Fallout", "Safety",
        "Clean Cut", "Breaking Point", "The Dark Side", "Day of Death", "Now and Then", "Follow-Up Day", "Casualties",
        "Hand-Off", "The Overnight", "Control", "Under the Gun", "The Q Word", "The Hunt",
    ],
    "Season 3 (2021)": [
        "Consequences", "In Justice", "La Fiera", "Sabotage", "Lockdown", "Revelations", "True Crime", "Bad Blood",
        "Amber", "Man of Honor", "New Blood", "Brave Heart", "Triple Duty", "Threshold",
    ],
    "Season 4 (2021–2022)": [
        "Life and Death", "Five Minutes", "In the Line of Fire", "Red Hot", "A.C.H.", "Poetic Justice", "Fire Fight",
        "Hit and Run", "Breakdown", "Heart Beat", "End Game", "The Knock", "Fight or Flight", "Long Shot", "Hit List",
        "Real Crime", "Coding", "Backstabbers", "Simone", "Enervo", "Mother's Day", "Day in the Hole",
    ],
    "Season 5 (2022–2023)": [
        "Double Down", "Labor Day", "Dye Hard", "The Choice", "The Fugitive", "The Reckoning", "Crossfire", "The Collar",
        "Take Back", "The List", "The Naked and the Dead", "Death Notice", "Daddy Cop", "Death Sentence", "The Con",
        "Exposed", "The Enemy Within", "Double Trouble", "A Hole in the World", "S.T.R.", "Going Under", "Under Siege",
    ],
    "Season 6 (2024)": [
        "Strike Back", "The Hammer", "Trouble in Paradise", "Pentagram Killer", "The Vow", "Lies and Secrets",
        "Desperate Nanny Search", "Open War", "The Noose Tightens", "The Escape",
    ],
    "Season 7 (2025)": [
        "Attention! New Recruits!", "A Neighborhood Superhero", "High Security", "The Threat", "To the End", "The Gala",
        "A Restless Night", "The Fire", "The Kiss", "The Veil of Lies", "Race Against the Bomb", "April Fools",
        "Bad Publicity", "Crime Crazies", "A Case Like No Other", "The Return", "Too Beautiful for Me",
        "The Good, the Bad, and the Oscar",
    ],
}

IMDB_ID = "tt7587890"

template = """
<!DOCTYPE html>
<html>
<head>
    <title>The Rookie Episodes</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #eee;
            margin: 0; padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            background-color: #222;
            width: 100%;
            padding: 20px 0;
            font-size: 2em;
            text-align: center;
            color: #61dafb;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.7);
        }
        main {
            display: flex;
            max-width: 1100px;
            width: 100%;
            margin: 20px;
            gap: 30px;
            flex-direction: {{ 'column' if is_mobile else 'row' }};
        }
        .seasons {
            flex: 1;
            max-width: 350px;
            overflow-y: auto;
            max-height: 80vh;
            background: #222;
            border-radius: 10px;
            padding: 15px;
        }
        .season {
            margin-bottom: 25px;
        }
        .season h2 {
            margin-bottom: 10px;
            border-bottom: 1px solid #444;
            padding-bottom: 5px;
            font-size: 1.3em;
        }
        .episode {
            margin: 6px 0;
        }
        .episode a {
            color: #61dafb;
            text-decoration: none;
            cursor: pointer;
            display: block;
            padding: 5px 8px;
            border-radius: 5px;
            transition: background-color 0.2s ease;
        }
        .episode a:hover {
            background-color: #333;
        }
        .player {
            flex: 2;
            background: #222;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 0 10px #61dafb;
            min-height: {{ '300px' if is_mobile else '450px' }};
            position: relative;
            margin-top: {{ '20px' if is_mobile else '0' }};
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 10px;
            z-index: 1;
            position: relative;
        }
        .no-selection {
            color: #777;
            font-style: italic;
            margin-top: 100px;
            text-align: center;
            position: relative;
            z-index: 1;
        }
        #search-box {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border-radius: 5px;
            border: none;
            font-size: 1em;
        }
    </style>
    <script>
        function playEpisode(seasonNum, episodeNum) {
            const iframe = document.getElementById('player-iframe');
            const noSelection = document.getElementById('no-selection');
            iframe.src = `https://vidsrc.to/embed/tv/{{ imdb_id }}/${seasonNum}/${episodeNum}`;
            noSelection.style.display = "none";

            document.querySelectorAll('.episode a').forEach(el => el.style.backgroundColor = '');
            const activeLink = document.getElementById('S' + seasonNum + 'E' + episodeNum);
            if (activeLink) {
                activeLink.style.backgroundColor = '#444';
            }
        }

        function filterEpisodes() {
            const input = document.getElementById('search-box');
            const filter = input.value.toLowerCase();
            const episodes = document.querySelectorAll('.episode');

            episodes.forEach(ep => {
                const text = ep.textContent.toLowerCase();
                if (text.indexOf(filter) > -1) {
                    ep.style.display = "";
                } else {
                    ep.style.display = "none";
                }
            });
        }
    </script>
</head>
<body>
    <header>The Rookie - Watch Episodes</header>
    <main>
        <div class="seasons">
            <input type="text" id="search-box" placeholder="Search episodes..." onkeyup="filterEpisodes()">
            {% for season_name, episodes in seasons.items() %}
            <div class="season">
                <h2>{{ season_name }}</h2>
                {% set season_num = loop.index %}
                {% for episode in episodes %}
                <div class="episode">
                    <a id="S{{season_num}}E{{loop.index}}" onclick="playEpisode({{season_num}}, {{loop.index}})" href="javascript:void(0);">
                        {{ loop.index }}. {{ episode }}
                    </a>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        <div class="player">
            <iframe id="player-iframe" src="" allowfullscreen allow="autoplay; fullscreen"></iframe>
            <div id="no-selection" class="no-selection">Select an episode to start watching.</div>
        </div>
    </main>
    <footer style="margin: 20px 0; color: #888; font-size: 0.9em; text-align: center;">
        OK
    </footer>
</body>
</html>
"""

@cache.cached(timeout=300)
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(mobile in user_agent for mobile in ['iphone', 'android', 'ipad', 'mobile'])
    return render_template_string(template, seasons=seasons, imdb_id=IMDB_ID, is_mobile=is_mobile)

if __name__ == '__main__':
    app.run(debug=True)