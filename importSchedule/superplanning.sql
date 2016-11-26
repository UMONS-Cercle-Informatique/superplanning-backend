CREATE SCHEMA IF NOT EXISTS superplanning;

CREATE TABLE IF NOT EXISTS superplanning.type
(
  id    bigserial             primary key,
  name  VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.course

(
  id          bigserial             primary key,
  small_name  VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.teacher
(
  id    bigserial             primary key,
  name  VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.unit
(
  id    bigserial             primary key,
  name  VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.location
(
  id        bigserial             primary key,
  location  VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.schedule
(
  id              bigserial           primary key,
  id_course       bigint    NOT NULL  references superplanning.course(id),
  id_type         bigint    NOT NULL  references superplanning.type(id),
  begin_timestamp timestamp NOT NULL,
  end_timestamp   timestamp NOT NULL,
  canceled        boolean   NOT NULL
);

CREATE TABLE IF NOT EXISTS superplanning.schedule_teacher
(
  id_schedule       bigint    NOT NULL  references superplanning.schedule(id),
  id_teacher        bigint    NOT NULL  references superplanning.teacher(id)
);

CREATE TABLE IF NOT EXISTS superplanning.schedule_unit
(
  id_schedule       bigint    NOT NULL  references superplanning.schedule(id),
  id_unit           bigint    NOT NULL  references superplanning.unit(id)
);


CREATE TABLE IF NOT EXISTS superplanning.schedule_location
(
  id_schedule       bigint    NOT NULL  references superplanning.schedule(id),
  id_location       bigint    NOT NULL  references superplanning.location(id)
)
