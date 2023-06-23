DROP INDEX categName on CATEGORY;
DROP INDEX custUserName on CUSTOMER;
DROP INDEX adminUserName on ADMIN;
DROP INDEX customerName on CUSTOMER;
DROP INDEX adminName on ADMIN;
DROP INDEX prodName on PRODUCT;

create unique index categName on CATEGORY(Name);

create unique index custUserName on CUSTOMER(Username);

create unique index adminUserName on ADMIN(Username);

create index customerName on CUSTOMER(Name);

create index adminName on ADMIN(Name);

create index prodName on PRODUCT(Name);