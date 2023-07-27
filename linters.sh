#!/bin/bash
flake8 app/ --config=./setup.cfg .
if [ $? = 0 ]; then
   echo 'Code style and syntax looks good to go.'
fi
