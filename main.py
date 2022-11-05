import json
import numpy as np
import pandas as pd
import hashlib


## creating a json encoder
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


## opening the csv file with pandas dataframe
data = pd.read_csv('Filename.csv')  # enter the filename you downloaded

hash_list = []
team_names = data['TEAM NAMES'].tolist()
string_names = [str(names) for names in team_names]
clean_names = []
count = 0
for n in string_names:
    if n != 'nan':
        clean_names.append(n)
    else:
        clean_names.append(clean_names[count - 1])
    count += 1
for i in range(data.shape[0]):

    details = {
        "format": "CHIP-0007",
        "name": data['Name'][i],
        "description": data['Description'][i],
        "minting_tool": clean_names[i],
        "sensitive_content": False,
        "series_number": data["Series Number"][i],
        "series_total": data.shape[0],
        "attributes": [
            {
                "trait_type": "gender",
                "value": data["Gender"][i],
            },

        ],
        "collection": {
            "name": "Zuri NFT Tickets for Free Lunch",
            "id": data['UUID'][i],
            "attributes": [
                {
                    "type": "description",
                    "value": "Rewards for accomplishments during HNGi9.",
                }
            ],
        },
    }
    attributes = [x.split(':') for x in data['Attributes'][i].split(';') if x]
    for attr in attributes:
        details['collection']['attributes'].append({'trait_type': attr[0].strip(), 'value': attr[1].strip()})

    ## creating a json file
    with open(f'output/{data["Filename"][i]}.json', 'w') as data_file:
        json.dump(details, data_file, indent=4, cls=NpEncoder)
    ##
    with open(f'output/{data["Filename"][i]}.json', "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        hash_list.append(readable_hash)

# appending the hash to the csv file
data['Hash'] = hash_list
data.to_csv('output.csv', index=False)
print('Task successful')