from django.db import models

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Curso(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    # Corregido aquí: on_delete en lugar de on_models
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos', null=True, blank=True)
    estudiantes = models.ManyToManyField(Estudiante, related_name='cursos', blank=True)

    def __str__(self):
        return self.nombre
