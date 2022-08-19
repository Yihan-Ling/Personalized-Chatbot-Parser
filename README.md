# Personalized Chatbot Parser
>This repository contains the source code for the models used in the following paper:
>(Fill Research Paper Publication link when available)

> This project was created during Summer of 2022

## Background
This parser aims to convert extracted information from social media into training data for the chatbot model. 

The chatbot model this research specifically focuses on is [Pistobot](https://github.com/pistocop/pistoBot) by [Simone Guardati](https://www.linkedin.com/in/simone-guardati/). 

Although Pistobot offers some form of parsing algorithms, it only supports parsing for Whatsapp and Telegram. My research requires parsing for more social media platforms in addition to Whatsapp and Telegram. 

So I've created this project to extend the list of social media available for parsing.

## Introduction
This Conversation Parser takes in extracted information from several social media platforms and converts the .zip extractions into plain text format for training chatbot. 

The supported social media platforms are:
- Facebook
- Instagram
- Twitter
- Telegram

To follow the format of the conversation parser offered by `Pistobot`, my parser will follow this output format:
```
[me] ...
[others]...
[me] ...
...
<|endoftext|>
```
`[me]` represents the user that made the extraction from the social media platform and `[others]` is any other participants in the chat. `<|endoftext|>` appears in between any texts separated by `4 hours` or longer. 

Unlike `Pistobot` parser, my parser takes the raw `.zip` file extracted from social media platforms as input. The parser unzips and processes the bundle automatically.

## Assumptions
This parser is built on the following assumptions:
- The extracted results from social media platforms are the same as the format of my extraction in 2022
  - With constant updates in social media platforms, the extraction format and structure are not guaranteed to always remain constant
- The export file format for each of the platforms are the same as below (different platforms offer multiple available extraction format):
  - Facebook: `.json`
  - Instagram: `.json`
  - Twitter: `.js`
  - Telegram: `.json`
- The extracted conversation data is not empty

## Setup
For the project to execute correctly, the user must have the following python packages installed:
- shutil 
- zipfile
- os
- json
- datetime

All these packages should be pre-installed with python.

## Method
To parse your own data extracted from different social media platforms, follow these directions:
1. Rename your .zip file into 
   1. `facebook_raw.zip`
   2. `instagram_raw.zip`
   3. `twitter_raw.zip`
   4. `telegram_raw.zip`
   
respectively

2. Under `./messaging-chat-parser/data/message_raw/`, put each renamed .zip file into their respective folder.


3. Run
   - `facebook_data_json.py`
   - `instagram_data_json.py`
   - `twitter_data_json.py`
   - `telegram_data_json.py`

The above python code may differ slightly from each other; however, they all serve a common purpose. The code all goes through these steps:

   - Unzip the `.zip` file and select only the files related to conversation parsing and put them under this path: `./messaging-chat-parser/data/data_unzip/{platform name}`
   - Determine the id or name for `[me]`
   - Parse the conversation
   - Output the parsed result into .txt files under this path: `./messaging-chat-parser/data/message_parsed/{platform name}_chat.txt`
   - Reverse the conversation order in the output file. (This step only applies to the extracted data that is in reverse chronological order, that is, the latest messages appear on the top of the raw extracted file.)


4. Run `plain_text_compile.py`

`plain_text_compile.py` takes in all the parsed data under `./messaging-chat-parser/data/message_parsed/` and combines them into one single `.txt` file named `all_messages.txt`, which is the input for `Pistobot`.

The parsing result will be under this path: `./messaging-chat-parser/data/message_parsed/all_messages.txt`

## Reference 
- Pistobot:

Guardati, Simone. “&nbsp;Pistobot.” PistoBot, https://pistocop.github.io/pistoBot-website/. 
