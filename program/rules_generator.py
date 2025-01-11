import pandas as pd
import pickle
import ssl
import os
from fpgrowth_py import fpgrowth


class PlaylistRulesGenerator:
    def __init__(self, min_sup_ratio=0.4, min_conf=0.6):
        """
        Inicializa o gerador de regras com suporte e confiança mínimos.
        :param min_sup_ratio: Suporte mínimo necessário para um itemset ser considerado frequente.
        :param min_conf: Confiança mínima para uma regra ser válida.
        """
        self.min_sup_ratio = min_sup_ratio
        self.min_conf = min_conf
        self.rules = []

    def generate_rules(self, transactions):
        """
        Gera regras de associação a partir de transações.
        :param transactions: Lista de listas, onde cada sublista representa uma cesta de itens.
        """
        freq_item_set, self.rules = fpgrowth(
            transactions, self.min_sup_ratio, self.min_conf
        )
        print(self.rules)
        return freq_item_set, self.rules

    def save_rules(self, filepath):
        """
        Salva as regras geradas em um arquivo utilizando pickle.
        :param filepath: Caminho do arquivo onde as regras serão armazenadas.
        """
        with open(filepath, "wb") as file:
            pickle.dump(self.rules, file)
        print(f"Regras salvas em: {filepath}")


# Exemplo de uso
if __name__ == "__main__":
    # Substitui o contexto HTTPS padrão por um contexto não verificado, permitindo conexões HTTPS sem verificar certificados SSL.
    ssl._create_default_https_context = ssl._create_unverified_context

    # Obtém o valor da variável de ambiente chamada 'DATASET' e o armazena na variável DATA.
    DATA = os.environ.get("DATASET")

    # Lê um arquivo CSV especificado no caminho armazenado em DATA.
    data = pd.read_csv(DATA, usecols=[6, 7])

    # Agrupa os dados no DataFrame pelo valor único da coluna 'pid'.Para cada grupo, agrega os valores da coluna 'track_name' em uma lista.
    transactions = data.groupby("pid")["track_name"].apply(list).tolist()

    # Inicializando o gerador de regras
    generator = PlaylistRulesGenerator(min_sup_ratio=0.05, min_conf=0.15)

    # Gerando regras
    frequent_itemsets, rules = generator.generate_rules(transactions)

    # Salvando regras
    generator.save_rules("./program/rules.pkl")
