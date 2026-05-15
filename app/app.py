"""
Atilim University - Cloud Computing Assignment
Simple in-memory app, no database used
Boutique Hotel Chain - Cloud Booking Platform
Designed for deployment on AWS EC2 (IaaS)
"""

from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)
# In-Memory Sample Data

HOTELS = [
    {
        "id": "HTL-001",
        "name": "Konyaaltı Breeze Hotel",
        "city": "Antalya",
        "district": "Konyaaltı",
        "address": "Konyaaltı Bulvarı No:42, Antalya, Turkey",
        "stars": 4,
        "description": "A serene beachfront retreat on the stunning Konyaaltı coastline, "
                       "offering panoramic views of the Taurus Mountains meeting the Mediterranean.",
        "amenities": ["outdoor pool", "private beach", "spa", "restaurant", "free wifi", "parking"],
        "phone": "+90 242 111 0001",
        "email": "konyaalti@boutiquehotels.com",
    },
    {
        "id": "HTL-002",
        "name": "Kaleiçi Old Town Suites",
        "city": "Antalya",
        "district": "Kaleiçi",
        "address": "Hadrian Sokak No:7, Kaleiçi, Antalya, Turkey",
        "stars": 4,
        "description": "Nestled inside Antalya's UNESCO-listed Roman harbour district, "
                       "this boutique property blends Ottoman architecture with contemporary comfort.",
        "amenities": ["rooftop terrace", "city tour desk", "restaurant", "free wifi", "bar"],
        "phone": "+90 242 111 0002",
        "email": "kaleici@boutiquehotels.com",
    },
    {
        "id": "HTL-003",
        "name": "Cappadocia Cave & Sky Lodge",
        "city": "Göreme",
        "district": "Cappadocia",
        "address": "Müze Caddesi No:15, Göreme, Nevşehir, Turkey",
        "stars": 5,
        "description": "Experience the magic of Cappadocia in hand-carved cave rooms with "
                       "direct views of the fairy chimneys and nightly hot-air balloon ascents.",
        "amenities": [
            "cave rooms", "hot-air balloon tours", "wine cellar", "hammam",
            "rooftop terrace", "free wifi", "airport shuttle",
        ],
        "phone": "+90 384 111 0003",
        "email": "goreme@boutiquehotels.com",
    },
    {
        "id": "HTL-004",
        "name": "Bodrum Aegean Pearl Resort",
        "city": "Bodrum",
        "district": "Yalıkavak",
        "address": "Yalıkavak Sahil Yolu No:22, Bodrum, Muğla, Turkey",
        "stars": 5,
        "description": "An adults-only escape perched above the crystal-clear Aegean Sea, "
                       "celebrated for its infinity pool, Michelin-recognised cuisine, and sunset views.",
        "amenities": [
            "infinity pool", "private pier", "yacht charter", "fine dining",
            "spa", "free wifi", "concierge", "gym",
        ],
        "phone": "+90 252 111 0004",
        "email": "bodrum@boutiquehotels.com",
    },
]

ROOMS = [
    # Konyaaltı Breeze Hotel
    {"room_id": "R-001-STD", "hotel_id": "HTL-001", "type": "Standard Sea View",
     "capacity": 2, "price_per_night": 120, "available": True,
     "features": ["sea view", "king bed", "balcony", "air conditioning"]},
    {"room_id": "R-001-DLX", "hotel_id": "HTL-001", "type": "Deluxe Beachfront",
     "capacity": 2, "price_per_night": 180, "available": True,
     "features": ["direct beach access", "king bed", "terrace", "minibar"]},
    {"room_id": "R-001-FAM", "hotel_id": "HTL-001", "type": "Family Suite",
     "capacity": 4, "price_per_night": 260, "available": False,
     "features": ["sea view", "two bedrooms", "kitchenette", "bunk beds"]},

    # Kaleiçi Old Town Suites
    {"room_id": "R-002-STD", "hotel_id": "HTL-002", "type": "Classic Ottoman Room",
     "capacity": 2, "price_per_night": 110, "available": True,
     "features": ["city view", "double bed", "stone walls", "air conditioning"]},
    {"room_id": "R-002-DLX", "hotel_id": "HTL-002", "type": "Harbour View Suite",
     "capacity": 2, "price_per_night": 195, "available": True,
     "features": ["harbour view", "king bed", "private terrace", "bathtub"]},

    # Cappadocia Cave & Sky Lodge
    {"room_id": "R-003-CAV", "hotel_id": "HTL-003", "type": "Standard Cave Room",
     "capacity": 2, "price_per_night": 220, "available": True,
     "features": ["cave interior", "fairy chimney view", "king bed", "underfloor heating"]},
    {"room_id": "R-003-LUX", "hotel_id": "HTL-003", "type": "Luxury Cave Suite",
     "capacity": 2, "price_per_night": 380, "available": True,
     "features": ["private jacuzzi", "panoramic view", "fireplace", "butler service"]},
    {"room_id": "R-003-HON", "hotel_id": "HTL-003", "type": "Honeymoon Cave",
     "capacity": 2, "price_per_night": 450, "available": False,
     "features": ["private terrace", "balloon view", "rose petal turn-down", "champagne"]},

    # Bodrum Aegean Pearl Resort
    {"room_id": "R-004-STD", "hotel_id": "HTL-004", "type": "Aegean View Room",
     "capacity": 2, "price_per_night": 280, "available": True,
     "features": ["sea view", "king bed", "private balcony", "minibar"]},
    {"room_id": "R-004-VIL", "hotel_id": "HTL-004", "type": "Private Pool Villa",
     "capacity": 4, "price_per_night": 750, "available": True,
     "features": ["private pool", "direct sea access", "outdoor shower", "kitchen", "daily butler"]},
]

# Bookings are stored in memory for the session lifetime only.
BOOKINGS = []


# Utility helpers


def find_room(room_id):
    return next((r for r in ROOMS if r["room_id"] == room_id), None)

def find_hotel(hotel_id):
    return next((h for h in HOTELS if h["id"] == hotel_id), None)


# Routes


@app.route("/")
def homepage():
    """
    Homepage – returns a plain HTML page with project information and navigation links.
    """
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boutique Hotel Chain – Cloud Booking Platform</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Georgia, 'Times New Roman', serif;
            background: #0d1117;
            color: #e6d9c7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px;
        }
        header { text-align: center; margin-bottom: 50px; }
        header h1 {
            font-size: 2.4rem;
            letter-spacing: 0.04em;
            color: #d4a96a;
            margin-bottom: 10px;
        }
        header p { color: #a89880; font-size: 1rem; }
        .tagline {
            font-style: italic;
            color: #8a7a6a;
            margin-top: 6px;
            font-size: 0.9rem;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            max-width: 900px;
            width: 100%;
            margin-bottom: 50px;
        }
        .card {
            background: #161b22;
            border: 1px solid #2a2f3a;
            border-radius: 8px;
            padding: 28px 24px;
            transition: border-color 0.2s, transform 0.2s;
        }
        .card:hover { border-color: #d4a96a; transform: translateY(-3px); }
        .card h2 { font-size: 1rem; color: #d4a96a; margin-bottom: 8px; font-family: monospace; }
        .card p { font-size: 0.85rem; color: #8a8a9a; line-height: 1.5; margin-bottom: 14px; }
        .card a {
            display: inline-block;
            padding: 7px 16px;
            border: 1px solid #d4a96a;
            border-radius: 4px;
            color: #d4a96a;
            text-decoration: none;
            font-size: 0.8rem;
            font-family: monospace;
            transition: background 0.2s, color 0.2s;
        }
        .card a:hover { background: #d4a96a; color: #0d1117; }
        .properties {
            max-width: 900px;
            width: 100%;
            margin-bottom: 50px;
        }
        .properties h3 {
            color: #d4a96a;
            font-size: 1rem;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        .prop-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }
        .prop-item {
            background: #161b22;
            border: 1px solid #2a2f3a;
            border-radius: 6px;
            padding: 14px 18px;
        }
        .prop-item .city { font-size: 0.7rem; color: #d4a96a; text-transform: uppercase; letter-spacing: 0.08em; }
        .prop-item .name { font-size: 0.9rem; color: #e6d9c7; margin-top: 4px; }
        footer { color: #3a3a4a; font-size: 0.75rem; text-align: center; margin-top: 20px; }
        footer span { color: #5a5a6a; }
    </style>
</head>
<body>
    <header>
        <h1>&#127968; Boutique Hotel Chain</h1>
        <p>Cloud-Based Direct Booking Platform</p>
        <p class="tagline"> Atilim University Cloud Computing Project &mdash; Deployed on AWS EC2 (IaaS)</p>
    </header>

    <div class="card-grid">
        <div class="card">
            <h2>GET /hotels</h2>
            <p>Lists all four properties with location, star rating, amenities and contact details.</p>
            <a href="/hotels">View Hotels &rarr;</a>
        </div>
        <div class="card">
            <h2>GET /rooms</h2>
            <p>Returns all room types across properties with pricing and real-time availability.</p>
            <a href="/rooms">View Rooms &rarr;</a>
        </div>
        <div class="card">
            <h2>POST /book</h2>
            <p>Accepts a JSON booking request and returns a confirmed reservation with a unique ID.</p>
            <a href="#book-help">See Usage &darr;</a>
        </div>
        <div class="card">
            <h2>GET /health</h2>
            <p>Returns service health status, uptime timestamp, and summary statistics for monitoring.</p>
            <a href="/health">Check Health &rarr;</a>
        </div>
    </div>

    <div class="properties">
        <h3>Our Properties</h3>
        <div class="prop-list">
            <div class="prop-item">
                <div class="city">Antalya</div>
                <div class="name">Konyaalt&#305; Breeze Hotel</div>
            </div>
            <div class="prop-item">
                <div class="city">Antalya</div>
                <div class="name">Kalei&#231;i Old Town Suites</div>
            </div>
            <div class="prop-item">
                <div class="city">G&ouml;reme &mdash; Cappadocia</div>
                <div class="name">Cave &amp; Sky Lodge</div>
            </div>
            <div class="prop-item">
                <div class="city">Bodrum</div>
                <div class="name">Aegean Pearl Resort</div>
            </div>
        </div>
    </div>

    <div class="properties" id="book-help">
        <h3>Booking API &mdash; Example Request</h3>
        <pre style="background:#161b22;border:1px solid #2a2f3a;border-radius:6px;
                    padding:20px;font-size:0.82rem;color:#8ab4f8;overflow-x:auto;">
curl -X POST http://&lt;your-ec2-ip&gt;:5000/book \\
     -H "Content-Type: application/json" \\
     -d '{
           "room_id":      "R-003-CAV",
           "guest_name":   "Ayşe Kaya",
           "guest_email":  "ayse@example.com",
           "check_in":     "2025-08-10",
           "check_out":    "2025-08-14",
           "guests":       2
         }'</pre>
    </div>

    <footer>
        <p>Powered by <span>Python Flask</span> &bull; Running on <span>AWS EC2 t2.micro</span></p>
        <p style="margin-top:6px;">In-memory data &mdash; no database required</p>
    </footer>
</body>
</html>"""
    return html


@app.route("/hotels", methods=["GET"])
def get_hotels():
    """
    Returns the full list of hotels as JSON.
    Optional query parameter: ?city=Antalya  (case-insensitive filter)
    """
    city_filter = request.args.get("city", "").strip().lower()
    result = HOTELS if not city_filter else [
        h for h in HOTELS if city_filter in h["city"].lower()
    ]
    return jsonify({
        "status": "success",
        "count": len(result),
        "hotels": result,
    })


@app.route("/rooms", methods=["GET"])
def get_rooms():
    """
    Returns all room types with pricing and availability.
    Optional query parameters:
      ?hotel_id=HTL-003    – filter by property
      ?available=true      – show only available rooms
    """
    hotel_filter = request.args.get("hotel_id", "").strip()
    avail_filter = request.args.get("available", "").strip().lower()

    result = list(ROOMS)

    if hotel_filter:
        result = [r for r in result if r["hotel_id"] == hotel_filter]

    if avail_filter == "true":
        result = [r for r in result if r["available"]]
    elif avail_filter == "false":
        result = [r for r in result if not r["available"]]

    # Enrich each room with its hotel name for convenience
    enriched = []
    for room in result:
        hotel = find_hotel(room["hotel_id"])
        enriched.append({
            **room,
            "hotel_name": hotel["name"] if hotel else "Unknown",
            "hotel_city": hotel["city"] if hotel else "Unknown",
        })

    return jsonify({
        "status": "success",
        "count": len(enriched),
        "rooms": enriched,
    })


@app.route("/book", methods=["POST"])
def create_booking():
    """
    Accepts a JSON body and creates an in-memory booking record.

    Required fields:
        room_id      (str)  – e.g. "R-003-CAV"
        guest_name   (str)  – full name of the primary guest
        guest_email  (str)  – contact email
        check_in     (str)  – ISO date YYYY-MM-DD
        check_out    (str)  – ISO date YYYY-MM-DD
        guests       (int)  – number of guests (must not exceed room capacity)

    Returns a booking confirmation with a unique booking ID.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Request body must be valid JSON."}), 400

    # --- Validate required fields ---
    required = ["room_id", "guest_name", "guest_email", "check_in", "check_out", "guests"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing)}",
        }), 400

    room_id     = str(data["room_id"]).strip()
    guest_name  = str(data["guest_name"]).strip()
    guest_email = str(data["guest_email"]).strip()
    check_in    = str(data["check_in"]).strip()
    check_out   = str(data["check_out"]).strip()

    try:
        guests = int(data["guests"])
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "'guests' must be an integer."}), 400

    # --- Validate dates ---
    try:
        ci = datetime.strptime(check_in, "%Y-%m-%d")
        co = datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Dates must be in YYYY-MM-DD format.",
        }), 400

    if co <= ci:
        return jsonify({
            "status": "error",
            "message": "check_out must be after check_in.",
        }), 400

    nights = (co - ci).days

    # --- Validate room ---
    room = find_room(room_id)
    if not room:
        return jsonify({"status": "error", "message": f"Room '{room_id}' not found."}), 404

    if not room["available"]:
        return jsonify({
            "status": "error",
            "message": f"Room '{room_id}' is currently unavailable.",
        }), 409

    if guests > room["capacity"]:
        return jsonify({
            "status": "error",
            "message": (
                f"Room '{room_id}' has a maximum capacity of {room['capacity']} guest(s); "
                f"{guests} requested."
            ),
        }), 400

    hotel = find_hotel(room["hotel_id"])

    # --- Create booking ---
    booking_id   = "BKG-" + str(uuid.uuid4()).upper()[:8]
    total_price  = nights * room["price_per_night"]
    booked_at    = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    booking = {
        "booking_id":    booking_id,
        "status":        "CONFIRMED",
        "guest_name":    guest_name,
        "guest_email":   guest_email,
        "hotel_id":      room["hotel_id"],
        "hotel_name":    hotel["name"] if hotel else "Unknown",
        "hotel_city":    hotel["city"] if hotel else "Unknown",
        "room_id":       room_id,
        "room_type":     room["type"],
        "check_in":      check_in,
        "check_out":     check_out,
        "nights":        nights,
        "guests":        guests,
        "price_per_night": room["price_per_night"],
        "total_price_usd": total_price,
        "booked_at":     booked_at,
        "message": (
            f"Your reservation at {hotel['name'] if hotel else room['hotel_id']} "
            f"is confirmed. Enjoy your stay!"
        ),
    }

    BOOKINGS.append(booking)

    return jsonify({"status": "success", "booking": booking}), 201


@app.route("/health", methods=["GET"])
def health_check():
    """
    Returns service health status and summary statistics.
    Intended for use with AWS CloudWatch, load-balancer health checks, or monitoring tools.
    """
    available_rooms = sum(1 for r in ROOMS if r["available"])
    total_rooms     = len(ROOMS)
    confirmed_bookings = sum(1 for b in BOOKINGS if b["status"] == "CONFIRMED")

    return jsonify({
        "status":     "healthy",
        "service":    "Boutique Hotel Chain – Cloud Booking Platform",
        "version":    "1.0.0",
        "timestamp":  datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "environment": "AWS EC2 (IaaS)",
        "statistics": {
            "total_hotels":       len(HOTELS),
            "total_room_types":   total_rooms,
            "available_rooms":    available_rooms,
            "unavailable_rooms":  total_rooms - available_rooms,
            "total_bookings":     len(BOOKINGS),
            "confirmed_bookings": confirmed_bookings,
        },
        "endpoints": [
            {"path": "/",        "method": "GET",  "description": "Homepage with API navigation"},
            {"path": "/hotels",  "method": "GET",  "description": "List all hotel properties"},
            {"path": "/rooms",   "method": "GET",  "description": "List room types and availability"},
            {"path": "/book",    "method": "POST", "description": "Create a booking"},
            {"path": "/health",  "method": "GET",  "description": "Service health check"},
        ],
    })



# Entry point


if __name__ == "__main__":
    print("=" * 60)
    print("  Boutique Hotel Chain – Cloud Booking Platform")
    print("  Running on http://0.0.0.0:5000")
    print("  Cloud Computing Project | AWS EC2 Deployment")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
