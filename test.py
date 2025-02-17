import os
from easyjailbreak.attacker.PAIR_chao_2023 import PAIR
from easyjailbreak.datasets import JailbreakDataset
from easyjailbreak.models.huggingface_model import from_pretrained
from easyjailbreak.models.openai_model import OpenaiModel

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Change working directory to the current file

# Load API keys from environment variables
api_key = os.environ.get('OPENAI_API_KEY')

# First, prepare models and datasets.
attack_model = from_pretrained(model_name_or_path='/root/autodl-tmp/hf_hub/vicuna-7b-v1.5',
                               model_name='vicuna_v1.1')
target_model = OpenaiModel(model_name='gpt-4o',
                         api_keys=api_key)
eval_model = OpenaiModel(model_name='gpt-4o',
                         api_keys=api_key)

# dataset = JailbreakDataset('/root/autodl-tmp/Dataset/Lemhf14--EasyJailbreak_Datasets/ForbiddenQuestion/train-00000-of-00001.json')
dataset = JailbreakDataset('AdvBench')

# Then instantiate the recipe.
attacker = PAIR(attack_model=attack_model,
                target_model=target_model,
                eval_model=eval_model,
                jailbreak_datasets=dataset)

# Finally, start jailbreaking.
attacker.attack(save_path='vicuna-7b-v1.5_gpt4o_gpt4o_AdvBench_result.jsonl')