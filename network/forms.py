from django import forms

class New_post(forms.Form):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Text - not more than 2000 characters",
            'style':"width:100%; height:137px"}
        ),
        max_length=2000,
        required=True,
        label =''
    )

