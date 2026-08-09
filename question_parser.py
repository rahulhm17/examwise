import re


# 🔹 STEP 1: CLEAN RAW OCR TEXT
def clean_text(text):
    # Fix common OCR mistakes
    text = text.replace("0R", "OR")
    text = text.replace("l0", "10")
    text = text.replace("1O", "10")

    # Remove unwanted symbols
    text = re.sub(r'[^a-zA-Z0-9.,()\-\n ]', ' ', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# 🔹 STEP 2: FIX WORD SPACING
def fix_word_spacing(text):
    # Add space between lowercase and uppercase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Add space between letters and numbers
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)

    # Common manual fixes (important for exam QP)
    fixes = {
        "thesign": "the design",
        "implementthe": "implement the",
        "designof": "design of",
        "fulladder": "full adder",
        "booleanfunction": "boolean function",
        "multiplexerusing": "multiplexer using",
        "kmap": "k map",
        "truth table": "truth table",
        "addercircuit": "adder circuit",
        "usingtwo": "using two",
    }

    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)

    return text


# 🔹 STEP 3: IMPROVE READABILITY
def improve_readability(text):
    # Add space after punctuation if missing
    text = re.sub(r'\.(?=[A-Za-z])', '. ', text)
    text = re.sub(r'\)(?=[A-Za-z])', ') ', text)

    return text


# 🔹 STEP 4: STRUCTURE QUESTIONS
def structure_questions(text):
    # Break before Q numbers
    text = re.sub(r'(Q\.?\s*\d+)', r'\n\n\1', text)

    # Break for sub-questions a), b)
    text = re.sub(r'(\b[a-zA-Z]\))', r'\n   \1', text)

    # Handle OR sections
    text = re.sub(r'\bOR\b', r'\n\n--- OR ---\n\n', text)

    return text


# 🔹 STEP 5: FINAL EXTRACTION
def extract_questions(text):
    text = clean_text(text)
    text = fix_word_spacing(text)
    text = improve_readability(text)
    text = structure_questions(text)

    lines = text.split("\n")

    final_questions = []
    buffer = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # New question starts
        if re.match(r'^Q\.?\s*\d+', line):
            if buffer:
                final_questions.append(buffer.strip())
            buffer = line
        else:
            buffer += " " + line

    if buffer:
        final_questions.append(buffer.strip())

    return final_questions


# 🔹 TEST MODE
if __name__ == "__main__":
    print("Paste OCR text:\n")
    sample = input()

    questions = extract_questions(sample)

    print("\n🔥 FINAL CLEAN OUTPUT:\n")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}\n")