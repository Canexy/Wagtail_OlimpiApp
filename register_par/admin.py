from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Equipos, Disciplinas, Pistas, Arbitros, Participantes, Encuentros, EncuentroEquipo

class EquiposAdmin(admin.ModelAdmin):
    list_display = ['idEqu', 'nomEqu', 'oliEqu', 'num_participantes', 'puede_eliminarse']
    list_filter = ['oliEqu']
    search_fields = ['nomEqu']
    actions = ['eliminar_equipos_seguros']
    
    def num_participantes(self, obj):
        return obj.participantes.count()
    num_participantes.short_description = 'Núm. de Participantes:'
    
    def puede_eliminarse(self, obj):
        return obj.puede_eliminarse()
    puede_eliminarse.boolean = True
    puede_eliminarse.short_description = '¿Puede Eliminarse?'
    
    def eliminar_equipos_seguros(self, request, queryset):
        eliminados = 0
        for equipo in queryset:
            if equipo.puede_eliminarse():
                equipo.delete()
                eliminados += 1
            else:
                self.message_user(
                    request, 
                    f"No se pudo eliminar {equipo.nomEqu}. Tiene encuentros asociados.", 
                    messages.WARNING
                )
        self.message_user(request, f"{eliminados} equipos eliminados correctamente.")
    eliminar_equipos_seguros.short_description = "Eliminar equipos (solo si no tienen encuentros)"

admin.site.register(Equipos, EquiposAdmin)

class ParticipantesAdmin(admin.ModelAdmin):
    list_display = ['idPar', 'nomPar', 'curPar', 'equipo']
    list_filter = ['equipo', 'curPar']
    search_fields = ['nomPar', 'curPar']

admin.site.register(Participantes, ParticipantesAdmin)

class DisciplinasAdmin(admin.ModelAdmin):
    list_display = ['idDis', 'nomDis', 'duracion_estimada', 'min_equipos', 'max_equipos']
    search_fields = ['nomDis']

admin.site.register(Disciplinas, DisciplinasAdmin)

class PistasAdmin(admin.ModelAdmin):
    list_display = ['idPis', 'nomPis', 'cubPis']
    list_filter = ['cubPis']
    search_fields = ['nomPis']

admin.site.register(Pistas, PistasAdmin)

class ArbitrosAdmin(admin.ModelAdmin):
    list_display = ['idArb', 'nomArb', 'telArb', 'conArb']
    search_fields = ['nomArb']

admin.site.register(Arbitros, ArbitrosAdmin)

class EncuentroEquipoFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        if any(self.errors):
            return
            
        if hasattr(self, 'instance') and hasattr(self.instance, 'idDis') and self.instance.idDis:
            disciplina = self.instance.idDis
            
            equipos_count = 0
            equipos_instances = []
            
            for form in self.forms:
                if (not form.cleaned_data.get('DELETE', False) and 
                    form.cleaned_data.get('equipo')):
                    equipos_count += 1
                    equipos_instances.append(form.cleaned_data['equipo'])
            
            if not (disciplina.min_equipos <= equipos_count <= disciplina.max_equipos):
                raise ValidationError(
                    f"Esta disciplina requiere entre {disciplina.min_equipos} y {disciplina.max_equipos} equipos. "
                    f"Tiene {equipos_count} equipos."
                )
            
            if equipos_count > 0:
                from django.db.models import Count
                equipos_con_ids = [equipo.idEqu for equipo in equipos_instances]
                equipos_con_conteo = Equipos.objects.filter(idEqu__in=equipos_con_ids).annotate(
                    num_participantes=Count('participantes')
                )
                
                for equipo in equipos_con_conteo:
                    if equipo.num_participantes < disciplina.min_participantes_por_equipo:
                        raise ValidationError(
                            f"El equipo '{equipo.nomEqu}' tiene {equipo.num_participantes} participantes. "
                            f"Mínimo requerido: {disciplina.min_participantes_por_equipo}"
                        )
                    if equipo.num_participantes > disciplina.max_participantes_por_equipo:
                        raise ValidationError(
                            f"El equipo '{equipo.nomEqu}' tiene {equipo.num_participantes} participantes. "
                            f"Máximo permitido: {disciplina.max_participantes_por_equipo}"
                        )

class EncuentroEquipoInline(admin.TabularInline):
    model = EncuentroEquipo
    formset = EncuentroEquipoFormSet
    extra = 1
    min_num = 1

@admin.register(Encuentros)
class EncuentrosAdmin(admin.ModelAdmin):
    inlines = [EncuentroEquipoInline]
    list_display = ['idEnc', 'idDis', 'finiEnc', 'ffinEnc', 'estado', 'idPis', 'arbitro']
    list_filter = ['idDis', 'idPis', 'finiEnc', 'estado']
    search_fields = ['idDis__nomDis', 'idPis__nomPis']
    readonly_fields = ['estado']
    date_hierarchy = 'finiEnc'
    
    def save_model(self, request, obj, form, change):
        if not obj.ffinEnc and obj.finiEnc and obj.idDis:
            from datetime import timedelta
            obj.ffinEnc = obj.finiEnc + obj.idDis.duracion_estimada
        super().save_model(request, obj, form, change)