#import nltk
#from nltk.stem import WordNetLemmatizer
#from nltk.corpus import stopwords
#
#from tkinter import Tk, filedialog
#import heapq
#from PyPDF2 import PdfReader
#import re
#
#def extract_text_from_pdf(file_path):
#    with open(file_path, 'rb') as file:
#        pdf_reader = PdfReader(file)
#        text = ''
#        num_pages = len(pdf_reader.pages)
#        for page in range(num_pages):
#            text += pdf_reader.pages[page].extract_text()
#            # Supprimer les numéros et les caractères spéciaux du texte
#            text = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ\sOUSPEVDUJPO]', '', text)
#            #page = pdf_reader.pages[0]
#            #text += page.extract_text()
#    return text
#
#def summarize(text, num_sentences=3):
#    #tokeize le texte en phrases
#    sentences = nltk.sent_tokenize(text)
#
#    #calcule de la fréquence de chaque mot dans le texte
#    word_freq = {}
#    for sentence in sentences:
#        for word in nltk.word_tokenize(sentence):
#            if word not in word_freq:
#                word_freq[word] = 1
#            else:
#                word_freq[word] += 1
#
#    #attribution d'un score à chaque phrase en fonction de la fréquence des mots qu'elle contient
#    sentence_scores = {}
#    for sentence in sentences:
#        for word in nltk.word_tokenize(sentence):
#            if sentence not in sentence_scores:
#                sentence_scores[sentence] = word_freq[word]
#            else:
#                sentence_scores[sentence] += word_freq[word]
#
#    #on sélectionne les phrases avec les scores les plus élevés pour former le résumé
#    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
#    summary = ' '.join(summary_sentences)
#
#    return summary
##nltk.download('punkt')
##nltk.download('averaged_perceptron_tagger')
##nltk.download('maxent_ne_chunker')
##nltk.download('words')
##nltk.download('stopwords')
##nltk.download('wordnet')
#
#def entree():
#    root = Tk()
#    root.withdraw()
#    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
#    with open(file_path, 'r', encoding='latin-1') as file:
#        text = file.read()
#    if file_path.endswith('.pdf'):
#        text = extract_text_from_pdf(file_path)
#    elif file_path.endswith('.txt'):
#        with open(file_path, 'r', encoding='utf-8') as file:
#            text = file.read()
#    else:
#        print("le fichier n'est pas un fichier pdf ou texte")
#    return text
#
#def main():
#    phrase = entree()
#    token = nltk.word_tokenize(phrase)
#    stop_words = set(stopwords.words('french'))
#    filtered_tokens = [token for token in token if token.lower() not in stop_words]#suppretion des mots comme comme "et", "ou", "le", "la", etc.
#    #ici c'est bon normalement
#    lemmatizer = WordNetLemmatizer()
#    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]# réduire les mots à leur forme de base
#    pos_tags = nltk.pos_tag(lemmatized_tokens)
#    named_entities = nltk.ne_chunk(pos_tags)#attribuer une étiquette à chaque mot
#    #resume le texte en entrée
#    summary = summarize(phrase)
#    print(phrase)
#    print("\n le texte resumé est :\n")
#    #print("###################################################################################################################################")
#    print(summary)
#
#
#main()
# ancien programme lent

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from tkinter import Tk, filedialog
import heapq
from PyPDF2 import PdfReader
import re

# Extraction de texte à partir d'un fichier PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page in range(num_pages):
            text += pdf_reader.pages[page].extract_text()
        text = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ\s]', '', text)  # Supprimer les caractères spéciaux
    return text

# Fonction pour résumer le texte
def summarize(text, num_sentences=3):
    sentences = sent_tokenize(text)
    word_freq = {}
    
    # Calculer la fréquence des mots
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word not in stopwords.words('french'):
                word_freq[word] = word_freq.get(word, 0) + 1

    # Score des phrases
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]

    # Sélection des phrases les plus importantes
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return summary

# Fonction pour choisir un fichier
def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    return file_path

# Fonction principale
def main():
    file_path = choose_file()
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        print("Le fichier n'est pas un fichier PDF ou texte.")
        return

    summary = summarize(text)
    print("Texte original :\n", text)
    print("\nTexte résumé :\n", summary)

if __name__ == "__main__":
    # Télécharger les ressources nécessaires de nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    
    main()
