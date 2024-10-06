from datetime import datetime


def check_date_equal(date_str:str)->bool:
    # 定义要比较的日期字符串
    #date_str = "2024-10-06 15:16"
    # 将字符串转换为datetime对象
    given_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    # 获取当前日期，精确到天
    current_date = datetime.now().date()  # 只保留日期部分
    # 获取给定日期的日期部分
    given_date_only = given_date.date()

    # 判断两者是否相等
    if given_date_only == current_date:
        print("给定日期与当前日期相等")
        return True
    else:
        return False


if __name__ == '__main__':
    check_date_equal("2024-10-06 15:16")