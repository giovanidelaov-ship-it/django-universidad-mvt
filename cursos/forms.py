
from django import forms
from .models import Curso, Estudiante, Profesor


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'codigo', 'profesor', 'estudiantes']

        labels = {
            'nombre': 'Nombre del curso',
            'codigo': 'Código del curso',
            'profesor': 'Profesor encargado',
            'estudiantes': 'Estudiantes inscritos',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del curso'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del curso'
            }),
            'profesor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estudiantes': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip().upper()

        if len(codigo) < 4:
            raise forms.ValidationError(
                'El código debe tener al menos 4 caracteres.'
            )

        return codigo


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'email', 'matricula']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'especialidad']

        labels = {
            'nombre': 'Nombre del profesor',
            'especialidad': 'Especialidad',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especialidad del profesor'
            }),
        }
