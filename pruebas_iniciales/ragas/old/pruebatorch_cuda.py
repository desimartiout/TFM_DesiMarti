import torch

if torch.cuda.is_available():
    print("CUDA is available")
    print("Device:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available")

#Para habilitar CUDA en torch
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

#Prueba del modelo
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

inputs = tokenizer("Cual es la capital de España?", return_tensors="pt").to(device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
