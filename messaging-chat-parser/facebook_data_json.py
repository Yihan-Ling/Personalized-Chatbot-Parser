import shutil
import zipfile
import os
import json
import datetime
contacts = []

def get_friend_names():
    friend_data_path = './data/data_unzip/facebook/friends_and_followers/friends.json'
    with open(friend_data_path, 'r') as f:
        friend_data = json.load(f)
    friends = []
    for friend in friend_data["friends_v2"]:
        friends.append(friend["name"])
    return friends

def unzip(input_path):

    with zipfile.ZipFile(input_path) as z:
        for folder in z.namelist():
            if folder.startswith('messages'):
                z.extract(folder)  # Unzip and extract the 'data' sub directory from the zip file
            if folder.startswith('friends_and_followers'):
                z.extract(folder)

    dest_path = './data/data_unzip/facebook'
    try:
        shutil.move('./messages', dest_path)
        shutil.move('./friends_and_followers', dest_path)
    except:
        print()

    for root, dirs, files in os.walk('./data/data_unzip/facebook/messages/inbox'):
        for file in files:
            if(file.startswith('message_1.json')):
                contact_name = root[42:]
                contacts.append(contact_name)
                shutil.copyfile(root+'/message_1.json', './data/data_unzip/facebook/'+contact_name+'.json')

def parse():
    friends = get_friend_names()
    message_file = open('./data/message_parsed/facebook_chats.txt', "w")
    message_file.write('')

    for name in contacts:
        previous_time = datetime.datetime(1970,12,30,14,28)
        with open('./data/data_unzip/facebook/' + name + '.json', 'r', encoding='utf-8') as f:
            # Reading from json file
            json_object = json.load(f)

        conversation = json_object['messages']
        for message in conversation:
            try:
                time_stamp = message['timestamp_ms']
                current_time = datetime.datetime.fromtimestamp(time_stamp / 1000.0)
                time_elapsed = previous_time-current_time
                if time_elapsed.total_seconds() > 14400:
                    message_file.write('<|endoftext|>\n')
                previous_time = current_time
                sender = message['sender_name']
                if sender in friends or sender == 'Facebook user':
                    sender = '[others]'
                else:
                    sender = '[me]'
                text = message['content']
                message_line = sender + ' ' + text + '\n'
                message_file.write(message_line)
            except:
                continue
        message_file.write('<|endoftext|>\n')

def reverse(file_path):
    with open(file_path, "r") as myfile:
        data = myfile.readlines()
    data_2 = data[::-1]
    message_file = open(file_path, "w")
    message_file.writelines(data_2)

    message_file.close()
def main():
    # Please rename your zip file to 'facebook_raw.zip'
    zip_file = 'facebook_raw.zip'

    input_path = './data/message_raw/Facebook/'+zip_file
    unzip(input_path)

    parse()

    reverse('./data/message_parsed/facebook_chats.txt')


if __name__ == '__main__':
    main()
