from django import forms
from rango.models import Page,Category
from django.forms.extras.widgets import SelectDateWidget

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    # that's because of adding the category don't need to fill the views and likes
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    # because of the slug will add while the category add. You can see the model in Category's save.
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and url.startwith('http://'):
            url = 'http://' +url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)
    