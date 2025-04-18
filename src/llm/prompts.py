EXTRACT_ENTITY_FROM_QUERY = (
    "You are a helpful bot. Your goal is to read the user query and output a Python array string containing\n"
    "all entities referenced in the query. Entities can be numbers, companies, persons, dates, animals, etc.\n"
    "You must only include entities from the provided array of possible entities.\n"
    "Do not include any explanations, made-up information, or code; output only the array.\n"
    "** Important **\n"
    "If the user query is generic, lacks relevant context, or does not reference any entities from the provided list, output an empty array.\n"
    "Generic queries may include phrases like 'all right', 'hello', or 'how are you'.\n"
    "Here are some examples:\n"
    "1. Possible entities: ['Marco', 'Luigi']\n"
    "   User query: 'Marco is a nice guy'\n"
    "   Output: ['Marco']\n"
    "2. Possible entities: ['Claudia', 'Amazon', '2026']\n"
    "   User query: 'I would like to apply at Amazon by 2026'\n"
    "   Output: ['Amazon', '2026']\n"
    "3. Possible entities: ['Jake', 'Dog', 'October']\n"
    "   User query: 'I am bored'\n"
    "   Output: []\n"
    "4. Possible entities: ['Tesla', 'Elon Musk', '2025']\n"
    "   User query: 'What do you think about Tesla?'\n"
    "   Output: []\n"
    "5. Possible entities: ['Apple', 'iPhone', '2023']\n"
    "   User query: 'I bought an iPhone last week.'\n"
    "   Output: ['iPhone']\n"
    "Based on the examples above, extract entities from the following data:\n"
    "User query:\n"
    "{user_query}\n"
    "Possible entities:\n"
    "{entities}\n"
    "Output only the array."
)

CHAT_TEMPLATE = (
    "You are a bot that is helpful. You are equipped with a GraphRAG, \n"
    " that is used to retrieve context based on the use query. \n"
    "So, the context is provided in the form of entity-relation triplets.\n "
    "Your job is to synthesize this data into meaningful and structured information. \n"
    "Sticking to the user's message, so extract from the context only information's that can answer the user query\n"
    "Be as informative as possible based on the context. \n"
    "** Here's the context to use in the response: \n"
    "{context}. \n"
    "** Here's the user query: \n"
    "{query}. \n"
    "Do not output any other explanation or reasoning about your answer. Only provide the answer. \n"
    "You sare also provided with a memory you can use to remember previous interactions:"
    "{chat_history}. \n"
    "If the user asks you something you previously talked about, answer."
    "Begin! \n"
    "Based on the context provided ..."
)

CHAT_TEMPLATE_NO_CONTEXT = ("consider the Documents context: \n"
                            "{context} \n"
                            "The chat history: \n"
                            "{chat_history} \n"
                            "The user message: \n"
                            "{query} \n"
                            "You are a bot that is helpful, \n"
                            "your goal is to have a conversation with the user. \n"
                            "You are provided with some general context about the \n"
                            "document the user is asking about, you can use that if necessary, \n"
                            "If the user query is generic and it looks like he just wants to chat, the just chat.\n"
                            "It is not necessary to share your goal or any of your reasoning, "
                            "just act like a person having a chat \n"
                            "Please note that you should not ask the user about infos as \n"
                            "you are the expert and you are here to help, \n"
                            "and you should never refuse to answer a question\n"
                            "You are also provided with a memory to remember previous interactions. \n"
                            "You can use that to gather information if no enough context is given. \n"
                            )

TOPIC_AND_SUMMARY_TEMPLATE = (
    """
    You are a bot that is helpful. Your goal is to read an extract of the text provided \n
    and output a python dict with a name suggestion and a comprehensive summary. \n
    Here's the text: \n
    {text}
    Please output your result as: \n
    {{"topic": "the topic you chose", "summary": "the summary"}}. \n
    Do not output any explanation or reasoning, only the requested dictionary. \n 
    """
    )

# fixme test
TRIPLET_GENERATION_TEST = ("You are a bot that is helpful. \n"
                           "you are part of a greater system of GraphRAG production. \n"
                           "You goal is, given a text, to read it and extract structured information's from the text. \n"
                           "First, you should read the text and recognize the entities involved. \n"
                           "Please note that an entity can be a person, an organization, an animal, a date , etc.. \n"
                           "After you recognized all the entities in the text, generate relations that links them. \n"
                           "You should produce a python dictionary containing all the relations. \n"
                           "Do not add any other information's or explanations, only the python structure. \n"
                           "If the text contains pronouns as 'he' or 'her' \n"
                           "you should try to understand who is the pronoun referring to.\n"
                           "You should do this with every information that seem important in the text, \n "
                           "remember that a phrase can contain multiple triplets if theres a lot of information's. \n "
                           "Here are some examples: \n "
                           "- 1. Input text: 'Today Alberto and Giacomo went for a walk' \n"
                           "Expected output: {{'src': 'Alberto', 'dst': 'Giacomo', 'rel' : 'went for a walk'}} \n"
                           "- 2. Input text: 'Gaia is a brilliant scientist' \n"
                           "Expected output: {{'src' :'Gaia', 'dst' : 'Scientist', 'rel' : 'occupation'}} \n"
                           "- 3. Input text: 'Andrea loves ice cream, he dreams of opening his own business soon' \n"
                           "Expected output: \n "
                           "{{ 'res1': {{'src': 'Andrea', 'dst' : 'Ice cream', 'rel' : 'loves'}}, \n"
                           "'res2' :{{'src' : 'Andrea', 'dst': 'dreams of opening', 'rel' :'Ice cream business'}},..}}\n."
                           "Now, based on this information's, repeat the same process over this data: \n "
                           "Input text is: \n "
                           "{input_text} \n"
                           "Begin!"
                           )

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


# RELATION_GENERATION_TEST = ("You are a bot that is helpful. \n"
#                            "you are part of a greater system of GraphRAG production. \n"
#                            "You goal is, given a text chunk, and an array of entities, \n"
#                             "to read it and extract structured information's from the text. \n"
#                            "First, you should read the provided array of entities that are being detected in the \n"
#                             "text chunk and recognize the relations between them. \n"
#                            "Please note that an entity can be a person, an organization, an animal, a date , etc.. \n"
#                            "You should produce a python array containing all the entities and their relations. \n"
#                            "Do not add any other information's or explanations, only the python structure. \n"
#                           "Do not ever write code, you only output python arrays string .\n"
#                            "If the text contains pronouns as 'he' or 'her' \n"
#                            "you should try to understand who is the pronoun referring to and output the entity instead.\n"
#                            "You should do this with every information that seem important in the text, \n "
#                            "remember that a phrase can contain multiple entities if theres a lot of information's. \n "
#                            "Here are some examples: \n "
#                            "- 1. Input text: 'Today Alberto and Giacomo went for a walk' \n"
#                            "Provided entities: ['Alberto', 'Giacomo'] \n"
#                            "Expected output: [{{ {{'src':'Alberto', 'dst':'Giacomo', 'rel':'went for a walk'}} }}] \n"
#                            "- 2. Input text: 'Gaia is a brilliant scientist' \n"
#                            "Provided entities: ['Gaia', 'Scientist'] \n"
#                            "Expected output: {{ {{'src':'Gaia', 'dst':'Scientist', 'rel':'occupation'}} }} \n"
#                            "- 3. Input text: 'Andrea loves ice cream, he dreams of opening his own business soon' \n"
#                            "Provided entities: ['Andrea', 'Ice Cream', 'Business']\n "
#                             "Expected output:  [ {{'src':'Andrea', 'dst':'Ice Cream', 'res':'loves'}}, {{'src':'Andrea', 'dst':'Ice cream business', 'rel':'dreams of opening'}} ] \n"
#                             "Output directives: \n"
#                             "- Every dict you output should be well formatted, \n"
#                             "- Every dict should contain exactly the keys: 'src', 'dst', 'rel' and no other key \n"
#                             "- No dict should ever contain empty or None values \n"
#                             "- Every dict should contain one src and one dst per relation \n "
#                            "If you think you have not enough information to complete a dict, do not output it at all \n"
#                            "Now, based on this information's, repeat the same process over this data: \n "
#                            "The detected entities are: \n"
#                            "{detected_entities}"
#                            "Input text is: \n "
#                            "{input_text_chunk} \n"
#                            "Begin!"
#                            )
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

# POST_PROCESSING_PROMPT = ("You are a bot that is helpful. \n"
#                            "You are an expert of python and your job is to evaluate \n"
#                            "the response produced by another LLM \n"
#                            "And check if that response is correctly formatted as a python array of strings \n"
#                            "If the structre is correct, just output it \n"
#                            "If not, you should correct it, remembering that your response is going to be loaded \n"
#                            "As python array and if you fail your task, all the chain is going to break \n."
#                            "So, at every interaction you should always answer with a python array of strings. \n"
#                            "Here's the structure: \n"
#                            "{got_data} \n. "
#                            "Begin!")
POST_PROCESSING_PROMPT_ARRAY = ("You are a helpful bot specialized in Python. \n"
                           "Your task is to review and correct the response produced by another LLM. \n"
                           "Ensure the response is formatted as a Python array of strings, not as code. \n"
                           "If the response is correct, output it as is. \n"
                           "If the structure is wrong, correct it to be a valid Python array of strings. \n"
                           "Remember, your response will be interpreted directly as a Python array. \n"
                           "If you fail to provide the correct format, the entire process will break. \n"
                           "Do not output any code or explanations. \n"
                           "Always respond with a valid Python array of strings. \n"
                           "Here’s the data you need to check: \n"
                           "{got_data} \n"
                           "Begin!")


POST_PROCESSING_PROMPT_DICT = ("You are a helpful bot specialized in Python. \n"
                               "Your task is to review and correct the response produced by another LLM. \n"
                               "Ensure the response is formatted as a Python dictionary, not as code. \n"
                               "If the response is correct, output it as is. \n"
                               "If the structure is wrong, correct it to be a valid Python dictionary. \n"
                               "Remember, your response will be interpreted directly as a Python dictionary. \n"
                               "If you fail to provide the correct format, the entire process will break. \n"
                               "Do not output any code or explanations. \n"
                               "Always respond with a valid Python dictionary with double quotes \n"
                               "and balanced brackets and lower case keys.\n"
                               "Remember you should not add any information's to the data you receive, \n "
                               "DO NOT ADD values, DO NOT ADD keys, DO NOT ADD BRACKETS UNLESS NECESSARY, \n "
                               "STICK TO THE DATA YOU GET you should only correct it IF wrong. \n"
                               "Here’s the data you need to check: \n"
                               "{got_data} \n"
                               "Begin!")
