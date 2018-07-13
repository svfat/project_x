BEGIN;
SELECT _v.register_patch('000-historical_prices', ARRAY ['000-extensions', '000-symbols'], NULL);

CREATE TABLE historical_prices (
  symbol_id UUID    NOT NULL REFERENCES symbols (id) ON DELETE CASCADE,
  date      DATE    NOT NULL,
  open      FLOAT   NOT NULL,
  high      FLOAT   NOT NULL,
  low       FLOAT   NOT NULL,
  close     FLOAT   NOT NULL,
  volume    INTEGER NOT NULL,
  PRIMARY KEY (symbol_id, date)
);

COMMIT;