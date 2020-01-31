from django import forms
from .models import User

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None):
        super(CustomCheckboxSelectMultiple, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        output = super(CustomCheckboxSelectMultiple, self).render(name, value, attrs, choices)

        style = self.attrs.get('style', None)
        if style:
            output = output.replace("<ul", format_html('<ul style="{0}"', style))

        return mark_safe(output)

class LanguagesForm(forms.Form):
    OPTIONS = [
        ("Python", "Python"),
        ("JavaScript", "JavaScript"),
        ("HTML/CSS", "HTML/CSS"),
        ("Java", "Java"),
        ("C/C++", "C/C++"),
        ("C#", "C#"),
        ("Swift", "Swift"),
        ("Node.js", "Node.js"),
        ("GO", "Go"),
        ("Ruby", "Ruby"),
        ("SQL", "SQL"),
        ("R", "R"),
        ("PHP", "PHP"),
        ("Perl", "Perl"),
        ("Kotlin", "Kotlin"),
        ("Rust", "Rust"),
        ("Scheme", "Scheme"),
        ("Erlang", "Erlang"),
        ("Scala", "Scala"),
        ("Elixir", "Elixir"),
        ("Haskell", "Haskell"),
    ]

    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

class FrameworksForm(forms.Form):
    OPTIONS = [
        ("Ruby on Rails", "Ruby on Rails"),
        ("Django", "Django"),
        ("Laravel", "Laravel"),
        ("Symfony", "Symfony"),
        ("Meteor.js", "Meteor.js"),
        ("Angular", "Angular"),
        ("Yii", "Yii"),
        ("Play", "Play"),
        ("React", "React"),
        ("Express.js", "Express.js"),
        ("Nest.js", "Nest.js"),
        ("Flask", "Flask"),
        ("Phoenix", "Phoenix"),
        ("Spring", "Spring"),
        ("CakePHP", "CakePHP"),
        ("Vue", "Vue"),
        ("TensorFlow", "TensorFlow"),
        ("PyTorch", "PyTorch"),
        ("Scikit-Learn", "Scikit-Learn"),
        ("Pandas", "Pandas"),
        ("Sonnet", "Sonnet"),
        ("Keras", "Keras"),
        ("MXNet", "MXNet"),
        ("Gluon", "Gluon"),
        ("Chainer", "Chainer"),
        ("DL4J", "DL4J"),
        ("ONNX", "ONNX"),
    ]

    # frameworks = forms.MultipleChoiceField(widget=CustomCheckboxSelectMultiple(attrs={'style': 'list-style: none; margin: 0;'}), choices=OPTIONS)
    frameworks = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

class DatabasesForm(forms.Form):
    OPTIONS = [
        ("MySQL", "MySQL"),
        ("Microsoft SQL Server", "Microsoft SQL Server"),
        ("PostgreSQL", "PostgreSQL"),
        ("IBM Db2 Family", "IBM Db2 Family"),
        ("Microsoft Access", "Microsoft Access"),
        ("MariaDB", "MariaDB"),
        ("SQLite", "SQLite"),
        ("IBM Informix", "IBM Informix"),
        ("MongoDB", "MongoDB"),
        ("noSQL", "noSQL"),
        ("Redis", "Redis"),
        ("Cassandra", "Cassandra"),
        ("Amazon DynamoDB", "Amazon DynamoDB"),
        ("Oracle NoSQL Database", "Oracle NoSQL Database"),
        ("Amazon Aurora", "Amazon Aurora"),
    ]

    databases = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

class CloudsForm(forms.Form):
    OPTIONS = [
        ("Amazon AWS", "Amazon AWS"),
        ("Microsoft Azure", "Microsoft Azure"),
        ("Google Cloud Platform", "Google Cloud Platform"),
        ("Heroku", "Heroku"),
        ("Alibaba", "Alibaba"),
        ("Firebase", "Firebase"),
        ("SAP", "SAP"),
    ]

    clouds = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

class PDFForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['resume', 'headshot'] 