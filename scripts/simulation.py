from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os

app = Flask(__name__)
STATE_FILE = "state.json"

ICE = 1
SOL = 10
MAP = [ICE, 2, 3, 4, 5, 6, 7, 8, 9, SOL]

# Rover states
TO_SOL = "going to Sol"
TO_ICE = "going to Ice"
AT_SOL = "at Sol"
AT_ICE = "at Ice"

# Rover commands
GO_TO_SOL = "go to Sol!"
GO_TO_ICE = "go to Ice!"

# State transitions table
# {current_state: {command: resulting_state}, ...}
state_transitions = {
    TO_SOL: {GO_TO_SOL: TO_SOL, GO_TO_ICE: TO_ICE},
    TO_ICE: {GO_TO_SOL: TO_SOL, GO_TO_ICE: TO_ICE},
    AT_SOL: {GO_TO_SOL: AT_SOL, GO_TO_ICE: TO_ICE},
    AT_ICE: {GO_TO_SOL: TO_SOL, GO_TO_ICE: AT_ICE},
}

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
                "Chip": {
                    "location": SOL,
                    "state": AT_SOL,
                    "energy": 0,
                    "water": 0,
                },
                "Dale": {
                    "location": ICE,
                    "state": AT_ICE,
                    "energy": 0,
                    "water": 0,
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
    if sol["water"] > 0: # water is needed for cooling the solar panels
        # spend one unit of water to produce two units of energy
        sol["water"] -= 1
        sol["energy"] += 2

    ice = state["bases"]["Ice"]
    if ice["energy"] > 0: # energy is needed for heating the ice
        # spend one unit of energy to produce two units of water
        ice["energy"] -= 1
        ice["water"] += 2
    save_state()

# Scheduled task for rover movement and cargo loading.
# If rover is at Sol, load one unit of energy per second, until the cargo of 10 units is full.
# If rover is at Ice, load one unit of water per second, until the cargo of 10 units is full.
# If rover is going to Sol, move one step per second towards Sol (+1).
# If rover is going to Ice, move one step per second towards Ice (-1).
def move_rover():
    for rover in state["rovers"].values():
        if rover["state"] == AT_SOL:
            sol = state["bases"]["Sol"]
            # try to unload the water from rover first
            if rover["water"] > 0:
                rover["water"] -= 1
                sol["water"] += 1
            # try to load the energy
            elif rover["energy"] < 10 and sol["energy"] > 0:
                sol["energy"] -= 1
                rover["energy"] += 1
            # if full, go to Ice
            elif rover["energy"] == 10:
                rover["state"] = TO_ICE
        elif rover["state"] == AT_ICE:
            ice = state["bases"]["Ice"]
            # try to unload the energy from rover first
            if rover["energy"] > 0:
                rover["energy"] -= 1
                ice["energy"] += 1
            # try to load the water
            elif rover["water"] < 10 and ice["water"] > 0:
                ice["water"] -= 1
                rover["water"] += 1
            # if full, go to Sol
            elif rover["water"] == 10:
                rover["state"] = TO_SOL
        elif rover["state"] == TO_SOL:
            rover["location"] += 1
            if rover["location"] == SOL:
                rover["state"] = AT_SOL
        elif rover["state"] == TO_ICE:
            rover["location"] -= 1
            if rover["location"] == ICE:
                rover["state"] = AT_ICE
    save_state()


scheduler = BackgroundScheduler()

# TODO combine these jobs into one?
scheduler.add_job(produce_resources, "interval", seconds=1)
scheduler.add_job(move_rover, "interval", seconds=1)

scheduler.start()

# Endpoint to get current state
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(state)

# Endpoint to get current base state, base name is passed as a query parameter
@app.route("/base", methods=["GET"])
def get_base():
    base_name = request.args.get("name")
    return jsonify(state["bases"][base_name])

# Endpoint to get current rover state, rover name is passed as a query parameter
@app.route("/rover", methods=["GET"])
def get_rover():
    rover_name = request.args.get("name")
    return jsonify(state["rovers"][rover_name])

# Endpoint to change a rover destination
@app.route("/rover", methods=["POST"])
def move_rover():
    rover_name = request.json["rover"]
    command = request.json["command"]
    rover = state["rovers"][rover_name]
    current_state = rover["state"]
    state["rovers"][rover_name]["state"] = state_transitions[current_state][command]

if __name__ == "__main__":
    app.run(debug=True)