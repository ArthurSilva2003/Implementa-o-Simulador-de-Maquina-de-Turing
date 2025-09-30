Uso

Executar no terminal:

python tm.py <arquivo.json> <entrada.in> <saida.txt>


Exemplo:

python tm.py duplo_bal.json duplobal.in saida_duplobal.txt


O programa imprime no console:

1 se a entrada for aceita

0 se a entrada for rejeitada

A fita final é salva no arquivo de saída (.txt).

Arquivos

tm.py: simulador principal

duplo_bal.json e igualdade.json: especificações das máquinas

duplobal.in, duplobal2.in, duplobal3.in: entradas de teste

saida_*.txt: fitas resultantes

Observação

Se a saída gerar uma linha muito grande (como vários "a"), isso ocorre porque a máquina continua processando símbolos sem encontrar uma condição de parada.
