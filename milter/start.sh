#!/usr/bin/env bash
python blockchain_milter.py &
sleep 1
chmod 777 /var/spool/postfix/blockchain_milter/blockchain_milter