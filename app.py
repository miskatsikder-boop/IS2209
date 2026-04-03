from flask import Flask, render_template, request, redirect
import requests
import random
import os

app = Flask(__name__)

saved_players = []

# List of real player names to "scout" from
PLAYER_POOL = ["Erling Haaland", "Lionel Messi", "Kylian Mbappe", "Bukayo Saka",
               "Marcus Rashford", "Kevin De Bruyne", "Vinicius Junior", "Mohamed Salah"]


@app.route("/")
def index():
    # Pick a random name from our pool
    target_name = random.choice(PLAYER_POOL)

    # Fetch real data from TheSportsDB using the test key '123'
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchplayers.php?p={target_name}"
    response = requests.get(url)
    data = response.json()

    # Get the first player found in the search
    player = data["player"][0]

    player_name = player["strPlayer"]
    player_image = player["strThumb"]  # This is the official player photo
    position = player["strPosition"]
    team = player["strTeam"]

    return render_template(
        "index.html",
        player_image=player_image,
        player_name=player_name,
        position=position,
        team=team,
        saved_players=saved_players
    )


@app.route("/save", methods=["POST"])
def save():
    player_image = request.form.get("player_image")
    player_name = request.form.get("player_name")

    if player_image:
        saved_players.append({
            "name": player_name,
            "image": player_image
        })

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "OK"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)