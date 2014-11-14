from django.views.generic import View

from braces.views import JSONResponseMixin

from .compare import find_comparable


class FindComparableView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        context = find_comparable(
            acres=request.GET.get('acres', None),
            sqft=request.GET.get('sqft', None),
        )
        return self.render_json_response(context)
