
import argparse, json, sys
from collections import defaultdict

class TuringMachine:
    def __init__(self, spec):
        try:
            self.initial = spec["initial"]
            self.finals = set(spec["final"])
            self.blank = spec.get("white", "_")
            trans_list = spec["transitions"]
        except KeyError as e:
            raise ValueError(f"Especificação JSON inválida, faltando chave: {e}")

        # Mapa de transições: (state, read_symbol) -> (next_state, write_symbol, move_dir)
        self.delta = {}
        for t in trans_list:
            try:
                s = t["from"]; to = t["to"]; r = t["read"]; w = t["write"]; d = t["dir"]
            except KeyError as e:
                raise ValueError(f"Transição inválida (chave ausente): {e}, transição={t}")
            d = d.upper()
            if d not in ("L","R","S","N"):
                raise ValueError(f"Direção inválida: {d}. Use L, R, S/N.")
            self.delta[(s, r)] = (to, w, d)

    def run(self, input_string, max_steps=10_000_000):
        # Fita como dicionário esparso
        tape = defaultdict(lambda: self.blank)
        for i, ch in enumerate(input_string):
            tape[i] = ch

        head = 0
        state = self.initial
        visited_min = 0
        visited_max = max(0, len(input_string)-1)

        steps = 0
        while steps < max_steps:
            steps += 1
            symbol = tape[head]
            key = (state, symbol)
            if key not in self.delta:
                # Sem transição: parada
                accepted = state in self.finals
                return accepted, tape, head, state, steps, (visited_min, visited_max)
            nxt_state, write, move = self.delta[key]
            tape[head] = write
            if move in ("R",):
                head += 1
            elif move in ("L",):
                head -= 1
            # S/N = stay
            state = nxt_state
            visited_min = min(visited_min, head)
            visited_max = max(visited_max, head)

        # Segurança: estouro de passos
        return False, tape, head, state, steps, (visited_min, visited_max)

    @staticmethod
    def tape_to_string(tape, blank, span):
        lo, hi = span
        # aparar brancos das pontas
        while lo <= hi and tape[lo] == blank:
            lo += 1
        while hi >= lo and tape[hi] == blank:
            hi -= 1
        if hi < lo:
            return ""
        return "".join(tape[i] for i in range(lo, hi+1))


def read_text_file(path):
    # lê arquivo como texto, tentando UTF-8 e caindo para latin-1 se necessário
    # remove quebras de linha e espaços das pontas
    # não colapsa espaços internos
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            return f.read().strip()


def write_text_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Simulador de Máquina de Turing (formato JSON do enunciado)"
    )
    parser.add_argument("json_spec", help="Arquivo .json com a especificação da MT")
    parser.add_argument("input_txt", help="Arquivo .txt/.in com a entrada (uma fita por arquivo)")
    parser.add_argument("output_txt", help="Arquivo de saída para escrever a fita final (.txt)")
    parser.add_argument("--debug", action="store_true", help="Imprime estado/cabeçote a cada passo")
    parser.add_argument("--max-steps", type=int, default=5_000_000, help="Limite de passos para evitar loop infinito")
    args = parser.parse_args()

    # Carrega JSON
    try:
        with open(args.json_spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except UnicodeDecodeError:
        with open(args.json_spec, "r", encoding="latin-1") as f:
            spec = json.load(f)

    tm = TuringMachine(spec)
    w = tm.blank

    input_string = read_text_file(args.input_txt)

    accepted, tape, head, state, steps, span = tm.run(input_string, max_steps=args.max_steps)
    final_tape = TuringMachine.tape_to_string(tape, w, span)

    # Escreve a fita final no arquivo de saída (apenas a região não-branca)
    write_text_file(args.output_txt, final_tape + "\n")

    # Enunciado: "um aviso indicando se aceita ou rejeita na linha de comando (1 aceita ou 0 rejeita)"
    sys.stdout.write(("1\n" if accepted else "0\n"))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
