BEGIN;
SELECT _v.register_patch('000-ticker', ARRAY ['000-extensions'], NULL);

CREATE TABLE ticker (
  id     UUID PRIMARY KEY   DEFAULT gen_random_uuid(),
  symbol TEXT UNIQUE NOT NULL
);

COMMIT;