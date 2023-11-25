#!/bin/bash

keytab_directory="/keytabs"

for keytab_file in "$keytab_directory"/*.keytab; do
    identity=$(basename "$keytab_file" .keytab)
    kinit -kt "$keytab_file" "$identity"
done

python app.py