import openai
import json
import argparse
import os
from openai import OpenAI
import time


argparser = argparse.ArgumentParser()
argparser.add_argument('--random_seed', type=int, default=11797, help='random seed')
argparser.add_argument('--model', type=str, default='gpt-3.5-turbo-instruct', choices=['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-instruct'])
argparser.add_argument('--key', type=str, default='', help='openai api key')
args = argparser.parse_args()

if args.key is not None:
    # openai.api_key = args.key
    client = OpenAI(api_key=args.key)
else:
    print('no api key provided, using default key')
    exit()

# def make_API_call(conversation, model='gpt-3.5-turbo'):
    
#     response = client.chat.completions.create(
#         model=model,
#         messages=conversation,
#         temperature=0.5,
#         seed = args.random_seed,
#         # max_tokens=4096,
#     )
#     # print('response: ', response)
#     # return response.choices[0].message.content
#     return response

def make_API_call(conversation, model='gpt-3.5-turbo-instruct'):
    
    response = client.completions.create(
        model=model,
        prompt=conversation,
    )
    # print('response: ', response)
    # return response.choices[0].message.content
    return response



def get_prompt(data):
    prompts = []
    for d in data:
        # prompt = 'The following sentence is a description for a cell in a financial table. Please refine it to be more semantically meaningful: '
        prompt = 'Please refine the following sentence to be more semantically meaningful as a description for a financial table cell: '
        prompt += d
        prompts.append(prompt)
    # prompt = 'The following sentence is a description for a cell in a financial table. Please refine it to be more semantically meaningful: '
    # prompt += data
    return prompts

def get_response(data):
    model = args.model
    prompts = get_prompt(data)
    # Initialize a conversation with a system message
    # for i in range(len(prompts)):
    #     conversation = [
    #     {"role": "system", "content": "You are a helpful agent that produces consistent and structured output.\n"},
    #     {"role": "system", "content": prompts[i]}
    #     ]
    #     prompts[i] = conversation
    # print(prompts[0][0])
    
    responses = None
    try_count = 0
    description = ['']* len(prompts)
    # make api call 20 prompts at a time
    for i in range(0, len(prompts), 20):
        assistant_response = make_API_call(prompts[i:i+20])
        responses = assistant_response
        for choice in responses.choices:
            description[choice.index+i] =  choice.text
    # while (try_count < 1 and responses is None):
    #     try:
    #         assistant_response = make_API_call(prompts)
    #     except:
    #         print('API call failed')
    #         try_count += 1
    #         continue
    #     responses = assistant_response

    # for choice in responses.choices:
    #     description[choice.index] = prompts[choice.index] + choice.text
    return description

def main():
    file = 'dev_old.json'
    save_path = 'dev_gpt.json'
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)
    s_time = time.time()
    if file.endswith(".json"):
        save_data = []
        data = json.load(open(file))
        for datum in data:
            table_description = datum['table_description']
            keys = list(table_description.keys())
            descriptions = list(table_description.values())
            response = get_response(descriptions)
            for i, key in enumerate(keys):
                table_description[key] = response[i]
            save_data.append(datum)
            #data length and time
            with open('time.txt', 'a') as f:
                f.write(str(len(save_data)) + ' ' + str(time.time()-s_time) + '\n')
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=4)
            break
                

if __name__ == '__main__':
    main()