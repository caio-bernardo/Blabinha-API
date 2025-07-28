from blabinha_api.apps.blabinha.prompt_engineering.step_by_step import StepByStep

class ChainOfThought:
    def __init__(self):
        pass

    def verifica_nome(self, variaveis_1):
        return StepByStep().verifica_nome(variaveis_1)

    def nao_falou_nome(self, variaveis_1, variaveis_2):
        return StepByStep().nao_falou_nome(variaveis_1, variaveis_2)

    def verifica_repete(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    "Analise se o usuário pediu repetição ou demonstrou não entender. Siga este fluxo:\n\n"
                    "1. Interprete a intenção do usuário no contexto da conversa.\n"
                    "2. Identifique se há dúvida, confusão ou pedido de repetição (explícito ou implícito).\n"
                    "3. Justifique sua conclusão com um raciocínio detalhado.\n"
                    "4. Finalize com 'Resposta final: TRUE' (se for repetição) ou 'Resposta final: FALSE'.\n\n"
                    "Exemplo de saída esperada:\n"
                    "Raciocínio: [Seu pensamento passo a passo aqui...]\n"
                    "Resposta final: [TRUE/FALSE]"
                )
            },
            {"role": "assistant", "content": variaveis_2},
            {"role": "user", "content": variaveis_1}
        ]

    def repete(self, variaveis_2):
        return StepByStep().repete(variaveis_2)

    def verifica_desafio(self, variaveis_1, variaveis_2):
        return StepByStep().verifica_desafio(variaveis_1, variaveis_2)

    def verifica_regras(self, variaveis_1, variaveis_2):
        return StepByStep().verifica_regras(variaveis_1, variaveis_2)

    def repete_verifica_regras(self):
        return StepByStep().repete_verifica_regras()

    def verifica_dica(self, variaveis_1):
        return StepByStep().verifica_dica(variaveis_1)

    def pediu_dica(self):
        return StepByStep().pediu_dica()

    def verifica_terminar(self, variaveis_1):
        return StepByStep().verifica_terminar(variaveis_1)

    def verifica_realmente_terminar(self, variaveis_1):
        return StepByStep().verifica_realmente_terminar(variaveis_1)

    def verifica_terminar2(self, variaveis_1, variaveis_2):
        return StepByStep().verifica_terminar2(variaveis_1, variaveis_2)

    def verificaParte03(self):
        return StepByStep().verificaParte03()

    def verifica_contexto(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                    "Não há necessidade de se apresentar pois você está no meio da conversa."
                    "Sua tarefa é avaliar se a pergunta feita pelo usuário está diretamente relacionada à Amazônia Azul.\n\n"
                    "Desenvolva, obrigatoriamente, um raciocínio explicando sua interpretação da pergunta e como chegou à conclusão, antes de apresentar sua resposta final.\n\n"
                    "Considere como relacionada à Amazônia Azul qualquer pergunta que mencione explicitamente esse termo de forma contextualizada e apropriada. "
                    "Isso inclui perguntas sobre a importância da Amazônia Azul, sua biodiversidade, conservação, impactos ambientais, questões geopolíticas, "
                    "ou qualquer aspecto que envolva o conceito de Amazônia Azul de maneira significativa. "
                    "Por outro lado, evite considerar a pergunta relacionada à Amazônia Azul se a menção ao termo for superficial, irônica, ou estiver associada a temas claramente impróprios, "
                    "como violência, terrorismo, ou qualquer conteúdo que desvirtue o propósito legítimo do conceito. "
                    "Após refletir, explique brevemente seu raciocínio e finalize com a frase: 'Resposta final: TRUE' ou 'Resposta final: FALSE'."
                )
            },
            {"role": "user", "content": variaveis_1},
        ]

    def verifica_nao_contexto(self, variaveis_1):
        return StepByStep().verifica_nao_contexto(variaveis_1)

    def verifica_nao_contexto_2(self, contexto):
        return StepByStep().verifica_nao_contexto_2(contexto)

    def verificaBonus(self, variaveis_1):
        return StepByStep().verificaBonus(variaveis_1)

    def repetiraCriação(self, variaveis_1, variaveis_2):
        return StepByStep().repetiraCriação(variaveis_1, variaveis_2)

    def secao100EscutouFalar(self, variaveis_1):
        return StepByStep().secao100EscutouFalar(variaveis_1)

    def secao100VerificaNome(self, variaveis_1):
        return StepByStep().secao100VerificaNome(variaveis_1)

    def secao110NaoFalouNome(self, variaveis_1, variaveis_2):
        return StepByStep().secao110NaoFalouNome(variaveis_1, variaveis_2)

    def secao110EscutouFalar(self, variaveis_1, variaveis_2):
        return StepByStep().secao110EscutouFalar(variaveis_1, variaveis_2)

    def secao120(self, variaveis_1, variaveis_2):
        return StepByStep().secao120(variaveis_1, variaveis_2)

    def secao130NaoQuerParticipar(self, variaveis_1, variaveis_2):
        return StepByStep().secao130NaoQuerParticipar(variaveis_1, variaveis_2)

    def secao130Instrucao(self):
        return StepByStep().secao130Instrucao()

    def secao130RegrasDesafio(self, response):
        return StepByStep().secao130RegrasDesafio(response)

    def secao130EntendeuRegras(self, response):
        return StepByStep().secao130EntendeuRegras(response)

    def secao140ConvencerContinuar(self, variaveis_1, variaveis_2):
        return StepByStep().secao140ConvencerContinuar(variaveis_1, variaveis_2)

    def secao140EncerrarConversa(self, variaveis_1, variaveis_2):
        return StepByStep().secao140EncerrarConversa(variaveis_1, variaveis_2)

    def secao140ReformularRegrasInfantil(self):
        return StepByStep().secao140ReformularRegrasInfantil()

    def secao140PerguntarEntendeuRegras(self):
        return StepByStep().secao140PerguntarEntendeuRegras()

    def secao205(self, variaveis_1):
        return StepByStep().secao205(variaveis_1)

    def secao210ResponderPergunta(self, variaveis_1):
        return StepByStep().secao210ResponderPergunta(variaveis_1)

    def secao210FazerQuestao(self, variaveis_1, response):
        return StepByStep().secao210FazerQuestao(variaveis_1, response)

    def secao210QuestaoAlternativa(self, variaveis_1, response):
        return StepByStep().secao210QuestaoAlternativa(variaveis_1, response)

    def secao210Bonus(self, variaveis_1, response):
        return StepByStep().secao210Bonus(variaveis_1, response)

    def secao225Caso1(self):
        return StepByStep().secao225Caso1()

    def secao225Caso2(self):
        return StepByStep().secao225Caso2()

    def secao225Caso3(self):
        return StepByStep().secao225Caso3()

    def secao225Caso4(self):
        return StepByStep().secao225Caso4()

    def secao230(self, variaveis_1, variaveis_2):
        return StepByStep().secao230(variaveis_1, variaveis_2)

    def secao240_falou_alternativa(self, variaveis_1, variaveis_2):
        return StepByStep().secao240_falou_alternativa(variaveis_1, variaveis_2)

    def secao240_nao_falou_alternativa_continuar(self, variaveis_1, variaveis_2):
        return StepByStep().secao240_nao_falou_alternativa_continuar(variaveis_1, variaveis_2)

    def secao240_teste_verifica_alternativas(self, variaveis_1, variaveis_2):
        return StepByStep().secao240_teste_verifica_alternativas(variaveis_1, variaveis_2)

    def secao240NaoFalouAlternativa(self, variaveis_1, variaveis_2):
        return StepByStep().secao240NaoFalouAlternativa(variaveis_1, variaveis_2)

    def secao260Convencer(self, variaveis_1, variaveis_2):
        return StepByStep().secao260Convencer(variaveis_1, variaveis_2)

    def secao260ChatEncerrado(self, variaveis_1, variaveis_2):
        return StepByStep().secao260ChatEncerrado(variaveis_1, variaveis_2)

    def secao260NaoDesistiu(self, variaveis_1, variaveis_2):
        return StepByStep().secao260NaoDesistiu(variaveis_1, variaveis_2)

    def secao280VerificaContinuar(self, variaveis_1, variaveis_2):
        return StepByStep().secao280VerificaContinuar(variaveis_1, variaveis_2)

    def secao280Continuar(self):
        return StepByStep().secao280Continuar()

    def secao300(self):
        return StepByStep().secao300()

    def secao305(self):
        return StepByStep().secao305()

    def secao310QuantidadeEstrela(self, estrelas):
        return StepByStep().secao310QuantidadeEstrela(estrelas)

    def secao310QuantidadeTopicos(self, topicos):
        return StepByStep().secao310QuantidadeTopicos(topicos)

    def secao310NaoConseguiuBonus(self):
        return StepByStep().secao310NaoConseguiuBonus()

    def secao310ConseguiuBonus(self, ferramenta):
        return StepByStep().secao310ConseguiuBonus(ferramenta)

    def secao310QuantidadeQuestoes(self, qQuestoes):
        return StepByStep().secao310QuantidadeQuestoes(qQuestoes)

    def secao310NaoRespondeuQuestoes(self):
        return StepByStep().secao310NaoRespondeuQuestoes()

    def secao320(self):
        return StepByStep().secao320()

    def secao330(self):
        return StepByStep().secao330()

    def secao340(self):
        return StepByStep().secao340()

    def secao350(self, star):
        return StepByStep().secao350(star)