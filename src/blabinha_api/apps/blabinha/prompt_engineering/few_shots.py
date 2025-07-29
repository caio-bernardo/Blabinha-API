from blabinha_api.apps.blabinha.prompt_engineering.one_shot import OneShot

class FewShots:
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

            {"role": "user", "content": "Pode me chamar de Eduardo"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Eduardo"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Meu nome é Vitória"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Meu apelido é Vi"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Vi"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Rafa"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Meu apelido é Rafa"},
            {"role": "assistant", "content": "'TRUE'" },

            {"role": "user", "content": "Oi, tudo bem?"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Não sei"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Pode me chamar de qualquer coisa"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": variaveis_1}
        ]

    def nao_falou_nome(self, variaveis_1, variaveis_2):
        return OneShot().nao_falou_nome(variaveis_1, variaveis_2)

    def verifica_repete(self, variaveis_1, variaveis_2):
        return [
            {"role": "system", "content": (
                "Sua tarefa é verificar se o usuário está pedindo para repetir algo ou se demonstrou não ter entendido o que foi dito. "
                "Responda 'TRUE' apenas se o usuário expressou algum pedido para repetição ou indicou que não entendeu. Caso contrário, responda 'FALSE'."
            )},
            {"role": "user", "content": "Desculpe, não entendi, pode repetir?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Não ficou claro para mim, você pode repetir?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Como assim?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Pode explicar melhor?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Hã?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Legal, continue."},
            {"role": "assistant", "content": "FALSE"},

            {"role": "user", "content": "Ah, entendi! Muito obrigado."},
            {"role": "assistant", "content": "FALSE"},

            {"role": "user", "content": variaveis_1},
            {"role": "assistant", "content": variaveis_2},
        ]

    def repete(self, variaveis_2):
        return OneShot().repete(variaveis_2)

    def verifica_desafio(self, variaveis_1, variaveis_2):
        return OneShot().verifica_desafio(variaveis_1, variaveis_2)

    def verifica_regras(self, variaveis_1, variaveis_2):
        return [
            {
                "role": "system",
                "content": (
                    "Responda 'TRUE' apenas quando a criança confirmar que entendeu as regras do desafio. "
                    "Responda 'FALSE' nos seguintes casos:\n"
                    "- A resposta for confusa ou irrelevante para o tema.\n"
                    "- A criança disser que não entendeu as regras.\n"
                    "- A criança mudar de assunto.\n"
                    "- Se não for claro que a criança entendeu as regras."
                )
            },

            {"role": "user", "content": "Sim, entendi as regras do desafio."},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Entendi as regras do jogo"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Entendi"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Aham"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Sim"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Não entendi as regras do desafio"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Não entendi, pode repetir?"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Mais ou menos"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "assistant", "content": variaveis_2},
            {"role": "user", "content": variaveis_1},
        ]

    def repete_verifica_regras(self):
        return OneShot().repete_verifica_regras()

    def verifica_dica(self, variaveis_1):
        return OneShot().verifica_dica(variaveis_1)

    def pediu_dica(self):
        return OneShot().pediu_dica()

    def verifica_terminar(self, variaveis_1):
        return OneShot().verifica_terminar(variaveis_1)

    def verifica_realmente_terminar(self, variaveis_1):
        return OneShot().verifica_realmente_terminar(variaveis_1)

    def verifica_terminar2(self, variaveis_1, variaveis_2):
        return OneShot().verifica_terminar2(variaveis_1, variaveis_2)

    def verificaParte03(self):
        return OneShot().verificaParte03()

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
            {"role": "user", "content": "Quais são os principais recursos naturais explorados na Amazônia Azul?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "O que tem na Amazônia Azul?"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Quem protege a Amazônia Azul?"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Fale sobre os peixes da Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Quais são os recursos minerais da Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "O governo brasileiro tem trabalhado na regulamentação da exploração de recursos naturais na Amazônia Azul?"},
            {"role": "assistant", "content": "TRUE"},

            {"role": "user", "content": "Fale sobre como o governo protege a Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Fale sobre a governança da Amazônia azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Quem protege os peixes da Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Fale sobre a Floresta Amazônica"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Qual o tamanho das árvores da Floresta Amazônica?"},
            {"role": "assistant", "content": "'FALSE'"},
            
            {"role": "user", "content": variaveis_1},
        ]

    def verifica_nao_contexto(self, variaveis_1):
        return OneShot().verifica_nao_contexto(variaveis_1)

    def verifica_nao_contexto_2(self, contexto):
        return OneShot().verifica_nao_contexto_2(contexto)

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

            {"role": "user", "content": "Fale sobre como o governo protege a Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Fale sobre a governança da Amazônia azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Quem protege os peixes da Amazônia Azul"},
            {"role": "assistant", "content": "'TRUE'"},

            {"role": "user", "content": "Fale sobre a Amazônia azul"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Fale sobre os peixes da Amazônia azul"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Fale sobre o governo brasileiro"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Fale sobre o governo brasileiro"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Governança"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": "Políticas públicas"},
            {"role": "assistant", "content": "'FALSE'"},

            {"role": "user", "content": variaveis_1}
        ]

    def repetiraCriação(self, variaveis_1, variaveis_2):
        return OneShot().repetiraCriação(variaveis_1, variaveis_2)

    def secao100EscutouFalar(self, variaveis_1):
        return OneShot().secao100EscutouFalar(variaveis_1)

    def secao100VerificaNome(self, variaveis_1):
        return OneShot().secao100VerificaNome(variaveis_1)

    def secao110NaoFalouNome(self, variaveis_1, variaveis_2):
        return OneShot().secao110NaoFalouNome(variaveis_1, variaveis_2)

    def secao110EscutouFalar(self, variaveis_1, variaveis_2):
        return OneShot().secao110EscutouFalar(variaveis_1, variaveis_2)

    def secao120(self, variaveis_1, variaveis_2):
        return OneShot().secao120(variaveis_1, variaveis_2)

    def secao130NaoQuerParticipar(self, variaveis_1, variaveis_2):
        return OneShot().secao130NaoQuerParticipar(variaveis_1, variaveis_2)

    def secao130Instrucao(self):
        return OneShot().secao130Instrucao()

    def secao130RegrasDesafio(self, response):
        return OneShot().secao130RegrasDesafio(response)

    def secao130EntendeuRegras(self, response):
        return OneShot().secao130EntendeuRegras(response)

    def secao140ConvencerContinuar(self, variaveis_1, variaveis_2):
        return OneShot().secao140ConvencerContinuar(variaveis_1, variaveis_2)

    def secao140EncerrarConversa(self, variaveis_1, variaveis_2):
        return OneShot().secao140EncerrarConversa(variaveis_1, variaveis_2)

    def secao140ReformularRegrasInfantil(self):
        return OneShot().secao140ReformularRegrasInfantil()

    def secao140PerguntarEntendeuRegras(self):
        return OneShot().secao140PerguntarEntendeuRegras()

    def secao205(self, variaveis_1):
        return OneShot().secao205(variaveis_1)

    def secao210ResponderPergunta(self, variaveis_1):
        return OneShot().secao210ResponderPergunta(variaveis_1)

    def secao210FazerQuestao(self, variaveis_1, response):
        return OneShot().secao210FazerQuestao(variaveis_1, response)

    def secao210QuestaoAlternativa(self, variaveis_1, response):
        return OneShot().secao210QuestaoAlternativa(variaveis_1, response)

    def secao210Bonus(self, variaveis_1, response):
        return OneShot().secao210Bonus(variaveis_1, response)

    def secao225Caso1(self):
        return OneShot().secao225Caso1()

    def secao225Caso2(self):
        return OneShot().secao225Caso2()

    def secao225Caso3(self):
        return OneShot().secao225Caso3()

    def secao225Caso4(self):
        return OneShot().secao225Caso4()

    def secao230(self, variaveis_1, variaveis_2):
        return OneShot().secao230(variaveis_1, variaveis_2)

    def secao240_falou_alternativa(self, variaveis_1, variaveis_2):
        return OneShot().secao240_falou_alternativa(variaveis_1, variaveis_2)

    def secao240_nao_falou_alternativa_continuar(self, variaveis_1, variaveis_2):
        return OneShot().secao240_nao_falou_alternativa_continuar(variaveis_1, variaveis_2)

    def secao240_teste_verifica_alternativas(self, variaveis_1, variaveis_2):
        return OneShot().secao240_teste_verifica_alternativas(variaveis_1, variaveis_2)

    def secao240NaoFalouAlternativa(self, variaveis_1, variaveis_2):
        return OneShot().secao240NaoFalouAlternativa(variaveis_1, variaveis_2)

    def secao260Convencer(self, variaveis_1, variaveis_2):
        return OneShot().secao260Convencer(variaveis_1, variaveis_2)

    def secao260ChatEncerrado(self, variaveis_1, variaveis_2):
        return OneShot().secao260ChatEncerrado(variaveis_1, variaveis_2)

    def secao260NaoDesistiu(self, variaveis_1, variaveis_2):
        return OneShot().secao260NaoDesistiu(variaveis_1, variaveis_2)

    def secao280VerificaContinuar(self, variaveis_1, variaveis_2):
        return OneShot().secao280VerificaContinuar(variaveis_1, variaveis_2)

    def secao280Continuar(self):
        return OneShot().secao280Continuar()

    def secao300(self):
        return OneShot().secao300()

    def secao305(self):
        return OneShot().secao305()
    
    def getBonusFerramenta(self, variaveis_1, variaveis_2):
        return OneShot().getBonusFerramenta(variaveis_1, variaveis_2)

    def secao310QuantidadeEstrela(self, estrelas):
        return OneShot().secao310QuantidadeEstrela(estrelas)

    def secao310QuantidadeTopicos(self, topicos):
        return OneShot().secao310QuantidadeTopicos(topicos)

    def secao310NaoConseguiuBonus(self):
        return OneShot().secao310NaoConseguiuBonus()

    def secao310ConseguiuBonus(self, ferramenta):
        return OneShot().secao310ConseguiuBonus(ferramenta)

    def secao310QuantidadeQuestoes(self, qQuestoes):
        return OneShot().secao310QuantidadeQuestoes(qQuestoes)

    def secao310NaoRespondeuQuestoes(self):
        return OneShot().secao310NaoRespondeuQuestoes()

    def secao320(self):
        return OneShot().secao320()

    def secao330(self):
        return OneShot().secao330()

    def secao340(self):
        return OneShot().secao340()

    def secao350(self, star):
        return OneShot().secao350(star)