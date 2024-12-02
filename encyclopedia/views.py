from django.shortcuts import render, redirect
import markdown
from . import util
import random
from django.http import HttpResponse

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdown.markdown(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' does not exist."
        }, status=404)
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry Page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title, 
                "content": html_content
            })

from django.shortcuts import render, redirect
from django.http import HttpResponse

def edit(request, title):
    if request.method == "POST":
        # Debugging: Log the request method and posted data
        print("Request method:", request.method)
        print("Posted data:", request.POST)

        # Extract the 'content' field from POST data
        content = request.POST.get('content', None)
        print("Content received:", content)  # Debugging: Log the content

        if content is None:
            # Handle the case where 'content' is missing
            print("Error: Content is missing!")  # Debugging: Log error
            return HttpResponse("Content field is missing!", status=400)

        # Save the changes (implement saving logic)
        # Example: Save the content for the page with the given title
        # save_content(title, content)  # Replace with your actual logic

        # Redirect the user back to the page after editing
        return redirect('wiki', title=title)  # Replace 'wiki' with your URL name

    # If GET request, render the edit page with the current content
    current_content = "Load current content here"  # Replace with your logic to fetch the content
    print("Rendering edit form for title:", title)  # Debugging: Log rendering action
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": current_content
    })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,  # Add a comma here
                "content": html_content
            })
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html",{
        "title": rand_entry,
        "content": html_content
    })