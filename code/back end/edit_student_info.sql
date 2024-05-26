DELIMITER //
CREATE PROCEDURE edit_student_info(IN no INT, IN name VARCHAR(20), IN sex CHAR(2), IN id CHAR(18), phone CHAR(11),
                                   ethics VARCHAR(20), place VARCHAR(20), level VARCHAR(20))
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    UPDATE student SET sname = name, ssex = sex, sid = id, sphone = phone, sethics = ethics, splace = place, slevel = level
    WHERE sno = no;
    if flag = 1 then
        ROLLBACK;
        SELECT 'fail';
    else
        COMMIT;
        SELECT 'success';
    end if;
end //
DELIMITER ;

CALL edit_student_info(10001, '张一', '男', '110101200001011234', '13812345678', '汉族', '北京', '本科');
