DELIMITER //
DROP FUNCTION IF EXISTS calculate_student_total_gpa;
CREATE FUNCTION calculate_student_total_gpa(sno INT)
RETURNS FLOAT
READS SQL DATA
BEGIN
    DECLARE total_credits FLOAT;
    DECLARE weighted_points FLOAT;
    DECLARE total_gpa FLOAT;

    # 给定学号，计算学生上课的总学分
    SELECT SUM(c.ccredit)
    INTO total_credits
    FROM course c
    INNER JOIN student_course sc ON c.cno = sc.cno
    WHERE sc.sno = sno;

    # 计算学生上课学分与gpa乘积
    SELECT SUM(c.ccredit * sc.gpa)
    INTO weighted_points
    FROM course c
    INNER JOIN student_course sc ON c.cno = sc.cno
    WHERE sc.sno = sno;

    # 计算学生的加权gpa
    IF total_credits > 0 THEN
        SET total_gpa = weighted_points / total_credits;
    ELSE
        SET total_gpa = 0;
    END IF;

    RETURN total_gpa;

END //
DELIMITER ;

SELECT calculate_student_total_gpa(10001);