import csv
import re
from datetime import datetime


# ======================================================
# EXCEÇÃO PERSONALIZADA
# ======================================================

class FormatoInvalidoError(Exception):
    """Erro utilizado quando algum campo possui formato inválido."""
    pass


# ======================================================
# VALIDAÇÕES COM REGEX
# ======================================================

def validar_email(email):
    """
    Valida um e-mail simples.

    Exemplo válido:
    nome@email.com
    """

    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.fullmatch(
        padrao,
        email
    ) is not None


def validar_cpf(cpf):
    """
    Valida apenas o formato do CPF.

    Formato esperado:
    000.000.000-00
    """

    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"

    return re.fullmatch(
        padrao,
        cpf
    ) is not None


def validar_telefone(telefone):
    """
    Valida telefone no formato:

    (98) 99999-9999
    """

    padrao = r"^\(\d{2}\)\s\d{5}-\d{4}$"

    return re.fullmatch(
        padrao,
        telefone
    ) is not None


def validar_data(data):
    """
    Valida data no formato:

    DD/MM/AAAA

    Além do regex, verifica se a data realmente existe.
    """

    padrao = r"^\d{2}/\d{2}/\d{4}$"

    if re.fullmatch(
        padrao,
        data
    ) is None:

        return False

    try:

        datetime.strptime(
            data,
            "%d/%m/%Y"
        )

        return True

    except ValueError:

        return False


# ======================================================
# VALIDAÇÃO DE REGISTRO
# ======================================================

def validar_registro(registro):
    """
    Valida todos os campos obrigatórios de um registro.

    Retorna uma lista contendo os erros encontrados.
    """

    erros = []

    email = registro["email"].strip()
    cpf = registro["cpf"].strip()
    telefone = registro["telefone"].strip()
    data = registro["data"].strip()

    if not validar_email(email):
        erros.append(
            "E-mail inválido"
        )

    if not validar_cpf(cpf):
        erros.append(
            "CPF inválido"
        )

    if not validar_telefone(telefone):
        erros.append(
            "Telefone inválido"
        )

    if not validar_data(data):
        erros.append(
            "Data inválida"
        )

    return erros


# ======================================================
# LEITURA DO ARQUIVO CSV
# ======================================================

def ler_arquivo_csv(nome_arquivo):
    """
    Lê o arquivo CSV e separa os registros em válidos
    e inválidos.
    """

    registros_validos = []
    registros_invalidos = []

    arquivo_processado = False

    try:

        with open(
            nome_arquivo,
            mode="r",
            encoding="utf-8",
            newline=""
        ) as arquivo:

            leitor = csv.DictReader(
                arquivo
            )

            colunas_obrigatorias = {
                "nome",
                "email",
                "cpf",
                "telefone",
                "data"
            }

            if leitor.fieldnames is None:

                raise FormatoInvalidoError(
                    "O arquivo CSV não possui cabeçalho."
                )

            colunas_arquivo = set(
                leitor.fieldnames
            )

            if not colunas_obrigatorias.issubset(
                colunas_arquivo
            ):

                colunas_faltando = (
                    colunas_obrigatorias
                    - colunas_arquivo
                )

                raise KeyError(
                    f"Colunas ausentes: "
                    f"{', '.join(colunas_faltando)}"
                )

            for numero_linha, registro in enumerate(
                leitor,
                start=2
            ):

                try:

                    nome = registro["nome"].strip()

                    if nome == "":

                        raise FormatoInvalidoError(
                            "Nome não pode ficar vazio."
                        )

                    erros = validar_registro(
                        registro
                    )

                    if erros:

                        registro_analisado = {
                            "linha": numero_linha,
                            "dados": registro,
                            "erros": erros
                        }

                        registros_invalidos.append(
                            registro_analisado
                        )

                    else:

                        registros_validos.append(
                            registro
                        )

                except KeyError as erro:

                    registros_invalidos.append(
                        {
                            "linha": numero_linha,
                            "dados": registro,
                            "erros": [
                                f"Campo ausente: {erro}"
                            ]
                        }
                    )

                except ValueError as erro:

                    registros_invalidos.append(
                        {
                            "linha": numero_linha,
                            "dados": registro,
                            "erros": [
                                f"Valor inválido: {erro}"
                            ]
                        }
                    )

                except FormatoInvalidoError as erro:

                    registros_invalidos.append(
                        {
                            "linha": numero_linha,
                            "dados": registro,
                            "erros": [
                                str(erro)
                            ]
                        }
                    )

        arquivo_processado = True

    except FileNotFoundError:

        print(
            f'Erro: o arquivo "{nome_arquivo}" '
            "não foi encontrado."
        )

    except KeyError as erro:

        print(
            f"Erro de estrutura no CSV: {erro}"
        )

    except ValueError as erro:

        print(
            f"Erro de valor: {erro}"
        )

    except FormatoInvalidoError as erro:

        print(
            f"Erro de formato: {erro}"
        )

    except Exception as erro:

        print(
            f"Erro inesperado: {erro}"
        )

    else:

        print(
            f'Arquivo "{nome_arquivo}" '
            "lido com sucesso."
        )

    finally:

        print(
            "Finalizando tentativa de leitura do arquivo."
        )

    if arquivo_processado:

        return (
            registros_validos,
            registros_invalidos
        )

    return (
        [],
        []
    )


# ======================================================
# RELATÓRIO
# ======================================================

def gerar_relatorio(
    registros_validos,
    registros_invalidos
):
    """
    Exibe o relatório final da análise.
    """

    total_validos = len(
        registros_validos
    )

    total_invalidos = len(
        registros_invalidos
    )

    total_registros = (
        total_validos
        + total_invalidos
    )

    if total_registros > 0:

        percentual_validos = (
            total_validos
            / total_registros
            * 100
        )

    else:

        percentual_validos = 0


    print("\n")
    print("=" * 60)
    print("RELATÓRIO DE ANÁLISE DE DADOS")
    print("=" * 60)


    print(
        f"\nTotal de registros: "
        f"{total_registros}"
    )

    print(
        f"Registros válidos: "
        f"{total_validos}"
    )

    print(
        f"Registros inválidos: "
        f"{total_invalidos}"
    )

    print(
        f"Percentual de registros válidos: "
        f"{percentual_validos:.2f}%"
    )


    print("\n===== DADOS VÁLIDOS =====")

    if registros_validos:

        for registro in registros_validos:

            print(
                f"Nome: {registro['nome']} | "
                f"E-mail: {registro['email']} | "
                f"CPF: {registro['cpf']} | "
                f"Telefone: {registro['telefone']} | "
                f"Data: {registro['data']}"
            )

    else:

        print(
            "Nenhum registro válido encontrado."
        )


    print("\n===== DADOS INVÁLIDOS =====")

    if registros_invalidos:

        for registro in registros_invalidos:

            linha = registro["linha"]

            dados = registro["dados"]

            erros = registro["erros"]

            nome = dados.get(
                "nome",
                "Não informado"
            )

            print(
                f"\nLinha {linha} - "
                f"Nome: {nome}"
            )

            for erro in erros:

                print(
                    f"- {erro}"
                )

    else:

        print(
            "Nenhum registro inválido encontrado."
        )


    print("\n")
    print("=" * 60)
    print("FIM DO RELATÓRIO")
    print("=" * 60)


# ======================================================
# FUNÇÃO PRINCIPAL
# ======================================================

def main():
    """
    Executa todo o sistema.
    """

    nome_arquivo = "dados.csv"

    (
        registros_validos,
        registros_invalidos
    ) = ler_arquivo_csv(
        nome_arquivo
    )

    gerar_relatorio(
        registros_validos,
        registros_invalidos
    )


if __name__ == "__main__":
    main()
