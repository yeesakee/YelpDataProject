CREATE TABLE Zipcode_data (
  zid INTEGER,
  median_income INTEGER,
  mean_income INTEGER,
  population INTEGER,
  PRIMARY KEY(zid)
  );

CREATE TABLE state (
  state_id VARCHAR(2) UNIQUE,
  PRIMARY KEY(state_id)
  );
  
CREATE TABLE City (
  state_id VARCHAR(2),
  city_name CHAR(100),
  city_id VARCHAR(103) UNIQUE,
  FOREIGN KEY(state_id) REFERENCES State(state_id),
  PRIMARY KEY(city_id)
  );
  
CREATE TABLE CityZip (
  city_id char(100),
  zid INTEGER,
  FOREIGN KEY(city_id) REFERENCES city(city_id),
  FOREIGN KEY(zid) REFERENCES zipcode_data(zid),
  PRIMARY KEY(city_id, zid)
  );


CREATE TABLE Categories(
  category_name VARCHAR(200),
  PRIMARY KEY(category_name)
 );

CREATE TABLE Business(
  bid VARCHAR(100),
  city_id VARCHAR(103) NOT NULL,
  zipcode_id INTEGER NOT NULL,
  name VARCHAR(100),
  address VARCHAR(200),
  stars FLOAT,
  review_count INTEGER,
  numCheckins INTEGER,
  reviewRating FLOAT,
  longitude FLOAT,
  latitude FLOAT,
  PRIMARY KEY(bid),
  FOREIGN KEY(city_id) REFERENCES City(city_id),
  FOREIGN KEY(zipcode_id) REFERENCES zipcode_data(zid)
 );
 
 CREATE TABLE BusinessCategory(
 	bid VARCHAR(100),
	category_name varchar(100),
 	FOREIGN KEY(bid) REFERENCES Business(bid),
	FOREIGN KEY(category_name) REFERENCES Categories(category_name),
	PRIMARY KEY(bid, category_name)
 );

CREATE TABLE Check_in(
  bid VARCHAR(100) NOT NULL,
  checkin_count INTEGER,
  FOREIGN KEY(bid) REFERENCES Business(bid)
 );

CREATE TABLE Reviews(
  bid VARCHAR(100) NOT NULL,
  stars INTEGER,
  text VARCHAR(5000),
  FOREIGN KEY(bid) REFERENCES Business(bid)
 );