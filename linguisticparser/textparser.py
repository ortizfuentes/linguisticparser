import re
import pandas as pd
import os

class TextParser:
  def __init__(self,text,text_name="no_name"):
    self.text = text
    self.text_name = text_name
    self.__clean_status = False

  def set_name(self,text_name):
    self.text_name = text_name

  def __erase_multiple_spaces(mytext):
    pattern = '( )( )+'
    new_text = re.sub(pattern, ' ', mytext)
    return new_text

  def __erase_tabs(mytext):
    pattern = '\t'
    new_text = re.sub(pattern, ' ', mytext)
    return new_text

  def __erase_multiple_linebreaks(mytext):
    pattern = '\n\n+'
    new_text = re.sub(pattern, '\n', mytext)
    return new_text

  def __point_in_linebreak(mytext): 
    pattern = "(?<=[a-zA-ZñÑáéíóúÁÉÍÓÚü1-9])( )*\n"
    new_text = re.sub(pattern, '.\n', mytext)
    return new_text

  def __erase_incorrect_linebreaks(mytext):
    pattern = "\b[^.]\n\b"
    new_text = re.sub(pattern, ' ', mytext)
    return new_text

  def __erase_bullets(mytext): #bullet or interpunct
    #pattern = '\u2022'
    pattern = "(\\ufeff|\\u2022|\u00B7|\u0387|\u05BC|\u16EB|\u2027|\u2218|\u2219|\u22C5|\u25CF|\u25E6|\u2981|\u2E30|\u2E31|\ufeff)"
    new_text = re.sub(pattern, '', mytext)
    return new_text

  def __erase_double_hyphen(mytext):
    pattern = '--'
    new_text = re.sub(pattern, '-', mytext)
    return new_text  

  def clean_text(mytext):
    '''
    This function receives a text and removes repetitions of spaces and some signs.
    '''
    new_text = mytext
    new_text = TextParser.__erase_bullets(new_text)
    new_text = TextParser.__erase_tabs(new_text)
    new_text = TextParser.__erase_multiple_spaces(new_text)
    new_text = TextParser.__erase_multiple_linebreaks(new_text)
    new_text = TextParser.__point_in_linebreak(new_text)
    new_text = TextParser.__erase_incorrect_linebreaks(new_text)
    new_text = TextParser.__erase_double_hyphen(new_text)
    return new_text


  def paragraphs_tokenize(mytext):
    '''
    This function receives as argument a text with several paragraphs in str 
    format and returns a list with sentences separated by line break, even when
    it ends in any punctuation. 
    '''

    mylist = mytext.split("\n")
    if len(mylist) > 1:
      for i in range(len(mylist)):
        mylist[i] = mylist[i].strip()
        ## Here dots should be deleted after exclamation points and punctuation
      if mylist[-1] == '':
        mylist.pop(-1)
      return mylist
    else:
      return [mytext]


  def find_abbreviations(mytext, debug=False):
    '''
    This function searches for abbreviations and acronyms. Return a list with this information
    '''
    
    pattern8 = r"\b(([A-ZÁÉÍÓÚ]{1,2}|[A-ZÁÉÍÓÚ][a-záéíóú]{0,2})\.(\s?)){1,2}[A-ZÁÉÍÓÚ]{2}\." #siglas de dos letras punto dos letras mayus punto
    pattern3 = r"\b(([A-ZÁÉÍÓÚ]{1,2}|[A-ZÁÉÍÓÚ][a-záéíóú]{0,2})\.(\s?)){1,2}(([A-ZÁÉÍÓÚ]{1,2}|[A-ZÁÉÍÓÚ][a-záéíóú]{0,2})\.?(\s?)){1}(?=\s[a-záéíóú])"
    pattern2 = r"\b[A-ZÁÉÍÓÚ]?[a-záéíóú]+\.(?=\s[a-záéíóú])" #Para buscar abreviaturas terminadas en punto cuyo contexto a la derecha es minuscula
    pattern1 = r"\b(([A-ZÁÉÍÓÚ]|[a-záéíóú])\.\s?){1,4}(?=\s[a-záéíóú])" #Letras minusculas o mayusculas por si solas acompañadas de punto y seguidas de minúsculas
    pattern5 = r"\b([0-9]\.)+([0-9])?" #Numeros seguidos de puntos 
    pattern4 = r"\$?[0-9]+[\.\,]([0-9]+[\.\,])*[0-9]+\b" #Números con puntos entremedios teniendo un $ o no
    pattern6 = r"((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*" #páginas web
    pattern7 = r"\b([a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b" #correo electronico
    pattern = "(" + pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4 + "|" + pattern5 + "|" + pattern6 + "|" + pattern7 + "|" + pattern8 + ")"
    list_abreviations = [a[0] for a in re.findall(pattern, mytext)]
    if debug == True:
      print("Lista de abreviaciones:")
      print(list_abreviations)
    new_text = mytext
    count = 0
    dict_regex = {}
    for a in list_abreviations:
      count += 1
      regex_name = '*REGEX'+str(count)+'*'
#      new_text = re.sub(a, regex_name, new_text)
      new_text = new_text.replace(a, regex_name)
      if debug == True:
        print("Regex ID: "+regex_name) #regex01 o asi
        print("Elemento encontrado: "+a) #original
        print("Texto con sustitución: "+ new_text) #texto
      dict_regex[regex_name] = a
    dict_regex['txt'] = new_text
    return dict_regex

  def sentence_tokenize(paragraph):
    '''
    This function receives a paragraph and segments it into orthographic
    sentences. It does not erroneously separate acronyms and abbreviations
    '''

    txt_coded = paragraph
    #Busca tres puntos que siguen de una mayuscula y una minuscula y los sustituye por un string de letras
    three_points_pattern1 = r'((\.\.\.)(?=\s[A-ZÁÉÍÓÚ]))'
    three_points_pattern2 = r'((\.\.\.)(?=\s[a-záéíóú]))'
    question_before_capital = r'(\?)(?=\s[A-ZÀÈÌÒÙ])'
    exclamation_before_capital = r'(\!)(?=\s[A-ZÀÈÌÒÙ])'

    txt_coded = re.sub(three_points_pattern1, '*P2ANDP3.', txt_coded)
    txt_coded = re.sub(three_points_pattern2, '*p2andp3', txt_coded)
    txt_coded = re.sub(question_before_capital, '?.', txt_coded)
    txt_coded = re.sub(exclamation_before_capital, '!.', txt_coded)
    

    #Busca las abreviaturas y las sustituye por un string de letras
    abb = TextParser.find_abbreviations(txt_coded)
    txt_coded = abb['txt']
    sentences_list = txt_coded.split(".")
    if sentences_list[-1] == "" or sentences_list[-1] == "." or sentences_list[-1] == " ":
      sentences_list = sentences_list[:-1]

    #Repara la puntuación y las abreviaturas

    for i in range(len(sentences_list)):
      #Elimina algunas oraciones que empiezan con " "
      try:
        if sentences_list[i][0] == " ": 
            sentences_list[i] = sentences_list[i][1:]
      except:
          sentences_list[i] = sentences_list[i].strip()

      #Agrega el punto final a las oraciones
      sentences_list[i] = sentences_list[i] + "."

      #Restituye las abreviaturas
      abreviations_in_s = [a for a in re.findall(r'\*REGEX\d+\*', sentences_list[i])]
      if abreviations_in_s is not []:
        for ab in abreviations_in_s:
          sentences_list[i] = sentences_list[i].replace(ab, abb[ab])

      sentences_list[i] = sentences_list[i].replace("..", ".")


      #Restituye los puntos suspensivos
      sentences_list[i] = sentences_list[i].replace("*P2ANDP3", "..")
      sentences_list[i] = sentences_list[i].replace("*p2andp3", "...")
      
      #Elimina el punto después de signo de interrogaciòn
      sentences_list[i] = sentences_list[i].replace("?.", "?")
      sentences_list[i] = sentences_list[i].replace(":.", ":")
      sentences_list[i] = sentences_list[i].replace("!.", "!")

      #Elimina caracteres raros
      sentences_list[i] = sentences_list[i].replace(r"\ufeff", "")

    return sentences_list

  def word_tokenize(sentence):
    '''
    This function receives a sentence and separates them by space 
    and punctuation. It correctly separates abbreviations and acronyms.
    '''

    abb = TextParser.find_abbreviations(sentence)
    new_sentence = abb['txt']
    word_list = new_sentence.split()
    for i in range(len(word_list)):    
      regex = re.match(r'\*REGEX\d+\*', word_list[i])
      try:
        word_list[i] = abb[regex.group()]
      except:
        pass
    return word_list
  #word_tokenize("Hay tres perros, gatos... y comen rico")


  def word_and_punct_tokenize(sentence):
    '''
    This function separates words by punctuation
    '''
    new_sentence = sentence
    punctuation = ['...', ',', ';', ':', '-', '(', ')', '[', ']', '?', '¿', '¡', '!']
    for p in punctuation:
      new_sentence = new_sentence.replace(p, " "+p+" ")
    return word_tokenize(new_sentence)
      


  
  def growing_wordings_tokenize(sentence):
    '''
    This function receives a sentence in text format (str), breaks it down by 
    spaces and returns a list with word strings ordered from fewer to more 
    words. 
    '''
    words_list = TextParser.word_tokenize(sentence) 
    combinations = []
    words_joined = ""
    for word in words_list:
      words_joined = words_joined +" " + word
      combinations.append(words_joined[1:])    
    return combinations

  def double_growing_wordings_tokenize(sentence):
    '''
    This function receives a sentence in text format (str), breaks it down by 
    spaces and returns a list with word strings ordered from fewer to more words
    and then removing words from the left.
    '''

    words_list = sentence.split()
    combinations = []
    large = len(words_list)
    for i in range(large):
      words_joined = ""
      for word in words_list:
        words_joined = words_joined +" " + word
        combinations.append(words_joined[1:])
      words_list = words_list[1:]
    return combinations

  def c_clean_text(self):
    self.text = TextParser.clean_text(self.text)
    self.__clean_status = True
    return self.text

  def text2df_tokenize(self, splitby='sentence_tokenize'):
    ''' 
    Receives a text in str format and returns a tokenized dataframe as 
    indicated in 'splitby' 
    
    Splitby possibilities 
    'sentence_tokenize'
    'growing_wordings_tokenize'
    'double_growing_wordings_tokenize'
    'clauses' --> 'pending'
    '''

    if self.__clean_status == False:
      self.c_clean_text()


    paragraphs = TextParser.paragraphs_tokenize(self.text)
    information =[]
    num_paragraph = 0
    for paragraph in paragraphs:
      num_paragraph += 1
      sentences = TextParser.sentence_tokenize(paragraph)
      num_sentence= 0
      for sentence in sentences:
        if splitby == 'growing_wordings_tokenize':
          num_sentence += 1
          wordings = TextParser.growing_wordings_tokenize(sentence)
          num_subsentence = 0
          for wording in wordings:
            num_subsentence += 1
            information.append([self.text_name, num_paragraph, num_sentence, num_subsentence, wording])
        elif splitby == 'double_growing_wordings_tokenize':
          num_sentence += 1
          wordings = TextParser.double_growing_wordings_tokenize(sentence)
          num_subsentence = 0
          for wording in wordings:
            num_subsentence += 1
            information.append([self.text_name, num_paragraph, num_sentence, num_subsentence, wording])
        elif splitby == 'sentence_tokenize':
          num_sentence += 1
          wording = sentence
          num_subsentence = 1
          information.append([self.text_name, num_paragraph, num_sentence, num_subsentence, wording])

    df = pd.DataFrame(information,columns=["text_name", "num_paragraph", "num_sentence", "num_subsentence", "wordings"])
    return df

  def folder2df_tokenize(folder_input, folder_output, splitby='sentence_tokenize'):
    '''
    Processes all the texts in a folder and applies the text2df function
    '''
    n_files = os.listdir(folder_input)
    try:
      os.stat(folder_output)
    except:
      os.mkdir(folder_output)
    for n_file in n_files:
      if n_file[-4:] == ".txt":
        file = open(folder+n_file,'r', encoding='UTF-8', errors='ignore')
        mytext = file.read()
        file.close()
        tlp = TextParser(mytext, text_name=n_file[:-4])
        txtdf = tlp.text2df_tokenize(splitby=splitby)
        txtdf.to_excel(folder_output + n_file[:-4]+ ".xlsx", sheet_name='text', index=False) 
    print("¡Listo!")

