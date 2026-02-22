from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper: find an event by ID to avoid repeating lookup logic
def find_event(event_id):
    return next((event for event in events if event.id == event_id), None)


# Welcome route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


# GET /events - Return all events as a JSON array
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Validate that JSON body contains a title
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Auto-increment ID based on the current max
    new_id = max((event.id for event in events), default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
