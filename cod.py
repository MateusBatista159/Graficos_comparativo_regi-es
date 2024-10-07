import os
import numpy as np
import matplotlib.pyplot as plt
import re

# Caminhos relativos aos diretórios
base_path = os.path.dirname(__file__)
input_path = os.path.join(base_path, '../input')
nasa_path = os.path.join(input_path, 'nasa')
output_path = os.path.join(base_path, '../output')

# Configuração das moléculas e arquivos
molecule_names = ['c24h12', 'c54h18', 'c96h24', 'c150h30', 'c216h36', 'c294h42', 'c384h48']
molecule_files = {
    'neutro': '{molecule}.dat',
    'cation': '{molecule}_cation+1.dat',
    'anion': '{molecule}_anion-1.dat'
}
color_obtido = 'black'  # Preto
color_pahdb = 'red'     # Vermelho
labels = ['Neutro', 'Cátion', 'Ânion']

# Fatores de escala, proposto no trabalho
scale_factors_1 = [1.04, 1.02, 1.031, 1.042]
scale_factors_2 = [1.035, 1.040, 1.058, 1.045]

# Função para escolher o conjunto de fatores de escala
def choose_scale_factors(molecule, state):
    if molecule == 'c216h36' and state in ['cation', 'anion']:
        return scale_factors_2
    elif molecule == 'c384h48':
        return scale_factors_2
    return scale_factors_1

# Função para aplicar fatores de escala
def apply_scale_factors(wavel, factors):
    factor1, factor2, factor3, factor4 = factors
    return np.where(wavel <= 5, wavel * factor1, 
                    np.where(wavel <= 10, wavel * factor2, 
                             np.where(wavel <= 15, wavel * factor3, 
                                      wavel * factor4)))

# Função para carregar e normalizar dados
def load_data(source):
    wavel, flux = np.loadtxt(source, usecols=[0, 1], unpack=True)
    return wavel, flux / np.max(flux) if np.max(flux) != 0 else flux

# Função para formatar nomes de moléculas
def format_molecule_name(name):
    return re.sub(r'(\d+)', r'$_{\1}$', name.upper())

# Função principal para plotar todas as moléculas
def plot_all_molecules(range_type):
    x_min, x_max, dashed_lines_positions, shaded_regions = get_plot_range(range_type)

    fig, axes = plt.subplots(len(molecule_names), 3, figsize=(18, 3 * len(molecule_names)), sharex=True, constrained_layout=True)

    for i, molecule in enumerate(molecule_names):
        formatted_name = format_molecule_name(molecule)
        for j, (state, filename_template) in enumerate(molecule_files.items()):
            plot_molecule(axes[i, j], molecule, state, filename_template, x_min, x_max, formatted_name, dashed_lines_positions, shaded_regions, i, j)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.081, left=0.08, right=0.985)
    output_filename = os.path.join(output_path, f'comparison_range_{range_type}.png')
    fig.savefig(output_filename, dpi=300)
    plt.show()

# Exemplo de uso: plotar a faixa 3 (10 a 20 microns) para todas as moléculas
if __name__ == "__main__":
    plot_all_molecules(3)
