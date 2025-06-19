#!/usr/bin/env python
"""
Script de verificación pre-despliegue para VEA WebApp
Verifica que todo esté listo para el despliegue en Azure
"""
import os
import sys
import subprocess
import importlib
from pathlib import Path
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Se requiere Python 3.8+ (actual: {version.major}.{version.minor})")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_django_installation():
    """Verifica la instalación de Django"""
    print("🔧 Verificando instalación de Django...")
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
        return True
    except ImportError:
        print("❌ Error: Django no está instalado")
        return False

def check_dependencies():
    """Verifica las dependencias del proyecto"""
    print("📦 Verificando dependencias...")
    required_packages = [
        'django',
        'azure-storage-blob',
        'django-storages',
        'pytest',
        'pytest-django'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - FALTANTE")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Faltan dependencias: {', '.join(missing_packages)}")
        return False
    
    return True

def check_django_settings():
    """Verifica la configuración de Django"""
    print("⚙️ Verificando configuración de Django...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    
    try:
        django.setup()
        print("✅ Configuración de Django - OK")
        
        # Verificar configuraciones críticas
        critical_settings = [
            'SECRET_KEY',
            'DEBUG',
            'ALLOWED_HOSTS',
            'DATABASES',
            'STATIC_URL',
            'MEDIA_URL'
        ]
        
        for setting in critical_settings:
            if hasattr(settings, setting):
                print(f"✅ {setting} - Configurado")
            else:
                print(f"⚠️ {setting} - No configurado")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración de Django: {e}")
        return False

def check_database():
    """Verifica la conexión a la base de datos"""
    print("🗄️ Verificando base de datos...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a base de datos - OK")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def check_migrations():
    """Verifica el estado de las migraciones"""
    print("🔄 Verificando migraciones...")
    
    try:
        # Verificar migraciones pendientes
        result = subprocess.run([
            'python', 'manage.py', 'showmigrations', '--list'
        ], capture_output=True, text=True, check=True)
        
        if '[X]' in result.stdout:
            print("✅ Migraciones aplicadas - OK")
        else:
            print("⚠️ Hay migraciones pendientes")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error verificando migraciones: {e}")
        return False

def check_static_files():
    """Verifica los archivos estáticos"""
    print("📁 Verificando archivos estáticos...")
    
    static_dirs = ['static', 'staticfiles']
    for static_dir in static_dirs:
        if Path(static_dir).exists():
            print(f"✅ Directorio {static_dir} - Existe")
        else:
            print(f"⚠️ Directorio {static_dir} - No existe")
    
    return True

def check_tests():
    """Ejecuta las pruebas para verificar que todo funciona"""
    print("🧪 Ejecutando pruebas...")
    
    try:
        # Ejecutar pruebas unitarias rápidas
        result = subprocess.run([
            'python', '-m', 'pytest', 'tests/unit/', '-v', '--tb=short'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Pruebas unitarias - PASARON")
        else:
            print("❌ Pruebas unitarias - FALLARON")
            print(result.stdout)
            print(result.stderr)
            return False
        
        return True
    except subprocess.TimeoutExpired:
        print("❌ Pruebas tardaron demasiado tiempo")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def check_azure_config():
    """Verifica la configuración de Azure"""
    print("☁️ Verificando configuración de Azure...")
    
    # Verificar archivos de configuración de Azure
    azure_files = [
        'azure.yaml',
        'infra/main.bicep',
        'infra/main.parameters.json'
    ]
    
    for azure_file in azure_files:
        if Path(azure_file).exists():
            print(f"✅ {azure_file} - Existe")
        else:
            print(f"⚠️ {azure_file} - No existe")
    
    # Verificar variables de entorno de Azure
    azure_env_vars = [
        'AZURE_STORAGE_CONNECTION_STRING',
        'AZURE_STORAGE_ACCOUNT_NAME',
        'AZURE_STORAGE_ACCOUNT_KEY'
    ]
    
    for env_var in azure_env_vars:
        if os.getenv(env_var):
            print(f"✅ {env_var} - Configurado")
        else:
            print(f"⚠️ {env_var} - No configurado")
    
    return True

def check_security():
    """Verifica configuraciones de seguridad"""
    print("🔒 Verificando configuraciones de seguridad...")
    
    try:
        # Verificar que DEBUG está en False para producción
        if settings.DEBUG:
            print("⚠️ DEBUG está en True - No recomendado para producción")
        else:
            print("✅ DEBUG está en False - OK")
        
        # Verificar SECRET_KEY
        if settings.SECRET_KEY and settings.SECRET_KEY != 'your-secret-key-here':
            print("✅ SECRET_KEY configurado - OK")
        else:
            print("❌ SECRET_KEY no configurado correctamente")
            return False
        
        # Verificar ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            print("✅ ALLOWED_HOSTS configurado - OK")
        else:
            print("⚠️ ALLOWED_HOSTS no configurado")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando seguridad: {e}")
        return False

def check_performance():
    """Verifica configuraciones de rendimiento"""
    print("⚡ Verificando configuraciones de rendimiento...")
    
    try:
        # Verificar configuración de caché
        if hasattr(settings, 'CACHES') and settings.CACHES:
            print("✅ Caché configurado - OK")
        else:
            print("⚠️ Caché no configurado")
        
        # Verificar configuración de sesiones
        if hasattr(settings, 'SESSION_ENGINE'):
            print("✅ Sesiones configuradas - OK")
        else:
            print("⚠️ Sesiones no configuradas")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando rendimiento: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando verificación pre-despliegue para VEA WebApp")
    print("=" * 60)
    
    checks = [
        check_python_version,
        check_django_installation,
        check_dependencies,
        check_django_settings,
        check_database,
        check_migrations,
        check_static_files,
        check_tests,
        check_azure_config,
        check_security,
        check_performance
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check in checks:
        try:
            if check():
                passed_checks += 1
            print()
        except Exception as e:
            print(f"❌ Error en verificación: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Resumen: {passed_checks}/{total_checks} verificaciones pasaron")
    
    if passed_checks == total_checks:
        print("🎉 ¡Todo listo para el despliegue!")
        return True
    else:
        print("⚠️ Hay problemas que deben resolverse antes del despliegue")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 