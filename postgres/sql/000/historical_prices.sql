BEGIN;
SELECT _v.register_patch('000-historical_prices', ARRAY ['000-extensions', '000-symbols'], NULL);

CREATE TABLE historical_prices (
  id        UUID PRIMARY KEY   DEFAULT gen_random_uuid(),
  symbol_id UUID NOT NULL REFERENCES symbols (id) ON DELETE CASCADE
);

COMMIT;