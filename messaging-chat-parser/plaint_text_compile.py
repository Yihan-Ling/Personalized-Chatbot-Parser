import os

def main():
    output_file_path = './data/message_parsed/all_messages.txt'
    output_file = open(output_file_path, "w")
    output_file.write('')
    for root, dirs, files in os.walk('./data/message_parsed'):
        for file in files:
            if file.endswith('_chats.txt'):
                input_file_path = root + '/' + file
                with open(input_file_path) as input_file:
                    input_content = input_file.read()

                output_file = open(output_file_path, "a")
                output_file.write(input_content+'\n')


if __name__ == '__main__':
    main()