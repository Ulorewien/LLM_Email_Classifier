import json, yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

with open("prompts.json", "r") as f:
    prompts = json.load(f)
    
email_classification_prompt = prompts["email_classification"][config["email_prompt"]]
response_generation_prompt = prompts["reponse_generation"][config["generation_prompt"]]

print(email_classification_prompt)
print(response_generation_prompt)