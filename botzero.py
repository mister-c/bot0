import os;
import re;

import time;
import markov;

from slackclient import SlackClient;
from random import randint;

import commands;

import schedule;

# Instantiate the client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'));

botzero_id = None;

GREETING_DELAY = 1;
RTM_READ_DELAY = 1;

# Commands
EXAMPLE_COMMAND = "do";
SHITPOST_SEND_COMMAND = "shitpost";
SHITPOST_COUNT_COMMAND = "how many shitposts do you have";
SHITPOST_HELP_COMMAND = "how do i upload shitpost";
MARKOV_COMMAND = "markov";
BIRTHDAY_COMMAND = "what is your birthday";
GREETING_1_COMMAND = "say hello";
GREETING_2_COMMAND = "howdy";

# Tags
SHITPOST_TAG = "funny";

# REGEX
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# MESSAGES
TIMESHEET_REMINDER = "Its Friday so... submit ya timesheets";
UPDOWN_REMINDER = "Send Adam your ups... and your downs.";

# Misc Globals
MAX_IMAGE_ID_NO = 9999999999;
MY_BIRTHDATE = 'Aug 20 06:26:12 CDT 2018';
MY_BIRTHDATE_TS = time.strptime(MY_BIRTHDATE, "%b %d %H:%M:%S %Z %Y");
VOLA_ROOM_ID = os.environ.get('VOLA_ROOM_ID');

#ACTIVE_CHANNEL = os.environ.get('PROD_CHAN');
ACTIVE_CHANNEL = os.environ.get('QA_CHAN');


# Define vola sync functions
def sched_vola_download():
        print(commands.getstatusoutput('python ./download_vola.py'));

def sched_dequeue_img():
        print(commands.getstatusoutput('python ./dequeue_img.py'));

# Define remiders
def sched_reminder(message, img_tag, img_title):
        channel = ACTIVE_CHANNEL;
        default_response = "Undefined reminder";
        if message:
                response = message;
        
        print("sched_reminder invoked!");

        post_rand_image(img_tag, img_title, channel);
        
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response or default_response
	);

def parse_human_message(message, user):
        print("its a human message: " + message);
        print("message is from: " + user);
        
        file_suffix = '_markov.txt';
        filename_pattern = user + file_suffix;
        cmd_out = commands.getstatusoutput('ls ' + '*' + filename_pattern)[1];

        print('grep output: ' + cmd_out);

        message = message + "\n\n";


        filename = "";
        
        if(cmd_out.startswith('ls: cannot access') or len(cmd_out) < 2):
                return;
        else:
                filename = cmd_out;
                print(cmd_out);
        
        
        with open(filename, "a") as markov_file:
                markov_file.write(message);
                markov_file.close();

        # cmd_out = commands.getstatusoutput('printf "' + message + '" >> ' + filename);
        # print(cmd_out);

        
def parse_bot_commands(slack_events):
	"""
		Parases a list of commands
		If command if found returns a tuple of command and channel
		else returns None, None
	"""
	for event in slack_events:
		if event["type"] == "message" and not "subtype" in event:
			user_id, message = parse_direct_mention(event["text"]);
			if user_id == botzero_id:
				return message, event["channel"];
                        elif event['user'] != botzero_id:
                                parse_human_message(event["text"], event["user"]);
	return None, None;

def parse_direct_mention(message_text):
	"""
		Finds a direct mention
		Returns user ID which was mentioned 
		Else returns None
	"""
	matches = re.search(MENTION_REGEX, message_text);
	return(matches.group(1), matches.group(2).strip()) if matches else (None, None);

# tag is the tag in the image filename that identifies the image
# title is the title of the uploaded image
def post_rand_image(tag, title, channel):
        file_list_str = commands.getstatusoutput('ls ./img/ | grep ' + tag)[1];
        file_list = file_list_str.split("\n");

        if len(file_list[0]) < 1:
                print("Invalid tag used: " + tag + ". Wont upload image");
                return;

        image_filename = file_list[randint(0,len(file_list) - 1)];
        image_title = title + '_' + str(randint(0,MAX_IMAGE_ID_NO));

        print('filename: ' + image_filename);

        with open('./img/' + image_filename) as file_content:
                slack_client.api_call(
                        "files.upload",
                        channels=channel,
                        file=file_content,
                        title=image_title
                );

def count_img(tag):
        file_list_str = commands.getstatusoutput('ls ./img/ | grep ' + tag)[1];
        file_list = file_list_str.split("\n");

        if len(file_list[0]) < 1:
                print("Invalid tag used: " + tag + ". Wont upload image");
                return 0;
        return len(file_list);

def find_birthday():
        return(time.strftime("%m/%d/%Y %H:%M:%S", MY_BIRTHDATE_TS));

def handle_command(command, channel):
	"""
		Execute a command. Idiot.
	"""
	default_response  = "Not a valid command.";

	# Find and exec the command
	response = None;
	if command.startswith(EXAMPLE_COMMAND):
		response = "AAAAAAAAAAAAAAAAAa";
	elif command.startswith(SHITPOST_SEND_COMMAND):
                post_rand_image(SHITPOST_TAG, 'shitpost', channel);
                response = "beep boop";
	elif command.startswith(SHITPOST_COUNT_COMMAND):
                response = "i got %d shitposts" % count_img(SHITPOST_TAG);
        elif command.startswith(SHITPOST_HELP_COMMAND):
                response = "upload shitposts to https://volafile.org/r/" + VOLA_ROOM_ID + " and ill dl 'em. " + \
                 "ill need like a minute or 2 to do that.";
        elif command.startswith(BIRTHDAY_COMMAND):
                response = "I was born on " + find_birthday();
	elif command.startswith(MARKOV_COMMAND):
                # Default response
                response = 'No can markov';
                
                markov_target_user = command;
                markov_target_user = markov_target_user.replace('markov', '');
                markov_target_user = markov_target_user.replace(' ', '');

                print('markov_target_user: ' + markov_target_user);
                markov_response = markov.markov(markov_target_user);
                if(markov_response != 'fail'):
                        response = markov_response;
	elif command.startswith(GREETING_1_COMMAND):
                time.sleep(GREETING_DELAY);
                response = "hello humans";
	elif command.startswith(GREETING_2_COMMAND):
                time.sleep(GREETING_DELAY);
                response = "howdy";
                
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response or default_response
	);


# Schedule stuff
schedule.every().friday.at("15:00").do(sched_reminder, TIMESHEET_REMINDER, 'time', 'timesheet');
schedule.every().wednesday.at("8:00").do(sched_reminder, UPDOWN_REMINDER, 'updown', 'ups_downs');

#sched_reminder(TIMESHEET_REMINDER);
schedule.every(1).minute.do(sched_vola_download);
schedule.every(1).minute.do(sched_dequeue_img);

#schedule.every(1).minute.do(sched_reminder, TIMESHEET_REMINDER, 'time', 'timesheet');
#schedule.every(1).minute.do(sched_reminder, UPDOWN_REMINDER, 'updown', 'ups_downs');

if __name__ == "__main__":
	if slack_client.rtm_connect(with_team_state=False):
                # Pre loop stuff

                # Sexy intro
		print("botzero is running, bitches!");
                
		# Read ID
		botzero_id = slack_client.api_call("auth.test")["user_id"];

                # Test stuff here
                # markov.markov('micah');
                # print("I am %d days old." % (time.mktime(MY_BIRTHDATE_TS) / ((60 * 60 * 60 * 24 * 365) * 1.0));
                # print("I am %d days old." % (time.mktime(MY_BIRTHDATE_TS) / seconds_per_year));
                # print(time.localtime(time.mktime(MY_BIRTHDATE_TS)));
                
		while True:
                        schedule.run_pending();
			command, channel = parse_bot_commands(slack_client.rtm_read());
			if command:
				handle_command(command, channel);
			time.sleep(RTM_READ_DELAY);
	else:
		print("CONNECTION FAILED!!!!!");
