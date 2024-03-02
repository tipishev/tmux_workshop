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

class RoverState(Enum):
    GOING_TO_SOL = 1
    GOING_TO_ICE = 2
    AT_SOL = 3
    AT_ICE = 4

# State transitions table
state_transitions = {
    RoverState.GOING_TO_SOL: {
        "move_to_sol": RoverState.AT_SOL,
        "move_to_ice": RoverState.GOING_TO_ICE,
    },
    RoverState.GOING_TO_ICE: {
        "move_to_sol": RoverState.GOING_TO_SOL,
        "move_to_ice": RoverState.AT_ICE,
    },
    RoverState.AT_SOL: {
        "move_to_sol": RoverState.AT_SOL,
        "move_to_ice": RoverState.GOING_TO_ICE,
    },
    RoverState.AT_ICE: {
        "move_to_sol": RoverState.GOING_TO_SOL,
        "move_to_ice": RoverState.AT_ICE,
    }
}

# Endpoint to move rover
@app.route("/move_rover", methods=["POST"])
def move_rover():
    data = request.json
    rover_name = data["rover"]
    destination = data["destination"]
    current_state = state["rovers"][rover_name]["state"]
    
    # Check if the action is valid for the current state
    if current_state in state_transitions and data["action"] in state_transitions[current_state]:
        # Update the rover's location and state
        state["rovers"][rover_name]["location"] = destination
        state["rovers"][rover_name]["state"] = state_transitions[current_state][data["action"]]
        save_state()
        return jsonify({"message": f"{rover_name} moved to {destination}"}), 200
    else:
        return jsonify({"message": "Invalid action for the current state"}), 400


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
                    "location": 1,
                    "state": "to Sol",
                    "cargo": {"energy": 0, "water": 0},
                },
                "Rover2": {
                    "location": 10,
                    "state": "to Ice",
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


scheduler = BackgroundScheduler()
scheduler.add_job(produce_resources, "interval", seconds=1)
scheduler.start()

# Endpoint to get current state
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)
