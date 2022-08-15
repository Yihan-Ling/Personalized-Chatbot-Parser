import datetime
import zipfile
import shutil
import json

def main():

    # zip file name may be different for every export
    zip_file = 'telegram_raw.zip'
    input_path = './data/message_raw/Telegram/' + zip_file
    json_object_path = unzip(input_path)

    parse(json_object_path)


def unzip(input_path):
    with zipfile.ZipFile(input_path) as z:
        for folder in z.namelist():
            if folder.startswith('Telegram Desktop/DataExport') and folder.endswith('result.json'):
                z.extract(folder)  # Unzip and extract the 'DataExport' sub directory from the zip file
                json_object_path = folder
    dest_path = './data/data_unzip/telegram'
    try:
        shutil.move('./Telegram Desktop', dest_path)
    except:
        print()
    json_object_path = dest_path + '/' + json_object_path
    return json_object_path


def parse(json_object_path):
    message_file = open("./data/message_parsed/telegram_chat.txt", "w")
    message_file.write('')
    message_file = open("./data/message_parsed/telegram_chat.txt", "a")

    with open(json_object_path, 'r') as f:
        # Reading from json file
        json_object = json.load(f)

    message_list = json_object['chats']['list']
    user_name = json_object['personal_information']['first_name']+' '+json_object['personal_information']['last_name']

    for conversation in message_list:
        previous_time = datetime.datetime(1970, 12, 30, 14, 28)
        for message in conversation['messages']:
            try:
                time_stamp = message['date']
                current_time = datetime.datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S")
                time_elapsed = current_time - previous_time
                if time_elapsed.total_seconds() > 14400:
                    message_file.write('<|endoftext|>\n')
                previous_time = current_time
                sender = message['from']
                if sender == user_name:
                    sender = '[me]'
                else:
                    sender = '[others]'
                text = message['text']
                message_line = sender + ' ' + text + '\n'
                message_file.write(message_line)
            except:
                continue
        message_file.write('\n')

if __name__ == '__main__':
    main()
