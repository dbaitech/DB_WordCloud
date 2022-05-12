# Start with loading all necessary libraries
import sys
import re
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path

import matplotlib.pyplot as plt

# Function to validate URL using regular expression
def is_valid_url(str):
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty return false
    if (str == None):
        return False

    # Return if the string matched the ReGex
    if (re.search(p, str)):
        return True
    else:
        return False


def get_text_from_html(url):
    # opening the url for reading
    r = requests.get(url)
   
    # URL exists
    if (r.status_code == 200):
        html = r.text
    else:
        return ""

    # parsing the html file
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find_all(text=True)

    # Remove unwanted tag elements:
    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style', ]

    # Then we will loop over every item in the extract text and make sure that
    # the beautifulsoup4 tag is NOT in the blacklist
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)

    # Remove any tab separation and strip the text:
    cleaned_text = cleaned_text.replace('\t', ' ')

    return cleaned_text

def get_text_from_file(str):
    f = open(str, 'r')
    text = f.read()
    f.close()
    return text


if __name__ == "__main__":
    # sys.argv[0] is the name of the script
    # first argument is the URL of file name we want to process
    # test to have at least one argument
    if len(sys.argv) > 1:
        text_source = str(sys.argv[1])  # text file source: text file of html web page
    else:
        print("You must provide the text source: a text file or an HTML web page ")
        exit(0)

    if is_valid_url(text_source):
        text = get_text_from_html(text_source)
    elif path.exists(text_source):
        text = get_text_from_file(text_source)
    else:
        print("The text source provided doesn't exists.")
        print("    ({})".format(text_source))
        exit(0)

    if len(text) > 1:
        # Create and generate a word cloud image:
        wordcloud = WordCloud(max_words=50, background_color="white").generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    else:
        print("The content at the source provided is empty.")
        print("    ({})".format(text_source))
