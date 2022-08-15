import shutil
import zipfile
import os
import json
import datetime
contacts = []


def get_user_name():
    personal_data_path = './data/data_unzip/instagram/account_information/personal_information.json'
    with open(personal_data_path, 'r') as f:
        personal_data = json.load(f)
    user_name = personal_data['profile_user'][0]['string_map_data']['Name']['value']
    return user_name

def unzip(input_path):

    with zipfile.ZipFile(input_path) as z:
        for folder in z.namelist():
            if folder.startswith('messages'):
                z.extract(folder)  # Unzip and extract the 'data' sub directory from the zip file
            if folder.startswith('account_information'):
                z.extract(folder)

    dest_path = './data/data_unzip/instagram'
    try:
        shutil.move('./messages', dest_path)
        shutil.move('./account_information', dest_path)
    except:
        print()

    for root, dirs, files in os.walk('./data/data_unzip/instagram/messages/inbox'):
        for file in files:
            if(file.startswith('message_1.json')):
                contact_name = root[43:]
                contacts.append(contact_name)
                shutil.copyfile(root+'/message_1.json', './data/data_unzip/instagram/'+contact_name+'.json')

def parse():
    user_name = get_user_name()
    message_file = open('./data/message_parsed/instagram_chats.txt', "w")
    message_file.write('')

    for name in contacts:
        previous_time = datetime.datetime(1970,12,30,14,28)
        with open('./data/data_unzip/instagram/' + name + '.json', 'r', encoding='utf-8') as f:
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
                if sender == user_name:
                    sender = '[me]'
                else:
                    sender = '[others]'
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
    # Please rename your zip file to 'instagram_raw.zip'
    zip_file = 'instagram_raw.zip'
    input_path = './data/message_raw/Instagram/'+zip_file

    unzip(input_path)

    parse()

    reverse('./data/message_parsed/instagram_chats.txt')

if __name__ == '__main__':
    main()
