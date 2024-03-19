# import nltk
# from nltk import pos_tag, word_tokenize, RegexpParser
# from nltk.tree import Tree
from multiprocessing import Pool
import time

import spacy
from spacy import displacy

import re
from utils import classify_sentence_structure, simple_sentence_extracting, compound_sentence_extracting

def complex_sentence_extracting(sentence):
    # print(simple_sentence_extracting(sentence))
    return simple_sentence_extracting(sentence)

def compound_complex_sentence_extracting(sentence):
    return 

def extract_spo(sentence_dict):
    spo_list = []
    i = 1
    with Pool(processes=16) as pool: # Use 4 processes as an example
        for spo in pool.imap_unordered(process_sentence, sentence_dict.items()):
            spo_list.append(spo)
            i += 1
    return spo_list

def process_sentence(item):
    key, value = item
    condition, sentence = classify_sentence_structure(value)
    print(key, condition)
    if condition == 'simple_sentence':
        return simple_sentence_extracting(sentence)
    elif condition == 'compound_sentence':
        return compound_sentence_extracting(sentence)
    elif condition == 'complex_sentence':
        return complex_sentence_extracting(sentence)
    elif condition == 'compound_complex_sentence':
        return compound_complex_sentence_extracting(sentence)

if __name__ == '__main__':
    sentences1 = {
        "sentence_1": "Joachim Peiper was born on January 30, 1915",
        "sentence_2": "During World War II, Peiper served as an officer in the Waffen-SS",
        "sentence_3": "Peiper was involved in the Malmedy massacre",
        "sentence_4": "He was convicted of war crimes for his role in the massacre",
        "sentence_5": "Peiper's actions during the war were controversial",
        "sentence_6": "After the war, Peiper faced trial for his actions",
        "sentence_7": "Peiper denied responsibility for the crimes he was accused of",
        "sentence_8": "He was sentenced to prison for his involvement in the war crimes",
        "sentence_9": "Peiper's post-war life was marked by controversy",
        "sentence_10": "In 1976, Peiper was killed in France",
        "sentence_11": "Mentha is a genus of flowering plants in the mint family",
        "sentence_12": "The mentha plant has a strong, refreshing aroma",
        "sentence_13": "Mentha leaves are often used to flavor food and drinks",
        "sentence_14": "Peppermint is a type of mentha known for its cooling effect",
        "sentence_15": "Mentha oil is extracted from the leaves of the mentha plant",
        "sentence_16": "Mentha tea is a popular herbal beverage enjoyed for its soothing properties",
        "sentence_17": "Mentha cultivation requires moist soil and plenty of sunlight",
        "sentence_18": "Mentha can be grown in gardens or pots for easy access",
        "sentence_19": "Mentha products are widely used in the pharmaceutical and food industries",
        "sentence_20": "Mentha essential oil is used in aromatherapy for its invigorating scent",
        "simple_sentence_a": "The cat slept peacefully on the windowsill",
        "simple_sentence_b": "The cake was baked by Mary",
        "compound_sentence_a": "The sun was shining, and the birds were singing",
        "compound_sentence_test": "John is a soldier and a farmer and a lawyer", 
        "compound_sentence_test1": "John is a soldier and Leyla is a farmer", 
        "compound_sentence_test1.5": "John and Leyla and Davis is a farmer", 
        "compound_sentence_test1.9": "John, Leyla and Davis is a farmer, soldier and teacher respectively", #case น่าปวดหัว of the day
        "conflict": "John, Sarah and Jonathan are farmer",
        "compound_sentence_test2": "John is a soldier and a farmer and Sarah is a lawyer and president and secretary and Jason is a mechanic",  #Success for compound
        "compound_sentence_b": "Joachim Peiper was a high ranking SS officer, and he gained notoriety for his involvement in the Malmedy massacre during World War II",
        "compound_sentence_c": "Cecil played a key role in the execution of Mary, Queen of Scots, and he was instrumental in negotiating the Treaty of London.",
        "conflict" : "Cecil played a key role in the execution of Mary, Queen of Scots, and he was instrumental in negotiating the Treaty of London, but his efforts were overshadowed by political intrigue.",
        "compound_sentence_48": "The cat sat on the mat, but it soon got bored and wandered off.",
        "complex_sentence_d": "He played a crucial role in the succession of James I, and his political influence extended throughout the Elizabethan and Jacobean eras.", #poss case
        "complex_sentence_a": "Although it was raining, she decided to go for a walk",
        "complex_sentence_b": "Because he studied hard, he passed the exam with flying colors",
        # "compound_complex_sentence_a": "As adjutant to Himmler, Peiper witnessed the SS implement the Holocaust with ethnic cleansing and genocide of Jews in Eastern Europe; facts that he obfuscated and denied in the post-War period",
        # "compound_complex_sentence_b": "She opened the umbrella because it was raining, but the wind blew it away before she could use it",
        # "ccs_and_cs": "He wanted to go to the movies, but she preferred staying home, so they compromised and watched a movie at home instead" #ระบบคิดว่ามันคือ compound ซึ่งก็ถูกและคาดว่าไม่มีปัญหาหากจะนำไปวิเคราะห์ต่อ
    }
    
    complex_sentences = {
        # "sentence1": "Although she was tired, she continued working on her project.",
        # "sentence2": "Because he studied hard, he passed the exam with flying colors.",
        # "sentence3": "Since it was raining heavily, they decided to stay indoors.",
        # "sentence4": "After he finished his dinner, he went for a walk in the park.",
        # "sentence5": "Although the traffic was terrible, she arrived at the meeting on time.",
        # "sentence6": "Since they were running late, they took a taxi to the airport.",
        # "sentence7": "Because she was feeling unwell, she decided to see a doctor.",
        # "sentence8": "After the storm passed, they went outside to assess the damage.",
        # "sentence9": "Since he forgot his umbrella, he got drenched in the rain.",
        # "sentence10": "Although it was late, they stayed up to finish their work.",
        # "sentence11": "After she completed her studies, she started looking for a job.",
        # "sentence12": "Because they missed the bus, they had to walk home.",
        # "sentence13": "Since he had saved enough money, he decided to buy a new car.",
        # "sentence14": "Although the movie received mixed reviews, they decided to watch it.",
        # "sentence15": "After he lost his job, he struggled to pay his bills.",
        # "sentence16": "Because she was allergic to seafood, she avoided eating sushi.",
        # "sentence17": "Since they had already eaten dinner, they declined the invitation to join them for a meal.",
        # "sentence18": "Although he was tired, he stayed up late to finish reading the book.",
        # "sentence19": "After she graduated from college, she traveled around the world.",
        # "sentence20": "Because they were on a tight budget, they opted for a staycation instead of a vacation.", #case นี้ไง
        # "sentence21": "While I enjoy cricket, hockey is my favorite sport."
    }

    start_time = time.time()
    
    spo_list = extract_spo(sentences1)
    for spo in spo_list:
        print(spo)

    end_time = time.time()
    print(f"Multiprocessing time taken: {end_time - start_time:.4f} seconds")

    # spo_list = extract_spo(sentences1)
    # for spo in spo_list:
    #     print(spo)