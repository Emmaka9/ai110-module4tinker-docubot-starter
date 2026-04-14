# Music Recommender Model Card

## 1. Model Name

**VibeFinder 1.0** — A content-based music recommendation simulator.

---

## 2. Goal / Task

VibeFinder tries to predict which songs a user will enjoy based on their stated preferences for genre, mood, and numerical audio features (energy, valence, danceability). It takes a user taste profile and a song catalog, then returns a ranked list of the top matching songs with explanations for each score.

---

## 3. Data Used

- **Dataset size:** 20 songs in `data/songs.csv`
- **Features per song (14 total):** title, artist, genre, mood, energy (0-1), tempo_bpm, valence (0-1), danceability (0-1), acousticness (0-1), popularity (0-100), release_decade, mood_tag, instrumentalness (0-1), lyricalness (0-1)
- **Genre distribution:** pop (4), rock (3), electronic (3), hip-hop (3), classical (2), lofi (1), ambient (1), acoustic (1), indie (1), soul (1)
- **Limitations:** The dataset is hand-curated and small. Pop, rock, electronic, and hip-hop are over-represented. Genres like lofi, ambient, acoustic, indie, and soul each have only one song, making it impossible for the system to provide variety within those genres. There is no user listening history or collaborative data — all recommendations are purely attribute-based.

---

## 4. Algorithm Summary

The system uses a weighted point system to score each song against a user profile. In the default "balanced" mode:

1. **Genre match** — Exact match awards +2.0 points (binary).
2. **Mood match** — Exact match awards +1.0 point (binary).
3. **Mood tag match** — Exact match on detailed mood tag awards +0.8 (binary).
4. **Decade match** — Exact match on release decade awards +0.5 (binary).
5. **Popularity similarity** — `0.3 * (1 - |song - target| / 100)`. Awards up to +0.3.
6. **Energy similarity** — `1.0 * (1 - |song - target|)`. Awards up to +1.0.
7. **Valence similarity** — Closeness formula, weighted at 0.5. Awards up to +0.5.
8. **Danceability similarity** — Closeness formula, weighted at 0.5. Awards up to +0.5.
9. **Acousticness similarity** — Closeness formula, weighted at 0.3. Awards up to +0.3.
10. **Instrumentalness similarity** — Closeness formula, weighted at 0.3. Awards up to +0.3.
11. **Lyricalness similarity** — Closeness formula, weighted at 0.3. Awards up to +0.3.

Total possible score (balanced): ~7.5. The system supports 5 scoring modes (balanced, genre-first, mood-first, energy-focused, discovery) that redistribute these weights. A diversity penalty reduces scores for songs whose artist or genre already appears in the top results. Songs are sorted by adjusted score descending and the top *k* are returned.

---

## 5. Observed Behavior / Biases

- **Genre dominance:** Genre match is worth 2.0 points, which is 40% of the maximum score. A song from the "wrong" genre must score near-perfect on every other feature to compete. This creates a **filter bubble** where users rarely discover songs outside their preferred genre.
- **Pop over-representation:** With 4 pop songs vs. 1 lofi song, pop-preferring users get more varied recommendations while lofi-preferring users see the same song every time.
- **Binary categorical matching:** The system treats "rock" and "indie" as equally different from each other as "rock" and "classical." In reality, rock and indie share significant musical overlap.
- **No temporal or contextual awareness:** The system doesn't account for time of day, listening context, or recent activity. A user's morning preferences likely differ from late-night ones.
- **Same song, every list:** In the "Sad Acoustic" profile, Nuvole Bianche always ranks #1 with a near-perfect 4.98 score because there are only two classical songs. Adding more classical/sad songs would improve diversity.

---

## 6. Evaluation Process

Tested with 5 distinct user profiles designed to span different musical tastes:

| Profile | Top Result | Score | Feels Right? |
|---------|-----------|-------|-------------|
| High-Energy Pop | Levitating (Dua Lipa) | 4.91 | Yes — upbeat pop hit |
| Chill Lofi | Lofi Sunrise (Sleepy Fish) | 4.90 | Yes — relaxed lofi track |
| Deep Intense Rock | Smells Like Teen Spirit (Nirvana) | 3.95 | Yes — iconic intense rock |
| EDM Party | Midnight City (M83) | 4.85 | Yes — energetic electronic |
| Sad Acoustic | Nuvole Bianche (Einaudi) | 4.98 | Yes — quiet, melancholy piano |

**Sensitivity experiment:** Switching from "balanced" to "energy-focused" mode (energy 1.0->3.0, genre 2.0->0.5) caused cross-genre songs to rise (Lose Yourself jumped from #4 to #2 for the Rock profile). Using "discovery" mode (genre=0.0) completely removed genre bias. This confirmed that the weight balance is the most influential design decision in the system.

**Diversity penalty experiment:** Without the diversity penalty, the "High-Energy Pop" top 4 were all pop songs. With the penalty, the same songs appear but their adjusted scores reflect the repetition, and cross-genre songs with strong numerical matches become more competitive.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Educational simulation to learn how content-based recommenders work
- Demonstrating the relationship between feature weights and recommendation outcomes
- Exploring filter bubble effects in simple algorithms

**Not intended for:**
- Production music streaming (dataset is too small, no collaborative filtering)
- Making inferences about real user behavior or musical preferences
- Replacing human curation or editorial playlists

---

## 8. Ideas for Improvement

1. **Add genre similarity** — Instead of binary match, use a genre distance matrix so "indie" and "rock" are treated as partially similar rather than completely different.
2. **Expand the dataset** — A larger, more balanced catalog (100+ songs across all genres) would reduce over-representation bias and improve recommendation diversity.
3. **Build a web UI** — Let users adjust profile sliders in a browser and see recommendations update in real time, making the system interactive.
