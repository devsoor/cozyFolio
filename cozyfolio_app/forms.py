from django import forms

class LanguagesForm(forms.Form):
    OPTIONS = [
        ("Python", "Python"),
        ("JavaScript", "JavaScript"),
        ("HTML/CSS", "HTML/CSS"),
        ("Java", "Java"),
        ("C/C++", "C/C++"),
        ("C#", "C#"),
        ("Swift", "Swift"),
        ("GO", "Go"),
        ("Ruby", "Ruby"),
        ("SQL", "SQL"),
        ("R", "R"),
    ]

    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

