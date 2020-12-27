from django import forms
from .models import DocumentPost, Comment


class DocumentPostForm(forms.ModelForm):

    class Meta:
        model = DocumentPost
        fields = ('title', 'description', 'document',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
