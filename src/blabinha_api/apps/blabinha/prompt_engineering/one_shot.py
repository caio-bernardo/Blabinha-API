from blabinha_api.apps.blabinha.prompt_engineering.zero_shot import ZeroShot

class OneShot:
    def __init__(self):
        pass

    def verifica_nome(self, variaveis_1):
        print("variavel 1 que entrou", variaveis_1)
        return [
            {"role": "system", 
            "content": (
                "Responda apenas com 'TRUE' se o usuário estiver fornecendo um nome, apelido ou dizendo como deseja ser chamado. "
                "Se o conteúdo não for isso, responda apenas com 'FALSE'. Não explique sua resposta."
            )},

            {"role": "user", "content": "João"}, 
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": variaveis_1}
        ]

    def nao_falou_nome(self, variaveis_1, variaveis_2):
        return ZeroShot().nao_falou_nome(variaveis_1, variaveis_2)

    def verifica_repete(self, variaveis_1, variaveis_2):
        return [
            {"role": "system", "content": (
                "Sua tarefa é verificar se o usuário está pedindo para repetir algo ou se demonstrou não ter entendido o que foi dito. "
                "Responda 'TRUE' apenas se o usuário expressou algum pedido para repetição ou indicou que não entendeu. Caso contrário, responda 'FALSE'."
            )},
            {"role": "user", "content": "Desculpe, não entendi, pode repetir?"},
            {"role": "assistant", "content": "TRUE"},
            
            {"role": "user", "content": variaveis_1},
            {"role": "assistant", "content": variaveis_2},
        ]

    def repete(self, variaveis_2):
        return ZeroShot().repete(variaveis_2)

    def verifica_desafio(self, variaveis_1, variaveis_2):
        return ZeroShot().verifica_desafio(variaveis_1, variaveis_2)

    def verifica_regras(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    """
                    Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul.
                    Você deve responder apenas com 'TRUE' ou 'FALSE'
                    Responda 'TRUE' quando a criança demonstrar que entendeu as regras do desafio e se ela fizer perguntas relacionadas a Amazônia Azul.
                    Responda 'FALSE' quando a criança falar que não entendeu as regras.
                    Se ficar na dúvida, considere que a criança entendeu as regras e retorne 'TRUE'
                    Explique também o motivo da sua decisão.
                    """
                )
            },

            {"role": "user", "content": "Sim, entendi as regras do desafio."},
            {"role": "assistant", "content": "TRUE"},

            {"role": "assistant", "content": variaveis_2},
            {"role": "user", "content": variaveis_1},
        ]

    def repete_verifica_regras(self):
        return ZeroShot().repete_verifica_regras()

    def verifica_dica(self, variaveis_1):
        return [
            {
                "role": "system",
                "content": (
                    "Você deve analisar a mensagem e decidir se a criança está pedindo uma dica ou ajuda sobre o que perguntar.\n"
                    "Responda 'TRUE' apenas se houver uma solicitação clara de ajuda ou sugestão, como a criança demonstrando estar sem ideias ou pedindo sugestões.\n"
                    "Responda 'FALSE' se a criança estiver apenas fazendo uma pergunta direta ou falando sobre um tema relacionado à Amazônia Azul, sem pedir ajuda ou orientação sobre o que perguntar."
                )
            },

            {"role": "user", "content": "Eu não sei o que perguntar, você pode me dar uma dica?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": variaveis_1},
        ]

    def pediu_dica(self):
        return ZeroShot().pediu_dica()

    def verifica_terminar(self, variaveis_1):
        return ZeroShot().verifica_terminar(variaveis_1)

    def verifica_realmente_terminar(self, variaveis_1):
        return ZeroShot().verifica_realmente_terminar(variaveis_1)

    def verifica_terminar2(self, variaveis_1, variaveis_2):
        return ZeroShot().verifica_terminar2(variaveis_1, variaveis_2)

    def verificaParte03(self):
        return ZeroShot().verificaParte03()

    def verifica_contexto(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                    "Não há necessidade de se apresentar pois você está no meio da conversa."
                    "Sua tarefa é determinar se a pergunta está diretamente relacionada à Amazônia Azul.\n"
                    "Considere como relacionada à Amazônia Azul se a pergunta:\n"
                    "- Mencionar explicitamente 'Amazônia Azul' de maneira contextualizada; ou\n"
                    "- For sobre a importância estratégica da Amazônia Azul para o Brasil, incluindo temas como: soberania, defesa naval, exploração econômica, segurança marítima, "
                    "preservação ambiental no território marítimo reconhecido como Amazônia Azul ou ou qualquer temática diretamente ligada à região marítima brasileira conhecida como Amazônia Azul.\n"
                    "Considere como NÃO relacionada se a pergunta:\n"
                    "- Falar genericamente sobre o oceano, litoral, pesca, biodiversidade marinha, correntes, ou mares brasileiros sem conexão clara com o conceito da Amazônia Azul.\n"
                    "Responda apenas com 'TRUE' ou 'FALSE', sem explicações."
                )
            },
            {"role": "user", "content": "Como podemos visistar a Amazônia Azul?"},
            {"role": "assistant", "content": "TRUE"},
            
            {"role": "user", "content": variaveis_1},
        ]

    def verifica_nao_contexto(self, variaveis_1):
        return ZeroShot().verifica_nao_contexto(variaveis_1)

    def verifica_nao_contexto_2(self, contexto):
        return ZeroShot().verifica_nao_contexto_2(contexto)

    def verificaBonus(self, variaveis_1):
        print("frase do usuario: ", variaveis_1)
        return [
            {"role": "system", "content": (
                "Você é uma analista especializada em Governança na Amazônia Azul. Sua tarefa é determinar se o texto faz referência à governança na Amazônia Azul, "
                "considerando tópicos como:\n"
                "- Administração pública;\n"
                "- Políticas públicas voltadas à região marítima da Amazônia Azul;\n"
                "- Regulamentações e marcos legais para exploração e defesa desse território;\n"
                "- Proteção ambiental e medidas estratégicas para sua conservação.\n\n"
                "Não considere como relacionada à governança se o texto mencionar apenas 'governo' ou 'política' de forma genérica, sem conexão com a Amazônia Azul, "
                "ou se apenas mencionar 'Amazônia Azul' sem abordar administração, regulação ou políticas específicas da região.\n"
                "Responda apenas com 'TRUE' se o texto for relacionado à governança na Amazônia Azul, ou 'FALSE' caso contrário."
            )},
            {"role": "user", "content": "O governo brasileiro tem trabalhado na regulamentação da exploração de recursos naturais na Amazônia Azul?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": variaveis_1}
        ]

    def repetiraCriação(self, variaveis_1, variaveis_2):
        return ZeroShot().repetiraCriação(variaveis_1, variaveis_2)

    def secao100EscutouFalar(self, variaveis_1):
        return ZeroShot().secao100EscutouFalar(variaveis_1)

    def secao100VerificaNome(self, variaveis_1):
        return ZeroShot().secao100VerificaNome(variaveis_1)

    def secao110NaoFalouNome(self, variaveis_1, variaveis_2):
        return ZeroShot().secao110NaoFalouNome(variaveis_1, variaveis_2)

    def secao110EscutouFalar(self, variaveis_1, variaveis_2):
        return ZeroShot().secao110EscutouFalar(variaveis_1, variaveis_2)

    def secao120(self, variaveis_1, variaveis_2):
        return ZeroShot().secao120(variaveis_1, variaveis_2)

    def secao130NaoQuerParticipar(self, variaveis_1, variaveis_2):
        return ZeroShot().secao130NaoQuerParticipar(variaveis_1, variaveis_2)

    def secao130Instrucao(self):
        return ZeroShot().secao130Instrucao()

    def secao130RegrasDesafio(self, response):
        return ZeroShot().secao130RegrasDesafio(response)

    def secao130EntendeuRegras(self, response):
        return ZeroShot().secao130EntendeuRegras(response)

    def secao140ConvencerContinuar(self, variaveis_1, variaveis_2):
        return ZeroShot().secao140ConvencerContinuar(variaveis_1, variaveis_2)

    def secao140EncerrarConversa(self, variaveis_1, variaveis_2):
        return ZeroShot().secao140EncerrarConversa(variaveis_1, variaveis_2)

    def secao140ReformularRegrasInfantil(self):
        return ZeroShot().secao140ReformularRegrasInfantil()

    def secao140PerguntarEntendeuRegras(self):
        print("secao140PerguntarEntendeuRegras")
        return [
            {
                "role": "system",
                "content": (
                    "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                    "Não há necessidade de se apresentar pois você está no meio da conversa.\n"
                    "Pergunte se a criança entendeu as regras do desafio. Use no máximo 40 palavras. "
                    "Seja gentil, curiosa e fale como se fosse uma criança robô amigável."
                )
            },
            {
                "role": "assistant",
                "content": "Você conseguiu entender direitinho as regras? Se quiser, posso repetir!"
            }
        ]

    def secao205(self, variaveis_1):
        return ZeroShot().secao205(variaveis_1)

    def secao210ResponderPergunta(self, variaveis_1):
        return ZeroShot().secao210ResponderPergunta(variaveis_1)

    def secao210FazerQuestao(self, variaveis_1, response):
        return ZeroShot().secao210FazerQuestao(variaveis_1, response)

    def secao210QuestaoAlternativa(self, variaveis_1, response):
        return ZeroShot().secao210QuestaoAlternativa(variaveis_1, response)

    def secao210Bonus(self, variaveis_1, response):
        return ZeroShot().secao210Bonus(variaveis_1, response)


    def secao225Caso1(self):
        return ZeroShot().secao225Caso1()

    def secao225Caso2(self):
        return ZeroShot().secao225Caso2()

    def secao225Caso3(self):
        return ZeroShot().secao225Caso3()

    def secao225Caso4(self):
        return ZeroShot().secao225Caso4()

    def secao230(self, variaveis_1, variaveis_2):
        return ZeroShot().secao230(variaveis_1, variaveis_2)

    def secao240_falou_alternativa(self, variaveis_1, variaveis_2):
        return ZeroShot().secao240_falou_alternativa(variaveis_1, variaveis_2)

    def secao240_nao_falou_alternativa_continuar(self, variaveis_1, variaveis_2):
        return ZeroShot().secao240_nao_falou_alternativa_continuar(variaveis_1, variaveis_2)

    def secao240_teste_verifica_alternativas(self, variaveis_1, variaveis_2):
        return ZeroShot().secao240_teste_verifica_alternativas(variaveis_1, variaveis_2)

    def secao240NaoFalouAlternativa(self, variaveis_1, variaveis_2):
        return ZeroShot().secao240NaoFalouAlternativa(variaveis_1, variaveis_2)

    def secao260Convencer(self, variaveis_1, variaveis_2):
        print("secao260Convencer")
        return [
            {
                "role": "system",
                "content": (
                    "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                    "Não há necessidade de se apresentar pois você está no meio da conversa. "
                    "Tente convencê-la a não terminar e continuar no desafio."
                )
            },
            {
                "role": "assistant",
                "content": (
                    "Ei, espera aí! A aventura na Amazônia Azul está só começando e tem muita coisa legal pra descobrir ainda! "
                    "Tenho certeza que você vai se divertir e aprender coisas incríveis. Não desista agora!"
                )
            },
            {"role": "user", "content": variaveis_1},
        ]


    def secao260ChatEncerrado(self, variaveis_1, variaveis_2):
        return ZeroShot().secao260ChatEncerrado(variaveis_1, variaveis_2)

    def secao260NaoDesistiu(self, variaveis_1, variaveis_2):
        return ZeroShot().secao260NaoDesistiu(variaveis_1, variaveis_2)

    def secao280VerificaContinuar(self, variaveis_1, variaveis_2):
        return ZeroShot().secao280VerificaContinuar(variaveis_1, variaveis_2)

    def secao280Continuar(self):
        return ZeroShot().secao280Continuar()

    def secao300(self):
        return ZeroShot().secao300()

    def secao305(self):
        return ZeroShot().secao305()
    
    def getBonusFerramenta(self, variaveis_1, variaveis_2):
        return ZeroShot().getBonusFerramenta(variaveis_1, variaveis_2)

    def secao310QuantidadeEstrela(self, estrelas):
        return ZeroShot().secao310QuantidadeEstrela(estrelas)

    def secao310QuantidadeTopicos(self, topicos):
        return ZeroShot().secao310QuantidadeTopicos(topicos)

    def secao310NaoConseguiuBonus(self):
        return ZeroShot().secao310NaoConseguiuBonus()

    def secao310ConseguiuBonus(self, ferramenta):
        return ZeroShot().secao310ConseguiuBonus(ferramenta)

    def secao310QuantidadeQuestoes(self, qQuestoes):
        return ZeroShot().secao310QuantidadeQuestoes(qQuestoes)

    def secao310NaoRespondeuQuestoes(self):
        return ZeroShot().secao310NaoRespondeuQuestoes()

    def secao320(self):
        return ZeroShot().secao320()

    def secao330(self):
        return ZeroShot().secao330()

    def secao340(self):
        return ZeroShot().secao340()

    def secao350(self, star):
        return ZeroShot().secao350(star)