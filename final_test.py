#!/usr/bin/env python
"""
Script final de verificación para VEA WebApp
"""
import os
import sys
import subprocess
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Función principal"""
    print("Ejecutando verificación final...")
    print("=" * 60)
    
    # Configurar variables de entorno para las pruebas
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
    os.environ.setdefault('DISABLE_AZURE_SIGNALS', 'True')
    
    try:
        # Ejecutar el script de verificación pre-despliegue
        print("Ejecutando verificación pre-despliegue...")
        result = subprocess.run([
            sys.executable, 'scripts/pre_deployment_check.py'
        ], capture_output=True, text=True, cwd=project_root)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("=" * 60)
            print("✅ Verificación final completada exitosamente")
            return True
        else:
            print("=" * 60)
            print("❌ Verificación final falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en verificación final: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 