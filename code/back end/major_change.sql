DELIMITER //
CREATE PROCEDURE major_change(IN no INT, IN major INT)
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    UPDATE student SET smajor = major WHERE sno = no;
    if flag = 1 then
        ROLLBACK;
        SELECT 'fail';
    else
        COMMIT;
        SELECT 'success';
    end if;
end //
DELIMITER ;

CALL major_change(10001, 40006);