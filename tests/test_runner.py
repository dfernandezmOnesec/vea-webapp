#!/usr/bin/env python
"""
Script personalizado para ejecutar pruebas de la aplicación VEA WebApp
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_tests(test_type=None, verbose=False, coverage=False):
    """
    Ejecuta las pruebas según el tipo especificado
    
    Args:
        test_type (str): Tipo de pruebas a ejecutar (unit, functional, integration, e2e, all)
        verbose (bool): Si mostrar salida detallada
        coverage (bool): Si generar reporte de cobertura
    """
    
    # Configurar variables de entorno
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    
    # Comandos base
    base_cmd = ['python', '-m', 'pytest']
    
    if verbose:
        base_cmd.append('-v')
    
    if coverage:
        base_cmd.extend(['--cov=apps', '--cov-report=html', '--cov-report=term-missing'])
    
    # Definir rutas de pruebas por tipo
    test_paths = {
        'unit': ['tests/unit/'],
        'functional': ['tests/functional/'],
        'integration': ['tests/integration/'],
        'e2e': ['tests/e2e/'],
        'all': ['tests/']
    }
    
    if test_type and test_type in test_paths:
        cmd = base_cmd + test_paths[test_type]
    else:
        cmd = base_cmd + ['tests/']
    
    print(f"Ejecutando pruebas: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Pruebas completadas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Las pruebas fallaron con código de salida: {e.returncode}")
        return False

def run_specific_test(test_file):
    """
    Ejecuta una prueba específica
    
    Args:
        test_file (str): Ruta al archivo de prueba
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    
    cmd = ['python', '-m', 'pytest', test_file, '-v']
    
    print(f"Ejecutando prueba específica: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Prueba completada exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ La prueba falló con código de salida: {e.returncode}")
        return False

def check_test_environment():
    """
    Verifica que el entorno de pruebas esté configurado correctamente
    """
    print("🔍 Verificando entorno de pruebas...")
    
    # Verificar que estamos en el directorio correcto
    if not Path('manage.py').exists():
        print("❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto.")
        return False
    
    # Verificar que existe el directorio de pruebas
    if not Path('tests').exists():
        print("❌ Error: No se encontró el directorio tests/")
        return False
    
    # Verificar que existen los subdirectorios de pruebas
    test_dirs = ['unit', 'functional', 'integration', 'e2e']
    for test_dir in test_dirs:
        if not Path(f'tests/{test_dir}').exists():
            print(f"⚠️  Advertencia: No se encontró el directorio tests/{test_dir}/")
    
    print("✅ Entorno de pruebas verificado")
    return True

def main():
    """
    Función principal del script
    """
    parser = argparse.ArgumentParser(description='Ejecutor de pruebas para VEA WebApp')
    parser.add_argument(
        '--type', 
        choices=['unit', 'functional', 'integration', 'e2e', 'all'],
        default='all',
        help='Tipo de pruebas a ejecutar'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar salida detallada'
    )
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Generar reporte de cobertura'
    )
    parser.add_argument(
        '--file', '-f',
        help='Ejecutar una prueba específica (ruta al archivo)'
    )
    
    args = parser.parse_args()
    
    # Verificar entorno
    if not check_test_environment():
        sys.exit(1)
    
    # Ejecutar pruebas
    if args.file:
        success = run_specific_test(args.file)
    else:
        success = run_tests(args.type, args.verbose, args.coverage)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main() 