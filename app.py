import os
import json
import anthropic
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert travel rewards advisor who helps people maximize credit card sign-up bonuses for specific trips. You have deep knowledge of:

- All major US credit card sign-up bonuses (Chase Sapphire Preferred/Reserve, Amex Platinum/Gold/Green, Capital One Venture/Venture X, Citi Premier, Bilt, etc.)
- Transfer partners: which cards transfer to which airlines and hotel programs, and at what ratios
- Point valuations: current estimated cent-per-point values for each program
- How many points/miles are typically needed for the described trip (economy, business, first class)
- Annual fees and whether they're worth it for the sign-up bonus alone
- Key rules: Chase 5/24, Amex once-per-lifetime bonus rules, etc.

When a user describes a trip, you:
1. Estimate how many points/miles are needed for that trip in the requested class
2. Identify which transfer partners are most useful (e.g., if flying United, Chase UR transfers to United)
3. Rank the top 5-7 credit cards by their value for THIS specific trip
4. For each card, clearly state:
   - Card name and issuer
   - Current sign-up bonus (and minimum spend required)
   - Estimated bonus value in dollars for this specific trip
   - Which transfer partner to use and how the points get there
   - Annual fee (and whether the first-year value justifies it)
   - Any important caveats (5/24, once-per-lifetime, etc.)

Be specific, practical, and honest. If the user already has certain cards, factor that in. Format your response with clear sections and use markdown formatting (headers, bullet points, bold text) for readability."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    destination = data.get("destination", "").strip()
    origin = data.get("origin", "").strip()
    travel_class = data.get("travel_class", "economy")
    num_travelers = data.get("num_travelers", "1")
    preferred_airlines = data.get("preferred_airlines", "").strip()
    preferred_hotels = data.get("preferred_hotels", "").strip()
    existing_cards = data.get("existing_cards", "").strip()
    flexibility = data.get("flexibility", "").strip()

    if not destination:
        return {"error": "Please provide a destination."}, 400

    user_message_parts = [f"I want to travel to **{destination}**"]
    if origin:
        user_message_parts.append(f"from {origin}")
    user_message_parts.append(f"in **{travel_class}** class")
    if num_travelers and num_travelers != "1":
        user_message_parts.append(f"for **{num_travelers} travelers**")

    user_message = " ".join(user_message_parts) + ".\n\n"

    if preferred_airlines:
        user_message += f"**Preferred airlines:** {preferred_airlines}\n"
    if preferred_hotels:
        user_message += f"**Preferred hotels/chains:** {preferred_hotels}\n"
    if existing_cards:
        user_message += f"**Cards I already have (so I can't get their bonus again):** {existing_cards}\n"
    if flexibility:
        user_message += f"**Additional context:** {flexibility}\n"

    user_message += "\nWhat credit cards should I sign up for to maximize points/miles for this trip? Please rank your recommendations and explain the strategy."

    def generate():
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
