#!/bin/bash
source ../venv/bin/activate
<<<<<<< HEAD
export POSTGRES_LMNOP_USER_PASSWORD=lmnop
=======
export POSTGRES_LMNOP_USER_PASSWORD=lmnop.sqlite
>>>>>>> 6fe25741f364a256478dd03a891a2000cdba654a
export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib
sudo ln -s /Library/PosgreSQL/9.5/lib/libssl.1.0.0.dylib /usr/local/lib
sudo ln -s /Library/PosgreSQL/9.5/lib/libcrypto.1.0.0.dylib /usr/local/lib
