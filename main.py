# Import the necessary libraries
import json
from twilio.rest import Client

# Print the options for the user
print("Please select an option:")
print("1. Send a message")
print("2. Check the status of a message")

# Prompt the user to choose an option
choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    # Try to read the contents of the 'user_info.json' file
    try:
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty dictionary
        user_info = {}

    # If the user_info dictionary is not empty, print a message indicating that the user's information is already saved
    if user_info:
        print("Your information is already saved in the 'user_info.json' file.")
    else:
        # Prompt the user to enter their Twilio Account SID
        user_info['account_sid'] = input("Please enter your Twilio Account SID: ")

        # Prompt the user to enter their Twilio Auth Token
        user_info['auth_token'] = input("Please enter your Twilio Auth Token: ")

        # Prompt the user to enter the phone number they want to send the message from
        user_info['from_number'] = input(
            "Please enter the phone number you want to send the message from (format: +12345678901): "
        )

    # Serialize the user's information as JSON and write it to a file
    with open('user_info.json', 'w') as f:
        json.dump(user_info, f)

    # Prompt the user to enter the phone number they want to send the message to
    to_number = input(
        "Please enter the phone number you want to send the message to (format: +12345678901): "
    )

    # Create a client object using the user's information
    client = Client(user_info['account_sid'], user_info['auth_token'])


    # Send the message
    def send_message(client, from_number, to_number, message_body):
        message = client.messages.create(body=message_body,
                                         from_=from_number,
                                         to=to_number)
        return message.sid


    # Prompt the user to enter the message they want to send
    message_body = input("Please enter the message you want to send: ")

    # Send the message and store the SID
    message_sid = send_message(client, user_info['from_number'], to_number, message_body)
    print(f"Message sent! Message SID: {message_sid}")

elif choice == "2":
    # Load the user information from the JSON file
    try:
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
    except FileNotFoundError:
        user_info = {}

    # Check if the 'account_sid' key is present in the user_info dictionary
    if 'account_sid' not in user_info:
        # If it's not present, prompt the user to enter their Twilio Account SID
        user_info['account_sid'] = input("Please enter your Twilio Account SID: ")

    # Check if the 'auth_token' key is present in the user_info dictionary
    if 'auth_token' not in user_info:
        # If it's not present, prompt the user to enter their Twilio Auth Token
        user_info['auth_token'] = input("Please enter your Twilio Auth Token: ")

    # Use the values from the user_info dictionary as the account SID and auth token
    client = Client(user_info['account_sid'], user_info['auth_token'], user_info['from_number'])

    # Check the status of a message by its SID


    def check_message_status(client, message_sid):
        message = client.messages(message_sid).fetch()
        return message.status


    # Prompt the user to enter the SID of the message they want to check
    message_sid = input("Please enter the SID of the message you want to check: ")

    # Check the status of the message
    message_status = check_message_status(client, message_sid)
    print(f"Message status: {message_status}")

else:
    print("Invalid choice. Please try again.")
