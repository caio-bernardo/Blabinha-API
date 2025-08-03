import random
import importlib

from typing import TYPE_CHECKING

from openai import OpenAI
from blabinha_api.apps.dialogs.models import Dialog
from blabinha_api.apps.chats.models import Chat
from blabinha_api.apps.chats.schemas import StrategyEnum
from blabinha_api.apps.blabinha import brain as br

if TYPE_CHECKING:
    from apps.dialogs.services import DialogService

class PromptStrategy:
    def __init__(self, original_strategy):
        self.strategy = StrategyEnum(original_strategy)
        print("Estratégia selecionada: ", self.strategy.value)

    def snake_to_camel(self, snake_string: str) -> str:
        return ''.join(word.capitalize() for word in snake_string.split('_'))

    def get_strategy(self):
        try:
            self.module_name = f"blabinha_api.apps.blabinha.prompt_engineering.{self.strategy.value}"

            self.class_name = self.snake_to_camel(self.strategy.value)

            strategy_module = importlib.import_module(self.module_name)
            strategy_class = getattr(strategy_module, self.class_name)

            return strategy_class()

        except ModuleNotFoundError:
            raise ValueError(f"Estratégia '{self.strategy.value}', com module '{self.module_name}' e classe '{self.class_name}' não encontrada.")

        except AttributeError:
            raise ValueError(f"A classe correspondente à estratégia '{self.strategy.value}' não foi encontrada no módulo.")


class Variaveis:
    def __init__(
        self,
        section: int,
        input: str,
        bonus: int,
        stars: int,
        heroFeatures: list[str],
        repetition: int,
        username: str,
        emotion: int,
    ):
        self.section = section
        self.input = input
        self.answer = ""
        self.bonus = bonus
        self.stars = stars
        self.heroFeatures: list[str] = heroFeatures
        self.tokens = 0
        self.repetition = repetition
        self.username = username
        self.emotion = emotion
        self.image = ""

    def add_hero_feature(self, feature: str):
        self.heroFeatures.append(feature)

    def add_star(self, qnt: int):
        self.stars += qnt


class Blab:
    def __init__(self, api_key: str, chat: Chat, dialog_service: 'DialogService'):
        self.chat_id = chat.id
        self.modelo = chat.model.value
        self.strategy = PromptStrategy(chat.strategy).get_strategy()
        print("Estratégia selecionada:", self.strategy)

        self.client = OpenAI(api_key=api_key)

        self.dialog_service = dialog_service

        br.select_model(self.modelo)
        print(f"Modelo '{self.modelo}' selecionado.\n")
        modeloLLM = self.modelo
        print(f"Modelo LLM selecionado: {modeloLLM}")

    def get_part2_dialogs(self) -> list[Dialog]:
        return self.dialog_service.get_all_part_two(self.chat_id)

    def printVerificador(self, tipoVerificador, caso):
        print("\n-------- Verificador: " + tipoVerificador + " -------- ")
        print("\n ##### \n" + caso + " \n #####")

    def printSecao(self, variaveis: Variaveis):
        print("\n-------- " + str(variaveis.section) + " -------- ")

    # TODO: modify this function
    # Formata a resposta do gpt, envia para criação de logs e retorna a resposta formatada
    def enviaResultados(self, respostas, variaveis: Variaveis) -> str:
        # Inicio as duas variaveis
        falaLLM_total: str = ""
        tokens = 0
        # lista = []
        # Recebo as respostas do GPT e formato os valores
        for r in respostas:
            falaLLM = r.choices[0].message.content
            falaLLM = falaLLM.replace(".", ".\n")
            falaLLM_total = falaLLM_total + "||" + falaLLM
            tokens = tokens + r.usage.total_tokens

        # lista.append(falaLLM_total)
        variaveis.tokens += tokens
        # Retorno a resposta do GPT formatada
        return falaLLM_total

    # Escolhe qual sequencia de prompt vai ser usada para responder
    def escolheParte(self, variaveis: Variaveis):
        """
        Escolhe qual função chamar conforme o que está na variavel[0] -> seção
        """
        secao = variaveis.section
        resposta = variaveis

        if 100 <= secao < 200:
            if secao == 100:
                resposta = self.secao100(variaveis)
            elif secao == 110:
                resposta = self.secao110(variaveis)
            elif secao == 120:
                resposta = self.secao120(variaveis)
            elif secao == 130:
                resposta = self.secao130(variaveis)
            elif 140 <= secao <= 141:
                resposta = self.secao140(variaveis)
            elif secao == 142:
                variaveis.answer = "Este chat está encerrado pois você informou que não gostaria de continuar."
                resposta = variaveis
            else:
                variaveis.answer = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 01"
                resposta = variaveis

        elif 200 <= secao < 300:
            if secao == 205:
                resposta = self.secao205(variaveis)
            elif 210 <= secao < 218:
                resposta = self.secao210(variaveis)
            elif secao == 218:
                resposta = self.secao305(variaveis)
            elif 230 <= secao <= 240:
                resposta = self.secao230(variaveis)
            elif 240 <= secao <= 250:
                resposta = self.secao240(variaveis)
            elif 260 <= secao < 280:
                resposta = self.secao260(variaveis)
            elif 280 <= secao <= 288:
                resposta = self.secao280(variaveis)
            elif 290 <= secao < 300:
                variaveis.answer = "Este chat está encerrado pois você informou que não gostaria de continuar."
                resposta = variaveis
            else:
                variaveis.answer = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 02"
                resposta = variaveis
        elif 300 <= secao < 400:
            if 300 <= secao < 310:
                resposta = self.secao300(variaveis)
            elif 310 <= secao < 320:
                resposta = self.secao310(variaveis)
            elif 320 <= secao < 330:
                resposta = self.secao320(variaveis)
            elif 330 <= secao < 340:
                resposta = self.secao330(variaveis)
            elif 340 <= secao < 350:
                resposta = self.secao340(variaveis)
            elif 350 <= secao < 360:
                resposta = self.secao350(variaveis)
            elif 370 <= secao < 380:
                variaveis.answer = "Este chat está encerrado."
                resposta = variaveis
            else:
                variaveis.answer = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 03"
                resposta = variaveis
        else:
            variaveis.answer = (
                "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 04"
            )
            resposta = variaveis
        return resposta

    # -------------------------------------------------------------------------------------------------
    # Verificadores da PARTE 1

    # Verifica se o nome da pessoa foi dito
    def verificaNome(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_nome(variaveis.input)
        print(variaveis.input)

        messages=prompt
        response = br.call(messages)
        print(response)
     
        assert response.choices[0].message.content is not None
        if response.choices[0].message.content.upper().__contains__("FALSE"):
            self.printVerificador("Falou nome", " A pessoa NÃO falou o nome!")
            if variaveis.section != 100:
                prompt = self.strategy.nao_falou_nome(variaveis.input, variaveis.answer)
                messages = prompt
                response = br.call(messages=prompt)
                print(response)
                variaveis.answer = self.enviaResultados([response], variaveis)
                return False

        else:
            self.printVerificador("Falou nome", "A pessoa falou o nome!")
            return True

    # Após detectar que ele falou o nome:
    def extraiNome(self, variaveis: Variaveis)-> str:
        messages=[
            {
                "role": "system",
                "content": "Extraia apenas o nome ou apelido que o usuário quer usar. Seja sucinto, responda apenas o nome, sem frases adicionais.",
            },
            {"role": "user", "content": variaveis.input},
        ]
        response = br.call(messages)
        content = response.choices[0].message.content
        if content is None:
            return ""
        return content.strip()


    # Verifica se a pessoa pediu para repetir
    def verificaRepete(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_repete(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)
        
        assert response.choices[0].message.content is not None
        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador(
                "Repete Fala",
                "A pessoa pediu para repetir ou não entendeu o que foi dito!",
            )
            prompt = self.strategy.repete(variaveis.answer)
            messages = prompt
            response = br.call(messages)

            falaLLM = self.enviaResultados([response], variaveis)
            variaveis.answer = falaLLM
            return True

        else:
            self.printVerificador(
                "Repete Fala",
                "A pessoa não pediu para repetir e entendeu o que foi dito!",
            )
            return False

    # Verifica se a pessoa terminou o desafio
    def verificaDesafio(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_desafio(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)


        falaLLM = response.choices[0].message.content
        self.printVerificador(
            "Verifica Desafio", "verifica Desafio saida :" + str(falaLLM)
        )
        assert response.choices[0].message.content is not None
        if response.choices[0].message.content.upper().__contains__("TRUE"):
            return True
        return False

    # Verifica se a pessoa entendeu as regras
    def verificaRegras(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_regras(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)

        assert response.choices[0].message.content is not None
        if response.choices[0].message.content.upper().__contains__("FALSE"):
            self.printVerificador("Verifica Regras", "A pessoa não entendeu as regras!")
            prompt = self.strategy.repete_verifica_regras()
            messages = prompt
            response = br.call(messages)
            variaveis.answer = self.enviaResultados([response], variaveis)
            return False
        else:
            self.printVerificador(
                "Verifica Regras", "A pessoa disse que entendeu as regras!"
            )
            return True

    def casoTeste(self, variaveis: Variaveis) -> bool:
        """
        Caso criado para teste
        Vai para função de teste se escrito "jaguatirica"
        """
        if variaveis.input == "jaguatirica":
            variaveis.section = 300
            return True
        return False

    # -------------------------------------------------------------------------------------------------
    # Verificadores da PARTE 2

    # Verifica se a pessoa pediu dica ou não
    def verificaDica(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_dica(variaveis.input)
        messages = prompt
        response = br.call(messages)

        assert response.choices[0].message.content is not None

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Dica", "A pessoa pediu alguma dica!")
            prompt = self.strategy.pediu_dica()
            messages = prompt
            response = br.call(messages)
            falaLLM = self.enviaResultados([response], variaveis)
            variaveis.answer = falaLLM
            return True

        else:
            self.printVerificador("Verifica Dica", "A pessoa não pediu nenhuma dica")
            return False

    # Verifica se a pessoa pediu para terminar
    def verificaTerminar(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_terminar(variaveis.input)
        messages = prompt
        response = br.call(messages)

        assert response.choices[0].message.content is not None

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Termino", "A pessoa pediu para terminar!")
            prompt = self.strategy.verifica_realmente_terminar(variaveis.input)
            messages = prompt
            response = br.call(messages)
            falaLLM = self.enviaResultados([response], variaveis)
            variaveis.answer = falaLLM
            variaveis.section += 50
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    def verificaTerminar2(self, variaveis: Variaveis):
        prompt = self.strategy.verifica_terminar2(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)

        assert response.choices[0].message.content is not None

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            self.printVerificador("Verifica Termino2", "A pessoa pediu para terminar!")
            prompt = self.strategy.verifica_realmente_terminar(variaveis.input)
            messages = prompt
            response = br.call(messages)
            falaLLM = self.enviaResultados([response], variaveis)
            variaveis.answer = falaLLM
            variaveis.section += 10
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    def verificaParte03(self, variaveis: Variaveis):
        frase = str.lower(variaveis.input)
        possibilidades = ["criar heroi", "criar héroi", "parte 3", "parte 03"]

        prompt = self.strategy.verificaParte03()
        if frase in possibilidades:
            messages = prompt
            response1 = br.call(messages)
            falaLLM = self.enviaResultados([response1], variaveis)
            variaveis.answer = falaLLM
            variaveis.section += 70
            return True

        else:
            self.printVerificador(
                "Verifica Termino", "A pessoa não pediu para terminar"
            )
            return False

    # Verifica se a pessoa falou sobre o contexto da amazônia Azul
    def verificaContexto(self, variaveis):

        #tirar answer
        prompt = self.strategy.verifica_contexto(variaveis.input, variaveis.answer)

        contexto = (
            "Amazônia Azul é a região que compreende a superfície do mar, águas sobrejacentes ao leito do mar, solo e subsolo marinhos contidos na extensão atlântica que se projeta a partir do litoral até o limite exterior da Plataforma Continental brasileira."
            "Podemos resumir como tudo que envolve o Mar Brasileiro como animais, locais, navios, etc")
        
        messages=prompt
        response = br.call(messages)

        print("Resposta do verifica contexto: \n", response.choices[0].message.content.upper())

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Verifica Contexto", "Falou sobre Amazônia Azul")
            print("caiu aqui no verifica contexto**")
            return True

        else:
            self.printVerificador("Verifica Contexto", "NÃO está dentro do contexto")

            prompt = self.strategy.verifica_nao_contexto(variaveis.input)
            messages=prompt
            response = br.call(messages)

            prompt = self.strategy.verifica_nao_contexto_2(contexto)
            messages=prompt
            response1 = br.call(messages)

            respostas = [response,response1]
            falaLLM = self.enviaResultados(respostas, variaveis)    
            falaRotativa = self.secao225(variaveis)
            variaveis.answer = falaLLM + falaRotativa  

            return False

    # Verifica se a pessoa falou alguma das palavras chaves
    def verificaBonus(self, variaveis: Variaveis):
        prompt = self.strategy.verificaBonus(variaveis.input)
        messages = prompt
        response = br.call(messages)
        
        falaLLM = response.choices[0].message.content

        assert falaLLM is not None

        if "FALSE" in falaLLM.upper():
            self.printVerificador("Verifica Bonus", "Não caiu no caso Bonus")
            return False

        elif "TRUE" in falaLLM.upper():
            self.printVerificador("Verifica Bonus", "Caiu no caso Bonus")
            return True

    def repetiraCriação(self, variaveis: Variaveis):
        prompt = self.strategy.repetiraCriação(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)

        falaLLM = response.choices[0].message.content

        assert falaLLM is not None

        if "FALSE" in falaLLM.upper():
            self.printVerificador("Verifica Bonus - Heroi", "Não caiu no caso Bonus")
            return False

        else:
            self.printVerificador("Verifica Bonus - Heroi", "Caiu no caso Bonus")
            return True

    def secao100(self, variaveis: Variaveis):
        prompt = self.strategy.secao100EscutouFalar(variaveis.input)

        if self.casoTeste(variaveis) is True:
            self.secao300(variaveis)
            return variaveis

        if self.verificaNome(variaveis) is True:
            print("caiu aqui")
            messages = prompt
            response = br.call(messages)
            respostas = [response]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = 120
            variaveis.username = self.extraiNome(variaveis)
            return variaveis

        prompt = self.strategy.secao100VerificaNome(variaveis.input)
        response = br.call(messages=prompt)
        respostas = [response]
        variaveis.answer = self.enviaResultados(respostas, variaveis)
        variaveis.section = 110
        return variaveis

    def secao110(self, variaveis: Variaveis):
        if self.casoTeste(variaveis) is True:
            self.secao300(variaveis)
            return variaveis

        if variaveis.repetition < 2:
            if self.verificaNome(variaveis) is False:
                variaveis.repetition += 1
                return variaveis
            else:
                variaveis.username = self.extraiNome(variaveis)
        else:
            prompt = self.strategy.secao110NaoFalouNome(variaveis.input, variaveis.answer)
            messages=prompt
            response = br.call(messages)
            respostas = [response]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = 120
            variaveis.repetition = 0
            return variaveis

        prompt = self.strategy.secao110EscutouFalar(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)
        respostas = [response]
        variaveis.answer = self.enviaResultados(respostas, variaveis)
        variaveis.section = 120
        variaveis.repetition = 0
        return variaveis

    def secao120(self, variaveis: Variaveis):
        if self.casoTeste(variaveis) is True:
            self.secao300(variaveis)
            return variaveis

        if self.verificaRepete(variaveis) is True:
            return variaveis
        
        prompt = self.strategy.secao120(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)
        respostas = [response]
        variaveis.answer = self.enviaResultados(respostas, variaveis)
        variaveis.section = 130
        variaveis.repetition = 0
        return variaveis

    def secao130(self, variaveis: Variaveis):
        if self.verificaRepete(variaveis) is True:
            return variaveis

        if self.verificaDesafio(variaveis) is False:

            prompt = self.strategy.secao130NaoQuerParticipar(variaveis.input, variaveis.answer)
            messages=prompt
            response = br.call(messages)

            respostas = [response]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = 140
            variaveis.repetition = 0
            return variaveis

        else:
            prompt = self.strategy.secao130Instrucao()
            messages=prompt
            response0 = br.call(messages)
            prompt = self.strategy.secao130RegrasDesafio(response0.choices[0].message.content)
            messages=prompt
            response1 = br.call(messages)

            prompt = self.strategy.secao130EntendeuRegras(response1.choices[0].message.content)
            messages=prompt
            response2 = br.call(messages)

            respostas = [response1, response2]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = 205
            variaveis.repetition = 0
            return variaveis

    def secao140(self, variaveis: Variaveis):
        prompt = self.strategy.secao140ConvencerContinuar(variaveis.input, variaveis.answer)
        result = self.verificaDesafio(variaveis)

        if result is False and variaveis.section < 141:
            messages=prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = variaveis.section + 1
            return variaveis

        if result is False and variaveis.section == 141:

            prompt = self.strategy.secao140EncerrarConversa(variaveis.input, variaveis.answer)
            messages=prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section += 1
            return variaveis

        prompt = self.strategy.secao140ReformularRegrasInfantil()
        messages=prompt
        response1 = br.call(messages)
        
        prompt = self.strategy.secao140PerguntarEntendeuRegras()
        messages=prompt
        response2 = br.call(messages)

        respostas = [response1, response2]
        variaveis.answer = self.enviaResultados(respostas, variaveis)
        variaveis.section = 205
        return variaveis

    def secao205(self, variaveis: Variaveis):
        prompt = self.strategy.secao205(variaveis.input)

        if self.verificaRegras(variaveis) is False:
            return variaveis

        messages=prompt
        response = br.call(messages)

        variaveis.answer = self.enviaResultados([response], variaveis)
        variaveis.section = 210
        return variaveis

    def secao210(self, variaveis: Variaveis):
        print("variavel 0 antes", variaveis.section)
        print("variavel 3 antes", variaveis.bonus)
        quests = [212, 214, 216]

        if self.verificaParte03(variaveis) is True:
            return variaveis

        if self.verificaTerminar(variaveis) is True:
            return variaveis

        if self.verificaDica(variaveis) is True:
            return variaveis

        if self.verificaContexto(variaveis) is False:
            return variaveis

        prompt = self.strategy.secao210ResponderPergunta(variaveis.input)
        messages=prompt
        response = br.call(messages)

        prompt = self.strategy.secao210FazerQuestao(variaveis.input, response.choices[0].message.content)

        if variaveis.section in quests:
            messages=prompt
            response1 = br.call(messages)

            prompt = self.strategy.secao210QuestaoAlternativa(variaveis.input, response.choices[0].message.content)

            messages=prompt
            response2 = br.call(messages)

            resposta = [response, response1, response2]
            variaveis.answer = self.enviaResultados(resposta, variaveis)
            variaveis.section += 21
            print("variavel 0 (21)", variaveis.section)
            return variaveis

        if not (self.verificaBonus(variaveis)):
            print("caiu no bonus")

            prompt = self.strategy.secao210Bonus(variaveis.input, response.choices[0].message.content)

            if variaveis.bonus < 1:
                print("caiu aquiaa1")
                messages=prompt
                response2 = br.call(messages)

                resposta = [response, response2]
                variaveis.section += 31
                variaveis.answer = self.enviaResultados(resposta, variaveis)
                variaveis.bonus += 1
                print("variavel 0 (31)", variaveis.section)
                print("variavel 3", variaveis.bonus)
                return variaveis

        resposta = [response]

        falaLLM = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)

        variaveis.section += 1
        print("variavel 0 fora", variaveis.section)
        variaveis.answer = falaLLM + falaRotativa

        return variaveis

    def secao225(self, variaveis: Variaveis):
        print("\n--------  225  -------- ")
        alea = random.randint(1, 4)
        if alea == 1:
            print("\n--------  caso1  -------- ")

            prompt = self.strategy.secao225Caso1()
            messages=prompt
            response = br.call(messages)
        elif alea == 2:
            print("\n--------  caso2  -------- ")
            prompt = self.strategy.secao225Caso2()
            messages=prompt
            response = br.call(messages)
        elif alea == 3:
            print("\n--------  caso3  -------- ")
            prompt = self.strategy.secao225Caso3()
            messages=prompt
            response = br.call(messages)
        else:
            print("\n--------  caso4  -------- ")
            print("\n--------  caso4  -------- ")
            prompt = self.strategy.secao225Caso4()
            messages=prompt
            response = br.call(messages)
            
        resposta = [response]

        falaLLM = self.enviaResultados(resposta, variaveis)

        return falaLLM

    def secao230(self, variaveis: Variaveis):
        print("entrou aqui no 230")
        # print("variaveis[0] antes de atualizada no 230", variaveis[0])
        prompt = self.strategy.secao230(variaveis.input, variaveis.answer)
        messages=prompt
        response = br.call(messages)
        resposta = [response]
        variaveis.section -= 20
        falaLLM = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis.answer = falaLLM + falaRotativa
        return variaveis

    def secao240(self, variaveis: Variaveis):
        self.printSecao(variaveis)
        print("limite está em", variaveis.repetition)

        value = self.verificaAlternativa(variaveis)
        if variaveis.repetition < 2 and value is False:
                return variaveis
        else:
            if value is True:
                    print("entrou aqui?")
                    #já que nao quer falar uma resposta valida, vamos seguir...
                    print(f"variavel 1: {variaveis.input}\n")
                    print(f"variavel 2: {variaveis.answer}\n")
                    prompt = self.strategy.secao240_falou_alternativa(variaveis.input, variaveis.answer)
            else:
                print("entrou no else")
                prompt = self.strategy.secao240_nao_falou_alternativa_continuar(variaveis.input, variaveis.answer)
        messages=prompt
        response = br.call(messages)
        resposta = [response]
        falaLLM = self.enviaResultados(resposta, variaveis)
        variaveis.section -= 30
        falaRotativa = self.secao225(variaveis)
        variaveis.answer = falaLLM + falaRotativa
        return variaveis

    def verificaAlternativa(self, variaveis):
        prompt = self.strategy.secao240_teste_verifica_alternativas(variaveis.input, variaveis.answer)
        contexto = variaveis.answer
        print(f"variavel 1 (verificaAlternativa): {variaveis.input}\n")
        print(f"variavel 2 (verificaAlternativa): {variaveis.answer}\n")
        print("dentro de verifica Alternativa")
        print("**limite está em", variaveis.repetition)
        messages=prompt
        response = br.call(messages)
        if (response.choices[0].message.content.upper().__contains__("FALSE")):
            variaveis.repetition += 1
            prompt = self.strategy.secao240NaoFalouAlternativa(variaveis.input, contexto)
            messages=prompt
            response = br.call(messages)
            variaveis.answer = self.enviaResultados([response], variaveis)
            return False
        else:
            # se falou a alternativa correta
            return True
        

    def secao260(self, variaveis: Variaveis):
        def retornaValor(status):
            estado = 0

            if status >= 260:
                estado = status - 260
            if status >= 270:
                estado = status - 270
            if status >= 280:
                estado = status - 280

            estado = estado + 210
            return estado

        result = self.verificaTerminar2(variaveis)

        if result is True and variaveis.section < 270:
            prompt = self.strategy.secao260Convencer(variaveis.input, variaveis.answer)
            messages = prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section += 10
            return variaveis

        elif result is True and variaveis.section >= 270:
            prompt = self.strategy.secao260ChatEncerrado(variaveis.input, variaveis.answer)
            messages = prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis.answer = self.enviaResultados(respostas, variaveis)
            variaveis.section = 295
            return variaveis
        else:
            prompt = self.strategy.secao260NaoDesistiu(variaveis.input, variaveis.answer)
            messages = prompt
            response1 = br.call(messages)

            respostas = [response1]
            falaLLM = self.enviaResultados(respostas, variaveis)
            falaRotativa = self.secao225(variaveis)
            variaveis.answer = falaLLM + falaRotativa
            variaveis.section = retornaValor(variaveis.section)
            return variaveis

    def secao280(self, variaveis: Variaveis):
        prompt = self.strategy.secao280VerificaContinuar(variaveis.input, variaveis.answer)
        messages = prompt
        response = br.call(messages)

        assert response.choices[0].message.content is not None

        if response.choices[0].message.content.upper().__contains__("TRUE"):
            return self.secao300(variaveis)

        prompt = self.strategy.secao280Continuar()
        messages = prompt
        response1 = br.call(messages)

        respostas = [response1]
        falaLLM = self.enviaResultados(respostas, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis.answer = falaLLM + falaRotativa
        variaveis.section = variaveis.section - 70
        print(variaveis.section)
        return variaveis

    def secao300(self, variaveis: Variaveis):
        prompt = self.strategy.secao300()
        messages=prompt
        response1 = br.call(messages)
        falaLLM = self.enviaResultados([response1], variaveis)
        variaveis.answer = falaLLM
        variaveis.section = 310
        return variaveis

    def secao305(self, variaveis: Variaveis):
        prompt = self.strategy.secao305()
        messages=prompt
        response1 = br.call(messages)
        falaLLM = self.enviaResultados([response1], variaveis)
        variaveis.answer = falaLLM
        variaveis.section = 310
        return variaveis

    def escolheQuestões(self, tamanho: int):
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

    def get_highest_past_turn(self, result: list[Dialog]) -> int:
        highest = 0
        for i in result:
            if i.section > highest:
                highest = i.section
        if highest >= 216:
            return 4
        if highest >= 215:
            return 3
        if highest >= 213:
            return 2
        if highest >= 211:
            return 1
        return 0

    def get_question(self, result: list[Dialog]) -> int:
        quests = [212, 214, 216]
        total = 0
        for r in result:
            if r.section in quests:
                total += 1
        return total

    def get_bonus(self, result: list[Dialog]) -> str | None:
        for r in result:
            if 250 > r.section > 240:
                prompt = self.strategy.getBonusFerramenta(r.input, r.answer)
                messages=prompt
                response = br.call(messages)
                return response.choices[0].message.content
        return None

    def geraTopicos(self, results: list[Dialog]) -> list[str|int]:
        topicos = ["Meio Ambiente", "Governança", "Riquezas"]

        lista = []
        contagem: list[str|int] = []

        for t in results:
            for x in topicos:
                messages=[
                    {"role": "user", "content": t.input},
                    {"role": "assistant", "content": t.answer},
                    {
                        "role": "system",
                        "content": "Leia a conversa e veja se ela está relacionada ao tópico "
                        + x
                        + "Para gerar a saida retorne TRUE se estiver relacionado e FALSE se não tiver",
                    },
                ]
                response =  br.call(messages)
                  
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

    def secao310(self, variaveis: Variaveis):
        dialogs: list[Dialog] = self.get_part2_dialogs()

        topicos = self.geraTopicos(dialogs)

        variaveis.add_star(int(topicos[3]))

        estrelas = self.get_highest_past_turn(dialogs)

        variaveis.add_star(estrelas)

        qQuestoes = self.get_question(dialogs)

        bonus = self.get_bonus(dialogs)

        prompt = self.strategy.secao310QuantidadeEstrela(estrelas)
        messages=prompt
        response1 = br.call(messages)


        prompt = self.strategy.secao310QuantidadeTopicos(topicos)
        messages=prompt
        response2 = br.call(messages)

        if not bonus:
            prompt = self.strategy.secao310NaoConseguiuBonus()
            messages=prompt
            response3 = br.call(messages)
            variaveis.add_hero_feature("Nada")

        else:
            # bonus ou ferramenta?
            prompt = self.strategy.secao310ConseguiuBonus(bonus)
            messages=prompt
            response3 = br.call(messages)
            variaveis.add_star(2)
            variaveis.add_hero_feature(bonus)

        if qQuestoes >= 1:
            prompt = self.strategy.secao310QuantidadeQuestoes(qQuestoes)
            messages=prompt
            response4 = br.call(messages)
            resposta = [response1, response2, response3, response4]
            variaveis.answer = self.enviaResultados(resposta, variaveis)
            variaveis.section = self.escolheQuestões(qQuestoes)
        else:
            prompt = self.strategy.secao310NaoRespondeuQuestoes()
            messages=prompt
            response4 = br.call(messages)
            resposta = [response1, response2, response3, response4]
            variaveis.answer = self.enviaResultados(resposta, variaveis)
            variaveis.section = 352
        return variaveis

    def secao320(self, variaveis: Variaveis):
        variaveis.add_hero_feature(variaveis.input)
        prompt = self.strategy.secao320()
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis.answer = self.enviaResultados(resposta, variaveis)
        if variaveis.section > 322:
            variaveis.section += 10
        else:
            variaveis.section = 350
        return variaveis

    def secao330(self, variaveis: Variaveis):
        variaveis.add_hero_feature(variaveis.input)
        prompt = self.strategy.secao330()
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis.answer = self.enviaResultados(resposta, variaveis)
        if variaveis.section > 333:
            variaveis.section += 10
        else:
            variaveis.section = 350
        return variaveis

    def secao340(self, variaveis: Variaveis):
        variaveis.add_hero_feature(variaveis.input)
        prompt = self.strategy.secao340()
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis.answer = self.enviaResultados(resposta, variaveis)
        variaveis.section = 350
        return variaveis

    def getHeroFeature(self, variaveis: Variaveis) -> str:
        lista = variaveis.heroFeatures
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

    def secao350(self, variaveis: Variaveis):
        variaveis.add_hero_feature(variaveis.input)
        prompt = self.strategy.secao350(str(variaveis.stars))
        messages=prompt
        response1 = br.call(messages)

        prompt = self.getHeroFeature(variaveis)

        frase = (
            "Gere um heroi que vai proteger o oceano do Brasil. Ele tem as seguintes caracteristicas:"
            + prompt
            + "A sua força está ligada com a quantidade de pontos. Ele tem"
            + str(variaveis.stars)
            + "pontos de um total de 10."
        )
        imagem = self.client.images.generate(
            model="dall-e-3",
            prompt=frase,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        resposta = [response1]
        variaveis.answer = self.enviaResultados(resposta, variaveis)
        assert imagem.data[0].url is not None
        variaveis.answer = (
            variaveis.answer + "\nlink para a imagem gerada:  " + imagem.data[0].url
        )
        variaveis.section = 371
        # TODO: Need to find a way to save the image
        # manip.saveImages(variaveis[4],variaveis[5],imagem.data[0].url)
        variaveis.image = imagem.data[0].url
        return variaveis

    def detecta_emocao(self, variaveis: Variaveis) -> int:
        prompt = (
            "Sua tarefa é identificar a emoção predominante em uma mensagem de um modelo de linguagem. "
            "Considere o tom geral da mensagem, a escolha das palavras e o sentimento que ela transmite.\n\n"
            "Classifique a emoção em apenas **uma única opção** entre as seguintes:\n"
            "0: normal — neutra, sem emoção destacada\n"
            "1: feliz — alegria, empolgação, satisfação\n"
            "2: triste — tristeza, desânimo, melancolia\n"
            "3: susto — surpresa inesperada, choque\n"
            "4: medo — preocupação, insegurança, tensão\n"
            "5: raiva — irritação, frustração, agressividade\n"
            "6: fofo — ternura, carinho, delicadeza\n\n"
            "**IMPORTANTE**: Responda SOMENTE com o número da emoção, sem texto adicional.\n"
            "Exemplos de resposta: `1` ou `4`\n"
        )
        
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": variaveis.answer},
            ]
        
        response = br.call(messages)

        content = response.choices[0].message.content

        if(content is not None):
            try:
                numero_emocao = int(content.strip())
                if 0 <= numero_emocao <= 6:
                    return numero_emocao
            except (ValueError, TypeError):
                pass

        return 0
