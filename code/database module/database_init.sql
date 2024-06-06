# 创建学籍管理系统数据库的基本表
# 1. 学生：表示学生实体。包含属性：学号（主码）、姓名、性别、身份证号、手机号、民族、籍贯、
# 学历层次。
# 2. 教师：表示教师实体。包含属性：教师编号（主码）、姓名、性别、身份证号、手机号、所在学
# 院、职称。
# 3. 课程：表示课程实体。包含属性：课程号（主码）、课程名称、开课专业、开课学院、学分、课
# 时、课程类型、上课时间与地点。
# 4. 专业：表示学生所在的专业实体。包含属性：专业号（主码）、专业名称、所属院系、要求总学
# 分。
# 5. 院系：表示教师所在的、专业所属的院系实体。包含属性：院系号（主码）、院系名、院长。
# 6. 奖惩：表示学生的奖惩实体。包含属性：奖惩编号（主码）、奖惩内容、奖励或惩罚。
# 7. 学生选课：表示学生选课关系。包含属性：学号、课程号、成绩。
# 8. 教师授课：表示教师授课关系。包含属性：教师编号、课程号。
# 9. 学生奖惩：表示学生奖惩关系。包含属性：学号、奖惩编号。

DROP TABLE IF EXISTS student_course;
DROP TABLE IF EXISTS teacher_course;
DROP TABLE IF EXISTS student_reward_punish;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS major;
DROP TABLE IF EXISTS college;
DROP TABLE IF EXISTS reward_punish;


CREATE TABLE student(
    sno INT PRIMARY KEY,   # 学号
    sname VARCHAR(20),          # 姓名
    ssex CHAR(2),               # 性别
    sid CHAR(18),               # 身份证号
    sphone CHAR(11),            # 手机号
    sethics VARCHAR(10),        # 民族
    splace VARCHAR(20),         # 籍贯
    slevel VARCHAR(20),         # 学历层次

    smajor INT,                 # 专业号
    CONSTRAINT sname_not_null CHECK (sname IS NOT NULL),
    CONSTRAINT ssex_not_null CHECK (ssex IS NOT NULL),
    CONSTRAINT sid_not_null CHECK (sid IS NOT NULL),
    CONSTRAINT slevel_not_null CHECK (slevel IS NOT NULL),
    CONSTRAINT UQ_sid UNIQUE (sid)
);

CREATE TABLE teacher(
    tno INT PRIMARY KEY,   # 教师编号
    tname VARCHAR(20),          # 姓名
    tsex CHAR(2),               # 性别
    tid CHAR(18),               # 身份证号
    tphone CHAR(11),            # 手机号
    tcollege INT,               # 所在学院
    ttitle VARCHAR(20),         # 职称
    CONSTRAINT tname_not_null CHECK (tname IS NOT NULL),
    CONSTRAINT tsex_not_null CHECK (tsex IS NOT NULL),
    CONSTRAINT tid_not_null CHECK (tid IS NOT NULL),
    CONSTRAINT ttitle_not_null CHECK (ttitle IS NOT NULL),
    CONSTRAINT UQ_tid UNIQUE (tid)
);

CREATE TABLE course(
    cno INT PRIMARY KEY,   # 课程号
    cname VARCHAR(20),          # 课程名称
    cmajor INT,         # 开课专业
    ccredit FLOAT,              # 学分
    cfull_time INT,             # 课时
    ctype VARCHAR(20),          # 课程类型
    ctime VARCHAR(20),                 # 上课时间
    cplace VARCHAR(20),         # 上课地点
    CONSTRAINT cname_not_null CHECK (cname IS NOT NULL),
    CONSTRAINT ccredit_not_null CHECK (ccredit IS NOT NULL),
    CONSTRAINT ctime_not_null CHECK (ctime IS NOT NULL),
    CONSTRAINT ctype_not_null CHECK (ctype IS NOT NULL)
);

CREATE TABLE major(
    mno INT PRIMARY KEY,        # 专业号
    mname VARCHAR(20),          # 专业名称
    mcollege INT,               # 所属院系
    mtotal_credit FLOAT,        # 要求总学分
    CONSTRAINT mname_not_null CHECK (mname IS NOT NULL),
    CONSTRAINT mtotal_credit_not_null CHECK (mtotal_credit IS NOT NULL)
);

CREATE TABLE college(
    cno INT PRIMARY KEY,   # 院系号
    cname VARCHAR(20),          # 院系名
    cdean VARCHAR(20),           # 院长
    CONSTRAINT college_name_not_null CHECK (cname IS NOT NULL),
    CONSTRAINT cdean_not_null CHECK (cdean IS NOT NULL)
);

CREATE TABLE reward_punish(
    rno INT PRIMARY KEY,   # 奖惩编号
    rcontent VARCHAR(100),      # 奖惩内容
    rtype VARCHAR(20),          # 奖励或惩罚
    CONSTRAINT rcontent_not_null CHECK (rcontent IS NOT NULL),
    CONSTRAINT rtype_not_null CHECK (rtype IS NOT NULL)
);

# 外键约束
ALTER TABLE student ADD CONSTRAINT FK_student_smajor FOREIGN KEY (smajor) REFERENCES major(mno);
ALTER TABLE teacher ADD CONSTRAINT FK_teacher_tcollege FOREIGN KEY (tcollege) REFERENCES college(cno);
ALTER TABLE major ADD CONSTRAINT FK_major_mcollege FOREIGN KEY (mcollege) REFERENCES college(cno);
ALTER TABLE course ADD CONSTRAINT FK_course_cmajor FOREIGN KEY (cmajor) REFERENCES major(mno);

CREATE TABLE student_course(
    sno INT,               # 学号
    cno INT,               # 课程号
    grade FLOAT,                # 成绩
    gpa FLOAT,                  # GPA
    CONSTRAINT PK_student_course PRIMARY KEY (sno, cno),
    CONSTRAINT FK_student_course_sno FOREIGN KEY (sno) REFERENCES student(sno),
    CONSTRAINT FK_student_course_cno FOREIGN KEY (cno) REFERENCES course(cno)
);

CREATE TABLE teacher_course(
    tno INT,               # 教师编号
    cno INT,               # 课程号
    CONSTRAINT PK_teacher_course PRIMARY KEY (tno, cno),
    CONSTRAINT FK_teacher_course_tno FOREIGN KEY (tno) REFERENCES teacher(tno),
    CONSTRAINT FK_teacher_course_cno FOREIGN KEY (cno) REFERENCES course(cno)
);

CREATE TABLE student_reward_punish(
    sno INT,               # 学号
    rno INT,               # 奖惩编号
    CONSTRAINT PK_student_reward_punish PRIMARY KEY (sno, rno),
    CONSTRAINT FK_student_reward_punish_sno FOREIGN KEY (sno) REFERENCES student(sno),
    CONSTRAINT FK_student_reward_punish_rno FOREIGN KEY (rno) REFERENCES reward_punish(rno)
);