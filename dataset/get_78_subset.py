import os
import json

file = 'dev_old.json'
save_path = 'dev.json'

llamma_file = 'dev_llama.json'

llamma_data = json.load(open(llamma_file))

save = []
data = json.load(open(file))

for i, datum in enumerate(llamma_data):
    assert datum['uid'] == data[i]['uid']
    save.append(data[i])
print(len(save))

with open(save_path, 'w') as f:
    json.dump(save, f, indent=4)