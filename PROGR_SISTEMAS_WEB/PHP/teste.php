<?php
echo "Digite a altura da pessoa: ";
$Altura = floatval(trim(fgets(STDIN)));
echo "Digite o sexo da pessoa (M/F): ";
$Sexo = strtoupper(fgets(STDIN));

if ($Sexo == "M") {
     $PesoIdeal = (72.7 * $Altura) - 58;
    echo "O Homem descrito deve pesar $PesoIdeal kg.\n";
} else{
    $PesoIdeal = (62.1 * $Altura) - 44.7;
    echo "A Mulher descrita deve pesar $PesoIdeal kg.\n";
}
