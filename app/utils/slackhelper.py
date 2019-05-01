import requests
import json
from slackclient import SlackClient
from config import get_env


class SlackHelper:

	def __init__(self):
		self.slack_token = get_env('SLACK_TOKEN')
		self.slack_client = SlackClient(self.slack_token)

	def post_message(self, msg, recipient, attachments=None):
		return self.slack_client.api_call(
			"chat.postMessage",
			channel=recipient,
			text=msg,
			attachments=attachments,
			as_user=True
		)

	def update_message(self, msg, recipient, message_ts=None, attachments=None):
		return self.slack_client.api_call(
			"chat.update",
			channel=recipient,
			ts=message_ts,
			text=msg,
			attachments=attachments,
			as_user=True
		)

	def file_upload(self, file_content, file_name, file_type, title=None, ):
		return self.slack_client.api_call(
			"files.upload",
			channels=self.slack_channel,
			content=file_content,
			filename=file_name,
			filetype=file_type,
			initial_comment='{} Log File'.format(file_name),
			title=title
		)

	def user_info(self, uid):
		return self.slack_client.api_call(
			"users.info",
			user=uid,
			token=self.slack_token
		)

	def dialog(self, dialog, trigger_id):
		return self.slack_client.api_call(
			"dialog.open",
			trigger_id=trigger_id,
			dialog=dialog
		)

	def send_delayed_msg(self, webhook_url, slack_data, check_error=True):
		response = requests.post(
			webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)

		if response.status_code != 200:
			if check_error and slack_data["errors"]:
				response = jsonify(slack_data)
				response.status_code = 200
				return response
			else:
				value_error_message = f"""Request to slack returned an error {response.status_code}, the response is:
{response.text}
"""
				raise ValueError(value_error_message)
		return response
