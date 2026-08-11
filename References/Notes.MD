## **Two Types of Language Models**


### **1. Masked Language Models (BERT-style) ->**  my - color is black
Bidirectional Encoder Representations from Transformers

**Masked Model (BERT)** = Fill in the blanks in an exam paper

- Predict missing tokens anywhere
- Uses left + right context
- Best for understanding tasks
Examples:

- Sentiment analysis
- Classification
- Code understanding
[https://www.geeksforgeeks.org/nlp/masked-language-models/](https://www.geeksforgeeks.org/nlp/masked-language-models/) 

> my  Fav color is black



“Playwright is a [MASK] automation tool.”



“Playwright is a **browser/web** automation tool.”



### **2. Autoregressive Language Models (GPT-style)**
**Autoregressive Model (GPT)** = Write an essay one word at a time

> Generative Pre-trained Transformer

- Predict next token only
- Generate text sequentially
- Best for **generation**
    - text
    - code
    - image
    - video
    - .....anythhing.



Examples:

- ChatGPT
- Code generation
- Writing, summarization


➡️ We mainly focuses on **autoregressive models**

> My eye color is _Black, Brown ,Grey



GPT -> Generative Pre Trained Transformer.



Read It and Give a Task - [app.thetestingacademy.com/ai/ml-ai-dl-engineer#tab1](https://app.thetestingacademy.com/ai/ml-ai-dl-engineer#tab1) 



1. LLM ->  large language model that predicts and generates text token-based 
2. Transformer ->  It is an attention-based neural architecture used by most modern large language models 
3. Paramaters
---

## Paramaters
Parameters in Large Language Models are the internal **weights and biases** that the model learns during training. 

More Parameter have you better. LLM





![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image_tBhlRJtRpMi7YF_-RWpB-.png?ixlib=js-3.8.0 "image.png")





![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image__sYCUaRX_EDQvLszzh95G.png?ixlib=js-3.8.0 "image.png")

Large Language Model  > 1B Large

Small Language Model < 1B  (SLM)



**Closed Source LLM**

- GPT 5.6


**Open Source LLM**

- Mistral 4
- DeepSeek v4 Flash


[huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/tree/main](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/tree/main) 

Hugging face is like a GitHub for the models, where you can host your model, you can download a model, and you can deploy and use it or test it also in this case.



