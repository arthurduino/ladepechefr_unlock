import requests
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser
import os


root = tk.Tk()
label = tk.Label(root, text="Entrez l'adresse de l'article à débloquer :", padx=10, pady=10)
label.pack()

ent = tk.Entry(root)
ent.pack()

def unlock():
    URL = ent.get()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("div", class_="article-full__body")
    title = '<h1>' + soup.find('title').text.strip() + '</h1>'
    metaTitle = '<title>' + soup.find('title').text.strip() + '</title>'
    covimage = '<img src="'+soup.find("meta", property="og:image")["content"]+'">'
    
    for result in results:
        #suuppression d'élements superflus
        chapoSpan = result.find("p", class_="article-full__chapo").find(recursive=True).decompose()
        alireAussi = result.findAll("p", class_="std-elt__inline")
        for el in alireAussi:
            el.decompose()

        chapo = '<p><strong>' + result.find("p", class_="article-full__chapo").text.strip() + '</strong></p>'

        article = [metaTitle, title, covimage, chapo]

        paragraphs = result.findAll()
        
        for p in paragraphs:
            if p.has_attr('class')==False:
                if p.text.strip() != 'Cet article est réservé aux abonnés' and p.text.strip()!='':
                    article.append('<p>'+p.text.strip()+'</p>')
            else:
                if p['class'][0] == 'std-img__img':
                    article.append('<img src=\"'+ p.get('data-src') + '\">')
                if p.name == 'h2':
                    article.append('<h2>'+p.text.strip()+'</h2>')

        #création de la page html
        file_name = 'article.html'
        with open(file_name, 'w', encoding='utf-8') as my_file:
            for el in article:
                my_file.write(el)
            my_file.close()
        filename = 'file:///'+os.getcwd()+'/' + file_name
        webbrowser.open_new_tab(filename)


widget = tk.Button(root, text='Go !', command=unlock)
widget.pack()
root.mainloop()
