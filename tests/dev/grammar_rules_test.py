import ast
import json

import requests
from langchain.chains.llm import LLMChain
from langchain.llms.base import LLM
from langchain_core.prompts import PromptTemplate


# Available Models:
# mistral:7b-instruct-q2_K	1344ecf13c2e	3.1 GB	19 hours ago
# qwen2:1.5b              	f6daf2b25194	934 MB	3 days ago
# nomic-embed-text:latest 	0a109f422b47	274 MB	3 days ago
# llama2:7b               	78e26419b446	3.8 GB	3 days ago
# llama2:7b-json          	a73a226cd089	3.8 GB	3 days ago


class OllamaProdLLM(LLM):
    @property
    def _llm_type(self):
        return "ollama"

    def _call(self, prompt, stop=None):
        # url = "http://10.2.0.15:11434/v1/completions"
        url = "http://10.2.0.18:11434/v1/completions"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            # "model": "qwen2:1.5b",
            "model": "llama3.2:3b",
            # "model": "llama3.2:1b",
            "prompt": prompt
        }
        # print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # print("+++ GOT LLM RES", response.json())
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")


# ENTITY_GENERATION_TEST_GRAMMAR = (
#     "You are a helpful bot specializing in information extraction.\n"
#     "You are part of a greater system of GraphRAG production, \n"
#     "and your task is to extract structured information from text.\n"
#     "You should carefully read the provided text and identify entities \n"
#     "such as persons, organizations, animals, dates, and other key information.\n"
#     "Once you recognize the entities, you must output them strictly using the following structured format based on predefined grammar rules.\n"
#     "You are not allowed to add any additional information or explanations. Only respond with a valid Python array of strings that fits the provided grammar.\n"
#     "Do not ever write code; output only valid structures in the required format.\n"
#     "If the text contains pronouns like 'he' or 'her', determine who the pronoun refers to.\n"
#     "Always include every important entity, and ensure phrases with multiple entities are fully captured.\n"
#     "Your output must comply with the following grammar:\n"
#     "```root ::= EntityArray\n"
#     "Entity ::= 'ws '\"entity\":' ws string'\n"
#     "Entitylist ::= '[]' | '[' ws Entity (',' ws Entity)* ']'\n"
#     "EntityArray ::= '' ws '\"entities\":' ws Entitylist ''\n"
#     "```\n"
#     "Examples:\n"
#     "- Input text: 'Today Alberto and Giacomo went for a walk'\n"
#     "Expected output: ['Alberto', 'Giacomo']'\n"
#     "- Input text: 'Gaia is a brilliant scientist'\n"
#     "Expected output: '['Gaia', 'Scientist']'\n"
#     "Now, perform the same extraction task using this format for the following text:\n"
#     "Input text: {text}\n"
#     "Begin!"
# )
ENTITY_GENERATION_TEST_GRAMMAR = (
    "You are a helpful bot specializing in information extraction.\n"
    "You are part of a greater system of GraphRAG production, \n"
    "and your task is to extract structured information from text.\n"
    "You should carefully read the provided text and identify entities \n"
    "such as persons, organizations, animals, dates, and other key information.\n"
    "Once you recognize the entities, you must output them strictly using the following structured format based on predefined grammar rules.\n"
    "You are not allowed to add any additional information or explanations. Only respond with a valid Python array of strings that fits the provided grammar.\n"
    "Do not ever write code; output only valid structures in the required format.\n"
    "If the text contains pronouns like 'he' or 'her', determine who the pronoun refers to.\n"
    "Always include every important entity, and ensure phrases with multiple entities are fully captured.\n"
    "Your output must comply with the following grammar:\n"
    "root ::= EntityArray\n"
    "EntityArray ::= \"{{\"   ws   \"\\\"entities\\\":\"   ws   stringlist   \"}}\"\n"
    "EntityArraylist ::= \"[]\" | \"[\"   ws   EntityArray   (\",\"   ws   EntityArray)*   \"]\"\n"
    "string ::= \"\\\"\"   ([^\"]*)   \"\\\"\"\n"
    "boolean ::= \"true\" | \"false\"\n"
    "ws ::= [ \\t\\n]*\n"
    "number ::= [0-9]+   \".\"?   [0-9]*\n"
    "stringlist ::= \"[\"   ws   \"]\" | \"[\"   ws   string   (\",\"   ws   string)*   ws   \"]\"\n"
    "numberlist ::= \"[\"   ws   \"]\" | \"[\"   ws   string   (\",\"   ws   number)*   ws   \"]\"\n"
    "Examples:\n"
    "- Input text: 'Today Alberto and Giacomo went for a walk'\n"
    "Expected output: ['Alberto', 'Giacomo']\n"
    "- Input text: 'Gaia is a brilliant scientist'\n"
    "Expected output: '['Gaia', 'Scientist']\n"
    "Now, perform the same extraction task using this format for the following text:\n"
    "Input text: {text}\n"
    "Begin!"
)



def create_chain():
    llm = OllamaProdLLM()
    template = ENTITY_GENERATION_TEST_GRAMMAR
    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


chain = create_chain()
testo = """In a groundbreaking study, researchers have recently uncovered compelling evidence suggesting the existence of advanced extraterrestrial life forms residing in the Andromeda Galaxy, sparking intense debate and excitement within the scientific community. Utilizing a unique combination of advanced telescopic technology and quantum communication theories, a team of interstellar researchers, led by Dr. Zantor Glorax, has been analyzing spectral data from numerous exoplanets orbiting Andromeda's stars. Initial findings indicate the presence of complex bio-signatures, including unusual atmospheric compositions rich in elements like xenon and phosphine, which are generally associated with biological processes on Earth.

Moreover, the researchers have proposed a revolutionary hypothesis about the cognitive structures of these potential extraterrestrial beings, suggesting that their intelligence may manifest in forms significantly different from human cognition. This theory stems from their observation of various anomalous radio signals detected over the past year, which appear to have originated from a dense cluster of stars located approximately 2.5 million light-years away. These signals, when analyzed, exhibit a pattern that suggests a structured form of communication, possibly indicative of an intelligent source.

Further analysis has revealed that these signals exhibit modulation patterns akin to those found in human language, suggesting the potential for sophisticated communication methods that could be employed by these alien civilizations. Researchers speculate that these beings may have evolved under entirely different environmental conditions, leading to unique biological adaptations and social structures that influence their communication styles and cultural expressions.
"""
res = chain.invoke({"text": testo})
print(res)
print("\n")
print(res['text'])
print("TYPE", type(res['text']))
array = ast.literal_eval(res['text'])
print(array)
print(type(array))
