#! /bin/bash

python=/home/paul/.virtualenvs/dj/bin/python
manager=/home/paul/djprojs/mysite/pester/pestering_manager.py

if ! [ -f $python ]; then
    echo "No python executable at $python"
    exit 1	
fi

if ! [ -f $manager ]; then
    echo "No pester manager found at $manager"
    exit 1
fi

exec $python $manager

exit 0
