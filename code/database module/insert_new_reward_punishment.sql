DELIMITER //
DROP PROCEDURE IF EXISTS insert_new_reward_punishment;
CREATE PROCEDURE insert_new_reward_punishment(IN no INT, IN content VARCHAR(20), IN type VARCHAR(20))
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET flag = 1;

    START TRANSACTION;
    INSERT INTO reward_punish (rno, rcontent, rtype)
    VALUES (no, content, type);
    if flag = 1 THEN
        ROLLBACK;
        SELECT 'fail';
    ELSE
        COMMIT;
        SELECT 'success';
    end if;
END //