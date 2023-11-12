import os
from embeder.retriever import get_most_close_sources
from tenacity import retry, wait_exponential
import openai
from openai import OpenAI
from constants.constants import OPENAI_KEY

# openai.api_key = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# context = ". ".join([el.text for el in get_most_close_sources(text)])
# print(context)
# for el in a:
#     print(el.link.strip())

def get_context(question: str, top_k: int):
    neighbors = get_most_close_sources(question, top_k)
    resp = [(el.text, el.link) for el in neighbors]
    context = [x[0] for x in resp]
    context = "\n".join(context)
    sources = {x[1] for x in resp}
    # print("srr", sources)
    return context, sources


def get_prompt(question: str, context: str):
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": f'''"{context}"'''},
        {"role": "user", "content": f'''"{question}"'''},
    #     {
    #         "role": "user",
    #         "content": f"""Answer the following Question based on the Context only. Only answer from the Context. If you don't know the answer, say 'I don't know'.
    # Question: {question}\n\n
    # Context: {context}\n\n
    # Answer:\n""",
        # },
    ]

# Function with tenacity for retries
@retry(wait=wait_exponential(multiplier=1, min=2, max=6))
def api_call(messages, model):
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stop=["\n\n"],
        max_tokens=100,
        temperature=0.0,
    )
# Main function to answer question
def answer_question(question: str, prompt_func=get_prompt, model="gpt-3.5-turbo-1106"):
    context = get_context(question, top_k=5)
    print(f"{context=}")
    messages = prompt_func(question, context)
    response = api_call(messages, model)
    return response["choices"][0]["message"]["content"]


# text = "who has been subsidizing its own steel industry for decades?"
# llm_response = answer_question(text)
# print(llm_response)

client = OpenAI(
    api_key=os.getenv('OPENAI_KEY')
)

# question = "who has been subsidizing its own steel industry for decades?"
# context = get_context(question, top_k=8)
# messages=get_prompt(question, context)

def get_llm_response(question: str):

    context, sources = get_context(question, top_k=8)
    messages=get_prompt(question, context)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
    )

    answer = "Thank you for waiting! \n\nThat is my response:\n\n    "
    answer = answer + "\n".join([choice.message.content for choice in response.choices])
    if sources:
        sources = "\n".join([src.strip() for src in sources])
        answer = answer + '\n\nsource links: \n\n' + sources

    return answer


# question = "who has been subsidizing its own steel industry for decades?"

# answer = get_llm_response(question)
# print(f"{answer}")
