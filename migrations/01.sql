CREATE SCHEMA IF NOT EXISTS hose;

SET search_path TO hose;

CREATE TABLE IF NOT EXISTS hose.user (
  id_user SERIAL PRIMARY KEY,
  name VARCHAR(256) UNIQUE,
  email TEXT UNIQUE,
  hashed_password VARCHAR,
  date_joined TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hose.hose (
  id_hose SERIAL PRIMARY KEY,
  id_user_a BIGINT REFERENCES hose.user(id_user),
  id_user_b BIGINT REFERENCES hose.user(id_user),
  date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  CHECK (id_user_a < id_user_b)
);

CREATE TABLE IF NOT EXISTS hose.content_type (
  id_content_type SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS hose.content (
  id_content SERIAL PRIMARY KEY,
  id_hose BIGINT REFERENCES hose.hose(id_hose),
  id_user_added BIGINT REFERENCES hose.user(id_user),
  date_added TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  source_path TEXT,
  id_content_type BIGINT REFERENCES content_type(id_content_type)
);