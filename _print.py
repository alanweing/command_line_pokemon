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


class Keys:
    text = 'text'
    color = 'color'
    bold = 'bold'
    underline = 'underline'
    background = 'background'
    alert = 'alert'
    end = 'end'


def _print(args, raw=False):
    import os
    rows, columns = os.popen('stty size', 'r').read().split()
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


def colorize(text, color, bold=False, underline=False, background=None,
             alert=False, end='\n', raw=False):
    _string = _print([{
        Keys.text: text,
        Keys.color: color,
        Keys.background: background,
        Keys.bold: bold,
        Keys.alert: alert,
        Keys.underline: underline,
        Keys.end: end
    }], raw=True)
    if raw:
        return _string
    print(_string, end=end)


def danger(text, bold=True, background=Color.REDBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


def warning(text, bold=True, background=Color.YELLOWBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


def success(text, bold=True, background=Color.GREENBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


def info(text, bold=True, background=Color.BLUEBG, alert=True):
    colorize(text, Color.WHITE, bold, False, background, alert)


def question(text):
    return colorize(text, Color.WHITE, False, False, Color.BLUEBG, False, '',
                    raw=True) + ' '
