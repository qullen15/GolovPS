## Задание 1:
grep -o '^[^:]*' /etc/passwd | sort

## Задание 2:
grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -rn | head -5

## Задание 3:
nano banner
    #!/bin/bash
    text="$1"
    line="+-$(printf '%*s' "${#text}" '' | tr ' ' '-')-+"
    echo "$line"
    echo "| $text |"
    echo "$line"
chmod +x banner
./banner "Hello from RTU MIREA!"
