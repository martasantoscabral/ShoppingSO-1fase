#!/bin/bash

# Verificar argumentos
if [ $# -ne 2 ]; then
    echo "Uso: $0 <pasta_dos_clientes> <max_processos>"
    exit 1
fi

echo "Analises começando!"

# ...
PASTA_DOS_CLIENTES=$1
#FICHEIROS=`ls $1`
MAX_PROCESSOS=$2
NUM_DE_PROCESSOS=0

for ficheiro in $PASTA_DOS_CLIENTES/*.csv
    do
        #echo $ficheiro
        if [[ $NUM_DE_PROCESSOS -eq $MAX_PROCESSOS ]]
	    then wait -n
            ((NUM_DE_PROCESSOS--))
        fi
            python3 analisar_cliente.py $ficheiro &
            ((NUM_DE_PROCESSOS++))

    done

wait

#for ficheiro in $FICHEIROS
#do
#	CAMINHO_FICHEIRO="${PASTA_DOS_CLIENTES}/$ficheiro"
#	(sleep 10 && echo $CAMINHO_FICHEIRO) &

	#wait -n
	#python3 analisar_cliente.py CAMINHO_FICHEIRO
#done

echo "Todas as análises concluídas."