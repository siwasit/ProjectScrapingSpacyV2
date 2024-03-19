import re, spacy
from spacy import displacy

def is_contained_in(a, b):
    return any(elem in b for elem in a)

def sep_sentence(compound_sentence, cconj):
    clauses = (re.split(rf'\s*\b({'|'.join(cconj)})\b\s*', compound_sentence))
    result = []
    for clause in clauses:
        if any(conj in clause for conj in cconj):
            sub_clauses = []
            while any(conj in clause for conj in cconj):
                sub_clause = clause.strip()
                sub_clauses.append(sub_clause)
                clause = ' '.join(sub_clause.split()[1:])
            result.extend(sub_clauses)
        else:
            result.append(clause.strip())
    return result

def classify_sentence_structure(sentence):
    # Perform part-of-speech tagging
    cleaned_sentence = re.sub(r'\([^)]*\)', '', sentence)

    # print(cleaned_sentence)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(cleaned_sentence)

    result = ''

    verb_index = []
    for i, token in enumerate(doc):
        if token.dep_ == 'ROOT':
            # verb_index.append(token)
            verb_index.append(i)
            verb_index += [i for i, word in enumerate(token.children) if word in [j for j in token.conjuncts]]
    verb = [doc[index] for index in verb_index]

    # marks = [token.dep_ for token in doc if token.dep_ == 'mark' or token.pos_ == 'SCONJ' or (token.dep_ == 'pcomp' and token.head in verb) or (token.dep_ == 'conj' and token.head.dep_ == 'ROOT' and 'poss' in [i.dep_ for i in token.children])]
    marks = []
    for token in doc:
        # print(verb, token.head)
        if token.dep_ == 'mark' or token.pos_ == 'SCONJ':
            marks.append(token.dep_)
        elif token.dep_ in ['pcomp'] and token.head in verb:
            marks.append(token.dep_)
        elif token.dep_ == 'conj' and token.head.dep_ == 'ROOT':
            for i in token.children:
                if i.dep_ == 'poss':
                    marks.append(token.dep_)
                    break
        elif token.dep_ == 'ccomp':
            marks.append(token.dep_)

    cconj = []
    FANBOYS = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so']
    for token in (doc): 
        if token.dep_ == 'conj' and token.head.dep_ == 'ROOT' : #and 'poss' not in [i.dep_ for i in token.children]
            cconj.append(token)
        elif token.dep_ == 'conj' and (token.pos_ == token.head.pos_):
            if is_contained_in(FANBOYS, [word for word in token.head.children]):
                cconj.append(token)
        # print(token, token.pos_, token.head.dep_)

    # print(marks, cconj)
    if marks != [] and cconj != []:
        result = 'compound_complex_sentence'
    elif marks != [] or 'pcomp' in marks and cconj == []:
        result = 'complex_sentence'
    elif marks == [] and cconj != [] :## มาต่อตรงนี้นะ ไม่ไหวละ poss กับ cc ตัวก่อนหน้า
        # print('poss' , [doc[index].dep_ for index in cconj])
        result = 'compound_sentence'
    elif marks == [] and cconj == []:
        result = 'simple_sentence' #

    html_content = displacy.render(doc, style="dep", options={'distance': 120}, page=True)
    with open('dependency_visualization.html', "w", encoding="utf-8") as file:
        file.write(html_content)

    return result, cleaned_sentence
    # return marks, cconj

def simple_sentence_extracting(sentence): #วิธีนี้ต้อง clean จุดออก
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    subject, predicate, object = '', '', ''
    for i, token in enumerate(doc):
        if token.dep_ == 'nsubj' or token.dep_ == 'nsubjpass':
            subject = [str(word.text) for word in doc[i].subtree]
        elif token.dep_ == 'ROOT':
            
            predicate = token.text
        elif token.dep_ in ['pobj', 'dobj'] and [word.text for word in token.ancestors] == [predicate]:
            object = [str(word.text) for word in doc[i].subtree]

        elif [word.text for word in token.ancestors] == [predicate] and token.dep_ not in ['pcomp', 'npadvmod']: #npadvmod ไว้ขยายคำนาม advmod ไว้ขยาย verb
            if object != '':
                object += [str(word.text) for word in doc[i].subtree]
            else:
                object = [str(word.text) for word in doc[i].subtree]
        
        object_phrase = ' '.join(list(object))
        subject_phrase = ' '.join(subject)

    # print(f'{subject_phrase =}, {predicate =}, {object_phrase =}')

    return [subject_phrase, predicate, object_phrase]

def compound_sentence_extracting(sentence): #ประเด็นคือประโยคที่ต่อ conj ด้วย verb ยังต้องการ subject ดังนั้นใส่ให้มันด้วย
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    compound_sentence = sentence
    spo_extract = []
    # print(compound_sentence)
    cconj = [cconj.text for cconj in doc if cconj.dep_ == 'cc']
    conj_pattern = '|'.join(cconj)
    # cc = "or"
    # Split the compound sentence into clauses using the conj_pattern
    clauses = []
    if len(cconj) > 1:
        # print(cconj)
        # clauses = re.split(f'\\s*({conj_pattern})\\s*', compound_sentence)
        clauses = sep_sentence(compound_sentence, cconj)
    else:
        for cc in cconj:
            clauses += (re.split(rf'\s*\b{str(cc)}\b\s*', compound_sentence))
            # print(clauses, cc)
    # clauses = re.split(f'\\s*({conj_pattern})\\s*', compound_sentence) ##เงื่อนไขคือถ้าประโยคทั้งสองมี SPO ของตัวเอง
    # clauses = re.split(rf'\\s*\\b({conj_pattern})\\b\\s*', compound_sentence)
    # clauses += (re.split(rf'\s*\b{str(cc)}\b\s*', compound_sentence))
    
    filtered_sentences = [sentence for sentence in clauses if sentence.lower() not in cconj]
    # print(filtered_sentences, cconj)
    share_sp = ['', '', '']
    for sent in filtered_sentences:

        if 'nsubj' in [token.dep_ for token in nlp(sent)] or 'nsubjpass' in [token.dep_ for token in nlp(sent)]:
            # print(spo_extract)
            spo_extract.append(simple_sentence_extracting(sent))
            share_sp[0], share_sp[1] = spo_extract[-1][0], spo_extract[-1][1]
        elif 'nsubj' not in [token.dep_ for token in nlp(sent)] and 'nsubjpass' not in [token.dep_ for token in nlp(sent)]:
            share_sp[2] = sent
            spo_extract.append(simple_sentence_extracting(' '.join(share_sp)))
            # share_sp = ['', '']

    #กรณีที่เป็น cconj ของตัวอื่นที่ไม่ใช่ root เรา Recursive แม่ม
    return spo_extract