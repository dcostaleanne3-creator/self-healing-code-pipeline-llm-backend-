from agents.llm_client import ask_llm

prompt = "Explain why Python cannot add a string and an integer."

response = ask_llm(prompt)

print(response)