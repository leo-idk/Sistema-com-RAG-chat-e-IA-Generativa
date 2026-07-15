from openai import OpenAI

token = input("Paste your GitHub Models Token here: ")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

print("Loading factory knowledge base...")

try:
    with open("data.txt", "r", encoding="utf-8") as file:
        knowledge = file.read()
    print("Knowledge base loaded successfully!\n")
except FileNotFoundError:
    knowledge = "No extra data found."
    print("File 'data.txt' not found!\n")

system_instructions = f"""
You are the virtual assistant for the factory anomaly totem.
Answer the operators' questions based EXCLUSIVELY on the rules below.
If the question is not in the rules, say you do not have this information.
Respond in a short, direct, and technical manner.

FACTORY DATABASE:
{knowledge}
"""

chat_history = [
    {"role": "system", "content": system_instructions}
]

print("Chat ready! Type 'exit' to close the system.")

while True:

    operator_question = input("\nReport the anomaly or question:\n> ")
    
    if operator_question.lower() == 'exit':
        print("\nPowering down the Totem. Have a great shift!")
        break

    print("Analyzing machine manuals...\n")

    chat_history.append({"role": "user", "content": operator_question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history
    )

    ai_response = response.choices[0].message.content

    print(ai_response)

    chat_history.append({"role": "assistant", "content": ai_response})
