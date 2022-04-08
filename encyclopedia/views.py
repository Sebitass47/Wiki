from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown as md
from random import choice
from . import util

class NewPage(forms.Form):
    title = forms.CharField(label = "Title")
    content =  forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All pages"
    })

def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry(title)),
            "title": title.capitalize()
        })

def search(request):
    if request.method == "POST":
        form = request.POST
        search = form["q"]
        search = search.lower().strip()
       
        if not search:
            return HttpResponseRedirect(reverse("index"))

        names = util.list_entries()
        for i in range(len(names)):
            names[i] = names[i].lower()

        if search in names:
            return render(request, "encyclopedia/entry.html", {
                "entry": md.markdown(util.get_entry(search)),
                "title": search.capitalize()
            })
        
        else:
            entries = []
            for name in names:
                if name.find(search) != -1:
                    entries.append(name.upper())
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "title": "Results"
            })  

def random(request):
    lista = util.list_entries()
    entry = choice(lista)
    #This is not the best way, because if I change the path, 
    # I should correct this, but I don't know any other way to solve it,
    #  and it works
    return HttpResponseRedirect("/wiki/" + entry)


def create(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            titles = util.list_entries()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in titles:
                error = "The name of the page already exists"
                return render(request, "encyclopedia/create.html",{
                    "form" : form,
                    "error": error
                })
            util.save_entry(title, content)
            return HttpResponseRedirect('/wiki/' + title)
        else:
            return render(request, "encyclopedia/create.html",{
        "form" : form,
    })
        
    return render(request, "encyclopedia/create.html",{
        "form" : NewPage(),
    })

def edit(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        form = request.POST
        content = form["content"]
        print(content)
        if not content:
            return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title": title,
        })

        util.save_entry(title, content)
        return HttpResponseRedirect('/wiki/' + title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title": title,
        })