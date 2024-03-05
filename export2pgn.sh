#!/bin/sh

export MONGO_HOST="mongodb+srv://ccvx01constellation:D2EQOkzTRzRl2htZ@pych.6hvaz7j.mongodb.net/?retryWrites=true&w=majority&appName=pych"

python3 -X dev server/export2pgn.py
