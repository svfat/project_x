BEGIN;
SELECT _v.register_patch('000-symbols', ARRAY ['000-extensions'], NULL);

CREATE TABLE symbols (
  id     UUID PRIMARY KEY   DEFAULT gen_random_uuid(),
  symbol TEXT UNIQUE NOT NULL
);

COMMIT;