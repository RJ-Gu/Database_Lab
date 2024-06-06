DELIMITER //
DROP PROCEDURE IF EXISTS insert_new_student;
CREATE PROCEDURE insert_new_student(IN no INT, IN name VARCHAR(20), IN sex CHAR(2), IN id CHAR(18), IN phone CHAR(11),
                                    IN ethics VARCHAR(20), IN place VARCHAR(20), IN level VARCHAR(20), IN major INT)
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    INSERT INTO student (sno, sname, ssex, sid, sphone, sethics, splace, slevel, smajor)
        VALUES (no, name, sex, id, phone, ethics, place, level, major);
    if flag = 1 THEN
        ROLLBACK;
        SELECT 'fail';
    ELSE
        COMMIT;
        SELECT 'success';
    end if;
END //
DELIMITER ;