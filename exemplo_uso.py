## exemplo_uso.py
"""
COMO USAR O SISTEMA DE RECOMENDAÇÃO?

Este arquivo mostra exemplos práticos de como usar o sistema.
Execute: python exemplo_uso.py
"""

# Importa sua função
from recomendacao import recomendar_carreira

print("=" * 50)
print("EXEMPLOS DE USO DO SISTEMA")
print("=" * 50)

# Exemplo 1
print("\n📍 EXEMPLO 1: Perfil técnico (Python + SQL)")
resultado = recomendar_carreira(
    habilidades="python,sql", 
    experiencia="Júnior",
    pais="Brasil"
)
print("Top 3 recomendações:")
print(resultado.head(3))
print()

# Exemplo 2  
print("📍 EXEMPLO 2: Perfil de negócios (Excel + Power BI)")
resultado = recomendar_carreira(
    habilidades="excel,power bi,sql",
    experiencia="Pleno", 
    pais="Brasil"
)
print("Top 3 recomendações:")
print(resultado.head(3))
