
# Simulador de Máquina de Turing (CLI)

**Uso:**  
```bash
python tm.py <especificacao.json> <entrada.in> <saida.txt>
```

A saída no **stdout** é `1` (aceita) ou `0` (rejeita).  
O arquivo indicado em `<saida.txt>` recebe **apenas a região não-branca** da fita final (sem espaços extras).

## Formato JSON esperado
```json
{
  "initial": 0,
  "final": [4],
  "white": "_",
  "transitions": [
    {"from":0,"to":1,"read":"a","write":"A","dir":"R"},
    {"from":1,"to":1,"read":"a","write":"a","dir":"R"}
  ]
}
```
- `dir`: `L` (esquerda), `R` (direita), `S`/`N` (sem mover).

## Entradas (.in / .txt)
- O simulador lê o arquivo como **texto** (tenta UTF‑8, cai para Latin‑1).  
- Quebras de linha das pontas são removidas. Se o Classroom mostrar “Binário”, ainda assim funcionará.

## Exemplos (Windows PowerShell)
```powershell
python tm.py duplo_bal.json duplobal.in duplobal.out.txt
python tm.py igualdade.json duplobal2.in duplobal2.out.txt
python tm.py igualdade.json duplobal3.in duplobal3.out.txt
```

## Dicas
- Se sua MT entrar em **loop**, use `--max-steps` para travar a execução e depurar.
- Para investigar, rode com `--debug` (imprime estado/cabeçote a cada passo).

## Saída
- **stdout**: `1` (aceita) ou `0` (rejeita)
- **arquivo**: conteúdo não-branco da fita final
```
