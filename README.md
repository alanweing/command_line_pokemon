# command_line_pokemon

Professor, ao entrar no programa pela primeira vez, depois de registrar, por
favor, executar o comando 'god_mode'. Todos os comandos disponíveis estão
descritos a partir da linha 119 desse README

Módulos NECESSÁRIOS:
------
  * pymysql
  * numpy


env.py
======
Para iniciar, altere as credenciais contidas no arquivo 'env.py' de acordo
com o banco de dados local (linhas 1 a 5), que deve ser MariaDB ou MySQL.
Não é necessário a criação do banco de dados, o programa irá criar se
não encontrar o banco especificado na variável DB (env.py).

Tudo que está dentro de POKEMONS e GLOBALS são configurações básicas para o
funcionamento do programa. SPAWN_RATIO_* descreve a probabilidade de encontrar
um pokemon para cada tipo de raridade. Variáveis definidas em GLOBALS
especifiam o tempo de espera para cada ato (ver nome da variável).



PONTOS DE INTERESSE PARA O TRABALHO:
======

Para cada monstro deve-se saber o nome, nível na classificação de raridade e pelo menos mais uma caraterística a sua escolha:
------
Todas as características estão armazenadas no banco de dados e podem saber facilmente recuperadas com os seguintes comandos:
    from models import Pokemon
```python
    # encontrar pelo nome:
    poke = Pokemon().where('name = "{}"'.format(nome_do_pokemon))
    # ou também, como nome é uma PK:
    poke = Pokemon().find(nome_do_pokemon)
    # encontrar por raridade
    poke = Pokemon().where('rarity = "{}"'.format(raridade))
    # a função 'where' pode recuperar qualquer dado, desde que as condições estejam na variável 'fields' que é executada na inicialização do Model
```

O algoritmo deve colocar os pokémons em ordem alfabética utilizando um dos seguintes métodos: selection, insertion, quicksort ou mergesort.
------
Os algorítmos estão implementados no arquivo functions.py. E são utilizados no arquivo controllers.py, nos métodos:
* order_pokemons(self, order_by)
* generate_vio(self, order_by)
Cada qual está devidamente comentado na sua utilização (linha 114 controllers.py)

    ::Além disso, através de VIOs ou encadeamento, você deve apresentar de forma
ordenada, os monstros capturados de acordo o nível de raridade e a outra
característica definida.
    Isso é feito na função generate_vio(self, order_by) do arquivo controllers.py

    ::Sempre que um novo monstro é capturado, a ordenação deve ser atualizada.
    Todo o controle é feito pela função add_pokemon(self, pokemon) no arquivo
controllers.py

    Todas as classes que estão em models.py representam uma tabela do banco de
dados e podem ser recuperadas/atualizadas/deletadas com os comandos:

    select(self, fields='*', conditions=None, order_by=None, limit=None)
    update(self, new_values, column_value, column_to_search=None)
    create(self, values_dict)
    delete(self, conditions)
    # first retorna a primeira linha que satisfaça a condição
    first(self, fields='*', conditions=None, order_by=None)
    # retorna todas as linhas que satisfaçam a condição
    where(self, conditions, fields='*', order_by=None, limit=None)
    # retorna uma linha pela chave primária
    find(self, value, fields='*', conditions=None)

    OBS.: Os modelos precisam ser instanciados antes de chamar qualquer função,
pois o Model precisa saber a qual tabela pertence, qual é a PK, quais colunas
tem acesso e quais pode alterar.



=>_input.py e _print.py

    São arquivos auxiliares para o funcionamento do programa. _input.py certifica
que todos is inputs do usuário são válidos a partir da função(reduzida):

get(self, message, _type, acceptable, loop=False), sendo:
    ->message: a mensagem a ser utilizada
    ->_type: o tipo a ser aceito pelo input ('string', 'int', 'float', 'mixed')
    ->acceptable: é um vetor de dados aceitos pelo input ou None para qualquer valor
    ->loop: se True dois 'enter' quebram o loop

    Já o arquivo _print.py deixa as mensagens mais apresentáveis ao usuário,
para simplificação foram feitas funções auxiliares para o programa seguir um
padrão. Sendo elas:

def danger(text, bold=True, background=Color.REDBG, alert=True)
def warning(text, bold=True, background=Color.YELLOWBG, alert=True)
def success(text, bold=True, background=Color.GREENBG, alert=True)
def info(text, bold=True, background=Color.BLUEBG, alert=True)
def question(text)

    Todas elas implementam a função colorize que por sua vez monta um dicionário
a ser passado ao _print.
    O formato do dicionário consiste em:
    {
        Keys.text: text, # texto a ser colorido
        Keys.color: color, # cor a ser usada
        Keys.background: background, # cor de fundo
        Keys.bold: bold, # negritou (bool)
        Keys.alert: alert, # se sim, ocupa 3 linhas e centraliza o texto(bool)
        Keys.underline: underline, # subscrito (bool)
        Keys.end: end # valor para o end do print
    }

    P.S.: Todas cores diponíveis se econtram na classe Color do arquivo _print.py



    Todas os demais casos de uso estão exemplificados e comentados em código.


COMANDOS ACEITOS PELO terminator
======

CREDENCIAIS
------
* login
* register

DEPOIS DE AUTORIZADO
------
* pokemon list (lista todos os pokemons do usuário)
* pokemon rename 'name' (renomeia o pokemon 'name' do usuário)
* pokemon sort 'sort_order'
        sort_order pode ser:
            - type (gera um VIO e mostra os pokemons ordenados por tipo)
            - rarity (gera um VIO e mostra os pokemons ordenados por raridade)
            - name (ordena fisicamente os pokemons por nome (dado pelo usuário; por padrão tem o mesmo nome do Pokemon))
            - pokemon (ordena fisicamente os pokemons por nome de pokemon)
        pokemons ordenados fisicamente não são mostrados na tela e, para isso,
        deve se chamar 'pokemon list'.
* hunt (caça um pokemon. Esse pokemon é definido aleatoriamente, sendo que
        as probabilidades para cada raridade de pokemon estão definidas no
        arquivo env.py. Pode-se também ser encontrado um ovo que depois de x
        segundos (sendo x também definido em env.py) gera um pokemon aleatório
        tendo sua raridade 'very common'. Se o jogador já tiver um pokemon e
        ao caçar encontrar outro pokemon, o sistema de batalha é chamado, mas
        esse ainda não está implentado)
* help (mostra todos os comandos disponíveis)
* exit (sai do programa)
* god_mode (todos os pokemons disponiveis são atribuidos ao jogador)
