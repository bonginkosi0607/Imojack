from flask import Flask, render_template, redirect, request, url_for
from bs4 import BeautifulSoup
import requests
import random
import zlib
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # If user submits form
    if request.method == "POST":
        # genarate code
        form = request.form
        url = form['url']
        code = str(random.randint(1, 999) * random.randint(1, 9)) + str(zlib.compress(bytes(url.encode("UTF-8")),\
         level=9)).replace("\\", "").replace("'", "").replace("x", "")
        r = requests.get(url)
        soup = BeautifulSoup(r.text , "html.parser")
        images = []
        css = []
        for image in soup.find_all('img'):
            try:
                img = image.attrs['src'].split("?", 1)[0]
                if img.endswith('.png') or img.endswith('.jpg'):
                    images.insert(1, img)
            except Exception:
                continue
        for css in soup.find_all('style'):
            try:
                print("entered style ")
                try:
                    css = image.attrs['href'].split("?", 1)[0]
                except Exception:
                    css = "none"
                if css.endswith('.css'):
                    print("in style")
                    with open(css) as css_file:
                        if "url(" in css_file.read():
                            urls_in_css = re.findall(r"(url\\(.*\\))", css_file.read())
                            for image in urls_in_css:
                                img = image.attrs['src'].split("?", 1)[0]
                                if img.endswith('.png') or img.endswith('.jpg'):
                                    print("css grabder is working.")
                                    images.insert(1, img)
                else:
                       if "url(" in r.text:
                            print("in style 2")
                            urls_in_css = re.findall(r'("/.*")', r.text)
                            print(urls_in_css[0])
                            for image in urls_in_css:
                                img = image.attrs['src'].split("?", 1)[0]
                                if img.endswith('.png') or img.endswith('.jpg'):
                                    print("css grabder is working.")
                                    images.insert(1, img)
            except Exception:
                continue
        test = ""
        for img in images:
            print(img)
            img = "<img src='" + img + "'/><hr/>"
            test += img
        return test

    else:
        return render_template('home.html')

if __name__ == '__main__':    
    app.run(debug=False)
