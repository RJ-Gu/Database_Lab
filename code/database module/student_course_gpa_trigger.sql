# 单门课 GPA 自动计算
# 换算公式：
# 100-95: 4.3
# 94-90: 4.0
# 89-85: 3.7
# 84-82: 3.3
# 81-78: 3.0
# 77-75: 2.7
# 74-72: 2.3
# 71-68: 2.0
# 67-65: 1.7
# 64: 1.5
# 63-61: 1.3
# 60: 1.0
# 59-0: 0.0

DELIMITER //
DROP TRIGGER IF EXISTS student_course_gpa_trigger;
CREATE TRIGGER student_course_gpa_trigger BEFORE INSERT ON student_course FOR EACH ROW
BEGIN
    DECLARE gpa FLOAT;
    IF NEW.grade is NULL THEN
        SET gpa = NULL;
    ELSEIF NEW.grade >= 95 THEN
        SET gpa = 4.3;
    ELSEIF NEW.grade >= 90 THEN
        SET gpa = 4.0;
    ELSEIF NEW.grade >= 85 THEN
        SET gpa = 3.7;
    ELSEIF NEW.grade >= 82 THEN
        SET gpa = 3.3;
    ELSEIF NEW.grade >= 78 THEN
        SET gpa = 3.0;
    ELSEIF NEW.grade >= 75 THEN
        SET gpa = 2.7;
    ELSEIF NEW.grade >= 72 THEN
        SET gpa = 2.3;
    ELSEIF NEW.grade >= 68 THEN
        SET gpa = 2.0;
    ELSEIF NEW.grade >= 65 THEN
        SET gpa = 1.7;
    ELSEIF NEW.grade >= 64 THEN
        SET gpa = 1.5;
    ELSEIF NEW.grade >= 61 THEN
        SET gpa = 1.3;
    ELSEIF NEW.grade >= 60 THEN
        SET gpa = 1.0;
    ELSE
        SET gpa = 0.0;
    END IF;
    SET NEW.gpa = gpa;
    END //
DELIMITER ;