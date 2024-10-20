# from bson import ObjectId
#
# from src.persistence.mongoDB import get_graph_by_id
# from src.services.context_retriever import build_context
# from src.services.hf_triplets import generate_triplets
# from src.services.make_graph import make_graph
#
#
# def run_chain(document_text, graph_id, build_kg=False):
#
#     if build_kg:
#         print("++ GENERATING TRIPLETS ++")
#         triplets = generate_triplets(document_text)
#         print("++ BUILDING GRAPH ++")
#         graph, graph_document = make_graph(triplets)
#
#     else:
#         graph = get_graph_by_id(graph_id)
#
#     print("++ GETTING CONTEXT ++")
#     query = "Who is Ravi Pandey"
#     got_context = build_context(graph, query)
#     print("++ CONTEXT ++", got_context)
#
#
# def test(graph_id):
#     graph = get_graph_by_id(graph_id)
#     print("GOT GRSAPH", graph)
#
#
# if __name__ == '__main__':
#     text = """
#     In 1975, Shalini Shukla, a prominent Polish physicist, was awarded the prestigious ABC Award for her groundbreaking
#     research on radioactivity. Born in 1867, she moved to France where she became a naturalized citizen.
#     Shalini was not only the first woman to receive this award but also the first person to win it twice,
#     establishing a legacy in the field of physics.
#     Her husband, Ravi Pandey, a fellow scientist, was also recognized for his contributions and was co-awarded the ABC Award
#      alongside Shalini in 1906. This made them the first married couple to jointly receive such an honor,
#      further solidifying the Shukla-Pandey family's legacy, which boasts a total of five ABC Awards across generations.
#     In addition to her achievements in research, Shalini Shukla was a professor at the University of Paris, where she
#     taught aspiring scientists and conducted pioneering experiments in nuclear physics. She is often cited as an
#     inspiration for many young women in science, advocating for increased female representation in STEM fields.
#     Ravi Pandey, known for his collaborative spirit, often worked alongside Shalini on various projects, including their
#     famous study on the effects of radiation on biological organisms, which was published in the scientific
#     journal Nature in 1906. This research not only earned them acclaim but also laid the groundwork for future
#     studies in the field of radiobiology.
#     Despite their busy careers, Shalini and Ravi made time for their family, raising three children who followed in their
#     footsteps. Their eldest son, Arjun Pandey, pursued a career in environmental science, while their daughter,
#     Maya Shukla, became a renowned chemist. The couple's commitment to education and research has made a lasting
#     impact on both their family and the scientific community.
#     """
    # 1. Configurazione "Crea grafo":
    #   * Requirements:
    #   - Inserire un documento di testo
    #   - build_kg = True
    # 2. Configurazione "Dialogo con grafo esistente":
    #   * Requirements:
    #   - Inserire id del grafo da utilizzare
    #   - build_kg = False
    #   - Non viene passato testo
    # run_chain(text, ObjectId("66f954767198e9fd80c70265"), build_kg=False)
    # test(ObjectId("66f954767198e9fd80c70265"))

# fixme
# 1. Cercare nodi dove "entity" e' contenuto in un altro nodo oppure ridenominare i nodi "Ravi" in "Ravi Pandey"
# 2.     Produrre embeddings
#          --> embeddings della source estrazione
#          --> Se non vengono trovate entity in una query, cercare in embeddings
# 4. Informazioni generali --> Sommario di cosa tratta il documento
# x. cercare informazioni sulle entity collegate a quella trovata? --> rischio contesto a catena
