from blabinha_api.apps.blabinha.prompt_engineering.few_shots import FewShots

class StepByStep:
    def __init__(self):
        pass

    def verifica_nome(self, variaveis_1):
        return [
            {
                "role": "system",
                "content": (
                    "Siga os passos abaixo para determinar se o usuário está fornecendo um nome, apelido ou dizendo como deseja ser chamado:\n\n"
                    "1. Leia atentamente a mensagem do usuário.\n"
                    "2. Verifique se o conteúdo parece ser um nome próprio, apelido ou uma forma de identificação pessoal.\n"
                    "3. Considere também se o tom ou estrutura da mensagem indica que o usuário está se apresentando ou respondendo a algo como 'qual é o seu nome?'.\n"
                    "4. Se a mensagem indicar isso claramente, responda apenas com 'TRUE'.\n"
                    "5. Caso contrário, responda apenas com 'FALSE'.\n\n"
                    "IMPORTANTE: Responda exclusivamente com 'TRUE' ou 'FALSE'. Não forneça explicações adicionais."
                )
            },
            {"role": "user", "content": variaveis_1}
        ]


    def nao_falou_nome(self, variaveis_1, variaveis_2):
        return FewShots().nao_falou_nome(variaveis_1, variaveis_2)

    #não ficou bom
    def verifica_repete(self, variaveis_1, variaveis_2):
        return [
            {"role": "system", "content": (
                "Siga os passos abaixo para determinar se o usuário pediu para repetir a fala:\n\n"
                "1. Verifique se o usuário está pedindo para repetir algo ou demonstrou não ter entendido o que foi expresso.\n"
                "2. Se o usuário:\n"
                "   a) Pediu explicitamente que repita, ou\n"
                "   b) Demonstrou confusão ou falta de entendimento,\n"
                "   então responda com 'TRUE'.\n"
                "3. Caso contrário, responda com 'FALSE'."
            )},
            {"role": "user", "content": variaveis_1},
            {"role": "assistant", "content": variaveis_2},
        ]


    def repete(self, variaveis_2):
        return FewShots().repete(variaveis_2)

    def verifica_desafio(self, variaveis_1, variaveis_2):
        return FewShots().verifica_desafio(variaveis_1, variaveis_2)

    def verifica_regras(self, variaveis_1, variaveis_2):
        return FewShots().verifica_regras(variaveis_1, variaveis_2)

    def repete_verifica_regras(self):
        return FewShots().repete_verifica_regras()

    def verifica_dica(self, variaveis_1):
        return FewShots().verifica_dica(variaveis_1)

    def pediu_dica(self):
        return FewShots().pediu_dica()

    def verifica_terminar(self, variaveis_1):
        return FewShots().verifica_terminar(variaveis_1)

    def verifica_realmente_terminar(self, variaveis_1):
        return FewShots().verifica_realmente_terminar(variaveis_1)

    def verifica_terminar2(self, variaveis_1, variaveis_2):
        return FewShots().verifica_terminar2(variaveis_1, variaveis_2)

    def verificaParte03(self):
        return FewShots().verificaParte03()

    def verifica_contexto(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                    "Não há necessidade de se apresentar pois você está no meio da conversa."
                    "Sua tarefa é verificar se a pergunta está diretamente relacionada à Amazônia Azul.\n\n"
                    "Siga os passos abaixo para determinar isso:\n\n"
                    "Passo 1: A pergunta menciona explicitamente o termo 'Amazônia Azul'?\n"
                    "- Se NÃO, responda 'FALSE'.\n"
                    "- Se SIM, prossiga para o passo 2.\n\n"
                    "Passo 2: A pergunta aborda sobre a Amazônia Azul de forma apropriada.\n"
                    "Considere os seguintes temas como exemplos, mas outros temas também são válidos:\n"
                    "- Soberania nacional\n"
                    "- Defesa naval\n"
                    "- Exploração econômica de recursos marítimos\n"
                    "- Segurança marítima\n"
                    "- Preservação ambiental da região marítima conhecida como Amazônia Azul\n"
                    "- Qualquer temática diretamente ligada à região marítima brasileira conhecida como Amazônia Azul\n"
                    "- Se SIM, responda 'TRUE'.\n"
                    "- Se NÃO, responda 'FALSE'.\n\n"
                    "Observação:\n"
                    "- Se a pergunta tratar de forma genérica sobre oceano, litoral, biodiversidade marinha, pesca, correntes marítimas ou mares brasileiros SEM relação clara com a Amazônia Azul, responda 'FALSE'.\n"
                    "- Em casos de dúvida ou menção superficial, responda 'FALSE'.\n\n"
                    "IMPORTANTE: Responda exclusivamente com 'TRUE' ou 'FALSE'. Não forneça explicações adicionais."
                )
            },
            {"role": "user", "content": variaveis_1},
        ]

    def verifica_nao_contexto(self, variaveis_1):
        return FewShots().verifica_nao_contexto(variaveis_1)

    def verifica_nao_contexto_2(self, contexto):
        return FewShots().verifica_nao_contexto_2(contexto)

    def verificaBonus(self, variaveis_1):
        print("frase do usuario: ", variaveis_1)
        return FewShots().verificaBonus(variaveis_1)

    def repetiraCriação(self, variaveis_1, variaveis_2):
        return FewShots().repetiraCriação(variaveis_1, variaveis_2)

    def secao100EscutouFalar(self, variaveis_1):
        return FewShots().secao100EscutouFalar(variaveis_1)

    def secao100VerificaNome(self, variaveis_1):
        return FewShots().secao100VerificaNome(variaveis_1)

    def secao110NaoFalouNome(self, variaveis_1, variaveis_2):
        return FewShots().secao110NaoFalouNome(variaveis_1, variaveis_2)

    def secao110EscutouFalar(self, variaveis_1, variaveis_2):
        return FewShots().secao110EscutouFalar(variaveis_1, variaveis_2)

    def secao120(self, variaveis_1, variaveis_2):
        return FewShots().secao120(variaveis_1, variaveis_2)

    def secao130NaoQuerParticipar(self, variaveis_1, variaveis_2):
        return FewShots().secao130NaoQuerParticipar(variaveis_1, variaveis_2)

    def secao130Instrucao(self):
        return FewShots().secao130Instrucao()

    def secao130RegrasDesafio(self, response):
        return FewShots().secao130RegrasDesafio(response)

    def secao130EntendeuRegras(self, response):
        return FewShots().secao130EntendeuRegras(response)

    def secao140ConvencerContinuar(self, variaveis_1, variaveis_2):
        return FewShots().secao140ConvencerContinuar(variaveis_1, variaveis_2)

    def secao140EncerrarConversa(self, variaveis_1, variaveis_2):
        return FewShots().secao140EncerrarConversa(variaveis_1, variaveis_2)

    def secao140ReformularRegrasInfantil(self):
        return FewShots().secao140ReformularRegrasInfantil()

    def secao140PerguntarEntendeuRegras(self):
        return FewShots().secao140PerguntarEntendeuRegras()

    def secao205(self, variaveis_1):
        return FewShots().secao205(variaveis_1)

    def secao210ResponderPergunta(self, variaveis_1):
        return FewShots().secao210ResponderPergunta(variaveis_1)

    def secao210FazerQuestao(self, variaveis_1, response):
        return FewShots().secao210FazerQuestao(variaveis_1, response)

    def secao210QuestaoAlternativa(self, variaveis_1, response):
        return FewShots().secao210QuestaoAlternativa(variaveis_1, response)

    def secao210Bonus(self, variaveis_1, response):
        return FewShots().secao210Bonus(variaveis_1, response)

    def secao225Caso1(self):
        return FewShots().secao225Caso1()

    def secao225Caso2(self):
        return FewShots().secao225Caso2()

    def secao225Caso3(self):
        return FewShots().secao225Caso3()

    def secao225Caso4(self):
        return FewShots().secao225Caso4()

    def secao230(self, variaveis_1, variaveis_2):
        return FewShots().secao230(variaveis_1, variaveis_2)

    def secao240_falou_alternativa(self, variaveis_1, variaveis_2):
        return FewShots().secao240_falou_alternativa(variaveis_1, variaveis_2)

    def secao240_nao_falou_alternativa_continuar(self, variaveis_1, variaveis_2):
        return FewShots().secao240_nao_falou_alternativa_continuar(variaveis_1, variaveis_2)

    def secao240_teste_verifica_alternativas(self, variaveis_1, variaveis_2):
        return FewShots().secao240_teste_verifica_alternativas(variaveis_1, variaveis_2)

    def secao240NaoFalouAlternativa(self, variaveis_1, variaveis_2):
        return FewShots().secao240NaoFalouAlternativa(variaveis_1, variaveis_2)

    def secao260Convencer(self, variaveis_1, variaveis_2):
        return FewShots().secao260Convencer(variaveis_1, variaveis_2)

    def secao260ChatEncerrado(self, variaveis_1, variaveis_2):
        return FewShots().secao260ChatEncerrado(variaveis_1, variaveis_2)

    def secao260NaoDesistiu(self, variaveis_1, variaveis_2):
        return FewShots().secao260NaoDesistiu(variaveis_1, variaveis_2)

    def secao280VerificaContinuar(self, variaveis_1, variaveis_2):
        return FewShots().secao280VerificaContinuar(variaveis_1, variaveis_2)

    def secao280Continuar(self):
        return FewShots().secao280Continuar()

    def secao300(self):
        return FewShots().secao300()

    def secao305(self):
        return FewShots().secao305()
    
    def getBonusFerramenta(self, variaveis_1, variaveis_2):
        return FewShots().getBonusFerramenta(variaveis_1, variaveis_2)

    def secao310QuantidadeEstrela(self, estrelas):
        return FewShots().secao310QuantidadeEstrela(estrelas)

    def secao310QuantidadeTopicos(self, topicos):
        return FewShots().secao310QuantidadeTopicos(topicos)

    def secao310NaoConseguiuBonus(self):
        return FewShots().secao310NaoConseguiuBonus()

    def secao310ConseguiuBonus(self, ferramenta):
        return FewShots().secao310ConseguiuBonus(ferramenta)

    def secao310QuantidadeQuestoes(self, qQuestoes):
        return FewShots().secao310QuantidadeQuestoes(qQuestoes)

    def secao310NaoRespondeuQuestoes(self):
        return FewShots().secao310NaoRespondeuQuestoes()

    def secao320(self):
        return FewShots().secao320()

    def secao330(self):
        return FewShots().secao330()

    def secao340(self):
        return FewShots().secao340()

    def secao350(self, star):
        return FewShots().secao350(star)
