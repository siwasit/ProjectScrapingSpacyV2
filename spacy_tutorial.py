import re

# compound_sentence = 'The cat sat on the mat, but it soon got bored and wandered off.'
# cconj = ['but', 'and']

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

# clauses = sep_sentence(compound_sentence, cconj)
# print(clauses)