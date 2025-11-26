'''import json
from flask import Flask, request, jsonify
from flask_cors import CORS
# NEW: Import necessary function from pywebpush
from pywebpush import webpush, WebPushException 

app = Flask(__name__)
CORS(app)

# --- CRITICAL CONFIGURATION (REPLACE WITH YOUR REAL GENERATED KEYS!) ---
VAPID_CLAIMS = {
    "sub": "geetanjali.30.01.06@gmail.com"  # Use a real email address
}
VAPID_PRIVATE_KEY = "MHcCAQEEIOAEzxyPHGX4G27D9siGqP+f5w8lwpQCA2VwHNzA9b/+oAoGCCqGSM49AwEHoUQDQgAEMgvXXy9P53pULNw5oJJChgQ7Z1Af//QlVRlalc5TBThBr7qCmtM+J2aNS7u2SnZVsfGHE8id7P8166fbPvzbQg==" # REPLACE ME!
VAPID_PUBLIC_KEY = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEMgvXXy9P53pULNw5oJJChgQ7Z1Af//QlVRlalc5TBThBr7qCmtM+J2aNS7u2SnZVsfGHE8id7P8166fbPvzbQg=="   # REPLACE ME!
# NOTE: The public key MUST also be updated in index.html (around line 400)!

# --- Mock Subscription Database (REPLACE WITH FIRESTORE LATER) ---
# In a full production app, this should query Firestore using the Admin SDK.
# For simplicity, we use an in-memory storage for subscriptions linked to UICs.
user_subscriptions = {} # { "123456": [{subscription_object}, {...}] }

# --- API Endpoints ---

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Receives and stores the client's push subscription object."""
    data = request.json
    uic = data.get('uic')
    subscription = data.get('subscription')

    if not all([uic, subscription]):
        return jsonify({"success": False, "message": "Missing UIC or subscription data."}), 400
    
    if uic not in user_subscriptions:
        user_subscriptions[uic] = []

    # Store the subscription payload
    if subscription not in user_subscriptions[uic]:
        user_subscriptions[uic].append(subscription)
        print(f"UIC {uic} subscribed successfully. Total subscriptions: {len(user_subscriptions[uic])}")
        return jsonify({"success": True, "message": "Subscription stored. Notifications are ready."})

    return jsonify({"success": True, "message": "Already subscribed."})


def send_push_notification(uic, message):
    """Sends the actual push notification using pywebpush."""
    if uic not in user_subscriptions or not user_subscriptions[uic]:
        print(f"Push Failed: UIC {uic} has no registered subscriptions.")
        return False
        
    for sub in user_subscriptions[uic]:
        try:
            # Send the encrypted payload to the push service endpoint
            response = webpush(
                subscription_info=sub,
                data=json.dumps({"title": "Item Found!", "body": message}),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print(f"Push Sent to {uic} successfully. Status: {response.status_code}")
            
        except WebPushException as e:
            # Handle expired subscription, invalid keys, etc.
            print(f"Push Failed to {uic} (Subscription): {e}")
            # In a real app, you would remove this bad subscription from the database.
        except Exception as e:
            print(f"Push Failed (General Error): {e}")
            
    return True

@app.route('/send_push_notification', methods=['POST'])
def trigger_push():
    """Endpoint hit by the frontend 'Report Found' logic to trigger a push."""
    data = request.json
    uic = data.get('uic')
    message = data.get('message')

    if not all([uic, message]):
        return jsonify({"success": False, "message": "Missing UIC or message."}), 400
    
    # Send the actual notification
    success = send_push_notification(uic, message)
    
    return jsonify({"success": success, "message": "Notification process completed."})


if __name__ == '__main__':
    print("Flask app running. Push logic is now LIVE.")
    app.run(debug=True, port=5000)'''
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pywebpush import webpush, WebPushException 

app = Flask(__name__)
# Enable CORS for communication between Firebase Hosting and Render
CORS(app, resources={r"/*": {"origins": "*"}})

# --- CRITICAL CONFIGURATION (REPLACE WITH YOUR REAL GENERATED KEYS!) ---
# NOTE: Keys must be the shorter, URL-Safe Base64 format (from vapidkeys.com)
VAPID_CLAIMS = {
    "sub": "mailto:geetanjali.30.01.06@gmail.com"  # Use your real email address
}
VAPID_PRIVATE_KEY = "pWNpNDrFUkS1ZcCclRM0I1FgYHB2UXh3i9GUPXrDudY"  # PASTE THE PRIVATE KEY HERE
VAPID_PUBLIC_KEY = "BLmzkIXG5ClilX89HV7WnoGo5alDiw5G4C8PW0Y2GykbEfuovNoj6_5wSmhv5vng-3GTnY8tP_KcLSTfpbzHn8c"    # PASTE THE PUBLIC KEY HERE

# --- Mock Subscription Database (In-memory storage) ---
user_subscriptions = {}

# --- API Endpoints ---

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Receives and stores the client's push subscription object."""
    data = request.json
    uic = data.get('uic')
    subscription = data.get('subscription')

    if not all([uic, subscription]):
        return jsonify({"success": False, "message": "Missing UIC or subscription data."}), 400
    
    if uic not in user_subscriptions:
        user_subscriptions[uic] = []

    # Store the subscription payload
    if subscription not in user_subscriptions[uic]:
        user_subscriptions[uic].append(subscription)
        print(f"UIC {uic} subscribed successfully.")
        return jsonify({"success": True, "message": "Subscription stored. Notifications are ready."})

    return jsonify({"success": True, "message": "Already subscribed."})


def send_push_notification(uic, message):
    """Sends the actual push notification using pywebpush."""
    if uic not in user_subscriptions.get(uic, []):
        print(f"Push Failed: UIC {uic} has no registered subscriptions.")
        return False
        
    for sub in user_subscriptions[uic]:
        try:
            # Send the encrypted payload to the push service endpoint
            response = webpush(
                subscription_info=sub,
                data=json.dumps({"title": "Item Found!", "body": message}),
                # CRITICAL: Use the correct Public and Private Keys here
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_public_key=VAPID_PUBLIC_KEY, 
                vapid_claims=VAPID_CLAIMS
            )
            print(f"Push Sent to {uic} successfully. Status: {response.status_code}")
            
        except WebPushException as e:
            print(f"Push Failed to {uic} (Subscription): {e}")
            # Note: In a real app, you would remove this bad subscription from the database.
        except Exception as e:
            print(f"Push Failed (General Error): {e}")
            
    return True

@app.route('/send_push_notification', methods=['POST'])
def trigger_push():
    """Endpoint hit by the frontend 'Report Found' logic to trigger a push."""
    data = request.json
    uic = data.get('uic')
    message = data.get('message')

    if not all([uic, message]):
        return jsonify({"success": False, "message": "Missing UIC or message."}), 400
    
    success = send_push_notification(uic, message)
    
    return jsonify({"success": success, "message": "Notification process completed."})

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "online"}), 200

if __name__ == '__main__':
    print("Flask app running. Push logic is now LIVE.")
    app.run(debug=True, port=5000)