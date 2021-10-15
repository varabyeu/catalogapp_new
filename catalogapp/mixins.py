from django.views.generic import View

from .models import Category, Selection, UserClass


class SelectionMixin(View):
    """
    Class is used to repeat pasting 'user' and 'selection'
    for Selection
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Function gets model checks is user authenticated and if not create new user.
        So it does with not authenticated user. Then returns a result of typical dispatch()
        """
        if request.user.is_authenticated:
            user = UserClass.objects.filter(user=request.user).first()
            if not user:
                user = UserClass.objects.create(
                    user=request.user
                )
            selection = Selection.objects.filter(owner=user, in_order=False).first()
            if not selection:
                selection = Selection.objects.create(owner=user)
        else:
            selection = Selection.objects.filter(is_anonymous=True).first()
            if not selection:
                selection = Selection.objects.create(is_anonymous=True)
        self.selection = selection
        return super().dispatch(request, *args, **kwargs)
