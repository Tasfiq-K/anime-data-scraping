import gradio as gr
import onnxruntime as rt
from transformers import AutoTokenizer
import torch, json

tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

with open("task_types_encoded.json", "r") as fp:
  encode_task_types = json.load(fp)

tasks = list(encode_task_types.keys())

inf_session = rt.InferenceSession('paper_task_classifier_quantized.onnx')
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name

def classify_book_genre(description):
  input_ids = tokenizer(description)['input_ids'][:512]
  logits = inf_session.run([output_name], {input_name: [input_ids]})[0]
  logits = torch.FloatTensor(logits)
  probs = torch.sigmoid(logits)[0]
  return dict(zip(tasks, map(float, probs))) 

label = gr.outputs.Label(num_top_classes=10)
iface = gr.Interface(fn=classify_book_genre, inputs="text", outputs=label)
iface.launch(inline=False)