
INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate) 
VALUES 
('Connor Powell','connorpowell@gmail.com','575-123-4567','123 connor street',24,'2025-02-27','2026-02-27'),
('Olivia Piper','oliviapiper@gmail.com','111-111-1111','123 olivia street',30,'2025-02-27','2026-02-27'),
('Brian Skinner','brianskinner@gmail.com','222-222-2222','123 brian street',22,'2025-02-27','2026-02-27'),
('Owen Wallace','owenwallace@gmail.com','333-333-3333','123 owen street',47,'2025-02-27','2026-02-27'),
('Natalie Lyman','natalielyman@gmail.com','444-444-4444','123 natalie street',34,'2025-02-27','2026-02-27');

INSERT INTO Class (className, classType, duration, classCapacity, instructorID, gymID) 
VALUES
('Weights with Eduardo','Weights',60,10,1,1),
('Yoga with Ludwig','Yoga',30,10,2,2),
('HIIT with Alena','HIIT',30,10,3,3),
('Zumba with Devon','Zumba',45,10,4,4),
('Yoga with John','Yoga',30,10,5,5);

INSERT INTO Instructor (name, specialty, phone, email) 
VALUES
('Eduardo Ceh-Varela','Weights','666-666-6666','eduardocehvarela@gmail.com'),
('Ludwig Scherer','Yoga','777-777-7777','ludwigscherer@gmail.com'),
('Alena Fisher','HIIT','888-888-8888','alenafisher@gmail.com'),
('Devon Alonzo','Zumba','999-999-9999','devonalonzo@gmail.com'),
('John Doe','Yoga','555-555-5555','johndoe@gmail.com');

INSERT INTO GymFacility (location, phone, manager) 
VALUES
('Portales','575-111-1111','Lebron James'),
('Clovis','575-222-2222','Kobe Bryant'),
('Albuquerque','575-333-3333','Michael Jordan'),
('Santa Fe','575-444-4444','Shaquille O''Neal'),
('Las Cruces','575-555-5555','Wilt Chamberlain');

INSERT INTO Equipment (name, classType, quantity, gymID)
VALUES
('Treadmill','Cardio',6,1),
('Bench Press','Strength',2,2),
('Yoga Mats','Flexibility',10,3),
('Massage Chair','Recovery',2,4),
('Squat Rack','Strength',4,5);

INSERT INTO MembershipPlan(planType, cost)
VALUES
('Annual',29.98),
('Annual',49.99),
('Monthly',10.99),
('Monthly',19.98),
('Annual',39.99);

INSERT INTO Payment (memberID, planId, amountPaid, paymentDate)
VALUES
(1,2,49.99,'2025-02-27'),
(2,2,49.99,'2025-02-27'),
(3,1,29.98,'2025-02-27'),
(4,5,39.99,'2025-02-27'),
(5,1,29.98,'2025-02-27');

INSERT INTO Attends (memberID, classID, attendanceDate)
VALUES
(1,2,'2025-03-01'),
(1,3,'2025-03-03'),
(2,1,'2025-03-01'),
(2,4,'2025-03-04'),
(4,5,'2025-03-02');

COMMIT;
