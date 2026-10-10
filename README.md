# Sistema de Análise de Dados - Semana 05

Projeto desenvolvido como Desafio Sprint 5 da disciplina de Desenvolvimento em Python.

## Objetivo

O objetivo deste projeto é aplicar conceitos de:

- manipulação de arquivos;
- arquivos CSV;
- expressões regulares;
- validação de dados;
- tratamento de exceções;
- exceções personalizadas;
- geração de relatórios.

O programa realiza a leitura de um arquivo CSV contendo informações pessoais e verifica se os dados possuem formatos válidos.

## Estrutura do projeto

```text
python-analise-dados-semana-05/
│
├── analise_dados.py
├── dados.csv
└── README.md
```

## Arquivo de entrada

O arquivo `dados.csv` contém os seguintes campos:

- nome;
- e-mail;
- CPF;
- telefone;
- data.

Exemplo:

```csv
nome,email,cpf,telefone,data
Rafael,rafael@email.com,123.456.789-00,(98) 99999-9999,23/10/2007
Mariana,mariana@email.com,987.654.321-00,(98) 98888-7777,15/05/2000
```

O arquivo também contém exemplos propositalmente inválidos para demonstrar as validações do sistema.

## Leitura de arquivos

O arquivo CSV é aberto utilizando:

```python
with open(
    nome_arquivo,
    mode="r",
    encoding="utf-8"
) as arquivo:
```

O uso de `with open()` garante que o arquivo seja fechado automaticamente após a leitura.

O parâmetro:

```text
encoding="utf-8"
```

permite trabalhar corretamente com caracteres acentuados.

## Validação de e-mail

O e-mail é validado utilizando expressão regular.

O padrão utilizado é:

```python
r"^[\w\.-]+@[\w\.-]+\.\w+$"
```

Esse padrão verifica a presença de:

- caracteres antes do `@`;
- símbolo `@`;
- domínio;
- ponto;
- extensão.

Exemplo válido:

```text
rafael@email.com
```

Exemplo inválido:

```text
rafaelemail.com
```

## Validação de CPF

O projeto valida o formato:

```text
000.000.000-00
```

A expressão regular utilizada é:

```python
r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
```

Essa validação verifica o formato do CPF, não o cálculo dos dígitos verificadores.

## Validação de telefone

O telefone deve seguir o formato:

```text
(98) 99999-9999
```

A expressão utilizada é:

```python
r"^\(\d{2}\)\s\d{5}-\d{4}$"
```

São verificados:

- dois dígitos para DDD;
- espaço;
- cinco dígitos;
- hífen;
- quatro dígitos finais.

## Validação de data

A data deve seguir:

```text
DD/MM/AAAA
```

O formato inicial é validado através de:

```python
r"^\d{2}/\d{2}/\d{4}$"
```

Além disso, é utilizado:

```python
datetime.strptime()
```

para verificar se a data realmente existe.

Por exemplo:

```text
31/02/2024
```

possui o formato `DD/MM/AAAA`, mas não corresponde a uma data existente e é considerada inválida.

## Tratamento de exceções

O projeto utiliza:

```python
try
except
else
finally
```

### FileNotFoundError

É tratado caso o arquivo informado não exista.

Exemplo:

```python
except FileNotFoundError:
```

Isso impede que o programa encerre inesperadamente caso `dados.csv` não seja encontrado.

### KeyError

É utilizado para tratar situações em que uma coluna obrigatória não existe no arquivo CSV.

As colunas esperadas são:

```text
nome
email
cpf
telefone
data
```

### ValueError

É utilizado para tratar valores inválidos e erros relacionados à conversão ou interpretação de dados.

## Exceção personalizada

O projeto possui uma exceção personalizada:

```python
class FormatoInvalidoError(Exception):
    pass
```

Ela é utilizada para representar regras específicas do sistema, como um arquivo CSV sem cabeçalho ou um nome vazio.

Criar exceções personalizadas permite representar problemas de negócio de forma mais clara.

## Bloco else

O bloco:

```python
else:
```

é executado quando nenhuma exceção ocorre durante a leitura do arquivo.

Nesse caso, o sistema informa que o arquivo foi lido com sucesso.

## Bloco finally

O bloco:

```python
finally:
```

é executado independentemente de ocorrer ou não uma exceção.

No projeto ele informa que a tentativa de leitura foi finalizada.

## Relatório

Após a análise, o programa gera um relatório com:

- total de registros;
- quantidade de registros válidos;
- quantidade de registros inválidos;
- percentual de registros válidos;
- dados válidos;
- erros encontrados nos registros inválidos.

A saída é formatada utilizando f-strings.

Exemplo:

```python
print(
    f"Registros válidos: {total_validos}"
)
```

## Exemplo de saída

Uma execução pode produzir uma saída semelhante a:

```text
Arquivo "dados.csv" lido com sucesso.
Finalizando tentativa de leitura do arquivo.

============================================================
RELATÓRIO DE ANÁLISE DE DADOS
============================================================

Total de registros: 6
Registros válidos: 2
Registros inválidos: 4
Percentual de registros válidos: 33.33%

===== DADOS VÁLIDOS =====
Nome: Rafael | E-mail: rafael@email.com | CPF: 123.456.789-00 | Telefone: (98) 99999-9999 | Data: 23/10/2007
Nome: Mariana | E-mail: mariana@email.com | CPF: 987.654.321-00 | Telefone: (98) 98888-7777 | Data: 15/05/2000
```

Os demais registros são apresentados junto com os motivos pelos quais não passaram na validação.

## Como executar

Abra o terminal na pasta do projeto e execute:

```bash
python analise_dados.py
```

Dependendo da configuração do sistema, também pode ser utilizado:

```bash
python3 analise_dados.py
```

É importante manter:

```text
analise_dados.py
```

e:

```text
dados.csv
```

na mesma pasta.

## Autor

Rafael Tajra
