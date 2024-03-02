from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
from enum import Enum

app = Flask(__name__)
STATE_FILE = "state.json"

SOL = 1
ICE = 10
MAP = [SOL, 2, 3, 4, 5, 6, 7, 8, 9, ICE]

# Rover states
TO_SOL = "going to Sol"
TO_ICE = "going to Ice"
AT_SOL = "at Sol"
AT_ICE = "at Ice"

# Rover commands
GO_TO_SOL = "go to Sol"
GO_TO_ICE = "go to Ice"

# State transitions table
# {current_state: {command: resulting_state}, ...}
state_transitions = {
    TO_SOL: {GO_TO_SOL: TO_SOL, GO_TO_ICE: TO_ICE},
    TO_ICE: {GO_TO_SOL: TO_SOL, GO_TO_ICE: TO_ICE},
    AT_SOL: {GO_TO_SOL: AT_SOL, GO_TO_ICE: TO_ICE},
    AT_ICE: {GO_TO_SOL: TO_SOL, GO_TO_ICE: AT_ICE},
}

# Endpoint to move rover
@app.route("/move_rover", methods=["POST"])
def move_rover():
    rover_name = request.json["rover"]
    command = request.json["command"]
    rover = state["rovers"][rover_name]
    current_state = rover["state"]
    state["rovers"][rover_name]["state"] = state_transitions[current_state][command]


def init_state(state_file=STATE_FILE):
    if os.path.exists(state_file):
        with open(state_file, "r") as file:
            return json.load(file)
    else:
        # Default state
        state = {
            "bases": {
                "Sol": {"energy": 10, "water": 10},
                "Ice": {"energy": 10, "water": 10},
            },
            "rovers": {
                "Rover1": {
                    "location": SOL,
                    "state": AT_SOL,
                    "cargo": {"energy": 0, "water": 0},
                },
                "Rover2": {
                    "location": ICE,
                    "state": AT_ICE,
                    "cargo": {"energy": 0, "water": 0},
                },
            },
        }
        with open(state_file, "w") as file:
            json.dump(state, file)
        return state


state = init_state()


def save_state():
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)


# Scheduled task for resource production
def produce_resources():
    sol = state["bases"]["Sol"]
    if sol["water"] > 0:
        # spend one unit of water to produce two units of energy
        sol["water"] -= 1
        sol["energy"] += 2

    ice = state["bases"]["Ice"]
    if ice["energy"] > 0:
        # spend one unit of energy to produce two units of water
        ice["energy"] -= 1
        ice["water"] += 2
    save_state()

# Scheduled task for rover movement and cargo loading
def move_rover():
    for rover in state["rovers"]:
        rover = state["rovers"][rover]
        if rover["state"] == TO_SOL:
            rover["location"] -= 1
            if rover["location"] == SOL:
                rover["state"] = AT_SOL
        elif rover["state"] == TO_ICE:
            rover["location"] += 1
            if rover["location"] == ICE:
                rover["state"] = AT_ICE
        elif rover["state"] == AT_SOL:
            sol = state["bases"]["Sol"]
            cargo = rover["cargo"]
            if sol["energy"] >= 1 and cargo["energy"] < 10:
                sol["energy"] -= 1
                cargo["energy"] += 1
        elif rover["state"] == AT_ICE:
            ice = state["bases"]["Ice"]
            cargo = rover["cargo"]
            if ice["water"] >= 1 and cargo["water"] < 10:
                ice["water"] -= 1
                cargo["water"] += 1
    save_state()

scheduler = BackgroundScheduler()
scheduler.add_job(produce_resources, "interval", seconds=1)
scheduler.add_job(move_rover, "interval", seconds=1)
scheduler.start()

# Endpoint to get current state
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)  