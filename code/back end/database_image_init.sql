# 创建学生学号到照片路径的一一对应
# 照片路径初始值为null
ALTER TABLE student DROP COLUMN image_path;

# ALTER TABLE student ADD image_path VARCHAR(100) DEFAULT NULL;