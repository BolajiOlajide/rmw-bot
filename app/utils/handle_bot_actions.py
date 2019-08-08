from flask import current_app

from app.actions.bot_actions import BotActions
from app.repositories.user_repo import UserRepo
from app.utils import elements, slackhelper


def handle_bot_actions(
    app, message_trigger, webhook_url, request_slack_id, command_text
):
    with app.app_context():
        slack_response = slackhelper.user_info(request_slack_id)

        current_user = UserRepo.find_or_create(
            request_slack_id, user_data=slack_response["user"]
        )
        bot_actions = BotActions(current_user=current_user)

        if not slack_response["ok"]:
            response_body = {"text": "An error occurred. Contact the admin."}

        if len(command_text) > 1 and int(command_text[1]) > 0:
            response_body = {"text": "Missing Required Parameter `ride id` "}

        action = command_text[0]

        if action == "show-rides":
            response_body = bot_actions.show_rides()

        elif action == "add-ride":
            dialog = {
                "title": "Add A Ride",
                "submit_label": "Add",
                "callback_id": slack_response["user"]["id"] + "_add_ride",
                "notify_on_cancel": True,
                "elements": elements,
            }
            slackhelper.dialog(dialog, message_trigger)
            msg = ":pencil: We are saving your ride..."
            response_body = {"text": msg}

        elif action == "ride-info":
            response_body = bot_actions.get_ride_info(command_text[1])
        elif action == "join-ride":
            response_body = bot_actions.join_ride(command_text[1])
        elif action == "cancel-ride":
            response_body = bot_actions.cancel_ride(command_text[1])
        elif action == "leave-ride":
            response_body = bot_actions.leave_ride(command_text[1])
        else:
            response_body = {"text": "An error occurred. Contact the admin."}

        return slackhelper.send_delayed_msg(webhook_url, response_body)
