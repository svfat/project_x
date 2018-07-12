FROM postgres:10

COPY apply_migrations.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/apply_migrations.sh
RUN ln -s /usr/local/bin/apply_migrations.sh /docker-entrypoint-initdb.d/

COPY sql /sql