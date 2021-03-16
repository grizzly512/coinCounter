from django.views.generic import TemplateView
from .file_processor import processFiles
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def ajax(request, *args, **kwargs):
    if request.is_ajax:
        files = request.FILES.getlist('file')
        parameters = processFiles(files)
        return JsonResponse({"parameters": parameters}, status=200)


class FileView(TemplateView):
    template_name = 'coins/file.html'
