from flask import Flask, render_template, request, redirect, url_for
import requests
import random

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "63f4945d921d599f27ae4fdf5bada3f1"

saved_players = []

INSULTS = [
    "Let’s just thank God you’re not a manager.",
    "Selection complete… football has been saved from your decisions.",
    "Done. UEFA is reviewing your choices as we speak.",
    "Process finished — your squad is… questionable at best.",
    "Selection complete. The fans are already protesting.",
    "Congratulations, you’ve officially been banned from scouting.",
    "Done. Even Sunday League wouldn’t accept this lineup.",
    "Selection finished — HR will be in touch.",
    "Great job. Please never manage a team again.",
    "Process complete. Your tactics scare me.",
]

GOALKEEPERS = [
    "Alisson",
    "Ederson",
    "Thibaut Courtois",
    "Marc-Andre ter Stegen",
    "Jan Oblak",
    "Manuel Neuer",
    "Gianluigi Donnarumma",
    "Mike Maignan",
    "Emiliano Martinez",
    "David De Gea",
    "Keylor Navas",
    "Hugo Lloris",
    "Jordan Pickford",
    "Aaron Ramsdale",
    "Andre Onana",
]

OUTFIELD_PLAYERS = [
    "Erling Haaland",
    "Kylian Mbappe",
    "Vinicius Junior",
    "Jude Bellingham",
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Eduardo Camavinga",
    "Mohamed Salah",
    "Harry Kane",
    "Rodri",
    "Bukayo Saka",
    "Phil Foden",
    "Jamal Musiala",
    "Florian Wirtz",
    "Cole Palmer",
    "Lamine Yamal",
    "Robert Lewandowski",
    "Luka Modric",
    "Martin Odegaard",
    "Virgil van Dijk",
    "Neymar",
    "Jorge DeGuzzman",
    "Bruno Fernandes",
    "Heung-min Son",
    "Marcus Aurelias",
]


@app.route("/")
def index():
    if len(saved_players) >= 11:
        return render_template(
            "index.html",
            player=None,
            saved_players=saved_players,
            insult=random.choice(INSULTS),
        )

    if not saved_players:
        target_name = random.choice(GOALIES)
        is_gk = True
    else:
        target_name = random.choice(OUTFIELD_PLAYERS)
        is_gk = False

    signed = any(p["name"] == target_name for p in saved_players)
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={target_name}"
    player_data = {
        "name": target_name,
        "image": "",
        "position": "Pro",
        "team": "Club",
        "is_gk": is_gk,
        "exists": signed,
    }

    try:
        r = requests.get(url)
        data = r.json()
        if data and data.get("player"):
            p = data["player"][0]
            player_data["name"] = p.get("strPlayer")
            player_data["image"] = p.get("strRender") or p.get("strThumb") or ""
            player_data["team"] = p.get("strTeam") or "Elite Club"
            player_data["position"] = p.get("strPosition") or "Star"
    except:
        pass

    return render_template(
        "index.html", player=player_data, saved_players=saved_players
    )


@app.route("/save", methods=["POST"])
def save():
    name = request.form.get("player_name")
    image = request.form.get("player_image")
    is_gk = request.form.get("is_gk") == "True"

    if len(saved_players) < 11 and not any(p["name"] == name for p in saved_players):
        saved_players.append({"name": name, "image": image, "is_gk": is_gk})
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    global saved_players
    saved_players = []
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
