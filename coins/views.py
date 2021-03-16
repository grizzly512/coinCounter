from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import FileForm
from .file_processor import processFiles


class FileView(FormView):
    template_name = 'coins/file.html'
    form_class = FileForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        print(request.POST)
        print(files)
        if form.is_valid():
            parameters = processFiles(files)
            request.session['files'] = parameters
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("coins:main")
