CREATE TABLE STUDENTS(
   GRADE_NUM NUMBER NOT NULL,
   FNAME VARCHAR2 (25) NOT NULL,
   LNAME VARCHAR2 (25) NOT NULL,
   DOB DATE NOT NULL,
   GENDER VARCHAR2 (15) NOT NULL,
   NATIONALITY VARCHAR2 (25) NOT NULL,
   STATUS VARCHAR2 (10) NOT NULL,
   MAJOR VARCHAR2 (20) NOT NULL,
   PRIMARY KEY (GRADE_NUM)
);

INSERT INTO STUDENTS VALUES (72269035, 'John', 'Smith', '05-JAN-2000', 'Male', 'Canadian', 'Placed', 'Computer Science');
INSERT INTO STUDENTS VALUES (88452883, 'Mary', 'Williams', '08-FEB-2001', 'Female', 'Canadian', 'Placed', 'Music');
INSERT INTO STUDENTS VALUES (26443806, 'Jose', 'Garcia', '12-APR-2000', 'Male', 'Mexican', 'Waiting', 'Physics');
INSERT INTO STUDENTS VALUES (72574765, 'Bob', 'Miller', '25-MAY-2000', 'Male', 'American', 'Placed', 'Engineering');
INSERT INTO STUDENTS VALUES (60270768, 'Jennifer', 'Johnson', '19-SEP-2000', 'Female', 'Canadian', 'Waiting', 'Biology');

--Question 1
DECLARE
stu_fname VARCHAR2(20);
stu_lname VARCHAR2(20);
stu_num NUMBER:=72269035;
stu_dob DATE;
stu_str char(35):='The information of the student is: ';
stu_status varchar2(10);
if_status boolean;
BEGIN
Select fname,lname,dob,status Into stu_fname,stu_lname,stu_dob,stu_status From STUDENTS
WHERE grade_num=stu_num;
if stu_status='Placed'
then if_status:=true;
else if_status:=false;
End if;
DBMS_OUTPUT.PUT_LINE(stu_str||'First Name: '||stu_fname||' ,Last Name: '||stu_lname||', DOB: '||stu_dob||', Status: '||case when if_status=true then 'Is Placed' else 'Is Waiting' end);
END;

--Question 2
CREATE OR REPLACE PROCEDURE STU_INFO(STU_NUM NUMBER)
AS
stu_lname students.lname%TYPE;
stu_fname students.fname%TYPE;
stu_status students.STATUS%TYPE;
Begin
select fname,lname,status into stu_fname,stu_lname,stu_status From STUDENTS 
WHERE grade_num=stu_num; 
DBMS_OUTPUT.PUT_LINE('Student Information: '||'First Name: '||stu_fname||', Last Name: '||stu_lname||', Status: '||stu_status); 
End;

BEGIN
    STU_INFO(26443806);
END;

--Question 3
Declare
stu_num students.GRADE_NUM%TYPE:=88452883;  
stu_status students.STATUS%TYPE; 
stu_dob students.dob%TYPE;
DateDiff number;
Begin
Select DOB,Status into stu_dob,stu_status from Students where stu_num=GRADE_NUM;
Select floor((CURRENT_DATE-stu_dob)/365) into DateDiff from dual;
--DBMS_OUTPUT.PUT_LINE(DateDiff);
If DateDiff>21
Then 
    If stu_status='Placed'
    Then DBMS_OUTPUT.PUT_LINE('Student '||stu_num||' is over 21 and placed.');
    Else DBMS_OUTPUT.PUT_LINE('Student '||stu_num||' is over 21 and waiting.');
    End if;
Else 
    If stu_status='Placed'
    Then DBMS_OUTPUT.PUT_LINE('Student '||stu_num||' is under 22 and placed.');
    Else DBMS_OUTPUT.PUT_LINE('Student '||stu_num||' is over 22 and waiting.');
    End if;
End if;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('STUDENT '||stu_num||' NOT FOUND.');
End;

--Question 7
CREATE OR REPLACE FUNCTION STUDENT_STATUS(STU_NUM IN STUDENTS.GRADE_NUM%TYPE)
RETURN VARCHAR2 AS
	STU_STATUS VARCHAR2(10);
BEGIN
	SELECT STATUS INTO STU_STATUS FROM STUDENTS
	WHERE GRADE_NUM = STU_NUM;
	RETURN STU_STATUS;
END;

DECLARE
	S_STATUS VARCHAR2(10);
BEGIN
	S_STATUS := STUDENT_STATUS(72269035);
	DBMS_OUTPUT.PUT_LINE('The student''s current status is: '||S_STATUS);
END;

--Question 8
CREATE OR REPLACE PACKAGE NEW_STUDENT AS
	PROCEDURE ADD_STUDENT(STU_RECORD IN STUDENTS%ROWTYPE);
	FUNCTION STUDENT_INFO(STU_NUM IN STUDENTS.GRADE_NUM%TYPE) RETURN STUDENTS%ROWTYPE;
END NEW_STUDENT;
/
CREATE OR REPLACE PACKAGE BODY NEW_STUDENT AS
	PROCEDURE ADD_STUDENT(STU_RECORD IN STUDENTS%ROWTYPE)
	AS
	BEGIN
		INSERT INTO STUDENTS VALUES(STU_RECORD.GRADE_NUM, STU_RECORD.FNAME, STU_RECORD.LNAME, STU_RECORD.DOB, STU_RECORD.GENDER, STU_RECORD.NATIONALITY, STU_RECORD.STATUS, STU_RECORD.MAJOR);
		COMMIT;
	END ADD_STUDENT;

	FUNCTION STUDENT_INFO(STU_NUM IN STUDENTS.GRADE_NUM%TYPE)
	RETURN STUDENTS%ROWTYPE
	AS
	GET_RECORD STUDENTS%ROWTYPE;
	BEGIN
		SELECT * INTO GET_RECORD FROM STUDENTS WHERE GRADE_NUM=STU_NUM;
		RETURN GET_RECORD;
	END STUDENT_INFO;
END NEW_STUDENT;

DECLARE
    STU_RECORD STUDENTS%ROWTYPE;
    GET_RECORD STUDENTS%ROWTYPE;
BEGIN
	STU_RECORD.GRADE_NUM:=35893025;
	STU_RECORD.FNAME:='Ian';
	STU_RECORD.LNAME:='Murray';
	STU_RECORD.DOB:='23-MAY-2000';
	STU_RECORD.GENDER:='Male';
	STU_RECORD.NATIONALITY:='Canadian';
	STU_RECORD.STATUS:='Waiting';
	STU_RECORD.MAJOR:='Psychology';
	NEW_STUDENT.ADD_STUDENT(STU_RECORD);
	GET_RECORD:=NEW_STUDENT.STUDENT_INFO(35893025);
	DBMS_OUTPUT.PUT_LINE('Student''s name: '||GET_RECORD.FNAME||' '||GET_RECORD.LNAME);
	DBMS_OUTPUT.PUT_LINE('Student''s date of birth: '||GET_RECORD.DOB);
	DBMS_OUTPUT.PUT_LINE('Student''s gender: '||GET_RECORD.GENDER);
	DBMS_OUTPUT.PUT_LINE('Student''s nationality: '||GET_RECORD.NATIONALITY);
	DBMS_OUTPUT.PUT_LINE('Student''s status: '||GET_RECORD.STATUS);
	DBMS_OUTPUT.PUT_LINE('Student''s major: '||GET_RECORD.MAJOR);
END;

--Question 9
CREATE OR REPLACE TRIGGER CHANGE_MAJOR
AFTER UPDATE ON STUDENTS
FOR EACH ROW
BEGIN
	DBMS_OUTPUT.PUT_LINE('Old major: '|| :OLD.MAJOR);
	DBMS_OUTPUT.PUT_LINE('New major: '|| :NEW.MAJOR);
	DBMS_OUTPUT.PUT_LINE('Date of change: '|| SYSDATE);
END;

UPDATE STUDENTS SET MAJOR = 'Biochemistry' WHERE GRADE_NUM = 60270768;
