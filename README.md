# Music Recommender Simulation

A Python-based music recommendation system that simulates how platforms like Spotify predict what users will love next. It uses a **content-based filtering** approach: matching song attributes (genre, mood, energy, valence, danceability) against user taste profiles to produce a ranked list of suggestions.

---

## How The System Works

### Real-World Context

Major streaming platforms use two main strategies to recommend music:

- **Collaborative filtering** leverages the behavior of millions of users. If User A and User B both loved songs X, Y, and Z, then a song User A loved that User B hasn't heard yet gets recommended to User B. This powers playlists like Spotify's "Discover Weekly."
- **Content-based filtering** looks at the attributes of the songs themselves — tempo, energy, mood, genre — and matches them against a user's known preferences. This is what our simulator implements.

Our system is a simplified content-based recommender. It reads a catalog of songs from a CSV file, compares each song's features against a user's taste profile, and returns the top matches with an explanation of why each song scored the way it did.

### Features Used

Each `Song` object contains:
- `genre` — categorical (pop, rock, electronic, hip-hop, lofi, classical, etc.)
- `mood` — categorical (happy, sad, chill, intense, energetic, epic, angry)
- `energy` — numeric 0.0–1.0 (how intense the track feels)
- `valence` — numeric 0.0–1.0 (musical positiveness / happiness)
- `danceability` — numeric 0.0–1.0 (how suitable for dancing)
- `acousticness` — numeric 0.0–1.0 (how acoustic the track is)
- `tempo_bpm` — integer (beats per minute)
- `popularity` — integer 0–100 (how mainstream the track is)
- `release_decade` — integer (decade the track was released, e.g. 2010)
- `mood_tag` — categorical detail tag (euphoric, aggressive, melancholic, dreamy, nostalgic, etc.)
- `instrumentalness` — numeric 0.0–1.0 (how instrumental the track is)
- `lyricalness` — numeric 0.0–1.0 (how lyric-focused the track is)

Each `UserProfile` contains:
- `favorite_genre` — preferred genre
- `favorite_mood` — preferred mood
- `target_energy` — ideal energy level (0.0–1.0)
- `target_valence` — ideal valence level (0.0–1.0)
- `target_danceability` — ideal danceability level (0.0–1.0)
- `target_acousticness` — ideal acousticness level (0.0–1.0)
- `target_popularity` — ideal popularity (0–100)
- `target_decade` — preferred release decade
- `target_mood_tag` — preferred mood tag
- `target_instrumentalness` — ideal instrumentalness (0.0–1.0)
- `target_lyricalness` — ideal lyricalness (0.0–1.0)

### Algorithm Recipe

The scoring function evaluates each song against a user profile using these weighted rules:

| Feature | Rule | Max Points (Balanced) |
|---------|------|----------------------|
| Genre | Exact match with `favorite_genre` | +2.0 |
| Mood | Exact match with `favorite_mood` | +1.0 |
| Mood Tag | Exact match with `target_mood_tag` | +0.8 |
| Decade | Exact match with `target_decade` | +0.5 |
| Popularity | `0.3 * (1 - abs(song - target) / 100)` | +0.3 |
| Energy | `1.0 * (1 - abs(song - target))` | +1.0 |
| Valence | `0.5 * (1 - abs(song - target))` | +0.5 |
| Danceability | `0.5 * (1 - abs(song - target))` | +0.5 |
| Acousticness | `0.3 * (1 - abs(song - target))` | +0.3 |
| Instrumentalness | `0.3 * (1 - abs(song - target))` | +0.3 |
| Lyricalness | `0.3 * (1 - abs(song - target))` | +0.3 |

**Maximum possible score (balanced): ~7.5**

The system supports **5 scoring modes** that shift the weight distribution:
- **balanced** — default weights, genre-heavy
- **genre-first** — genre boosted to 4.0, everything else reduced
- **mood-first** — mood boosted to 3.0, mood_tag to 2.0, genre drops to 0.5
- **energy-focused** — energy boosted to 3.0, danceability to 1.5, genre/mood reduced
- **discovery** — genre weight set to 0.0 to encourage cross-genre exploration

A **diversity penalty** (Challenge 3) reduces adjusted scores by 0.5 if an artist already appears in the results, and by 0.25 if the genre already appears. This prevents the top list from being dominated by one artist or genre.

After scoring every song, the system sorts descending and returns the top *k* results.

### Potential Biases

- This system may over-prioritize genre since it's worth 2x the next highest feature. A great mood/energy match from a different genre gets penalized.
- The dataset is small (20 songs) and genre distribution is uneven — pop has 4 entries while some genres have only 1, which biases results toward better-represented genres.
- Categorical matching is binary (match or no match), ignoring that "indie" and "rock" are closer than "indie" and "classical."

### Data Flow

```
Input (User Prefs)
       |
       v
Process (Loop through every song in CSV)
       |  -- score_song() judges each song --
       v
Output (Sort by score, return Top K)
```

---

## Setup

### Install Python dependencies

    pip install -r requirements.txt

### Run the recommender

    python -m src.main

This loads 20 songs from `data/songs.csv`, runs 5 user profiles, and prints ranked recommendations with scores and explanations.

---

## Project Structure

```
data/songs.csv          # Song catalog (20 tracks, 14 attributes each)
src/
  __init__.py            # Package init
  recommender.py         # Core logic: load_songs, score_song, recommend_songs,
                         #   5 scoring modes, diversity penalty
  main.py                # CLI runner with 5 user profiles, mode comparison,
                         #   tabulate-based ASCII table output
model_card.md            # Model Card documenting the system
reflection.md            # Personal reflection on the process
requirements.txt         # Python dependencies (includes tabulate)
```

---

## User Profiles Tested

| Profile | Genre | Mood | Energy | MoodTag | Decade | Popularity |
|---------|-------|------|--------|---------|--------|-----------|
| High-Energy Pop | pop | happy | 0.75 | euphoric | 2020 | 90 |
| Chill Lofi | lofi | chill | 0.20 | dreamy | 2020 | 40 |
| Deep Intense Rock | rock | intense | 0.90 | aggressive | 1990 | 85 |
| EDM Party | electronic | energetic | 0.85 | euphoric | 2010 | 80 |
| Sad Acoustic | classical | sad | 0.10 | melancholic | 2000 | 65 |

---

## Sample Output

```
==========================================================================================
  Profile: High-Energy Pop   |   Mode: balanced
  Genre=pop  Mood=happy  Energy=0.75  Valence=0.85  Dance=0.7
  MoodTag=euphoric  Decade=2020  Popularity=90
==========================================================================================
+---+-----------------+-------------+------------+--------------+--------------------------------------------+
| # | Title           | Artist      | Genre/Mood | Score        | Reasons                                    |
+===+=================+=============+============+==============+============================================+
| 1 | Levitating      | Dua Lipa    | pop/happy  | 7.37         | genre match (+2.0), mood match (+1.0)      |
|   |                 |             |            |              | mood_tag match (+0.8), decade match (+0.5) |
|   |                 |             |            |              | popularity similarity (+0.29)              |
|   |                 |             |            |              | energy similarity (+0.94), ...             |
+---+-----------------+-------------+------------+--------------+--------------------------------------------+
| 2 | Blinding Lights | The Weeknd  | pop/happy  | 7.32 -> 7.07 | genre match (+2.0), mood match (+1.0)     |
|   |                 |             |            |              | (diversity penalty applied: same genre)    |
+---+-----------------+-------------+------------+--------------+--------------------------------------------+
```

Note: `Score -> AdjustedScore` indicates the diversity penalty was applied because the song's artist or genre already appeared higher in the results.

---

## Sensitivity Experiment

**Change:** Switched from `balanced` mode to `energy-focused` mode (energy weight 1.0 -> 3.0, genre weight 2.0 -> 0.5).

**Result:** Cross-genre songs with matching energy levels rose significantly. For the "Deep Intense Rock" profile, Lose Yourself (hip-hop) jumped from #4 to #2 because its perfect energy match now outweighed the genre penalty. In `discovery` mode (genre weight = 0.0), Get Lucky appeared in the EDM results despite being tagged `happy` not `energetic`, because its numerical features aligned well. This confirms that the weight distribution is the single most influential design decision.

## Optional Extensions Implemented

- **Challenge 1: Advanced Features** — Added 5 new attributes (popularity, release_decade, mood_tag, instrumentalness, lyricalness) with math-based scoring rules for each.
- **Challenge 2: Multiple Scoring Modes** — 5 modes (balanced, genre-first, mood-first, energy-focused, discovery) using a Strategy-like dict pattern. The CLI runs a full mode comparison.
- **Challenge 3: Diversity Penalty** — Songs are penalized (-0.5 artist, -0.25 genre) if their artist or genre already appears higher in the results. Shown as `Score -> AdjustedScore` in the output.
- **Challenge 4: Visual Summary Table** — Output uses the `tabulate` library with ASCII grid formatting. Each table row shows rank, title, artist, genre/mood, score, and wrapped reasons.
