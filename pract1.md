## Задание 1:
```
grep -o '^[^:]*' /etc/passwd | sort
```

## Задание 2:
```
grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -rn | head -5
```

## Задание 3:
```
nano banner
    #!/bin/bash
    text="$1"
    line="+-$(printf '%*s' "${#text}" '' | tr ' ' '-')-+"
    echo "$line"
    echo "| $text |"
    echo "$line"
chmod +x banner
./banner "Hello from RTU MIREA!"
```

## Задание 4:
```
nano ident
    #!/bin/bash
    grep -o '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | tr '\n' ' '
    echo
chmod +x ident
./ident hello.cpp
```

## Задание 5:
```
nano reg
    #!/bin/bash
    chmod 755 "$1"
    cp "$1" /usr/local/bin/
chmod +x reg
sudo ./reg banner
```
