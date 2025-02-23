CREATE TABLE Class (
    classID INTEGER PRIMARY KEY AUTOINCREMENT,
    className varchar(50) not null,
    -- 
    classType: varchar(50) not null, 
    duration INTEGER not null,
    classCapacity INTEGER not null,
    instructorID INTEGER,
    gymID INTEGER,
    foreign key (instructorID) references Instuctor(instructorID),
    foreign key (gymID) references GymFacility(gymID)
);

CREATE TABLE Instructor (
    instructorID INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(50) not null,
    specialty varchar(50),
    phone varchar(15),
    email varchar(50) not null
);

CREATE TABLE GymFacility (
    gymID INTEGER PRIMARY KEY AUTOINCREMENT,
    location varchar(100) not null,
    phone varchar(50),
    manager varchar(50)
);

CREATE TABLE Equipment (
    equipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(50) not null,
    type varchar(30),
    quantity INTEGER check (quantity >= 0),
    gymId INTEGER,
    foregin key (gymId) references GymFacility(gymId)
);

CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType varchar(50)
    cost numeric not null
);


CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberID INTEGER
    planId INTEGER
    amountPaid real not null,
    paymentDate DATE not null
    foregin key (memberId) references Member(memberId)
    foregin key (planId) references MembershipPlan(planId)
);

CREATE TABLE Attends (
    memberId INTEGER,
    classId INTEGER,
    attendanceDate DATE not null,
    foregin key (memberId) references Member(memberId)
    foregin key (classId) references Class(memberId)
);

