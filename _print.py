# classe que contém todas as cores e atributos que podem ser aplicados ao texto
class Color:
    END = '\33[0m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    UNDERLINE = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'

    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'

    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    GREY = '\33[90m'
    RED2 = '\33[91m'
    GREEN2 = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2 = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2 = '\33[96m'
    WHITE2 = '\33[97m'

    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'


# classe auxiliar para assegurar que todas chaves essencias estão presentes no
# dicionário passado à função _print e que as mesmas tenham o mesmo nome
class Keys:
    text = 'text'
    color = 'color'
    bold = 'bold'
    underline = 'underline'
    background = 'background'
    alert = 'alert'
    end = 'end'


# função responsável por 'embelezar' o texto, aceita apenas um vetor como
# argumento, nesse vetor devem conter dicionários para cada palavra
# se raw: o texto não será impresso mas será retornado
def _print(args, raw=False):
    import os
    # rows e column tem o tamanho do terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    # line é o caractér a ser usado para preencher a linha quando alert for
    # True
    line = '-' * int(columns)
    final_string = ''
    end = '\n'
    for _dict in args:
        if Keys.text in _dict:
            if Keys.alert in _dict and _dict[Keys.alert] is True:
                final_string += '\n'
            if Keys.color in _dict:
                final_string += _dict[Keys.color]
            if Keys.background in _dict and _dict[Keys.background] is not None:
                final_string += _dict[Keys.background]
            if Keys.bold in _dict and _dict[Keys.bold] is True:
                final_string += Color.BOLD
            if Keys.underline in _dict and _dict[Keys.underline] is True:
                final_string += Color.UNDERLINE
            if Keys.alert in _dict and _dict[Keys.alert] is True:
                final_string += line + (_dict[Keys.text]).center(int(columns),
                                                                 ' ') + line
            else:
                final_string += _dict[Keys.text]
            final_string += Color.END
            if Keys.alert in _dict and _dict[Keys.alert] is True:
                final_string += '\n'
        else:
            _print([{
                Keys.text: 'MISSING ARGUMENTS!',
                Keys.color: Color.RED,
                Keys.bold: True,
                Keys.alert: True
            }])
            continue
    if raw:
        return final_string
    print(final_string, end=end)

# exemplo de uso da função print:
# _print([
#     {
#         Keys.text: 'texto um',
#         Keys.color: Color.RED,
#         Keys.background: Color.BEIGEBG2,
#         Keys.bold: True,
#         Keys.alert: False
#     }],
#     {
#         Keys.text: 'texto dois',
#         Keys.color: Color.YELLOW,
#         Keys.background: Color.REDBG,
#         Keys.underline: True,
#         Keys.end: '\n\n'
#     })


# funçao responsável por criar o dicionário enviado à funcão _print. Em
# contrapartida só imprime o texto sem variação de cores
# se raw: o texto não será impresso mas será retornado
def colorize(text, color, bold=False, underline=False, background=None,
             alert=False, end='\n', raw=False):
    _string = _print([{
        Keys.text: text,  # texto a ser impresso na tela
        Keys.color: color,  # cor do texto
        Keys.background: background,  # cor de fundo
        Keys.bold: bold,  # negrito (bool)
        Keys.alert: alert,  # se True, ocupará 3 linhas e o texto será
                            # centralizado com preenchimento em cima e
                            # embaixo(bool)
        Keys.underline: underline,  # sobscrito (bool)
        Keys.end: end  # valor final do texto
    }], raw=True)
    if raw:
        return _string
    print(_string, end=end)


# todas as funções abaixo, exceto question, implementam alert como True

# fundo vermelho com texto em branco
def danger(text, bold=True, background=Color.REDBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


# fundo amarelo com texto em branco
def warning(text, bold=True, background=Color.YELLOWBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


# fundo verde com texto em branco
def success(text, bold=True, background=Color.GREENBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


# fundo azul com texto em branco
def info(text, bold=True, background=Color.BLUEBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


# texto a ser impresso na hora de realizar um input; fundo azul com texto em
# branco
def question(text):
    return colorize(text, Color.WHITE, False, False, Color.BLUEBG, False, '',
                    raw=True) + ' '
