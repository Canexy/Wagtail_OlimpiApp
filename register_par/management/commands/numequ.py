from django.core.management.base import BaseCommand, CommandError
from register_par.models import Equipos
import argparse


class Command(BaseCommand):
    help = 'Enseña el número de equipos totales registrados actualmente.'

    def add_arguments(self, parser):
        parser.add_argument('--oli', '-o', type=str, help='Indica si el equipo es olímpico o no.')
        # choices={'n', 's'},

    def handle(self, *args, **options):
        oliEqu = options['oli']

        if oliEqu is None:
            total = Equipos.objects.count()
            self.stdout.write(f"Número total de equipos registrados: {total}.")
        else:
            oliEqu = oliEqu.upper()
            if oliEqu not in ['N', 'S']:
                raise CommandError("El argumento -o debe ser 'n' para equipos no olímpicos, o 's' para equipos olímpicos.")
            try:
                total = Equipos.objects.filter(oliEqu=oliEqu.upper()).count()
            except Equipos.DoesNotExist:
                raise CommandError("No existe ningún equipo con el valor especificado.")

            if total == 0:
                self.stdout.write(f"No hay equipos con esa condición.")
            else:
                if oliEqu == 'S':
                    self.stdout.write(f"Número total de equipos olímpicos registrados: {total}.")
                else:
                    self.stdout.write(f"Número total de equipos no olímpicos registrados: {total}.")