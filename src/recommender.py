"""Core music recommendation engine: load songs, score them, and rank recommendations."""

import csv


# ---------------------------------------------------------------------------
# Scoring Mode Strategies (Challenge 2)
# ---------------------------------------------------------------------------

SCORING_MODES = {
    "balanced": {
        "genre": 2.0,
        "mood": 1.0,
        "energy": 1.0,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.3,
        "popularity": 0.3,
        "decade": 0.5,
        "mood_tag": 0.8,
        "instrumentalness": 0.3,
        "lyricalness": 0.3,
    },
    "genre-first": {
        "genre": 4.0,
        "mood": 0.5,
        "energy": 0.5,
        "valence": 0.3,
        "danceability": 0.3,
        "acousticness": 0.2,
        "popularity": 0.2,
        "decade": 0.3,
        "mood_tag": 0.4,
        "instrumentalness": 0.2,
        "lyricalness": 0.2,
    },
    "mood-first": {
        "genre": 0.5,
        "mood": 3.0,
        "energy": 0.8,
        "valence": 1.0,
        "danceability": 0.5,
        "acousticness": 0.3,
        "popularity": 0.2,
        "decade": 0.3,
        "mood_tag": 2.0,
        "instrumentalness": 0.3,
        "lyricalness": 0.3,
    },
    "energy-focused": {
        "genre": 0.5,
        "mood": 0.5,
        "energy": 3.0,
        "valence": 0.5,
        "danceability": 1.5,
        "acousticness": 0.5,
        "popularity": 0.2,
        "decade": 0.2,
        "mood_tag": 0.4,
        "instrumentalness": 0.3,
        "lyricalness": 0.2,
    },
    "discovery": {
        "genre": 0.0,
        "mood": 1.5,
        "energy": 1.5,
        "valence": 1.0,
        "danceability": 0.8,
        "acousticness": 0.5,
        "popularity": 0.5,
        "decade": 0.3,
        "mood_tag": 1.0,
        "instrumentalness": 0.4,
        "lyricalness": 0.3,
    },
}


def load_songs(filepath="data/songs.csv"):
    """Load songs from a CSV file and return a list of dictionaries with typed values."""
    songs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in ("energy", "valence", "danceability", "acousticness",
                        "instrumentalness", "lyricalness"):
                row[key] = float(row[key])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["popularity"] = int(row["popularity"])
            row["release_decade"] = int(row["release_decade"])
            songs.append(row)
    return songs


def score_song(user_prefs, song, mode="balanced"):
    """Score a single song against user preferences using a chosen scoring mode."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons = []

    # Genre match (categorical)
    if weights["genre"] > 0 and song["genre"] == user_prefs.get("favorite_genre"):
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts:.1f})")

    # Mood match (categorical)
    if weights["mood"] > 0 and song["mood"] == user_prefs.get("favorite_mood"):
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts:.1f})")

    # Mood tag match (categorical — Challenge 1)
    if weights["mood_tag"] > 0 and song.get("mood_tag") == user_prefs.get("target_mood_tag"):
        pts = weights["mood_tag"]
        score += pts
        reasons.append(f"mood_tag match (+{pts:.1f})")

    # Decade match (categorical — Challenge 1)
    if weights["decade"] > 0 and "target_decade" in user_prefs:
        if song.get("release_decade") == user_prefs["target_decade"]:
            pts = weights["decade"]
            score += pts
            reasons.append(f"decade match (+{pts:.1f})")

    # Popularity similarity (Challenge 1): closer to target = higher score
    if weights["popularity"] > 0 and "target_popularity" in user_prefs:
        gap = abs(song["popularity"] - user_prefs["target_popularity"]) / 100.0
        pts = round(weights["popularity"] * (1 - gap), 2)
        score += pts
        reasons.append(f"popularity similarity (+{pts:.2f})")

    # --- Numerical similarity features ---
    num_features = [
        ("energy",           "target_energy"),
        ("valence",          "target_valence"),
        ("danceability",     "target_danceability"),
        ("acousticness",     "target_acousticness"),
        ("instrumentalness", "target_instrumentalness"),
        ("lyricalness",      "target_lyricalness"),
    ]
    for feat, pref_key in num_features:
        w = weights.get(feat, 0)
        if w > 0 and pref_key in user_prefs:
            gap = abs(song[feat] - user_prefs[pref_key])
            pts = round(w * (1 - gap), 2)
            score += pts
            reasons.append(f"{feat} similarity (+{pts:.2f})")

    return round(score, 2), reasons


def _apply_diversity_penalty(scored_list, penalty=0.5):
    """Challenge 3: Greedily re-rank to penalize repeated artists/genres."""
    if not scored_list:
        return scored_list

    selected = []
    seen_artists = set()
    seen_genres = set()

    for item in scored_list:
        song = item["song"]
        adjusted = item["score"]

        # Penalize if artist already in selected list
        if song["artist"] in seen_artists:
            adjusted -= penalty
        # Penalize if genre already in selected list
        if song["genre"] in seen_genres:
            adjusted -= penalty * 0.5

        selected.append({
            "song": song,
            "score": item["score"],
            "adjusted_score": round(adjusted, 2),
            "reasons": item["reasons"],
        })

        seen_artists.add(song["artist"])
        seen_genres.add(song["genre"])

    # Re-sort by adjusted score
    selected.sort(key=lambda x: x["adjusted_score"], reverse=True)
    return selected


def recommend_songs(user_prefs, songs, k=5, mode="balanced", diversity=True):
    """Score all songs and return the top k recommendations sorted by score."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append({"song": song, "score": song_score, "reasons": reasons})

    # Initial sort by raw score
    scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)

    # Apply diversity penalty (Challenge 3)
    if diversity:
        scored_sorted = _apply_diversity_penalty(scored_sorted)

    return scored_sorted[:k]
