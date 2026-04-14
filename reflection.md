# Reflection

## Profile Comparison Notes

**High-Energy Pop vs. Chill Lofi:**
The pop profile's top 5 are all upbeat songs with high valence and danceability (Levitating, Blinding Lights, Shape of You). The lofi profile flips completely — Lofi Sunrise and Weightless dominate because they have low energy and a chill mood. This makes sense because the profiles target opposite ends of the energy spectrum (0.75 vs 0.20), so there is almost zero overlap in their top results.

**Deep Intense Rock vs. EDM Party:**
Both profiles target high energy (0.90 vs 0.85), but the genre and mood differences push them in very different directions. The rock profile picks Smells Like Teen Spirit and Thunderstruck, while the EDM profile picks Midnight City and Strobe. Interestingly, Thunderstruck (#2 for rock) also appears at #4 for EDM because it's high-energy and "energetic" mood matches — this shows how shared numerical features can bridge different genre preferences.

**Sad Acoustic vs. High-Energy Pop:**
These two profiles are the most extreme opposites. Sad Acoustic targets energy 0.10, valence 0.15 — the output is dominated by Nuvole Bianche and Clair de Lune (quiet classical pieces). High-Energy Pop targets energy 0.75, valence 0.85 — the output is all danceable pop hits. There is zero overlap in their top 5 lists, which validates that the scoring function meaningfully differentiates between user types.

**EDM Party vs. Chill Lofi:**
The EDM profile wants high energy (0.85) and high danceability (0.75). The lofi profile wants low energy (0.20) and low danceability (0.30). These are near-opposite on numerical features, and the genre/mood preferences are also completely different. The result: EDM gets Midnight City and Strobe while lofi gets Lofi Sunrise and Weightless. The system correctly separates "party music" from "study music."

---

## Personal Reflection

### Biggest Learning Moment

The most eye-opening part was the sensitivity experiment. When I doubled the energy weight and halved the genre weight, Lose Yourself (a hip-hop song) jumped from #4 to #2 in the rock profile. That single weight change fundamentally altered which genres appeared in the results. It made me realize that the "feel" of a recommendation system isn't just about the algorithm — it's about the specific numbers someone chose for the weights. Those choices are subjective design decisions disguised as math.

### How AI Tools Helped

AI tools were most helpful for generating the initial CSV dataset with realistic attribute values and for quickly scaffolding the boilerplate (CSV loading, CLI formatting). I needed to double-check the scoring math manually because it's easy for generated code to use the wrong formula — for example, rewarding high energy instead of closeness to the target energy. The distinction between "higher is better" and "closer is better" was a critical detail that required human judgment.

### What Surprised Me

I was surprised by how convincing the results felt even with just 20 songs and a simple point system. When the "Chill Lofi" profile returned Lofi Sunrise at #1 and Weightless at #2, it genuinely felt like a reasonable playlist suggestion. Simple algorithms can produce results that "feel" like real recommendations because they exploit the same feature signals (genre, mood, energy) that our brains use informally when we think about what music we like.

### What I Would Try Next

If I extended this project, I would:
1. Add a **genre similarity matrix** so "indie" and "rock" get partial credit instead of zero.
2. Implement a **diversity penalty** that prevents the same artist or genre from dominating the top results.
3. Build a **simple web UI** where users can adjust their profile sliders and see recommendations update in real time.
4. Add **collaborative filtering** — track which profiles liked which songs and use that to recommend songs that similar profiles enjoyed.
