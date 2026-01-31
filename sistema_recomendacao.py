# ====================================================
# SISTEMA DE RECOMENDAÇÃO DE CARREIRA EM TECNOLOGIA
# Versão Profissional - Tudo em uma única célula
# ====================================================

# Instalar bibliotecas necessárias
!pip install pandas matplotlib seaborn -q

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("SISTEMA DE RECOMENDAÇÃO DE CARREIRA EM TECNOLOGIA")
print("=" * 60)

# ====================================================
# 1. BASE DE DADOS DE CARGOS EM TECNOLOGIA
# ====================================================
print("\nCRIANDO BASE DE DADOS DE CARGOS...")

# Dados dos cargos em tecnologia
cargos_data = [
    # Cargo, Habilidades, Salário BR, Salário USD, Experiência, Demanda, Descrição
    ["Cientista de Dados", "python,machine learning,estatistica,sql", 12000, 120000, "Senior", "Alta", "Analisa dados complexos e cria modelos preditivos"],
    ["Engenheiro de Dados", "sql,cloud,etl,data pipelines", 11000, 110000, "Pleno", "Alta", "Constrói e mantém pipelines de dados"],
    ["Analista de Dados", "sql,excel,power bi,analise", 8000, 80000, "Junior", "Muito Alta", "Transforma dados em insights para negócios"],
    ["Desenvolvedor Frontend", "javascript,react,css,html", 9000, 90000, "Pleno", "Alta", "Desenvolve interfaces web responsivas"],
    ["Desenvolvedor Backend", "python,java,apis,banco de dados", 9500, 95000, "Pleno", "Alta", "Desenvolve lógica de servidor e APIs"],
    ["Engenheiro DevOps", "docker,aws,linux,ci/cd", 11500, 115000, "Senior", "Alta", "Automatiza infraestrutura e processos de deployment"],
    ["Designer UX/UI", "figma,ui,ux,prototipacao", 8500, 85000, "Pleno", "Media", "Cria interfaces e experiências do usuário"],
    ["Engenheiro de Machine Learning", "python,tensorflow,deep learning,cloud", 13000, 130000, "Senior", "Alta", "Desenvolve e implanta modelos de ML"],
    ["Analista de Business Intelligence", "power bi,sql,dashboards,negocios", 7500, 75000, "Junior", "Alta", "Cria dashboards e relatórios de negócio"],
    ["Engenheiro de Cloud", "aws,azure,docker,kubernetes", 12500, 125000, "Senior", "Muito Alta", "Gerencia infraestrutura na nuvem"],
    ["Gerente de Produto", "produto,estrategia,agile,leadership", 15000, 150000, "Senior", "Alta", "Define estratégia e roadmap de produtos"],
    ["QA Engineer", "testes,automacao,selenium,jira", 7000, 70000, "Junior", "Media", "Garante qualidade do software através de testes"]
]

# Criar DataFrame
df_cargos = pd.DataFrame(cargos_data, columns=["Cargo", "Habilidades", "Salario_BR", "Salario_USD", "Experiencia", "Demanda", "Descricao"])

print(f"Base criada com {len(df_cargos)} cargos em tecnologia")
print("\nCARGOS DISPONIVEIS PARA ANALISE:")
for i, cargo in enumerate(df_cargos["Cargo"], 1):
    print(f"   {i:2d}. {cargo}")

# ====================================================
# 2. SISTEMA DE RECOMENDAÇÃO
# ====================================================
def recomendar_carreira(habilidades_usuario, experiencia_usuario, pais="Brasil"):
    """
    Sistema de recomendação baseado em compatibilidade de habilidades
    
    Args:
        habilidades_usuario: string com habilidades separadas por vírgula
        experiencia_usuario: 'Junior', 'Pleno' ou 'Senior'
        pais: 'Brasil' ou 'EUA' para referência salarial
    """
    resultados = []
    
    # Processar habilidades do usuário
    habilidades_lista = [h.strip().lower() for h in habilidades_usuario.split(",")]
    
    for _, cargo in df_cargos.iterrows():
        # Processar habilidades do cargo
        habilidades_cargo = [h.strip().lower() for h in cargo["Habilidades"].split(",")]
        
        # Calcular compatibilidade de habilidades
        habilidades_comuns = set(habilidades_lista) & set(habilidades_cargo)
        compatibilidade_base = (len(habilidades_comuns) / len(habilidades_cargo)) * 100
        
        # Ajuste por nível de experiência
        ajuste_experiencia = 0
        if cargo["Experiencia"] == experiencia_usuario:
            ajuste_experiencia = 20  # Bônus por experiência compatível
        
        # Ajuste por demanda no mercado
        ajuste_demanda = {
            "Muito Alta": 15,
            "Alta": 10,
            "Media": 5
        }.get(cargo["Demanda"], 0)
        
        # Score total de compatibilidade
        compatibilidade_total = compatibilidade_base + ajuste_experiencia + ajuste_demanda
        compatibilidade_total = min(compatibilidade_total, 100)  # Limitar a 100%
        
        # Selecionar faixa salarial conforme o país
        if pais == "Brasil":
            salario = cargo["Salario_BR"]
            moeda = "R$"
        else:
            salario = cargo["Salario_USD"]
            moeda = "US$"
        
        # Coletar resultado
        resultados.append({
            "Cargo": cargo["Cargo"],
            "Compatibilidade (%)": round(compatibilidade_total, 1),
            "Salario": f"{moeda} {salario:,.0f}",
            "Experiencia_Ideal": cargo["Experiencia"],
            "Demanda_Mercado": cargo["Demanda"],
            "Habilidades_Compatíveis": len(habilidades_comuns),
            "Total_Habilidades": len(habilidades_cargo),
            "Descricao": cargo["Descricao"]
        })
    
    # Ordenar por compatibilidade (maior para menor)
    resultados.sort(key=lambda x: x["Compatibilidade (%)"], reverse=True)
    
    return pd.DataFrame(resultados)

# ====================================================
# 3. DEMONSTRAÇÃO DO SISTEMA
# ====================================================
print("\n" + "=" * 60)
print("DEMONSTRACAO DO SISTEMA")
print("Perfil de exemplo: Habilidades = 'python, sql' | Experiencia = 'Junior'")
print("-" * 60)

# Teste demonstrativo
resultados_exemplo = recomendar_carreira("python,sql", "Junior", "Brasil")

print("\nTOP 3 RECOMENDACOES (EXEMPLO):")
print("-" * 40)
for i in range(min(3, len(resultados_exemplo))):
    rec = resultados_exemplo.iloc[i]
    print(f"\n{i+1}. {rec['Cargo']}")
    print(f"   Compatibilidade: {rec['Compatibilidade (%)']}%")
    print(f"   Salario medio: {rec['Salario']}")
    print(f"   Demanda: {rec['Demanda_Mercado']}")
    print(f"   Habilidades compativeis: {rec['Habilidades_Compatíveis']}/{rec['Total_Habilidades']}")

# ====================================================
# 4. COLETA DE DADOS DO USUARIO
# ====================================================
print("\n" + "=" * 60)
print("ANALISE PERSONALIZADA - SEU PERFIL")
print("=" * 60)

print("\nINSTRUCOES:")
print("1. Digite suas habilidades tecnicas")
print("2. Informe seu nivel de experiencia")
print("3. Selecione sua localizacao para referencia salarial")
print("\nExemplo de habilidades: python, sql, excel, javascript")
print("Separar habilidades por virgula")

# Coletar dados do usuario
habilidades_usuario = input("\nDigite suas habilidades tecnicas: ")

print("\nNIVEIS DE EXPERIENCIA DISPONIVEIS:")
print(" - Junior (0-2 anos de experiencia)")
print(" - Pleno (2-5 anos de experiencia)")
print(" - Senior (5+ anos de experiencia)")
experiencia_usuario = input("Selecione seu nivel: ")

print("\nLOCALIZACAO PARA REFERENCIA SALARIAL:")
print(" - Brasil (salarios em Reais)")
print(" - EUA (salarios em Dólares)")
pais_usuario = input("Selecione: ")

# Validar entrada
if experiencia_usuario not in ["Junior", "Pleno", "Senior"]:
    experiencia_usuario = "Junior"
    print("Nivel padrao 'Junior' selecionado.")

if pais_usuario not in ["Brasil", "EUA"]:
    pais_usuario = "Brasil"
    print("Localizacao padrao 'Brasil' selecionada.")

print(f"\nAnalisando perfil...")
print(f"Habilidades: {habilidades_usuario}")
print(f"Experiencia: {experiencia_usuario}")
print(f"Localizacao: {pais_usuario}")

# ====================================================
# 5. PROCESSAMENTO E ANALISE
# ====================================================
resultados_usuario = recomendar_carreira(habilidades_usuario, experiencia_usuario, pais_usuario)

print("\n" + "=" * 60)
print("RESULTADOS DA ANALISE")
print("=" * 60)

print(f"\nCARGOS ANALISADOS: {len(resultados_usuario)}")
print(f"COMPATIBILIDADE MEDIA: {resultados_usuario['Compatibilidade (%)'].mean():.1f}%")

# ====================================================
# 6. TOP RECOMENDACOES
# ====================================================
print("\nTOP 5 RECOMENDACOES PARA SEU PERFIL:")
print("-" * 50)

for i in range(min(5, len(resultados_usuario))):
    rec = resultados_usuario.iloc[i]
    
    # Classificar nivel de compatibilidade
    if rec['Compatibilidade (%)'] > 80:
        classificacao = "EXCELENTE"
    elif rec['Compatibilidade (%)'] > 60:
        classificacao = "BOA"
    elif rec['Compatibilidade (%)'] > 40:
        classificacao = "MODERADA"
    else:
        classificacao = "BAIXA"
    
    print(f"\n{i+1}. {rec['Cargo']} - [{classificacao}]")
    print(f"   Compatibilidade: {rec['Compatibilidade (%)']}%")
    print(f"   Salario de mercado: {rec['Salario']}")
    print(f"   Nivel de experiencia ideal: {rec['Experiencia_Ideal']}")
    print(f"   Demanda no mercado: {rec['Demanda_Mercado']}")
    print(f"   Habilidades compativeis: {rec['Habilidades_Compatíveis']} de {rec['Total_Habilidades']}")
    print(f"   Descricao: {rec['Descricao']}")

# ====================================================
# 7. VISUALIZACAO GRAFICA
# ====================================================
print("\n" + "=" * 60)
print("VISUALIZACAO GRAFICA DOS RESULTADOS")
print("=" * 60)

# Configurar estilo dos graficos
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Criar figura com subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Grafico 1: Top 5 cargos por compatibilidade
top5 = resultados_usuario.head(5).copy()
top5 = top5.sort_values('Compatibilidade (%)', ascending=True)

cores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']
bars1 = axes[0].barh(top5['Cargo'], top5['Compatibilidade (%)'], color=cores, edgecolor='black', height=0.7)

# Adicionar valores nas barras
for bar, valor in zip(bars1, top5['Compatibilidade (%)']):
    axes[0].text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2, 
                f'{valor:.1f}%', va='center', fontweight='bold')

axes[0].set_xlabel('Compatibilidade (%)', fontweight='bold')
axes[0].set_title('TOP 5 - Compatibilidade por Cargo', fontweight='bold', pad=15)
axes[0].set_xlim([0, 105])
axes[0].grid(True, alpha=0.3, linestyle='--')

# Grafico 2: Comparacao salarial
salarios = []
for salario_str in top5['Salario']:
    # Extrair valor numerico
    valor = float(''.join(filter(str.isdigit, salario_str)))
    salarios.append(valor)

bars2 = axes[1].bar(top5['Cargo'], salarios, color='#28a745', alpha=0.7, edgecolor='black')

# Adicionar valores nas barras
for bar, valor, cargo in zip(bars2, salarios, top5['Cargo']):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(salarios)*0.02,
                f'{valor:,.0f}', ha='center', va='bottom', fontsize=9)

axes[1].set_ylabel('Salario Medio', fontweight='bold')
axes[1].set_title('Comparacao Salarial - Top 5 Cargos', fontweight='bold', pad=15)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.show()

# ====================================================
# 8. ANALISE ESTATISTICA DETALHADA
# ====================================================
print("\n" + "=" * 60)
print("ANALISE ESTATISTICA DETALHADA")
print("=" * 60)

# Calcular estatisticas
compatibilidade_max = resultados_usuario['Compatibilidade (%)'].max()
cargo_max = resultados_usuario.loc[resultados_usuario['Compatibilidade (%)'].idxmax(), 'Cargo']

compatibilidade_min = resultados_usuario['Compatibilidade (%)'].min()
cargo_min = resultados_usuario.loc[resultados_usuario['Compatibilidade (%)'].idxmin(), 'Cargo']

compatibilidade_media = resultados_usuario['Compatibilidade (%)'].mean()
compatibilidade_mediana = resultados_usuario['Compatibilidade (%)'].median()

alta_compatibilidade = len(resultados_usuario[resultados_usuario['Compatibilidade (%)'] > 70])
baixa_compatibilidade = len(resultados_usuario[resultados_usuario['Compatibilidade (%)'] < 30])

print("\nESTATISTICAS DA ANALISE:")
print(f"• Maior compatibilidade: {compatibilidade_max:.1f}% ({cargo_max})")
print(f"• Menor compatibilidade: {compatibilidade_min:.1f}% ({cargo_min})")
print(f"• Compatibilidade media: {compatibilidade_media:.1f}%")
print(f"• Compatibilidade mediana: {compatibilidade_mediana:.1f}%")
print(f"• Cargos com alta compatibilidade (>70%): {alta_compatibilidade}")
print(f"• Cargos com baixa compatibilidade (<30%): {baixa_compatibilidade}")

# Distribuicao por nivel de compatibilidade
print("\nDISTRIBUICAO POR NIVEL DE COMPATIBILIDADE:")
distribuicao = {
    "Excelente (>80%)": len(resultados_usuario[resultados_usuario['Compatibilidade (%)'] > 80]),
    "Boa (60-80%)": len(resultados_usuario[(resultados_usuario['Compatibilidade (%)'] >= 60) & 
                                          (resultados_usuario['Compatibilidade (%)'] <= 80)]),
    "Moderada (40-60%)": len(resultados_usuario[(resultados_usuario['Compatibilidade (%)'] >= 40) & 
                                               (resultados_usuario['Compatibilidade (%)'] < 60)]),
    "Baixa (<40%)": len(resultados_usuario[resultados_usuario['Compatibilidade (%)'] < 40])
}

for categoria, quantidade in distribuicao.items():
    percentual = (quantidade / len(resultados_usuario)) * 100
    print(f"   {categoria}: {quantidade} cargos ({percentual:.1f}%)")

# ====================================================
# 9. RECOMENDACOES PERSONALIZADAS
# ====================================================
print("\n" + "=" * 60)
print("RECOMENDACOES PERSONALIZADAS")
print("=" * 60)

cargo_recomendado = resultados_usuario.iloc[0]['Cargo']
compatibilidade_recomendado = resultados_usuario.iloc[0]['Compatibilidade (%)']

print(f"\nCARGO MAIS COMPATIVEL: {cargo_recomendado}")
print(f"COMPATIBILIDADE: {compatibilidade_recomendado}%")

if compatibilidade_recomendado > 70:
    print("\nANALISE: Seu perfil apresenta excelente compatibilidade com o mercado.")
    print("RECOMENDACAO: Focar no cargo mais compativel e buscar oportunidades.")
    
elif compatibilidade_recomendado > 50:
    print("\nANALISE: Seu perfil apresenta boa compatibilidade com o mercado.")
    print("RECOMENDACAO: Desenvolver habilidades especificas para aumentar a compatibilidade.")
    
else:
    print("\nANALISE: Seu perfil apresenta compatibilidade moderada com o mercado.")
    print("RECOMENDACAO: Investir em capacitacao nas areas de maior demanda.")

# Sugestoes de desenvolvimento
print("\nSUGESTOES PARA DESENVOLVIMENTO PROFISSIONAL:")
print("1. Identifique as habilidades faltantes para os cargos de interesse")
print("2. Busque cursos e certificacoes nas areas de maior compatibilidade")
print("3. Participe de projetos praticos para ganhar experiencia")
print("4. Conecte-se com profissionais da area para networking")
print("5. Atualize seu curriculo e perfil no LinkedIn")

# ====================================================
# 10. EXPORTACAO DOS RESULTADOS
# ====================================================
print("\n" + "=" * 60)
print("EXPORTACAO DOS RESULTADOS")
print("=" * 60)

# Criar nome do arquivo com timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nome_arquivo_csv = f"recomendacao_carreira_{timestamp}.csv"
nome_arquivo_txt = f"resumo_recomendacao_{timestamp}.txt"

# Salvar resultados completos em CSV
resultados_usuario.to_csv(nome_arquivo_csv, index=False, encoding='utf-8-sig')

# Salvar resumo em arquivo de texto
with open(nome_arquivo_txt, 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("RELATORIO DE RECOMENDACAO DE CARREIRA\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"Data da analise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    f.write(f"Habilidades informadas: {habilidades_usuario}\n")
    f.write(f"Nivel de experiencia: {experiencia_usuario}\n")
    f.write(f"Localizacao de referencia: {pais_usuario}\n\n")
    
    f.write("-" * 60 + "\n")
    f.write("TOP 3 RECOMENDACOES\n")
    f.write("-" * 60 + "\n\n")
    
    for i in range(min(3, len(resultados_usuario))):
        rec = resultados_usuario.iloc[i]
        f.write(f"{i+1}. {rec['Cargo']}\n")
        f.write(f"   Compatibilidade: {rec['Compatibilidade (%)']}%\n")
        f.write(f"   Salario: {rec['Salario']}\n")
        f.write(f"   Experiencia ideal: {rec['Experiencia_Ideal']}\n")
        f.write(f"   Demanda: {rec['Demanda_Mercado']}\n")
        f.write(f"   Descricao: {rec['Descricao']}\n\n")
    
    f.write("-" * 60 + "\n")
    f.write("PLANO DE ACAO SUGERIDO\n")
    f.write("-" * 60 + "\n\n")
    
    f.write("1. Focar no desenvolvimento das habilidades para o cargo mais compativel\n")
    f.write("2. Buscar capacitacao nas areas identificadas como prioritarias\n")
    f.write("3. Participar de comunidades e eventos da area\n")
    f.write("4. Desenvolver projetos praticos para portfolio\n")
    f.write("5. Atualizar curriculo e perfis profissionais\n")

print(f"Arquivos gerados com sucesso:")
print(f"1. {nome_arquivo_csv} - Tabela completa com todos os resultados")
print(f"2. {nome_arquivo_txt} - Resumo da analise com recomendacoes")

print("\nINSTRUCOES PARA DOWNLOAD:")
print("1. No menu esquerdo, clique no icone de pasta")
print("2. Clique no botao 'Atualizar'")
print("3. Localize os arquivos gerados")
print("4. Clique nos tres pontos ao lado de cada arquivo")
print("5. Selecione 'Download'")

# ====================================================
# 11. RESUMO FINAL
# ====================================================
print("\n" + "=" * 60)
print("RESUMO FINAL DA ANALISE")
print("=" * 60)

print(f"""
PERFIL ANALISADO:
• Habilidades: {habilidades_usuario}
• Experiencia: {experiencia_usuario}
• Localizacao: {pais_usuario}

PRINCIPAIS RESULTADOS:
• Cargo mais compativel: {resultados_usuario.iloc[0]['Cargo']}
• Compatibilidade do top 1: {resultados_usuario.iloc[0]['Compatibilidade (%)']}%
• Faixa salarial de referencia: {resultados_usuario.iloc[0]['Salario']}
• Cargos com alta compatibilidade: {alta_compatibilidade}

PROXIMOS PASSOS SUGERIDOS:
1. Analisar detalhadamente o cargo mais compativel
2. Identificar lacunas de habilidades para desenvolvimento
3. Buscar recursos de capacitacao nas areas prioritarias
4. Iniciar projetos praticos para aplicacao do conhecimento
5. Participar de comunidades profissionais da area

ARQUIVOS DISPONIVEIS PARA CONSULTA:
• {nome_arquivo_csv} - Dados completos da analise
• {nome_arquivo_txt} - Resumo executivo com plano de acao
""")

# ====================================================
# 12. INFORMACOES ADICIONAIS
# ====================================================
print("\n" + "=" * 60)
print("INFORMACOES ADICIONAIS E CONTATO")
print("=" * 60)

print("""
SOBRE O SISTEMA:
Este sistema de recomendacao foi desenvolvido com base em analise de dados
do mercado de tecnologia. Os dados salariais sao referencias medias e podem
variar conforme regiao, empresa e nivel de senioridade.

LIMITACOES:
• Analise baseada em habilidades tecnicas declaradas
• Dados salariais sao referencias medias do mercado
• Compatibilidade calculada com base em correspondencia de habilidades

PRECISAO:
O sistema apresenta uma analise preliminar baseada nas informacoes fornecidas.
Para uma avaliacao mais precisa, recomenda-se consultar fontes adicionais e
conversar com profissionais da area.

DESENVOLVIMENTO:
Sistema desenvolvido utilizando Python e bibliotecas de analise de dados,
baseado nos conceitos aprendidos em Ciencia de Dados.

PARA NOVAS ANALISES:
Execute esta celula novamente para analisar diferentes combinacoes de
habilidades, niveis de experiencia ou localizacoes.
""")

print("\n" + "=" * 60)
print("ANALISE CONCLUIDA COM SUCESSO")
print("=" * 60)
