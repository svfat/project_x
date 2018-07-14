BEGIN;
SELECT _v.register_patch('000-insider_trade', ARRAY ['000-extensions', '000-ticker'], NULL);

CREATE TABLE insider (
  id   TEXT NOT NULL PRIMARY KEY,
  name TEXT
);

CREATE TABLE insider_trade (
  id               UUID PRIMARY KEY   DEFAULT gen_random_uuid(),
  insider_id       TEXT    NOT NULL REFERENCES insider (id) ON DELETE CASCADE,
  relation         TEXT,
  last_date        DATE    NOT NULL,
  transaction_type TEXT,
  owner_type       TEXT,
  shares_traded    INTEGER NOT NULL,
  last_price       FLOAT,
  shares_held      INTEGER NOT NULL,
  ticker_id        UUID    NOT NULL REFERENCES ticker (id) ON DELETE CASCADE
);

COMMIT;