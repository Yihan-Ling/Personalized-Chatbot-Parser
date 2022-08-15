import zipfile
import json
import shutil
import datetime



def get_user_name():
    personal_data_path = './data/data_unzip/twitter/account.js'
    with open(personal_data_path, 'r') as f:
        personal_data = json.load(f)
    user_name = personal_data[0]['account']['accountId']
    return user_name



def unzip(input_path):
    with zipfile.ZipFile(input_path) as z:
        for folder in z.namelist():
            if folder.startswith('data/account.js') or folder.startswith('data/direct-messages-group.js') or folder.startswith('data/direct-messages.js'):
                z.extract(folder)  # Unzip and extract the 'data' sub directory from the zip file
    dest_path = './data/data_unzip/twitter'
    try:
        shutil.move('./data/account.js', dest_path)
        shutil.move('./data/direct-messages.js', dest_path)
        shutil.move('./data/direct-messages-group.js', dest_path)
    except:
        print()
    clean_up_js()




def clean_up_js():
    with open("./data/data_unzip/twitter/account.js") as input_file:
        input_content = input_file.read()

    output_content = input_content.replace("window.YTD.account.part0 = ", "")
    output_file = open("./data/data_unzip/twitter/account.js", "w")
    output_file.write(output_content)

    with open("./data/data_unzip/twitter/direct-messages-group.js") as input_file:
        input_content = input_file.read()

    output_content = input_content.replace("window.YTD.direct_messages_group.part0 = ", "")
    output_file = open("./data/data_unzip/twitter/direct-messages-group.js", "w")
    output_file.write(output_content)

    with open("./data/data_unzip/twitter/direct-messages.js") as input_file:
        input_content = input_file.read()

    output_content = input_content.replace("window.YTD.direct_messages.part0 = ", "")
    output_file = open("./data/data_unzip/twitter/direct-messages.js", "w")
    output_file.write(output_content)



def parse():

    user_name = get_user_name()
    message_file = open("./data/message_parsed/twitter_chats.txt", "w")
    message_file.write('')

    # Opening direct-messages-group JSON file
    with open('./data/data_unzip/twitter/direct-messages-group.js', 'r') as f:
        # Reading from json file
        json_object = json.load(f)
    message_file = open("./data/message_parsed/twitter_chats.txt", "a")

    for group in json_object:
        previous_time = datetime.datetime(1970, 12, 30, 14, 28)
        conversation = group['dmConversation']['messages']

        for message in conversation:
            try:
                message_create = message['messageCreate']
                time_stamp = message_create['createdAt']
                current_time = datetime.datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                time_elapsed = previous_time - current_time
                if time_elapsed.total_seconds() > 14400:
                    message_file.write('<|endoftext|>\n')
                previous_time = current_time
                sender = message_create['senderId']
                if sender == user_name:
                    sender = '[me]'
                else:
                    sender = '[others]'
                text = message_create['text']
                message_line = sender + ' ' + text + '\n'

                message_file.write(message_line)
            except:
                continue
        message_file.write('\n')

    # Opening direct-messages-group JSON file
    with open('./data/data_unzip/twitter/direct-messages.js', 'r') as f:
        # Reading from json file
        json_object = json.load(f)

    for group in json_object:
        conversation = group['dmConversation']['messages']
        for message in conversation:
            # try:
                message_create = message['messageCreate']
                time_stamp = message_create['createdAt']
                current_time = datetime.datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                time_elapsed = previous_time - current_time
                if time_elapsed.total_seconds() > 14400:
                    message_file.write('<|endoftext|>\n')
                previous_time = current_time

                sender = message_create['senderId']
                if sender == user_name:
                    sender = '[me]'
                else:
                    sender = '[others]'
                text = message_create['text']
                message_line = sender + ' ' + text + '\n'

                message_file.write(message_line)
            # except:
            #     continue
        message_file.write('\n')

def reverse(file_path):
    with open(file_path, "r") as myfile:
        data = myfile.readlines()
    data_2 = data[::-1]
    message_file = open(file_path, "w")
    message_file.writelines(data_2)

    message_file.close()


def main():

    # zip file name is different for every export
    zip_file = 'twitter_raw.zip'
    input_path = './data/message_raw/Twitter/' + zip_file

    unzip(input_path)

    parse()

    reverse('./data/message_parsed/twitter_chats.txt')

if __name__ == '__main__':
    main()
