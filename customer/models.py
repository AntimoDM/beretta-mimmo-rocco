from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel


class Customer(TimeStampedModel, models.Model):
    name = models.CharField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Cliente(TimeStampedModel, models.Model):
    nome_cognome_import = models.CharField(max_length=150)
    anagrafica_import = models.CharField(max_length=300)
    telefono_principale = models.CharField(max_length=20, null=True, unique=True)

    # da qui in poi i campi potrebbero essere deprecati
    nome = models.CharField(max_length=50, null=True)
    cognome = models.CharField(max_length=50, null=True)
    strada = models.CharField(max_length=100, null=True)
    numero_civico = models.CharField(max_length=50, null=True)
    provincia = models.CharField(max_length=50, null=True)
    comune = models.CharField(max_length=50, null=True)
    codicefiscale = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.nome_cognome_import


class TecnicoCaldaia(models.Model):
    nome = models.CharField(max_length=50, null=True)


class Intervento(TimeStampedModel, models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=False)
    tecnico = models.ForeignKey(TecnicoCaldaia, on_delete=models.CASCADE, blank=True, null=True)

    data_chiamata = models.DateField(null=False)
    data_completamento = models.DateField(null=True)
    data_assegnamento = models.DateField(null=True)
    motivazione = models.CharField(max_length=100, null=False)
    note_per_tecnico = models.CharField(max_length=200, null=False)
    note_del_tecnico = models.CharField(max_length=200, null=False)
    SELEZIONE_STATI = (
        (1, "Nuovo"),
        (2, "Assegnato"),
        (3, "Completato"),
        (4, "Bloccato"),
    )
    stato = models.CharField(max_length=10, choices=SELEZIONE_STATI, default=1)


class NumeroDiTelefonoAggiuntivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=False)

    numero = models.CharField(max_length=20, null=True)
