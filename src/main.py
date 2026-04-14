"""CLI runner for the Music Recommender Simulation."""

from tabulate import tabulate
from src.recommender import load_songs, recommend_songs, SCORING_MODES


# ---------------------------------------------------------------------------
# User Profiles (with advanced features from Challenge 1)
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "target_valence": 0.85,
        "target_danceability": 0.70,
        "target_acousticness": 0.10,
        "target_popularity": 90,
        "target_decade": 2020,
        "target_mood_tag": "euphoric",
        "target_instrumentalness": 0.0,
        "target_lyricalness": 0.85,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.20,
        "target_valence": 0.50,
        "target_danceability": 0.30,
        "target_acousticness": 0.85,
        "target_popularity": 40,
        "target_decade": 2020,
        "target_mood_tag": "dreamy",
        "target_instrumentalness": 0.75,
        "target_lyricalness": 0.10,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.30,
        "target_danceability": 0.45,
        "target_acousticness": 0.05,
        "target_popularity": 85,
        "target_decade": 1990,
        "target_mood_tag": "aggressive",
        "target_instrumentalness": 0.05,
        "target_lyricalness": 0.75,
    },
    "EDM Party": {
        "favorite_genre": "electronic",
        "favorite_mood": "energetic",
        "target_energy": 0.85,
        "target_valence": 0.60,
        "target_danceability": 0.75,
        "target_acousticness": 0.05,
        "target_popularity": 80,
        "target_decade": 2010,
        "target_mood_tag": "euphoric",
        "target_instrumentalness": 0.40,
        "target_lyricalness": 0.50,
    },
    "Sad Acoustic": {
        "favorite_genre": "classical",
        "favorite_mood": "sad",
        "target_energy": 0.10,
        "target_valence": 0.15,
        "target_danceability": 0.10,
        "target_acousticness": 0.95,
        "target_popularity": 65,
        "target_decade": 2000,
        "target_mood_tag": "melancholic",
        "target_instrumentalness": 0.95,
        "target_lyricalness": 0.05,
    },
}


# ---------------------------------------------------------------------------
# Challenge 4: Visual Summary Table using tabulate
# ---------------------------------------------------------------------------

def print_recommendations(profile_name, prefs, recommendations, mode):
    """Display recommendations as a formatted ASCII table."""
    print("=" * 90)
    print(f"  Profile: {profile_name}   |   Mode: {mode}")
    print(f"  Genre={prefs['favorite_genre']}  Mood={prefs['favorite_mood']}  "
          f"Energy={prefs['target_energy']}  Valence={prefs['target_valence']}  "
          f"Dance={prefs['target_danceability']}")
    print(f"  MoodTag={prefs.get('target_mood_tag', 'N/A')}  "
          f"Decade={prefs.get('target_decade', 'N/A')}  "
          f"Popularity={prefs.get('target_popularity', 'N/A')}")
    print("=" * 90)

    rows = []
    for rank, rec in enumerate(recommendations, start=1):
        song = rec["song"]
        adj = rec.get("adjusted_score")
        score_str = str(rec["score"])
        if adj is not None and adj != rec["score"]:
            score_str += f" -> {adj}"
        reason_text = ", ".join(rec["reasons"])
        # Wrap long reason text for readability
        wrapped = _wrap_reasons(reason_text, width=48)
        rows.append([
            rank,
            song["title"],
            song["artist"],
            f"{song['genre']}/{song['mood']}",
            score_str,
            wrapped,
        ])

    headers = ["#", "Title", "Artist", "Genre/Mood", "Score", "Reasons"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()


def _wrap_reasons(text, width=48):
    """Wrap a long reason string to fit in a table cell."""
    words = text.split(", ")
    lines = []
    current = ""
    for w in words:
        candidate = f"{current}, {w}" if current else w
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return "\n".join(lines)


def main():
    """Load songs, run recommendations for each profile and mode, and display results."""
    songs = load_songs()
    print(f"\nLoaded songs: {len(songs)}")
    print(f"Available scoring modes: {', '.join(SCORING_MODES.keys())}\n")

    # Run each profile with the default "balanced" mode
    for name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5, mode="balanced", diversity=True)
        print_recommendations(name, prefs, recs, mode="balanced")

    # --- Challenge 2 demo: run one profile across all modes ---
    demo_profile = "High-Energy Pop"
    demo_prefs = PROFILES[demo_profile]
    print("\n" + "#" * 90)
    print(f"  SCORING MODE COMPARISON — Profile: {demo_profile}")
    print("#" * 90 + "\n")

    for mode_name in SCORING_MODES:
        recs = recommend_songs(demo_prefs, songs, k=5, mode=mode_name, diversity=True)
        print_recommendations(demo_profile, demo_prefs, recs, mode=mode_name)


if __name__ == "__main__":
    main()
