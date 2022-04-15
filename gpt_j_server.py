import uvicorn
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from transformers import AutoTokenizer, GPTJForCausalLM,AutoModelForCausalLM
import json

class Input(BaseModel):
    prompt: str
    answer_length: int
    do_sample: bool
    top_p: float
    top_k: int
    temperature: float
    stop_words: list
    min_length: Optional[int] = None
    length_penalty: Optional[float] = None
    repetition_penalty: Optional[float] = None
    bad_words_ids: Optional[list] = None


app = FastAPI()
device = torch.device('cuda:2')
print('start')
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B",revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True).to(device)
#model2 = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B").to(device)
print('model load finish')
def stop_stopwords(tokenizer,answer,stop_words):
    stop_t = []
    for i in stop_words:
        stop_t.append(tokenizer.encode(i))
    #print(stop_t)
    answer = answer.tolist()
    for stopword in stop_t:
        answer_pair = []
        for i in range(len(answer)-len(stopword)+1):
            answer_pair.append(answer[i:i+len(stopword)])
        if stopword in answer_pair:
            loc = answer_pair.index(stopword)
            answer1 = answer[:loc]
            return answer1
    return answer

def gpt_j_create(prompt, answer_length, do_sample,
 top_p, top_k, temperature,stop_words = [' q:',' a:'],tokenizer = tokenizer,
 min_length = 10,length_penalty=1.0,repetition_penalty=1.0,bad_words_ids=[]):
    inputs = tokenizer(prompt, add_special_tokens=False, return_tensors="pt")["input_ids"].to(device)
    prompt_len = len(inputs[0])
    max_length = answer_length + prompt_len
    min_length = int(min_length) + prompt_len
    outputs = model.generate(inputs, 
        max_length=max_length,
        do_sample=do_sample,
        top_p=top_p,
        top_k=top_k,
        temperature=temperature,
        pad_token_id = 50256,
        early_stopping = False,
        min_length = min_length,
        length_penalty = length_penalty,
        repetition_penalty = repetition_penalty,
        bad_words_ids = bad_words_ids)
    answer = outputs[0][prompt_len:]
    answer = stop_stopwords(tokenizer,answer,stop_words)
    answer = tokenizer.decode(answer)
    return answer

@app.post("/gpt_j_server")
async def predict(item : Input):
    if item.min_length == None:item.min_length == 10
    if item.length_penalty == None:item.length_penalty=1.0
    if item.repetition_penalty == None:item.repetition_penalty=1.0
    if item.bad_words_ids == None:item.bad_words_ids = [[50399]]

    answer = gpt_j_create(
        prompt = item.prompt,
        answer_length = item.answer_length, 
        do_sample = item.do_sample, 
        top_p = item.top_p, 
        top_k = item.top_k, 
        temperature = item.temperature,
        stop_words = item.stop_words,
        tokenizer = tokenizer,
        min_length = item.min_length,
        length_penalty = item.length_penalty,
        repetition_penalty = item.repetition_penalty,
        bad_words_ids = item.bad_words_ids
        )
    return answer


if __name__ == '__main__':
    uvicorn.run(app="f1:app", port=8000, reload=True, debug=True)