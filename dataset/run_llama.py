from transformers import pipeline, AutoTokenizer
import torch
import json 
import time

model = "/data/models/huggingface/meta-llama/Llama-2-13b-chat-hf"
# Load tokenizer and mcodel
tokenizer = AutoTokenizer.from_pretrained(model)

# Determine device
device = -1  # Default to CPU
if torch.cuda.is_available():
    device = 0  # Use the first GPU

# Initialize pipeline with device setting
text_gen_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
    torch_dtype=torch.float16
)

# x = '''[INST]<<SYS>>
#         You are a helpful and honest assistant. Please answer consistent and in struectued format. The following sentence is a description for a financial table cell, and please refine the following sentence to be one sentence that semantically meaningful. 
#         <</SYS>> Group retirement products 2007 of Premiums and Other Considerations is $446..
#         [/INST]'''

# response = text_gen_pipeline(x, max_length=512)

def get_clean_respose(response):
    response = response[0]['generated_text']
    response = response.split('[/INST]')[1]
    response = response.split('\n\n')[1]
    return response
# response = get_clean_respose(response)


batch_size = 20
file = 'dev_old.json'
save_path = 'dev_llama.json'
s_time = time.time()

save_data = []
data = json.load(open(file))
for datum in data:
    table_description = datum['table_description']
    keys = list(table_description.keys())
    descriptions = list(table_description.values())
    responses = []
    for i in range(0, len(descriptions), batch_size):
        batch_texts = descriptions[i:i+batch_size]
        batch_prompts = [
            f'''[INST]<<SYS>>
        You are a helpful and honest assistant. Please answer consistent and in structured format. The following sentence is a description for a financial table cell, and please refine the following sentence to be one sentence that semantically meaningful. 
        <</SYS>> {text} [/INST]''' for text in batch_texts
        ]
        batch_responses = text_gen_pipeline(batch_prompts, max_length=512)
        batch_responses = [get_clean_respose(response) for response in batch_responses]
        responses.extend(batch_responses)
        print(f"Processed {i + len(batch_texts)} descriptions")
    for i, key in enumerate(keys):
        table_description[key] = responses[i]
    save_data.append(datum)
    #data length and time
    with open('time.txt', 'a') as f:
        f.write(str(len(save_data)) + ' ' + str(time.time()-s_time) + '\n')
    with open(save_path, 'w') as f:
        json.dump(save_data, f, indent=4)

# Process the dataset in batches
