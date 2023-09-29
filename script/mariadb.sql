CREATE TABLE financials (
    year VARCHAR(10) NOT NULL,
    sales FLOAT NOT NULL,
    operatingProfit FLOAT NOT NULL,
    netIncome FLOAT NOT NULL,
    operatingProfitRatio FLOAT NOT NULL,
    netProfitRatio FLOAT NOT NULL,
    code VARCHAR(20) NOT NULL,
    symbolCode VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    sectorCode VARCHAR(20) NOT NULL,
    sectorName VARCHAR(50) NOT NULL
);

ALTER TABLE financials
ADD PRIMARY KEY (year, code);