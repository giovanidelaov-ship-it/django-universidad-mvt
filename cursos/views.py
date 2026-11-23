
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Curso, Profesor, Estudiante
from .forms import CursoForm, EstudianteForm, ProfesorForm


# 1. LISTAR CURSOS CON BUSCADOR (PÚBLICA)
class CursoListView(ListView):
    model = Curso
    template_name = 'cursos/lista.html'
    context_object_name = 'cursos'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(codigo__icontains=query) |
                Q(profesor__nombre__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cursos'] = self.object_list.count()
        context['query'] = self.request.GET.get('q', '')
        return context


# 2. DETALLE DE CURSO (PÚBLICA)
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'cursos/detalle.html'
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = self.object.estudiantes.all()
        return context


# 3. DETALLE DE PROFESOR (PÚBLICA)
class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'cursos/profesor_detalle.html'
    context_object_name = 'profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = self.object.cursos.all()
        return context


# 4. CREAR CURSO (PROTEGIDA)
class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue creado exitosamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Curso (Protegido)'
        return context


# 5. EDITAR CURSO (PROTEGIDA)
class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue actualizado correctamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Curso: {self.object.nombre}'
        return context


# 6. ELIMINAR CURSO (PROTEGIDA)
class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    success_url = reverse_lazy('web_lista_cursos')
    context_object_name = 'curso'

    def delete(self, request, *args, **kwargs):
        curso = self.get_object()
        messages.warning(
            self.request,
            f"El curso '{curso.nombre}' fue eliminado del sistema."
        )
        return super().delete(request, *args, **kwargs)


# 7. LISTAR PROFESORES (PÚBLICA Y PAGINADA)
class ProfesorListView(ListView):
    model = Profesor
    template_name = 'cursos/profesores_lista.html'
    context_object_name = 'profesores'
    paginate_by = 3


# 8. CREAR PROFESOR (PROTEGIDA)
class ProfesorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'cursos/profesor_formulario.html'
    success_url = reverse_lazy('web_lista_profesores')
    success_message = "¡El profesor '%(nombre)s' fue registrado correctamente!"


# 9. EDITAR PROFESOR (PROTEGIDA)
class ProfesorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'cursos/profesor_formulario.html'
    success_url = reverse_lazy('web_lista_profesores')
    success_message = "¡El profesor '%(nombre)s' fue actualizado correctamente!"


# 10. ELIMINAR PROFESOR (PROTEGIDA)
class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    template_name = 'cursos/profesor_confirm_delete.html'
    success_url = reverse_lazy('web_lista_profesores')
    context_object_name = 'profesor'

    def delete(self, request, *args, **kwargs):
        profesor = self.get_object()
        messages.warning(
            self.request,
            f"El profesor '{profesor.nombre}' fue eliminado."
        )
        return super().delete(request, *args, **kwargs)


# 11. LISTAR ESTUDIANTES CON BUSCADOR (PÚBLICA Y PAGINADA)
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'cursos/estudiantes_lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(matricula__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


# 12. DETALLE DE ESTUDIANTE
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'cursos/estudiante_detalle.html'
    context_object_name = 'estudiante'


# 13. CREAR ESTUDIANTE (PROTEGIDA)
class EstudianteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡El estudiante '%(nombre)s %(apellido)s' fue registrado con éxito!"


# 14. EDITAR ESTUDIANTE (PROTEGIDA)
class EstudianteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡Los datos del estudiante '%(nombre)s' fueron actualizados correctamente!"


# 15. ELIMINAR ESTUDIANTE (PROTEGIDA)
class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'cursos/estudiante_confirm_delete.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    context_object_name = 'estudiante'

    def delete(self, request, *args, **kwargs):
        estudiante = self.get_object()
        messages.warning(
            self.request,
            f"El estudiante '{estudiante.nombre} {estudiante.apellido}' fue eliminado."
        )
        return super().delete(request, *args, **kwargs)
