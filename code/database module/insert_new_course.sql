DELIMITER //
DROP PROCEDURE IF EXISTS insert_new_course;
CREATE PROCEDURE insert_new_course(IN no INT, IN name VARCHAR(20), IN credit FLOAT, IN full_time INT,
                                   IN type VARCHAR(20), IN time VARCHAR(20), IN place VARCHAR(20), IN major_id INT)
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    INSERT INTO course (cno, cname, ccredit, cfull_time, ctype, ctime, cplace, cmajor)
    VALUES (no, name, credit, full_time, type, time, place, major_id);
    if flag = 1 THEN
        ROLLBACK;
        SELECT 'fail';
    ELSE
        COMMIT;
        SELECT 'success';
    end if;
END //
DELIMITER ;