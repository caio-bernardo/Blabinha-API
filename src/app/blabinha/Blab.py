import random
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

stat = 0

# ******** OBSERVAÇÂO ***********
# A lista chat['varial'] é utilizada para trocar informações entre a interface e o GPT
# Presta atenção o que cada posição representa
# [0] -> Status | [1] -> Fala Usuario Atual | [2] -> Fala GPT Atual  | [3] -> Quantidade de Bônus rodados | [4] -> Nome da pessoa | [5] -> Nome da Pasta Log


client = OpenAI(
    # api_key defaults to os.environ.get("openai_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
)


class BlabGPT:

    def __init__(
        self,
        modelo: str,
        dialogRepository: dialogRepository,
        userName: str,
        chatName: str,
    ):
        self.modelo = modelo
        self.dialogRepository = dialogRepository
        self.userName = userName
        self.chatName = chatName

    def printVerificador(self, tipoVerificador, caso):
        print("\n-------- Verificador: " + tipoVerificador + " -------- ")
        print("\n ##### \n" + caso + " \n #####")

    def printSecao(self, variaveis):
        print("\n-------- " + str(variaveis[0]) + " -------- ")

    # TODO: modify this function
    # Formata a resposta do gpt, envia para criação de logs e retorna a resposta formatada
    def enviaResultados(self, respostas, variaveis) -> str:

        # Inicio as duas variaveis
        falaGPT_total = ""
        tokens = 0
        # lista = []
        # Recebo as respostas do GPT e formato os valores
        for r in respostas:
            falaGPT = r.choices[0].message.content
            falaGPT = falaGPT.replace(".", ".\n")
            falaGPT_total = falaGPT_total + "||" + falaGPT
            tokens = tokens + r.usage.total_tokens

        # lista.append(falaGPT_total)
        variaveis[7] += tokens
        # Retorno a resposta do GPT formatada
        return falaGPT_total

    # -------------------------------------------------------------------------------------------------
    # Verificadores da PARTE 1

    # Verifica se o nome da pessoa foi dito
    def verificaNome(self, variaveis):
        print(variaveis[1])
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você está verificando se o usuário mencionou seu nome. Responda TRUE se o usuário mencionou seu nome ou como deseja ser chamado, e FALSE caso contrário.",
                },
                {
                    "role": "system",
                    "content": "Exemplos: User:'Teodoro' asssistant: 'TRUE', User:'Não quero' asssistant:'FALSE', User:'Me chamo Pedro' asssistant:'TRUE', User:'Adoro poneis' assistant: 'FALSE'"
                    + " User:'Bibi' assistant:'TRUE', User:'Me chame de Gustavo' asssistant:'TRUE', User:'Que legal você ser um robô' assistant: 'FALSE',  User:'Meu nome é  Claudio' asssistant:'TRUE', User:'Pode me chamar de Teodoro' asssistant:'TRUE', User:'Adoro nomes' assistant: 'FALSE'",
                },
                {"role": "user", "content": variaveis[1]},
            ],
        )

        if response.choices[0].message.content.upper().__contains__("FALSE"):
            self.printVerificador("Falou nome", " A pessoa NÃO falou o nome!")
            if variaveis[0] != 100:
                response = client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "assistant", "content": variaveis[2]},
                        {"role": "user", "content": variaveis[1]},
                        {
                            "role": "system",
                            "content": "Responda explicando que não entedeu como a pessoa se chama e então diga que ela precisa explicar como chama-la.  Use no maximo 100 palavras",
                        },
                    ],
                )

                variaveis[2] = self.enviaResultados([response], variaveis)
                return False

        else:
            self.printVerificador("Falou nome", "A pessoa falou o nome!")
            return True

    # Verifica se a pessoa pediu para repetir
    def verificaRepete(self, variaveis):

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                # Responda, Sim, se a pessoa tiver
                {
                    "role": "system",
                    "content": "Responda TRUE se o usuario pediu para repetir, caso contrario, responda FALSE",
                },
            ],
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador(
                "Repete Fala",
                "A pessoa pediu para repetir ou não entendeu o que foi dito!",
            )
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": variaveis[2]},
                    {
                        "role": "system",
                        "content": "Explique que vai repetir o que tinha dito. "
                        + "Termine reformulando a frase acima sem perder o significado",
                    },
                ],
            )
            falaGPT = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            return True

        else:
            self.printVerificador(
                "Repete Fala",
                "A pessoa não pediu para repetir e entendeu o que foi dito!",
            )
            return False

    # Verifica se a pessoa terminou o desafio
    def verificaDesafio(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa tiver aceito o desafio e FALSE se tiver negado ",
                },
                {
                    "role": "system",
                    "content": "Exemplos: User:'Aceito o desafio' asssistant: 'TRUE', User:'Não quero' asssistant:'FALSE', User:'Topo participar' asssistant:'TRUE', User:'Não topo' assistant: 'FALSE'",
                },
            ],
        )

        falaGPT = response.choices[0].message.content
        self.printVerificador(
            "Verifica Desafio", "verifica Desafio saida :" + str(falaGPT)
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            return True
        return False

    # Verifica se a pessoa entendeu as regras
    def verificaRegras(self, variaveis):

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                # Responda, Sim, se a pessoa tiver
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa afirmar ou dizer que entendeu e FALSE ela negar ou dizer que não entendeu",
                },
            ],
        )

        if response.choices[0].message.content.upper().__contains__("FALSE"):
            self.printVerificador("Verifica Regras", "A pessoa não entendeu as regras!")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Diga que vai repetir e termine reformulando a frase abaixo mantendo o mesmo significado e para parecer que está falando com uma criança",
                    },
                    {
                        "role": "user",
                        "content": "'As regras do desafio são as seguintes: Primeiro é preciso fazer perguntas para mim (Blabinha), essas perguntas tem que que ser sobre a o assunto "
                        + "Amazônia azul. Quanto mais você manter no assunto mais pontos vai ganhar. Caso não saiba sobre o que falar pode pedir dica de algum assunto."
                        + "Além disso você pode pedir para terminar e sair a hora que quiser'",
                    },
                ],
            )
            variaveis[2] = self.enviaResultados([response], variaveis)
            return False
        else:
            self.printVerificador(
                "Verifica Regras", "A pessoa disse que entendeu as regras!"
            )
            return True

    def casoTeste(self, variaveis) -> bool:
        """
        Caso criado para teste
        Vai para função de teste se escrito "jaguatirica"
        """
        if variaveis[1] == "jaguatirica":
            variaveis[0] == 300
            return True
        return False

    # -------------------------------------------------------------------------------------------------
    # Verificadores da PARTE 2

    # Verifica se a pessoa pediu dica ou não
    def verificaDica(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                # Responda, Sim, se a pessoa tiver
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa pediu dica e FALSE se não pediu",
                },
                {"role": "user", "content": variaveis[1]},
            ],
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Dica", "A pessoa pediu alguma dica!")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Amazônia Azul é a região que compreende a superfície do mar, águas sobrejacentes ao leito do mar, solo e subsolo marinhos contidos na extensão atlântica que se projeta a partir do litoral até o limite exterior da Plataforma Continental brasileira",
                    },
                    {
                        "role": "system",
                        "content": "Primeiro diga que vai dar dica de assuntos sobre a Amazônia Azul e termine enumerando 4 possiveis assuntos que estejam relacionados a Amazônia Azul.",
                    },
                ],
            )
            falaGPT = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            return True

        else:
            self.printVerificador("Verifica Dica", "A pessoa não pediu nenhuma dica")
            return False

    # Verifica se a pessoa pediu para terminar
    def verificaTerminar(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                # Responda, Sim, se a pessoa tiver
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa pediu para terminar ou acabar e FALSE se não pediu",
                },
                {"role": "user", "content": variaveis[1]},
            ],
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Termino", "A pessoa pediu para terminar!")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {
                        "role": "system",
                        "content": "Pergunte se a pessoa realmente quer terminar. Diga que falta pouco para ela concluir e criar o herói",
                    },
                    {"role": "user", "content": variaveis[1]},
                ],
            )
            falaGPT = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 50
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    def verificaTerminar2(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                # Responda, Sim, se a pessoa tiver
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa(user) pediu para terminar ou acabar e FALSE se não pediu",
                },
            ],
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Termino2", "A pessoa pediu para terminar!")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {
                        "role": "system",
                        "content": "Pergunte se a pessoa realmente quer terminar. Diga que falta pouco para ela concluir e criar o herói",
                    },
                    {"role": "user", "content": variaveis[1]},
                ],
            )
            falaGPT = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 10
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    def verificaParte03(self, variaveis):
        frase = str.lower(variaveis[1])
        possibilidades = ["criar heroi", "criar héroi", "parte 3", "parte 03"]

        if frase in possibilidades:
            response1 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                    },
                    {
                        "role": "system",
                        "content": "Pergunte se a pessoa(criança) realmente quer ir para parte da criação de herói. Termine dizendo que quanto mais ela interagir mais forte o herói será.",
                    },
                ],
            )
            falaGPT = self.enviaResultados([response1], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 70
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    # Verifica se a pessoa falou sobre o contexto da amazônia Azul
    def verificaContexto(self, variaveis):
        contexto = (
            "Amazônia Azul é a região que compreende a superfície do mar, águas sobrejacentes ao leito do mar, solo e subsolo marinhos contidos na extensão atlântica que se projeta a partir do litoral até o limite exterior da Plataforma Continental brasileira."
            "Podemos resumir como tudo que envolve o Mar Brasileiro como animais, locais, navios,etc"
        )

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": " Responda TRUE se o user tiver feito uma pergunta dentro do contexto da Amazônia Azul. Para decidir se uma pergunta está dentro do contexto da Amazônia azul existem 2 possibilidades:"
                    + "1 - É uma pergunta sobre o Brasil e sobre o mar, ou seja peixes, ilhas, barcos, o propio mar, etc. 2 - É uma pergunta diretamente sobre a Amazônia Azul, ou seja tem Amazônia Azul na pergunta. Responda FALSE se for sobre outro contexto",
                },
            ],
        )

        if response.choices[0].message.content.upper().__contains__("FALSE"):
            self.printVerificador("Verifica Contexto", "NÃO está dentro do contexto")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Não responda o User, explique para ele que o assunto que ele falou não está relacionado com a Amazônia azul. Use no maximo 30 palavras",
                    },
                ],
            )
            response1 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": contexto},
                    {
                        "role": "system",
                        "content": "Explique que o user deve falar sobre Amazônia Azul e de 4 exemplos de assuntos que ele pode fala que sejam sobre a Amazônia Azul. Use no máximo 150 palavras",
                    },
                ],
            )
            respostas = [response, response1]
            falaGPT = self.enviaResultados(respostas, variaveis)
            falaRotativa = self.secao225(variaveis)
            variaveis[2] = falaGPT + falaRotativa

            return False

        else:
            self.printVerificador("Verifica Contexto", "Falou sobre Amazônia Azul")
            return True

    # Verifica se a pessoa falou alguma das palavras chaves
    def verificaBonus(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Você é uma analista de textos, e precisa ver se o texto fala de alguma forma sobre 'Governo'. Retorne como saida TRUE se for dito e FALSE se não for",
                },
            ],
        )

        falaGPT = response.choices[0].message.content

        if (falaGPT.upper()).__contains__("FALSE"):
            self.printVerificador("Verifica Bonus", "Caiu no caso Bonus")
            return False

        else:
            self.printVerificador("Verifica Bonus", "Não caiu no caso Bonus")
            return True

    def repetiraCriação(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Responda TRUE se a pessoa quiser ir para criação e FALSE se não quiser",
                },
            ],
        )
        falaGPT = response.choices[0].message.content

        if (falaGPT.upper()).__contains__("FALSE"):
            self.printVerificador("Verifica Bonus", "Caiu no caso Bonus")
            return False

        else:
            self.printVerificador("Verifica Bonus", "Não caiu no caso Bonus")
            return True

    def secao100(self, variaveis):

        if self.verificaNome(variaveis) is True:
            print("caiu aqui")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Seu objetivo é falar sobre a Amazônia Azul. Evite gerar perguntas. Use no máximo 100 palavras",
                    },
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Siga somente os passos para gerar o texto: Passo 1 - Reaja ao que a pessoa falou  Passo 2 - Exlique o que você é"
                        + "Passo 3 - Por ultimo pergunte se pessoa já ouviu falar da Amazônia Azul.",
                    },
                ],
            )
            respostas = [response]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = 120
            return variaveis

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Seu objetivo é falar sobre a Amazônia Azul. Evite gerar perguntas. Use no máximo 100 palavras",
                },
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Siga somente os passos para gerar o texto: Passo 1 - Reaja ao que a pessoa falou  Passo 2 - Exlique o que você é"
                    + "Passo 3 - Por ultimo pergunte como pode chamar a pessoa.",
                },
            ],
        )
        respostas = [response]
        variaveis[2] = self.enviaResultados(respostas, variaveis)
        variaveis[0] = 110
        return variaveis

    def secao110(self, variaveis):
        if variaveis[5] < 2:
            if self.verificaNome(variaveis) is False:
                variaveis[5] = variaveis[5] + 1
                return variaveis
        else:
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança."
                        + "Evite gerar perguntas. Use no máximo 100 palavras.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que já que ela não quer falar o nome vamos seguir em frente e por ultimo pergunte se ela já ouviu fala na Amazônia Azul",
                    },
                ],
            )
            respostas = [response]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = 120
            variaveis[5] = 0
            return variaveis

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança."
                    + "Evite gerar perguntas. Use no máximo 100 palavras.",
                },
                {
                    "role": "system",
                    "content": "Para responder primeiro demonstre contentamento em conhecer a pessoa e por ultimo pergunte se ela já ouviu fala sobre a Amazônia Azul",
                },
            ],
        )
        respostas = [response]
        variaveis[2] = self.enviaResultados(respostas, variaveis)
        variaveis[0] = 120
        variaveis[5] = 0
        return variaveis

    def secao120(self, variaveis):

        if self.verificaRepete(variaveis) is True:
            return variaveis

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 150 palavras.",
                },
                {
                    "role": "system",
                    "content": "Siga somente os passos para gerar o texto:"
                    + "Passo 1- Se a pessoa já souber sobre amazônia azul parabenize ela, se não diga algo reconfortante."
                    + "Passo 2- Explique brevemente que o desafio consiste em criar um super-herói e para isso vai ser"
                    + " preciso aprender sobre a amazônia azul"
                    + "Passo 3 - CONVIDE ela para participar do desafio",
                },
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
            ],
        )
        respostas = [response]
        variaveis[2] = self.enviaResultados(respostas, variaveis)
        variaveis[0] = 130
        variaveis[5] = 0
        return variaveis

    def secao130(self, variaveis):

        if self.verificaRepete(variaveis) is True:
            return variaveis

        if self.verificaDesafio(variaveis) is False:

            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Pergunte se realmente a pessoa não está querendo participar do desafio",
                    },
                ],
            )

            respostas = [response]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = 140
            variaveis[5] = 0
            return variaveis

        else:
            response0 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Evite gerar perguntas. Explique o que é o desafio refazendo a frase abaixo e mantendo o mesmo significado",
                    },
                    {
                        "role": "system",
                        "content": "A criança fazer perguntas sobre a Amazônia Azul para você (Blabinha) de forma a criar um héroi. Quanto mais perguntas forem feitas mais forte o héroi será.",
                    },
                ],
            )
            response1 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "assistant",
                        "content": response0.choices[0].message.content,
                    },
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Evite gerar perguntas. Complemente a explicação do desafio refazendo a frase abaixo  e mantendo o mesmo significado",
                    },
                    {
                        "role": "system",
                        "content": "As regras do desafio são as seguintes: Primeiro explique que acontecem no máximo 7 turnos. Somente perguntas que a Blabinha entender como Amazônia Azul contam como turnos. Você (criança) pode pedir dicas sobre"
                        + "possiveis assuntos da Amazônia Azul. Além disso pode pedir para terminar, ou seja acabar o jogo. Ou pedir para criar o héroi em algum momento da interação.Termine dizendo que esses três ultimos casos não contam como turno",
                    },
                ],
            )
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "assistant",
                        "content": response1.choices[0].message.content,
                    },
                    {
                        "role": "system",
                        "content": "Termine perguntando se a pessoa entendeu as regras. Use no maximo 40 palavras",
                    },
                ],
            )

            respostas = [response1, response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = 205
            variaveis[5] = 0
            return variaveis

    def secao140(self, variaveis):

        result = self.verificaDesafio(variaveis)

        if result is False and variaveis[0] < 141:
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Tente convencer a ela não terminar e participar do desafio",
                    },
                ],
            )
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = variaveis[0] + 1
            return variaveis

        if result is False and variaveis[0] == 141:
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Diga que tudo bem que ela não queira participar do desafio. Termine dizendo que esse chat vai ser encerrado e se quiser falar denovo tera de abrir um novo chat",
                    },
                ],
            )
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = variaveis[0] + 1
            return variaveis

        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Refaça a frase abaixo mantendo o mesmo significado e para parecer que está falando com uma criança",
                },
                {
                    "role": "user",
                    "content": "As regras do desafio são as seguintes: Primeiro é preciso fazer perguntas para mim (Blabinha), essas perguntas tem que que ser sobre a o assunto "
                    + " Amazônia azul. Quanto mais você manter no assunto mais pontos vai ganhar. Caso não saiba sobre o que falar pode pedir dica de algum assunto."
                    + "Além disso você pode pedir para terminar e sair a hora que quiser",
                },
            ],
        )
        response2 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Pergunte se a pessoa entendeu as regras. Use no maximo 40 palavras",
                }
            ],
        )

        respostas = [response1, response2]
        variaveis[2] = self.enviaResultados(respostas, variaveis)
        variaveis[0] = 205
        return variaveis

    def secao205(self, variaveis):

        if self.verificaRegras(variaveis) is False:
            return variaveis

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 50 palavras.",
                },
                {
                    "role": "system",
                    "content": "Explique que agora a pessoa precisa fazer perguntas sobre Amazônia Azul e que você vai responde-las",
                },
            ],
        )

        variaveis[2] = self.enviaResultados([response], variaveis)
        variaveis[0] = 210
        return variaveis

    def secao210(self, variaveis):
        quests = [212, 214, 216]

        if self.verificaParte03(variaveis) is True:
            return variaveis

        if self.verificaTerminar(variaveis) is True:
            return variaveis

        if self.verificaDica(variaveis) is True:
            return variaveis

        if self.verificaContexto(variaveis) is False:
            return variaveis

        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança use um tom infantil. Use no máximo 150 palavras.",
                },
                {
                    "role": "system",
                    "content": "Amazônia Azul é a região que compreende a superfície do mar, águas sobrejacentes ao leito do mar, solo e subsolo marinhos contidos na extensão atlântica que se projeta a partir do litoral até o limite exterior da Plataforma Continental brasileira."
                    "Podemos resumir como tudo que envolve o Mar Brasileiro, fauna, flora e microorganismos",
                },
                {
                    "role": "system",
                    "content": "Sabendo disso tudo responda a pergunta que foi feita",
                },
            ],
        )

        if variaveis[0] in quests:
            response1 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    },
                    {
                        "role": "system",
                        "content": "Explique que vai fazer agora um questão sobre o assunto tratado. Use no máximo 50 palavras",
                    },
                ],
            )
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    },
                    {
                        "role": "system",
                        "content": "Dado o assunto tratado gere uma questão contendo 4 alternativas e uma só resposta correta enumere elas de 1) a 4). Fale somente a questão e as alternativas, não passe a resposta.",
                    },
                ],
            )
            resposta = [response, response1, response2]
            variaveis[2] = self.enviaResultados(resposta, variaveis)
            variaveis[0] = variaveis[0] + 21
            return variaveis

        if not (self.verificaBonus(variaveis)):

            if variaveis[3] < 1:
                response2 = client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "user", "content": variaveis[1]},
                        {
                            "role": "assistant",
                            "content": response.choices[0].message.content,
                        },
                        {
                            "role": "system",
                            "content": "Demonstre animação e  diga que a pessoa caiu em um bonus! Pergunte a ela que ferramenta o super-heroi vai usar. Dado o assunto tratado dê 4 possibilidades"
                            "de ferramentas que o heroi pode usar para proteger o mar do Brasil. Enumere elas de 1) a 4) como se fosse uma pergunta com alternativas. Use no maximo 120 palavras ",
                        },
                    ],
                )
                resposta = [response, response2]
                variaveis[0] = variaveis[0] + 31
                variaveis[2] = self.enviaResultados(resposta, variaveis)
                variaveis[3] = variaveis[3] + 1
                return variaveis

        resposta = [response]

        falaGPT = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)

        variaveis[0] = variaveis[0] + 1
        variaveis[2] = falaGPT + falaRotativa

        return variaveis

    def secao225(self, variaveis):
        print("\n--------  225  -------- ")
        alea = random.randint(1, 4)
        if alea == 1:
            print("\n--------  caso1  -------- ")

            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no maximo 30 palavras.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa pode fazer mais perguntas ou pode pedir para terminar",
                    },
                ],
            )
        elif alea == 2:
            print("\n--------  caso2  -------- ")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no maximo 30 palavras.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa pode fazer mais perguntas e também caso não saiba um assunto pode pedir dicas",
                    },
                ],
            )
        elif alea == 3:
            print("\n--------  caso3  -------- ")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no maximo 30 palavras.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa pode fazer mais perguntas mas não deve se esquecer que tem que falar sobre Amazônia Azul",
                    },
                ],
            )
        else:
            print("\n--------  caso4  -------- ")
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no maximo 30 palavras.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa pode fazer mais perguntas",
                    },
                ],
            )

        resposta = [response]

        falaGPT = self.enviaResultados(resposta, variaveis)

        return falaGPT

    def secao230(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Verifique se a resposta está certa. Parabenize se estiver correta e se estiver errada explique o que está errado e qual seria a correta. Use no máximo 50 palavras",
                },
            ],
        )
        resposta = [response]
        variaveis[0] = variaveis[0] - 20
        falaGPT = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis[2] = falaGPT + falaRotativa
        return variaveis

    def secao240(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Usando no maximo 50 palavras de uma opnião sobre a escolha da pessoa.",
                },
            ],
        )
        resposta = [response]
        falaGPT = self.enviaResultados(resposta, variaveis)
        variaveis[0] = variaveis[0] - 30
        falaRotativa = self.secao225(variaveis)
        variaveis[2] = falaGPT + falaRotativa
        return variaveis

    def secao260(self, variaveis):
        def retornaValor(status):

            if status >= 260:
                estado = status - 260
            if status >= 270:
                estado = status - 270
            if status >= 280:
                estado = status - 280

            estado = estado + 210
            return estado

        result = self.verificaTerminar2(variaveis)

        if result is True and variaveis[0] < 270:
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 150 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Tente convencer a ela não terminar e continuar no desafio",
                    },
                ],
            )
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = variaveis[0] + 10
            return variaveis

        elif result is True and variaveis[0] >= 270:
            response2 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 150 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Diga que tudo bem que ela não queira participar do desafio. Termine dizendo que esse chat vai ser encerrado e se quiser falar denovo tera de abrir um novo chat",
                    },
                ],
            )
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)
            variaveis[0] = 295
            return variaveis
        else:
            response1 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                    },
                    {"role": "assistant", "content": variaveis[2]},
                    {"role": "user", "content": variaveis[1]},
                    {
                        "role": "system",
                        "content": "Demonstre que está feliz pela pessoa não ter deistido e diga que ela pode continuar",
                    },
                ],
            )

            respostas = [response1]
            falaGPT = self.enviaResultados(respostas, variaveis)
            falaRotativa = self.secao225(variaveis)
            variaveis[2] = falaGPT + falaRotativa
            variaveis[0] = retornaValor(variaveis[0])
            return variaveis

    def secao280(self, variaveis):
        response = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "assistant", "content": variaveis[2]},
                {"role": "user", "content": variaveis[1]},
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Verifique se a pessoa realmente quer seguir para criação do héroi. Responda TRUE se sim e FALSE se não.",
                },
            ],
        )

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            return self.secao300(variaveis)

        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança. Use no máximo 100 palavras",
                },
                {
                    "role": "system",
                    "content": "Demonstre que está feliz pela pessoa querer jogar mais e diga que ela pode continuar",
                },
            ],
        )

        respostas = [response1]
        falaGPT = self.enviaResultados(respostas, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis[2] = falaGPT + falaRotativa
        variaveis[0] = variaveis[0] - 70
        print(variaveis[0])
        return variaveis

    def secao300(self, variaveis):

        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Diga que agora para criar o héroi a pessoa(criança) precisa ter paciência pois você(blabinha) "
                    + "precisa ler toda conversa com ajuda de um script e então avaliar. Diga também que a pessoa(criança) só pode escrever depois que a Blabinha falar algo. Termine dizendo que para começar basta a pessoa escrever qualquer coisa",
                },
            ],
        )
        falaGPT = self.enviaResultados([response1], variaveis)
        variaveis[2] = falaGPT
        variaveis[0] = 310
        return variaveis

    def secao305(self, variaveis):

        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Diga que a pessoa conversou tanto que chegou no final e que agora vamos para criação do herói. Para criar o héroi a pessoa(criança) precisa ter paciência pois você(blabinha) "
                    + "precisa ler toda conversa com ajuda de um script e então avaliar. Diga também que a pessoa(criança) só pode escrever depois que a Blabinha falar algo. Termine dizendo que para começar basta a pessoa escrever qualquer coisa",
                },
            ],
        )
        falaGPT = self.enviaResultados([response1], variaveis)
        variaveis[2] = falaGPT
        variaveis[0] = 310
        return variaveis

    def escolheQuestões(self, tamanho):
        """
        Retorna onde ir conforme a quantidade de questões respondidass
        :param int tamanho: tamanho das questões
        :return: valor da secao
        :rtype: int
        """
        if tamanho > 2:
            return 324
        if tamanho > 1:
            return 323
        return 322

    def get_highest_past_turn(self, result: list) -> int:
        highest = 0
        for i in result:
            if i[2] > highest:
                highest = i[2]
        if highest >= 216:
            return 4
        if highest >= 215:
            return 3
        if highest >= 213:
            return 2
        if highest >= 211:
            return 1
        return 0

    def get_question(self, result: list) -> int:
        quests = [212, 214, 216]
        total = 0
        for r in result:
            if r[2] in quests:
                total += 1
        return total

    def get_bonus(self, result: list) -> str | None:
        for r in result:
            if 250 > r[2] > 240:
                response = client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "user", "content": r[0]},
                        {"role": "assistant", "content": r[1]},
                        {
                            "role": "system",
                            "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                        },
                        {
                            "role": "system",
                            "content": "Verifique qual ferramenta a pessoa escolheu. E retorne somente o qual é a ferramenta. Exemplo de saida: 'Tridente Mágico', 'Escudo protetor'",
                        },
                    ],
                )
                return response.choices[0].message.content
        return None

    def geraTopicos(self, results: list) -> list:

        topicos = ["Meio Ambiente", "Governança", "Riquezas"]

        lista = []
        contagem = []

        for t in results:
            for x in topicos:
                response = client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "user", "content": t[0]},
                        {"role": "assistant", "content": t[1]},
                        {
                            "role": "system",
                            "content": "Leia a conversa e veja se ela está relacionada ao tópico "
                            + x
                            + "Para gerar a saida retorne TRUE se estiver relacionado e FALSE se não tiver",
                        },
                    ],
                )
                if response.choices[0].message.content == "TRUE":
                    lista.append(x)

        for x in topicos:
            contagem.append(str(lista.count(x)) + "vezes do tópico:" + str(x))

        if len(lista) >= 14:
            contagem.append(4)
        elif len(lista) >= 10:
            contagem.append(3)
        elif len(lista) >= 7:
            contagem.append(2)
        else:
            contagem.append(1)

        return contagem

    def secao310(self, variaveis):

        dialogs = self.dialogRepository.get_part2_chats_dialog(
            self.userName, self.chatName
        )
        assert dialogs is not None

        topicos = self.geraTopicos(dialogs)

        self.dialogRepository.increment_stars(self.userName, self.chatName, topicos[3])

        estrelas = self.get_highest_past_turn(dialogs)

        self.dialogRepository.increment_stars(self.userName, self.chatName, estrelas)

        qQuestoes = self.get_question(dialogs)

        bonus = self.get_bonus(dialogs)

        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Explique que agora você vai começar a dar a pontuação do jogo."
                    + "Depois, diga que analisando o quanto ela interagiu ela ganhou: "
                    + str(estrelas)
                    + "estrelas de um total de quatro"
                    + "Termine analisando a quantidade que a criança conseguiu",
                },
            ],
        )

        response2 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Siga os passos a seguir para gerar a saida:"
                    + "1 - Explique que agora você vai fazer uma analise de topicos sobre toda conversa. 2 - Diga que ela falou"
                    + topicos[0]
                    + " e "
                    + topicos[1]
                    + " e "
                    + topicos[2]
                    + "Termine falando que ela conseguiu "
                    + str(topicos[3])
                    + "estrelas por causa disso de um total de 4",
                },
            ],
        )

        if not bonus:
            response3 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa não conseguiu chamar nenhum bônus e por isso não ganhou nenhuma estrela!",
                    },
                ],
            )
            self.dialogRepository.increment_heroFeature(
                self.userName, self.chatName, "Nada"
            )

        else:
            response3 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                    },
                    {
                        "role": "system",
                        "content": "Diga que a pessoa ganhou achou um bônus e por isso ganhou duas estrelas! Termine dizendo que a ferramenta :"
                        + bonus
                        + "vai ser usada pelo super-herói.",
                    },
                ],
            )
            self.dialogRepository.increment_stars(self.userName, self.chatName, 2)
            self.dialogRepository.increment_heroFeature(
                self.userName, self.chatName, bonus
            )

        if qQuestoes >= 1:
            response4 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                    },
                    {
                        "role": "system",
                        "content": "Siga os passos a seguir para gerar a saida:"
                        + "1 - Diga que a pessoa respondeu  "
                        + str(qQuestoes)
                        + " perguntas de um total de 3 e que por isso ela vai poder escolher "
                        + str(qQuestoes + 1)
                        + " atributos do herói."
                        + "2 - Termine dizendo que o primeiro atributo é a roupa do super herói, então pergunte como ela quer que seja a roupa do herói",
                    },
                ],
            )
            resposta = [response1, response2, response3, response4]
            variaveis[2] = self.enviaResultados(resposta, variaveis)
            variaveis[0] = self.escolheQuestões(qQuestoes)
        else:
            response4 = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                    },
                    {
                        "role": "system",
                        "content": "Siga os passos a seguir para gerar a saida:"
                        + "1 - Diga que como a pessoa não respondeu corretamente nenhuma pergunta. E por isso só podera escolher uma caracteristica do herói"
                        + "2 - Diga para ela não ficar triste pois mesmo não acertando podera escolher a cor da roupa do herói. "
                        + "3 - Terminando perguntado qual cor de roupa ela quer para seu super herói?",
                    },
                ],
            )
            resposta = [response1, response2, response3, response4]
            variaveis[2] = self.enviaResultados(resposta, variaveis)
            variaveis[0] = 352
        return variaveis

    def secao320(self, variaveis):
        self.dialogRepository.increment_heroFeature(
            self.userName, self.chatName, variaveis[1]
        )
        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Diga que o segundo atributo é a capa, então pergunte como ela quer que seja a capa do herói",
                },
            ],
        )
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta, variaveis)
        if variaveis[0] > 322:
            variaveis[0] = variaveis[0] + 10
        else:
            variaveis[0] = 350
        return variaveis

    def secao330(self, variaveis):
        self.dialogRepository.increment_heroFeature(
            self.userName, self.chatName, variaveis[1]
        )
        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Diga que o terceiro atributo é o companheiro de exploração, então pergunte qual companheiro o herói vai ter?",
                },
            ],
        )
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta, variaveis)
        if variaveis[0] > 333:
            variaveis[0] = variaveis[0] + 10
        else:
            variaveis[0] = 350
        return variaveis

    def secao340(self, variaveis):
        self.dialogRepository.increment_heroFeature(
            self.userName, self.chatName, variaveis[1]
        )
        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": "Diga que o quarto atributo é a casa do herói, então pergunte como será a casa do herói?",
                },
            ],
        )
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta, variaveis)
        variaveis[0] = 350
        return variaveis

    def getHeroFeature(self) -> str:
        feature = (
            self.dialogRepository.get_heroFeature(self.userName, self.chatName) or ""
        )
        lista = feature.split("//")
        tamanho = len(lista)
        frase_final = ""
        if tamanho >= 5:
            frase_final = "O herói tem uma casa: " + lista[4]
        if tamanho >= 4:
            frase_final = frase_final + ". O herói tem como companheiro um :" + lista[3]
        if tamanho >= 3:
            frase_final = (
                frase_final
                + ". O herói tem uma capa com as seguintes características:"
                + lista[2]
            )
        if tamanho >= 2:
            frase_final = (
                frase_final
                + ". A roupa do herói tem as seguintes características :"
                + lista[1]
            )
        return frase_final + ". O herói tem como ferramenta :" + lista[0]

    def secao350(self, variaveis):
        self.dialogRepository.increment_heroFeature(
            self.userName, self.chatName, variaveis[1]
        )
        response1 = client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um robô chamado Blabinha e está conversando com uma criança.",
                },
                {
                    "role": "system",
                    "content": " Diga que a pessoa conseguiu "
                    + str(variaveis[4])
                    + " estrelas de um total de 10."
                    + "Então reaja a quantidade de estrelas que ela ganhou. E termine dizendo que o héroi foi criado e que tem uma imagem dele.",
                },
            ],
        )

        prompt = self.getHeroFeature()

        frase = (
            "Gere um heroi que vai proteger o oceano do Brasil. Ele tem as seguintes caracteristicas:"
            + prompt
            + "A sua força está ligada com a quantidade de pontos. Ele tem"
            + str(variaveis[4])
            + "pontos de um total de 10."
        )
        imagem = client.images.generate(
            model="dall-e-3",
            prompt=frase,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta, variaveis)
        variaveis[2] = (
            variaveis[2] + "\nlink para a imagem gerada:  " + imagem.data[0].url
        )
        variaveis[0] = 371
        # TODO: Need to find a way to save the image
        # manip.saveImages(variaveis[4],variaveis[5],imagem.data[0].url)
        return variaveis
