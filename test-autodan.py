import os
from easyjailbreak.attacker.AutoDAN_Liu_2023 import AutoDAN
from easyjailbreak.datasets import JailbreakDataset
from easyjailbreak.models.huggingface_model import from_pretrained
from easyjailbreak.models.openai_model import OpenaiModel

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Change working directory to the current file

# Load API keys from environment variables
# api_key = os.environ.get('OPENAI_API_KEY')
api_key = ''

# First, prepare models and datasets.
attack_model = from_pretrained(model_name_or_path='/root/autodl-tmp/hf_hub/llama2-7B-chat-hf',
                               model_name='llama2')
target_model = OpenaiModel(model_name='gpt-4o',
                         api_keys=api_key)
eval_model = OpenaiModel(model_name='gpt-4o',
                         api_keys=api_key)

# dataset = JailbreakDataset('/root/autodl-tmp/Dataset/Lemhf14--EasyJailbreak_Datasets/ForbiddenQuestion/train-00000-of-00001.json')
dataset = JailbreakDataset('AdvBench')

# Then instantiate the recipe.
attacker = AutoDAN(attack_model=attack_model,
                target_model=target_model,
                jailbreak_datasets=dataset)

# Finally, start jailbreaking.
attacker.attack()