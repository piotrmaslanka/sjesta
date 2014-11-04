CREATE TABLE datasets
(
  id bigserial NOT NULL,
  data bytea NOT NULL,
  CONSTRAINT pk_datasets PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE TABLE jobs
(
  id bigserial NOT NULL, -- Job ID
  scheduled_by character varying(256) NOT NULL, -- Name of the user who scheduled the job
  scheduled_at bigint NOT NULL, -- UNIX timestamp of when was the job scheduled
  completed_on bigint, -- UNIX timestamp of when the job was completed
  return_code integer, -- Return code of the job
  description text, -- Job description
  started_at bigint, -- UNIX timestamp of when job execution started
  stdin bigint, -- Dataset of standard input
  stdout bigint, -- Dataset of standard output
  stderr bigint, -- Dataset of standard error
  program text NOT NULL, -- Program + args to execute as the job
  niceness smallint, -- Priority of job. The lower, the better
  CONSTRAINT pk_jobs PRIMARY KEY (id),
  CONSTRAINT fk_jobs_stderr FOREIGN KEY (stderr)
      REFERENCES datasets (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_jobs_stdin FOREIGN KEY (stdin)
      REFERENCES datasets (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_jobs_stdout FOREIGN KEY (stdout)
      REFERENCES datasets (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);

CREATE INDEX fki_jobs_stderr
  ON jobs
  USING btree
  (stderr);

CREATE INDEX fki_jobs_stdin
  ON jobs
  USING btree
  (stdin);

CREATE INDEX fki_jobs_stdout
  ON jobs
  USING btree
  (stdout);

CREATE INDEX i_jobs_completed_on
  ON jobs
  USING btree
  (completed_on)
  WHERE completed_on IS NOT NULL;

