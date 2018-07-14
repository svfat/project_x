BEGIN;
SELECT _v.register_patch('000-historical_price', ARRAY ['000-extensions', '000-ticker'], NULL);

CREATE TABLE historical_price (
  ticker_id UUID    NOT NULL REFERENCES ticker (id) ON DELETE CASCADE,
  date      DATE    NOT NULL,
  open      FLOAT   NOT NULL,
  high      FLOAT   NOT NULL,
  low       FLOAT   NOT NULL,
  close     FLOAT   NOT NULL,
  volume    INTEGER NOT NULL,
  PRIMARY KEY (ticker_id, date)
);

COMMIT;