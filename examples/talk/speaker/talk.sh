#!/bin/bash
set -e

n=1
astro="Hey Moon, I want to learn more about coding with large language models"
echo $astro >astro.txt
cat astro.txt
echo "<ASTRO>" >>talk.xml && cat astro.txt >>talk.xml && echo "</ASTRO>" >>talk.xml
python speak.py Algenib astro.txt $n 2>/dev/null
n=$((n+1))
echo 

for i in {1..2};do
    ../../cmd/bin/sqirvy-cli query moon.md astro.txt >moon.txt 2>/dev/null
    cat moon.txt
    echo "<MOON>" >>talk.xml && cat moon.txt >>talk.xml && echo "</MOON>" >>talk.xml
    python speak.py Sulafat moon.txt $n 2>/dev/null
    n=$((n+1))
    echo 

    ../../cmd/bin/sqirvy-cli query astro.md moon.txt >astro.txt 2>/dev/null
    cat astro.txt
    echo "<ASTRO>" >>talk.xml && cat astro.txt >>talk.xml && echo "</ASTRO>" >>talk.xml
    python speak.py Algenib astro.txt $n 2>/dev/null
    n=$((n+1))
    echo 
done
