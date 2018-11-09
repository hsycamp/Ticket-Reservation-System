CREATE TABLE buildings (
	id int(11) AUTO_INCREMENT,
	name varchar(200),
	location varchar(200),
	capacity int(11),
	assigned int(11),
	PRIMARY KEY (`id`)
) ;

CREATE TABLE audiences (
  id int(11) AUTO_INCREMENT,
  name varchar(200),
  gender char(1),
  age int(11),
  PRIMARY KEY (`id`)
) ;

CREATE TABLE performances (
  id int(11) AUTO_INCREMENT,
  name varchar(200),
  type varchar(200),
  price int(11),
  booked int(11) DEFAULT 0,
  building_id int(11),
  PRIMARY KEY (id),
  FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE SET NULL
) ;


CREATE TABLE books (
  seat_number int(200) DEFAULT NULL,
  audience_id int(11) DEFAULT NULL,
  performance_id int(11) DEFAULT NULL,
  PRIMARY KEY (seat_number,performance_id),
  FOREIGN KEY (audience_id) REFERENCES audiences(id) ON DELETE CASCADE,
  FOREIGN KEY (performance_id) REFERENCES performances(id) ON DELETE CASCADE
) ;