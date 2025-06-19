import google.generativeai as genai

genai.configure(api_key="AIzaSyDZ3v-bceUq3sLbEtcKSAjd1CLQ_y7eQyo")

models = genai.list_models()
for m in models:
    print(m.name)
