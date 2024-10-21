from src.llm.prompts import EXTRACT_ENITTY_FROM_QUERY, CHAT_TEMPLATE, TOPIC_AND_SUMMARY_TEMPLATE, \
    CHAT_TEMPLATE_NO_CONTEXT, TRIPLET_GENERATION_TEST, ENTITY_GENERATION_TEST, RELATION_GENERATION_TEST, \
    POST_PROCESSING_PROMPT_ARRAY, POST_PROCESSING_PROMPT_DICT


def get_entity_recognition_template():
    return EXTRACT_ENITTY_FROM_QUERY


def get_chat_template():
    return CHAT_TEMPLATE


def get_chat_template_no_context():
    return CHAT_TEMPLATE_NO_CONTEXT


def get_topic_and_summary_template():
    return TOPIC_AND_SUMMARY_TEMPLATE


# fixme test
def get_triplet_production_template():
    return TRIPLET_GENERATION_TEST


# fixme test
def get_entity_production_template():
    return ENTITY_GENERATION_TEST


# fixme test
def get_relation_production_template():
    return RELATION_GENERATION_TEST


# fixme test
def get_data_check_template_array():
    return POST_PROCESSING_PROMPT_ARRAY


def get_data_check_template_dict():
    return POST_PROCESSING_PROMPT_DICT
