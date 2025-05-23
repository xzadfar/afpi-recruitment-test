CREATE SCHEMA IF NOT EXISTS DWH;

CREATE TABLE IF NOT EXISTS DWH.NPP (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(9) UNIQUE,
    npp DOUBLE PRECISION 
);

CREATE TABLE IF NOT EXISTS DWH.TRX (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(9) UNIQUE,
    trx INTEGER
);

CREATE VIEW DWH.TICKET_SIZE AS 
SELECT 
    ROW_NUMBER() OVER (ORDER BY TRX.id) AS id,
    TRX.bulan AS bulan, 
    TRX.trx/NPP.npp AS ticket_size 
FROM DWH.TRX 
INNER JOIN DWH.NPP ON NPP.bulan = TRX.bulan 
order by TRX.id;