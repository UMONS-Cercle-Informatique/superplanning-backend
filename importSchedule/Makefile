## This Makefile must only be used for testing. It creates a local directory for
## the database.
## See Makefile.conf for configuration.

include Makefile.conf

ENV_PSQL          := PGHOST=$(DB_HOST) PGDATABASE=$(DB_NAME) PGPORT=$(DB_PORT) \
                     PGUSER=$(DB_USER) PGPASSWORD=$(DB_PASSWORD)

pg_dump = pg_dump

# Rule to get the pg_ctl binary.
ifeq ($(shell psql --version 2> /dev/null),)
$(error "PostgreSQL is not installed")
else
PSQL_VERSION := $(shell psql --version | cut -d' ' -f 3 | cut -d'.' -f 1-2)
pg_ctl       := $(shell \
                  sh -c "which pg_ctl" || \
                  sh -c "echo /usr/lib/postgresql/$(PSQL_VERSION)/bin/pg_ctl")
endif

## ---------------------------------------------------------------------
## Here some rules to easily manage the database.
# - db-init:
#   Initialise the database. It creates the directory PSQL_DIR and
#   start the database.
#
# - db-start:
#   Start the database.
#
# - db-stop:
#   Stop the database.
#
# - db-status:
#   Get the database status.
#
# - db-create:
#   Create the database and use UNICODE.
#
# - db-schema:
#   Execute the SQL file contained in the PSQL_FILE variable to create the
#   schema and the tables.
#
# - db-drop:
#   Drop the database but doesn't remove the database directory PSQL_DIR.
#
# - db-psql:
#   Connect to the database.
#
# - db-delete:
#   Stop the database (without error if it's not running) and remove
#   the database directory containing all database data.

##----------------------------------------------------------------------

$(PSQL_DIR):
	-mkdir -p $@

db-init: $(PSQL_DIR)
	$(pg_ctl) initdb -D $(PSQL_DIR)
	echo unix_socket_directories = \'/tmp\' >> $(PSQL_DIR)/postgresql.conf
	$(pg_ctl) -o "-p $(DB_PORT)" -D $(PSQL_DIR) -l $(PSQL_LOG) start

db-start:
	$(pg_ctl) -o "-p $(DB_PORT)" -D $(PSQL_DIR) -l $(PSQL_LOG) start

db-stop:
	$(pg_ctl) -D $(PSQL_DIR) -l $(PSQL_LOG) stop

db-status:
	$(pg_ctl) -D $(PSQL_DIR) -l $(PSQL_LOG) status

db-delete:
	$(pg_ctl) -D $(PSQL_DIR) -l $(PSQL_LOG) stop || true
	rm -rf $(PSQL_DIR)

db-snapshot:
	@echo "# Creating $(DB_SNAPSHOT)"
	$(ENV_PSQL) $(pg_dump) --clean --create --no-owner --encoding=utf8 \
        $(DB_NAME) | gzip > $(DB_SNAPSHOT)

db-create:
	$(ENV_PSQL) createdb --encoding UNICODE $(DB_NAME)

db-schema:
	$(ENV_PSQL) psql -d $(DB_NAME) -f $(PSQL_FILE)

db-drop:
	$(ENV_PSQL) dropdb $(DB_NAME)

db-psql:
	$(ENV_PSQL) psql $(DB_NAME)

##----------------------------------------------------------------------
