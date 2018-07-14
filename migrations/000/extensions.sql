BEGIN;
SELECT _v.register_patch('000-extensions', NULL, NULL);

CREATE EXTENSION pgcrypto;

COMMIT;