from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.core.validators import RegexValidator

class Equipos(models.Model):
    OPCIONES_SN = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]
    
    idEqu = models.AutoField(primary_key=True, verbose_name='ID:')
    nomEqu = models.CharField(max_length=25, verbose_name='Nom. del equipo:')
    oliEqu = models.CharField(max_length=1, choices=OPCIONES_SN, verbose_name='¿Es olímpico?')
    
    class Meta:
        db_table = 'EQUIPOS'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        constraints = [
            models.CheckConstraint(
                check=models.Q(oliEqu__in=['S', 'N']),
                name='check_oliEqu'
            )
        ]
    
    def __str__(self):
        return self.nomEqu
    
    def puede_eliminarse(self):
        return not self.encuentroequipo_set.exists()
    
    def delete(self, *args, **kwargs):
        if not self.puede_eliminarse():
            raise ValidationError(
                f"No se puede eliminar el equipo '{self.nomEqu}'. Está participando en algún encuentro."
            )
        super().delete(*args, **kwargs)
    
class Disciplinas(models.Model):
    idDis = models.AutoField(primary_key=True, verbose_name='ID:')
    nomDis = models.CharField(max_length=50, verbose_name='Nom. de la disciplina:')
    min_equipos = models.PositiveIntegerField(default=1, verbose_name='Mín. de equipos por encuentro:')
    max_equipos = models.PositiveIntegerField(default=10, verbose_name='Máx. de equipos por encuentro:')
    min_participantes_por_equipo = models.PositiveIntegerField(default=1, verbose_name='Mín. de participantes por equipo:')
    max_participantes_por_equipo = models.PositiveIntegerField(default=10, verbose_name='Máx. de participantes por equipo:')
    duracion_estimada = models.DurationField(
        verbose_name='Duración estimada del encuentro:',
        default=timedelta(hours=1)
    )
    
    class Meta:
        db_table = 'DISCIPLINAS'
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
    
    def __str__(self):
        return self.nomDis
    
    def clean(self):
        super().clean()
        if self.min_equipos > self.max_equipos:
            raise ValidationError('El mínimo de equipos no puede ser mayor al máximo.')
        if self.min_participantes_por_equipo > self.max_participantes_por_equipo:
            raise ValidationError('El mínimo de participantes por equipo no puede ser mayor al máximo.')

class Pistas(models.Model):
    OPCIONES_SN = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]
    
    idPis = models.AutoField(primary_key=True, verbose_name='ID:')
    nomPis = models.CharField(max_length=25, verbose_name='Nom. de la pista:')
    cubPis = models.CharField(max_length=1, choices=OPCIONES_SN, verbose_name='¿Está cubierta?')
    
    class Meta:
        db_table = 'PISTAS'
        verbose_name = 'Pista'
        verbose_name_plural = 'Pistas'
        constraints = [
            models.CheckConstraint(
                check=models.Q(cubPis__in=['S', 'N']),
                name='check_cubPis'
            )
        ]
    
    def __str__(self):
        return self.nomPis
    
phone_validator = RegexValidator(
    regex=r'^\d+$',
    message="El teléfono de contacto sólo debe contener números."
)

class Arbitros(models.Model):
    idArb = models.AutoField(primary_key=True, verbose_name='ID:')
    nomArb = models.CharField(max_length=50, verbose_name='Nom. completo:')
    telArb = models.CharField(max_length=9, verbose_name='Teléfono de contacto:', validators=[phone_validator])
    conArb = models.EmailField(max_length=75, verbose_name='Correo de contacto:')
    
    class Meta:
        db_table = 'ARBITROS'
        verbose_name = 'Árbitro'
        verbose_name_plural = 'Árbitros'
    
    def __str__(self):
        return self.nomArb

class Participantes(models.Model):
    idPar = models.AutoField(primary_key=True, verbose_name='ID:')
    nomPar = models.CharField(max_length=75, verbose_name='Nom. completo:')
    fecPar = models.DateField(verbose_name='Fecha de nacimiento:')
    curPar = models.CharField(max_length=5, verbose_name='Curso:')
    telPar = models.CharField(max_length=9, verbose_name='Teléfono de contacto:', validators=[phone_validator])
    conPar = models.EmailField(max_length=75, verbose_name='Correo de contacto:')
    equipo = models.ForeignKey(
        Equipos, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Equipo asociado:',
        related_name='participantes'
    )

    class Meta:
        db_table = 'PARTICIPANTES'
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
    
    def __str__(self):
        return f"{self.nomPar} ({self.curPar})"
    
    def delete(self, *args, **kwargs):
        from django.db import transaction
        with transaction.atomic():
            equipo = self.equipo
            super().delete(*args, **kwargs)
            if equipo and equipo.participantes.count() == 0 and equipo.puede_eliminarse():
                equipo.delete()

class Encuentros(models.Model):
    ESTADOS_ENCUENTRO = [
        ('CONFIRMADO', 'Confirmado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('FINALIZADO', 'Finalizado'),
    ]
    
    idEnc = models.AutoField(primary_key=True, verbose_name='ID:')
    idDis = models.ForeignKey(Disciplinas, on_delete=models.CASCADE, verbose_name='Disciplina:')
    finiEnc = models.DateTimeField(verbose_name='Fecha de inicio:')
    ffinEnc = models.DateTimeField(verbose_name='Fecha de fin:', null=True, blank=True)
    idPis = models.ForeignKey(Pistas, on_delete=models.CASCADE, verbose_name='Pista:')
    arbitro = models.ForeignKey(Arbitros, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Árbitro asociado:')
    equipos = models.ManyToManyField(Equipos, through='EncuentroEquipo', verbose_name='Equipos participantes:')
    estado = models.CharField(
        max_length=15, 
        choices=ESTADOS_ENCUENTRO, 
        default='CONFIRMADO',
        verbose_name='Estado del encuentro:'
    )
    
    class Meta:
        db_table = 'ENCUENTROS'
        verbose_name = 'Encuentro'
        verbose_name_plural = 'Encuentros'
        constraints = [
            models.CheckConstraint(
                check=models.Q(ffinEnc__gt=models.F('finiEnc')) | models.Q(ffinEnc__isnull=True),
                name='check_fechas_encuentro'
            )
        ]
    
    def __str__(self):
        return f"Encuentro {self.idEnc} - {self.idDis} ({self.estado})"
    
    def clean(self):
        super().clean()
        if self.finiEnc and self.ffinEnc and self.ffinEnc <= self.finiEnc:
            raise ValidationError({'ffinEnc': 'La fecha de fin debe ser posterior a la fecha de inicio.'})
    
    def save(self, *args, **kwargs):
        from django.utils import timezone
        if not self.ffinEnc and self.finiEnc and self.idDis:
            self.ffinEnc = self.finiEnc + self.idDis.duracion_estimada
        
        now = timezone.now()
        if self.finiEnc and self.ffinEnc:
            if now < self.finiEnc:
                self.estado = 'CONFIRMADO'
            elif self.finiEnc <= now <= self.ffinEnc:
                self.estado = 'EN_PROGRESO'
            else:
                self.estado = 'FINALIZADO'
        elif self.finiEnc and now >= self.finiEnc:
            self.estado = 'EN_PROGRESO'
        else:
            self.estado = 'CONFIRMADO'
            
        super().save(*args, **kwargs)

class EncuentroEquipo(models.Model):
    encuentro = models.ForeignKey(Encuentros, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ENCUENTRO_EQUIPO'
        unique_together = ('encuentro', 'equipo')
        verbose_name = 'Equipo participante'
        verbose_name_plural = 'Equipos participantes'

    def __str__(self):
        return f"{self.equipo.nomEqu}"