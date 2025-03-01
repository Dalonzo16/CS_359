
INSERT INTO Member VALUES(1,'Connor Powell','connorpowell@gmail.com','575-123-4567','123 connor street',24,'2025-02-27','2026-02-27');
INSERT INTO Member VALUES(2,'Olivia Piper','oliviapiper@gmail.com','111-111-1111','123 olivia street',30,'2025-02-27','2026-02-27');
INSERT INTO Member VALUES(3,'Brian Skinner','brianskinner@gmail.com','222-222-2222','123 brian street',22,'2025-02-27','2026-02-27');
INSERT INTO Member VALUES(4,'Owen Wallace','owenwallace@gmail.com','333-333-3333','123 owen street',47,'2025-02-27','2026-02-27');
INSERT INTO Member VALUES(5,'Natalie, Lyman','natalielyman@gmail.com','444-444-4444','123 natalie street',34,'2025-02-27','2026-02-27');


INSERT INTO Class VALUES(1,'Weights with Eduardo','Weights','1 Hour',10,1,1);
INSERT INTO Class VALUES(2,'Yoga with Ludwig','Yoga','30 Minutes',10,2,2);
INSERT INTO Class VALUES(3,'HIIT with Alena','HIIT','30 Minutes',10,3,3);
INSERT INTO Class VALUES(4,'Zumba with Devon','Zumba','45 Minutes',10,4,4);
INSERT INTO Class VALUES(5,'Yoga with John','Yoga','30 minutes',10,5,5);


INSERT INTO Instructor VALUES(1,'Eduardo Ceh-Varela','Weights','666-666-6666','eduardocehvarela@gmail.com');
INSERT INTO Instructor VALUES(2,'Ludwig Scherer','Yoga','777-777-7777','ludwigscherer@gmail.com');
INSERT INTO Instructor VALUES(3,'Alena Fisher','HIIT','888-888-8888','alenafisher@gmail.com');
INSERT INTO Instructor VALUES(4,'Devon Alonzo','Zumba','999-999-9999','devonalonzo@gmail.com');
INSERT INTO Instructor VALUES(5,'John Doe','Yoga','555-555-5555','johndoe@gmail.com');


INSERT INTO GymFacility VALUES(1,'Portales','575-111-1111','Lebron James');
INSERT INTO GymFacility VALUES(2,'Clovis','575-222-2222','Kobe Bryant');
INSERT INTO GymFacility VALUES(3,'Albuquerque','575-333-3333','Michael Jordan');
INSERT INTO GymFacility VALUES(4,'Santa Fe','575-444-4444','Shaquille O"Neal');
INSERT INTO GymFacility VALUES(5,'Las Cruces','575-555-5555','Wilt Chamberlain');


INSERT INTO Equipment VALUES(1,'Treadmill','Cardio',6,1);
INSERT INTO Equipment VALUES(2,'Bench Press','Strength',2,2);
INSERT INTO Equipment VALUES(3,'Yoga Mats','Flexibility',10,3);
INSERT INTO Equipment VALUES(4,'Massage Chair','Recovery',2,4);
INSERT INTO Equipment VALUES(5,'Squat Rack','Strength',4,5);


INSERT INTO MembershipPlan VALUES(1,'Annual',29.98999999999999844);
INSERT INTO MembershipPlan VALUES(2,'Annual',49.99000000000000198);
INSERT INTO MembershipPlan VALUES(3,'Monthly',10.99000000000000021);
INSERT INTO MembershipPlan VALUES(4,'Monthly',19.98999999999999843);
INSERT INTO MembershipPlan VALUES(5,'Annual',39.99000000000000198);


INSERT INTO Payment VALUES(1,1,2,49.99000000000000198,'2025-02-27');
INSERT INTO Payment VALUES(2,2,2,49.99000000000000198,'2025-02-27');
INSERT INTO Payment VALUES(3,3,1,29.98999999999999844,'2025-02-27');
INSERT INTO Payment VALUES(4,4,5,39.99000000000000198,'2025-02-27');
INSERT INTO Payment VALUES(5,5,1,29.98999999999999844,'2025-02-27');
CREATE TABLE Attends 


INSERT INTO Attends VALUES(1,2,'2025-03-01');
INSERT INTO Attends VALUES(1,3,'2025-03-03');
INSERT INTO Attends VALUES(2,1,'2025-03-01');
INSERT INTO Attends VALUES(2,4,'2025-03-04');
INSERT INTO Attends VALUES(4,5,'2025-03-02');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Member',5);
INSERT INTO sqlite_sequence VALUES('Instructor',5);
INSERT INTO sqlite_sequence VALUES('GymFacility',5);
INSERT INTO sqlite_sequence VALUES('MembershipPlan',5);
INSERT INTO sqlite_sequence VALUES('Class',5);
INSERT INTO sqlite_sequence VALUES('Equipment',5);
INSERT INTO sqlite_sequence VALUES('Payment',5);
COMMIT;
