#!/usr/bin/env bash
echo "non_smtpd_milters = unix:blockchain_milter/blockchain_milter" >> /etc/postfix/main.cf
mkdir /var/spool/postfix/blockchain_milter
chown postfix:postfix /var/spool/postfix/blockchain_milter
chmod g+w /var/spool/postfix/blockchain_milter
systemctl restart postfix.service