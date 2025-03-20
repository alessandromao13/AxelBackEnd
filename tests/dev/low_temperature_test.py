import ast
import json

import requests
from langchain.chains.llm import LLMChain
from langchain.llms.base import LLM
from langchain_core.prompts import PromptTemplate


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
            "prompt": prompt,
            "temperature": 0
        }
        # print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # print("+++ GOT LLM RES", response.json())
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")


ENTITY_GENERATION_TEST = ("You are a bot that is helpful. \n"
                           "you are part of a greater system of GraphRAG production. \n"
                           "You goal is, given a text, to read it and extract structured information's from the text. \n"
                           "First, you should read the text and recognize the entities involved. \n"
                           "Please note that an entity can be a person, an organization, an animal, a date , etc.. \n"
                           "You should produce a python array containing all the entities. \n"
                           "Do not add any other information's or explanations, only the python structure. "
                          "Please ouput only one array at a time. \n"
                          "Do not ever write code, you only output python arrays string .\n"
                           "If the text contains pronouns as 'he' or 'her' \n"
                           "you should try to understand who is the pronoun referring to.\n"
                           "You should do this with every information that seem important in the text, \n "
                           "remember that a phrase can contain multiple entities if theres a lot of information's. \n "
                           "Here are some examples: \n "
                           "- 1. Input text: 'Today Alberto and Giacomo went for a walk' \n"
                           "Expected output: ['Alberto', 'Giacomo'] \n"
                           "- 2. Input text: 'Gaia is a brilliant scientist' \n"
                           "Expected output: ['Gaia', 'Scientist'] \n"
                           "- 3. Input text: 'Andrea loves ice cream, he dreams of opening his own business soon' \n"
                           "Expected output: ['Andrea', 'Ice Cream', 'Business']\n "
                           "Now, based on this information's, repeat the same process over this data: \n "
                           "Input text is: \n "
                           "{input_text} \n"
                           "Begin!"
                           )


RELATION_GENERATION_TEST = ("You are a bot that is helpful. \n"
                           "You are part of a greater system of GraphRAG production. \n"
                           "Your goal is, given a text chunk and an array of entities, \n"
                           "to extract structured information from the text. \n"
                           "First, read the provided array of entities and recognize the relationships between them. \n"
                           "Entities can include people, organizations, animals, dates, etc. \n"
                           "Output a Python array containing all the entities and their relationships. \n"
                           "Do not add any other information or explanations; only return the Python structure. \n"
                           "Never write code; only output Python array strings. \n"
                           "If the text contains pronouns such as 'he' or 'her', \n "
                            "try to identify who the pronoun refers to and output the entity instead of the pronoun. \n"
                           "Ensure to capture all important information in the text, as a phrase can contain multiple entities. \n"
                           "Examples: \n"
                           "- Input text: 'Today Alberto and Giacomo went for a walk.' \n"
                           "  Provided entities: ['Alberto', 'Giacomo'] \n"
                           "  Expected output: [{{'src': 'Alberto', 'dst': 'Giacomo', 'rel': 'went for a walk'}}] \n"
                           "- Input text: 'Gaia is a brilliant scientist.' \n"
                           "  Provided entities: ['Gaia', 'Scientist'] \n"
                           "  Expected output: [{{'src': 'Gaia', 'dst': 'Scientist', 'rel': 'occupation'}}] \n"
                           "- Input text: 'Andrea loves ice cream; he dreams of opening his own business soon.' \n"
                           "  Provided entities: ['Andrea', 'Ice Cream', 'Business'] \n"
                           "  Expected output: [{{'src': 'Andrea', 'dst': 'Ice Cream', 'rel': 'loves'}}, {{'src': 'Andrea', 'dst': 'Ice Cream Business', 'rel': 'dreams of opening'}}] \n"
                           "Output directives: \n"
                           "- Every dictionary must be well formatted. \n"
                           "- Each dictionary should contain exactly the keys: 'src', 'dst', 'rel' and no others. \n"
                           "- No dictionary should contain empty or None values. \n"
                           "- Each dictionary must contain one 'src' and one 'dst' per relation. \n"
                           "- If you lack sufficient information to complete a dictionary, do not output it at all. \n"
                           "- Avoid including any punctuation or extraneous text that is not part of the relationship. \n"
                           "Now, based on this information, process the following data: \n"
                           "Detected entities: \n"
                           "{detected_entities} \n"
                           "Input text is: \n"
                           "{input_text_chunk} \n"
                           "Begin!"
                           )


testo = """
In a groundbreaking study, researchers have recently uncovered compelling evidence suggesting the existence of advanced extraterrestrial life forms residing in the Andromeda Galaxy, sparking intense debate and excitement within the scientific community. Utilizing a unique combination of advanced telescopic technology and quantum communication theories, a team of interstellar researchers, led by Dr. Zantor Glorax, has been analyzing spectral data from numerous exoplanets orbiting Andromeda's stars. Initial findings indicate the presence of complex bio-signatures, including unusual atmospheric compositions rich in elements like xenon and phosphine, which are generally associated with biological processes on Earth.
Moreover, the researchers have proposed a revolutionary hypothesis about the cognitive structures of these potential extraterrestrial beings, suggesting that their intelligence may manifest in forms significantly different from human cognition. This theory stems from their observation of various anomalous radio signals detected over the past year, which appear to have originated from a dense cluster of stars located approximately 2.5 million light-years away. These signals, when analyzed, exhibit a pattern that suggests a structured form of communication, possibly indicative of an intelligent source.
Further analysis has revealed that these signals exhibit modulation patterns akin to those found in human language, suggesting the potential for sophisticated communication methods that could be employed by these alien civilizations. Researchers speculate that these beings may have evolved under entirely different environmental conditions, leading to unique biological adaptations and social structures that influence their communication styles and cultural expressions.
To advance their investigation, the team has developed the Quantum Entangled Communication Relay (QECR), a novel apparatus designed to utilize quantum entanglement for instantaneous data transmission across interstellar distances. Preliminary tests of the QECR have yielded promising results, demonstrating its potential to facilitate communication with extraterrestrial civilizations. The researchers believe that if these beings exist, they might already be aware of our presence through the same radio signals we have been detecting.
"""


def create_entity_chain():
    llm = OllamaProdLLM()
    template = ENTITY_GENERATION_TEST
    prompt = PromptTemplate(
        template=template,
        input_variables=["input_text"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def create_entity_relation_chain():
    llm = OllamaProdLLM()
    template = RELATION_GENERATION_TEST
    prompt = PromptTemplate(
        template=template,
        input_variables=["detected_entities", "input_text_chunk"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


chain = create_entity_chain()
entities_res = chain.invoke({"input_text": testo})
print("RES", entities_res['text'])
entities = ast.literal_eval(entities_res['text'])
print("JSON", entities)
print("TYPE", type(entities))

triplet_chain = create_entity_relation_chain()
triplet_res = triplet_chain.invoke({"detected_entities": entities, "input_text_chunk": testo})
print("RESULT", triplet_res)
print("RESULT", triplet_res['text'])
triplets = ast.literal_eval(triplet_res['text'])
print("TRIPLETS", triplets)
print("TYPE", type(triplets))



