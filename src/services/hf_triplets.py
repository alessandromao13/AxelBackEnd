from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def flatten_triplets(chunked_triplets):
    return [triplet for sublist in chunked_triplets for triplet in sublist]


def extract_triplets(text, chunk=None):
    triplets = []
    relation, subject, object_ = '', '', ''
    text = text.strip()
    current = 'x'

    # Split text into tokens
    tokens = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split()

    for token in tokens:
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append(
                    {'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip(), "source": chunk})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append(
                    {'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip(), "source": chunk})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token

    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip(), "source": chunk})
    return triplets


def chunk_text(text, max_length=1024):
    # Split the text into chunks based on a maximum length
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
gen_kwargs = {
    "max_length": 1024,
    "length_penalty": 0,
    "num_beams": 3,
    "num_return_sequences": 3,
}


def generate_triplets(text):
    model_inputs = tokenizer(text, max_length=1024, padding=True, truncation=True, return_tensors='pt')

    # Generate triplets for the entire text
    generated_tokens = model.generate(
        model_inputs["input_ids"].to(model.device),
        attention_mask=model_inputs["attention_mask"].to(model.device),
        **gen_kwargs,
    )

    # Extract text
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # Extract triplets from the entire text
    all_text_triplets = []
    for sentence in decoded_preds:
        triplet = extract_triplets(sentence)
        all_text_triplets.extend(triplet)

    # Chunking the text
    chunks = chunk_text(text)

    # Process each chunk
    all_chunked_triplets = []

    for idx, chunk in enumerate(chunks):
        print("CHUNK", chunk)
        print(f'Processing chunk {idx + 1}:')
        model_inputs = tokenizer(chunk, max_length=1024, padding=True, truncation=True, return_tensors='pt')

        # Generate
        generated_tokens = model.generate(
            model_inputs["input_ids"].to(model.device),
            attention_mask=model_inputs["attention_mask"].to(model.device),
            **gen_kwargs,
        )

        # Extract text
        decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

        # Extract triplets
        for sentence_idx, sentence in enumerate(decoded_preds):
            print(f'Prediction triplets for sentence {sentence_idx}:')
            print("SENTENCE:", sentence)
            triplet = extract_triplets(sentence, chunk)
            print("TRIPLET", triplet)
            if triplet not in all_chunked_triplets:
                print("Triplet is not in the list. Adding it.")
                all_chunked_triplets.append(triplet)
            else:
                print("++++ TRIPLET already exists in the list")

    flat_chunked_triplets = flatten_triplets(all_chunked_triplets)

    unique_triplets = {tuple(triplet.items()) for triplet in all_text_triplets}
    unique_triplets.update(tuple(triplet.items()) for triplet in flat_chunked_triplets)
    final_triplets = [dict(triplet) for triplet in unique_triplets]
    print("++ ALL TEXT TRIPLETS")
    print(all_text_triplets)
    print("++ ALL CHUNKED TRIPLETS")
    print(flat_chunked_triplets)
    print("++ FINAL UNIQUE TRIPLETS")
    print(final_triplets)
    print("LGT", len(final_triplets))
    return final_triplets


