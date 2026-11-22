from django import forms

from .models import Loan


class LoanForm(forms.ModelForm):
    member = forms.CharField(strip=False)
    isbn = forms.CharField(strip=False)

    class Meta:
        model = Loan
        fields = ('member', 'isbn')

    def clean_member(self):
        member = self.cleaned_data['member']
        if not member.strip():
            raise forms.ValidationError('This field is required.')
        return member

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        if not isbn.strip():
            raise forms.ValidationError('This field is required.')
        return isbn
