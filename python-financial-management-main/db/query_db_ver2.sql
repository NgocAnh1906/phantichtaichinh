USE MASTER
CREATE DATABASE FinancialAnalysis
GO
USE FinancialAnalysis

-- Tạo bảng "Company"
CREATE TABLE Company (
    CompanyID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyName NVARCHAR(255),
    Address NVARCHAR(255),
    ContactNumber NVARCHAR(15)
);

-- Tạo bảng "FinancialStatement"
CREATE TABLE FinancialStatement (
    StatementID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyID INT,
    Year INT,
    Revenue FLOAT,
    Profit FLOAT,
    Assets FLOAT,
    Liabilities FLOAT,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID),
	CONSTRAINT FS_Company_Year UNIQUE (CompanyID, Year)
);

-- Tạo bảng "FinancialRatio"
CREATE TABLE FinancialRatio (
    RatioID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyID INT,
    Year INT,
    CurrentRatio FLOAT,
    DebtEquityRatio FLOAT,
    ProfitMargin FLOAT,
    ReturnOnAssets FLOAT,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID),
	CONSTRAINT FR_Company_Year UNIQUE (CompanyID, Year)
);

-- Tạo bảng "CashFlow"
CREATE TABLE CashFlow (
    CashFlowID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyID INT,
    Year INT,
    OperatingCashFlow FLOAT,
    InvestingCashFlow FLOAT,
    FinancingCashFlow FLOAT,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID),
	CONSTRAINT CF_Company_Year UNIQUE (CompanyID, Year)
);

-- Chèn dữ liệu vào bảng "Company"
SET IDENTITY_INSERT Company ON
INSERT INTO Company (CompanyID, CompanyName, Address, ContactNumber)
VALUES 
    (1, 'ABC Company', '123 Main Street', '123-456-7890'),
    (2, 'XYZ Corporation', '456 Elm Street', '987-654-3210'),
    (3, 'DEF Ltd', '789 Oak Avenue', '555-555-5555'),
    (4, 'GHI Industries', '321 Maple Road', '222-333-4444'),
    (5, 'JKL Group', '555 Pine Avenue', '111-222-3333'),
    (6, 'MNO Enterprises', '777 Walnut Boulevard', '444-444-4444'),
    (7, 'PQR Inc', '999 Cherry Lane', '777-888-9999'),
    (8, 'STU Corp', '222 Cedar Street', '222-111-0000'),
    (9, 'VWX Ltd', '888 Oak Street', '333-999-7777'),
    (10, 'YZA Corporation', '555 Elm Avenue', '444-666-2222');
SET IDENTITY_INSERT Company OFF

-- Chèn dữ liệu vào bảng "FinancialStatement"
SET IDENTITY_INSERT FinancialStatement ON
INSERT INTO FinancialStatement (StatementID, CompanyID, Year, Revenue, Profit, Assets, Liabilities)
VALUES 
    (1, 1, 2021, 1000000.00, 500000.00, 2000000.00, 1000000.00),
    (2, 2, 2021, 1500000.00, 800000.00, 3000000.00, 1500000.00),
    (3, 3, 2021, 1200000.00, 600000.00, 2500000.00, 1200000.00),
    (4, 4, 2021, 800000.00, 400000.00, 1800000.00, 800000.00),
    (5, 5, 2021, 2000000.00, 1000000.00, 4000000.00, 2000000.00),
    (6, 6, 2021, 3000000.00, 1500000.00, 6000000.00, 3000000.00),
    (7, 7, 2021, 1800000.00, 900000.00, 3500000.00, 1800000.00),
    (8, 8, 2021, 2200000.00, 1100000.00, 2800000.00, 1200000.00),
    (9, 9, 2021, 2500000.00, 1300000.00, 4200000.00, 2000000.00),
    (10, 10, 2021, 2800000.00, 1400000.00, 3200000.00, 1500000.00);
SET IDENTITY_INSERT FinancialStatement OFF

-- Chèn dữ liệu vào bảng "FinancialRatio"
SET IDENTITY_INSERT FinancialRatio ON
INSERT INTO FinancialRatio (RatioID, CompanyID, Year, CurrentRatio, DebtEquityRatio, ProfitMargin, ReturnOnAssets)
VALUES 
    (1, 1, 2021, 2.5, 0.8, 0.25, 0.15),
    (2, 2, 2021, 3.0, 0.6, 0.20, 0.12),
    (3, 3, 2021, 2.2, 0.7, 0.18, 0.10),
    (4, 4, 2021, 2.0, 0.9, 0.22, 0.13),
    (5, 5, 2021, 2.8, 0.5, 0.30, 0.18),
    (6, 6, 2021, 1.9, 0.7, 0.15, 0.08),
    (7, 7, 2021, 2.3, 0.6, 0.28, 0.17),
    (8, 8, 2021, 1.8, 0.9, 0.20, 0.12),
    (9, 9, 2021, 2.6, 0.8, 0.25, 0.15),
    (10, 10, 2021, 2.9, 0.5, 0.32, 0.20);
SET IDENTITY_INSERT FinancialRatio OFF

-- Chèn dữ liệu vào bảng "CashFlow"
SET IDENTITY_INSERT CashFlow ON
INSERT INTO CashFlow (CashFlowID, CompanyID, Year, OperatingCashFlow, InvestingCashFlow, FinancingCashFlow)
VALUES 
    (1, 1, 2021, 500000.00, -200000.00, -300000.00),
    (2, 2, 2021, 800000.00, -300000.00, -500000.00),
    (3, 3, 2021, 600000.00, -250000.00, -350000.00),
    (4, 4, 2021, 400000.00, -150000.00, -250000.00),
    (5, 5, 2021, 900000.00, -400000.00, -500000.00),
    (6, 6, 2021, 1200000.00, -500000.00, -700000.00),
    (7, 7, 2021, 700000.00, -200000.00, -400000.00),
    (8, 8, 2021, 600000.00, -300000.00, -500000.00),
    (9, 9, 2021, 800000.00, -400000.00, -600000.00),
    (10, 10, 2021, 1000000.00, -500000.00, -700000.00);
SET IDENTITY_INSERT CashFlow OFF


USE MASTER
-- Tạo người dùng mới
CREATE LOGIN UserPyDB WITH PASSWORD = '123';

-- Tạo người dùng tương ứng trong cơ sở dữ liệu
USE FinancialAnalysis
CREATE USER UserPyDB FOR LOGIN UserPyDB;

-- Cấp quyền select, insert, update và delete cho tất cả các bảng trong cơ sở dữ liệu
USE FinancialAnalysis;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO UserPyDB;
