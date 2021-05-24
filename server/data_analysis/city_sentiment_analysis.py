"""
Analysis the sentiment scores within every different city.
1. Create the view;
2. Get the data from MapReduce view based on different city view.
3. Analysis the text of every tweet within cities.
4. return the JSON to Flask as API.
"""
import re
from utils import dbOperations
import os

#----------------------------------------------------------------#
#    Functions Definitions
#----------------------------------------------------------------#
def get_score_mapping(filePath= "AFINN.txt"):
    """
    Parser the AFINN.txt file, extracting the word and socres.
    return:
           @dict: {short:, longer:} 
           eg. long: no fun : 
    """
    scores = {"long":{}, "short":{}}
    with open(filePath, "r") as txt_f:
        for idx, line in enumerate(txt_f):
            line_l = line.split()
            if len(line_l) == 2: scores["short"][line_l[0]] = int(line_l[1])
            else:
                scores["long"][" ".join(line_l[:-1])] = int(line_l[-1])
    #log_info("total length of afinn.txt: {}".format(idx))
    return scores

#----------------------------------------------------------------#
#    Global Variable Generating
#----------------------------------------------------------------#
AFINN = {}
AFINN = get_score_mapping()
## connect the CouchDB
db_name = "au_tweets"
db_ip = os.getenv("COUCH_DB_IP", "null")
if db_ip == "null":
    db_ip = "172.26.129.170"
server = dbOperations(db_ip, db_port=5984, db_username="ccc58", db_passwd="ccc58", databases=[db_name])

def calculate_sentiment_scores(text, AFINN):
    """
    Eg, "good -> match
        good!!.. -> match
        good!@.. -> not match
        no fun -> match
    """
    scores = 0
    head_symbols = ("'", '"')
    tail_symbols = ("!","?",",",".","'",'"') ## these consider as exact match, when it appears with word.
    context = text.lower()
    context = context.replace("\n", "")
    # match the symbols not in tail_symbols list, remove these word.
    ## At first, match the long word, then remove them from the text.
    for long_word in AFINN["long"].keys():
        if long_word in context:
            scores += AFINN["long"][long_word]
            context.replace(long_word, "")
    ## then, catch the single word from head with " ', or tail with ("!","?",",",".","'",'"')
    for word in context.split():
        # if word.isalpha():
        # if word in AFINN["short"].keys(): scores += AFINN["short"][word]
        if bool(re.search(r'\d', word)): continue # if string contains digital, continue.
        elif word.startswith(head_symbols): # "hello if remove ", the whole data become alpha, match.
            if bool(re.search(r"\W",word[1:])):
                if word.endswith(tail_symbols):
                    if len(set(re.findall(r"\W", word[1:])).difference(set(tail_symbols))) > 0: 
                        continue
                    else:
                        word = re.findall("^[a-z]*", word[1:])[0]
                else: continue
            else: 
                word = word[1:]
        elif word.endswith(tail_symbols):
            if len(set(re.findall(r"\W", word)).difference(set(tail_symbols))) > 0: 
                continue
            else:
                word = re.findall("^[a-z]*", word)[0]
        if word in AFINN["short"].keys(): 
            scores += AFINN["short"][word]
    return scores

def get_data_from_json(path):
    pass

def generate_map_function(city_name):
    mapFunction = '''function (doc) {
                        if(doc.place.name == "XXX")
                        emit(doc.id, [doc.place.name, doc.text, doc.lang]);
                    }'''.replace("XXX", city_name)
    return mapFunction

def get_data_from_db_views(db_name, city_name): # db_name, design_doc_name, view_name, map_function
    try:
        mapFunction = generate_map_function(city_name)
        server._create_view(db_name, design_doc_name= str(city_name)+"_DOC",
                            view_name= str(city_name)+"_info", map_function=mapFunction)
    except:
        print("[*] view has already exist!")
    view_str = city_name+"_DOC/"+city_name+"_info"
    return server._get_view_data(db_name, view_str)

def process_data(input):
    sentiment = 0
    for item in get_data_from_db_views(db_name=input[0], city_name=input[1]):
        if len(item.value[1]) == 0:
            continue
        sentiment += calculate_sentiment_scores(item.value[1], input[2])
    return (input[1], sentiment)

def _sentiment_result(db_name, AFINN=AFINN):
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth (WA)", "Adelaide"]
    inputs, r = [], {}
    for i in range(len(cities)):
        inputs.append([db_name, cities[i], AFINN])
    sentiments = {}
    result = map(process_data, inputs)
    for res in result:
        sentiments[res[0]] = res[1]
    return sentiments

if __name__ == "__main__":
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth (WA)", "Adelaide"]
    #get_data_from_db_views("sydney", cities[0])
    print(_sentiment_result("whole_au"))