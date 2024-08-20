from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.files.storage import FileSystemStorage


def process_get_view(request: HttpRequest) -> HttpResponse:

    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,

    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:

    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    limit = 2 * 1024 * 1024
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()

        if myfile.size > limit:
            print("file upload error (size)")
            return render(request, "requestdataapp/file-upload-errors.html")

        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)
        return render(request, "requestdataapp/file-upload.html")

