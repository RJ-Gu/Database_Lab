DELIMITER //
DROP PROCEDURE IF EXISTS edit_course_info;
CREATE PROCEDURE edit_course_info(IN no INT, IN name VARCHAR(20), IN credit INT, IN full_time INT, IN type VARCHAR(20),
                                  IN time VARCHAR(20), IN place VARCHAR(20), IN major INT)
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    UPDATE course SET cname = name, ccredit = credit, cfull_time = full_time, ctype = type, ctime = time, cplace = place, cmajor = major
    WHERE cno = no;
    IF flag = 1 THEN
        ROLLBACK;
        SELECT 'fail';
    ELSE
        COMMIT;
        SELECT 'success';
    END IF;
END //
DELIMITER ;