import json
import time

from src.services.chat import create_summarization_chain
from src.services.hf_triplets import generate_triplets
from src.services.make_graph import make_graph


def get_execution_time(start_time):
    # End time
    end_time = time.time()

    # Calculate execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")


def generate_kg(text, user_id=None, topic=None, summary=None):
    print(f"Building new graph from text: {text}")
    if topic is None and summary is None:
        topic, summary = produce_topic_and_summary(text)
    triplets = generate_triplets(text)
    graph = make_graph(text, triplets, topic, summary, user_id)
    return graph


def produce_topic_and_summary(text):
    chain = create_summarization_chain()
    llm_result = chain.invoke({"text": text})
    # print("+++ GOT LLM RESULT", llm_result)
    processed_res = process_llm_response(llm_result)
    try:
        topic = processed_res['topic']
        summary = processed_res['summary']
        return topic, summary
    except KeyError as e:
        print(f"ERROR EXTRACTING TOPIC AND SUMMARY {e}")
        return None, None


def process_llm_response(llm_res):
    try:
        cleaned_string = extract_inner_content(llm_res['text'])
        loaded_result = json.loads(cleaned_string)
        return loaded_result
    except json.JSONDecodeError as e:
        print(f"ERROR PRODUCING JSON {e}")
    return None


def extract_inner_content(response):
    start_index = response.find('{')
    end_index = response.rfind('}') + 1
    inner_content = response[start_index:end_index]
    inner_content = inner_content.replace("'", '"')
    inner_content = inner_content.replace(".", '')
    return inner_content


# if __name__ == '__main__':
#     text = """
#     In a groundbreaking study, researchers have recently uncovered compelling evidence suggesting the existence of advanced extraterrestrial life forms residing in the Andromeda Galaxy, sparking intense debate and excitement within the scientific community. Utilizing a unique combination of advanced telescopic technology and quantum communication theories, a team of interstellar researchers, led by Dr. Zantor Glorax, has been analyzing spectral data from numerous exoplanets orbiting Andromeda's stars. Initial findings indicate the presence of complex bio-signatures, including unusual atmospheric compositions rich in elements like xenon and phosphine, which are generally associated with biological processes on Earth.
# Moreover, the researchers have proposed a revolutionary hypothesis about the cognitive structures of these potential extraterrestrial beings, suggesting that their intelligence may manifest in forms significantly different from human cognition. This theory stems from their observation of various anomalous radio signals detected over the past year, which appear to have originated from a dense cluster of stars located approximately 2.5 million light-years away. These signals, when analyzed, exhibit a pattern that suggests a structured form of communication, possibly indicative of an intelligent source.
# Further analysis has revealed that these signals exhibit modulation patterns akin to those found in human language, suggesting the potential for sophisticated communication methods that could be employed by these alien civilizations. Researchers speculate that these beings may have evolved under entirely different environmental conditions, leading to unique biological adaptations and social structures that influence their communication styles and cultural expressions.
#
# To advance their investigation, the team has developed the Quantum Entangled Communication Relay (QECR), a novel apparatus designed to utilize quantum entanglement for instantaneous data transmission across interstellar distances. Preliminary tests of the QECR have yielded promising results, demonstrating its potential to facilitate communication with extraterrestrial civilizations. The researchers believe that if these beings exist, they might already be aware of our presence through the same radio signals we have been detecting.
#
# In addition to communication strategies, the researchers have explored the implications of using gravitational wave technology to send messages to potential extraterrestrial intelligences. They theorize that gravitational waves could serve as an effective medium for transmitting information, as these waves travel unimpeded through the fabric of space-time. By encoding messages in gravitational wave signals, humanity could potentially reach out to these distant civilizations, fostering a new era of intergalactic dialogue.
#
# The researchers have also made strides in identifying candidate exoplanets within the Andromeda Galaxy that are most likely to harbor life. Through meticulous analysis of data gathered from the Andromeda X-1 system, they have pinpointed three specific exoplanets, designated X-1a, X-1b, and X-1c, as prime targets for further investigation. These planets exhibit Earth-like characteristics, including stable atmospheres and suitable temperatures for sustaining liquid water, a crucial factor for life as we know it.
#
# To confirm the presence of life on these planets, the team plans to deploy a series of unmanned exploratory spacecraft equipped with advanced sensors capable of analyzing the atmospheres and surfaces of these distant worlds. If successful, this mission could provide definitive evidence of extraterrestrial life, fundamentally altering our understanding of life in the universe.
#
# In light of these remarkable findings, the scientific community has begun to reconsider long-held assumptions about the uniqueness of life on Earth. While skepticism remains, the possibility that we are not alone in the universe has ignited a new wave of enthusiasm and curiosity among researchers and the general public alike. Future collaborations with international space agencies and private space exploration companies are in the planning stages, aimed at enhancing our capabilities for interstellar exploration and communication.
#
# As humanity stands on the brink of potentially making contact with an intelligent alien civilization, ethical considerations regarding our approach to such interactions have come to the forefront. Debates surrounding the implications of revealing our existence to extraterrestrial beings are ongoing, with experts emphasizing the need for caution and a well-thought-out strategy for communication. Ultimately, this groundbreaking research not only enhances our understanding of the universe but also challenges us to rethink our place within it. The quest for knowledge continues, and as we delve deeper into the mysteries of the cosmos, the possibility of discovering intelligent life in the Andromeda Galaxy seems closer than ever.
#     """
#     generate_kg(text)

# # fixme: main for testing purposes
# if __name__ == '__main__':
#     text = """
#     Artemis Corp was founded by Athena Helios in the year 2010, with its headquarters located in the city of Olympus,
#     which is part of the country Skyland. Athena Helios is married to Apollo Solaris, who works as an astrophysicist
#     at the Solar Research Institute. The institute itself has been in operation since 1985.
#     Athena Helios is well known for her achievements, including receiving the prestigious Golden Innovation Award.
#     She was also mentored by Hestia Ignis, a renowned molecular chemist who won the Nobel Prize in Chemistry for her
#     contributions to the field. Artemis Corp also developed a significant project known as Hyperion, which aims to
#     provide renewable energy solutions, and it earned the Green Tech Prize for its groundbreaking advancements.
#     Apollo Solaris, aside from his work at the Solar Research Institute, made a significant discovery—a star named
#     Solaris Nova, which is located in the constellation Phoenix.
#     """
#     # json_sbagliato = "ecco a te la risposta bastardo {'1': 'x', '2': y'}x fai cosa credi"
#     # print(extract_inner_content(json_sbagliato))
#     produce_topic_and_summary(text)
