from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Categories


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HOME Furniture Store"
        context['content'] = "Магазин мебели HOME"
        return context

# def index(request):

#     context = {
#         "title": "HOME Furniture Store"
#     }
#     return render(request, "main/index.html", context)



class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "О нас"
        return context


# def about(request):

#     return render(request, "main/about.html")