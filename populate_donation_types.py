from apps.donations.models import DonationType

def populate_types():
    tipos = [
        'Diezmo/Ofrenda',
        'Alimento',
        'Ropa',
        'Material Bíblico',
        'Equipo o tecnología',
        'Voluntariado',
        'Capacitación',
        'Medicamentos',
    ]
    for tipo in tipos:
        DonationType.objects.get_or_create(name=tipo)
    print('Tipos de donación creados o actualizados.')

populate_types() 