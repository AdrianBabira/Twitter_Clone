#!/bin/sh
mkdir -p /var/lib/postgresql/logs
chmod 755 /var/lib/postgresql/logs
psql -U admin -tc "SELECT 1 FROM pg_database WHERE datname = 'twitter_clone_db'" | grep -q 1 || psql -U admin -c "CREATE DATABASE twitter_clone_db"
