import re
import cn2an


def get_label_count(label_name):
    """
    根据给定的【X单Y组,X单,Y组】这一标签，转换为字典计数
    :param label_name: X单Y组,X单,Y组 这一标签
    :return: dict 一字典，给出单数和组数
    """
    # 匹配中文或阿拉伯数字及其单位
    pattern = re.compile(r'([\d零一二三四五六七八九十百千万亿]+)(单|组)?')
    matches = pattern.findall(label_name)

    count_dict = {'单': 0, '组': 0}

    for match in matches:
        num_str, unit = match
        # 将中文数字转换为阿拉伯数字
        try:
            num = int(cn2an.cn2an(num_str, mode='smart'))
        except ValueError:
            # 不是中文数字会走这里
            num = int(num_str)

        if unit == '单':
            count_dict['单'] = num
        elif unit == '组':
            count_dict['组'] = num

    return count_dict


def split_string(input_string):
    """
    将一行字符串按照给定的分隔符分隔开，返回list
    :param input_string: str 输入的字符串，一行
    :return: list 分割后得到的列表
    """
    # 使用正则表达式定义多个分隔符
    separators = r"[，。 、,\.]"
    result = re.split(separators, input_string)
    # 去除空字符串
    result = [x for x in result if x]
    return result


def get_label(line_list: list):
    """
    从分割后的行list中获取，X单Y组,X单,Y组 这一标签
    :param line_list: list 行分割后得到的列表
    :return: str X单Y组,X单,Y组 这一标签
    """
    for sep in line_list:
        if '单' in sep or '组' in sep:
            return sep


def beautify_dict(result_dict: dict, label: str):
    """
    美化打印的dict，dict的value为list[list]
    :param result_dict: 美化前dict
    :return: 美化后字符串
    """
    sorted_lines = []
    for key in sorted(result_dict.keys()):  # 按照单的序号递增排序
        lines = result_dict[key]
        sorted_lines.append(f"{key}{label}:")
        # 每行按照序号递增排序
        sorted_lines.append(" ".join(sorted(lines)))
        sorted_lines.append("")  # 添加空行作为分隔
    result = "\n".join(sorted_lines)
    return result


def process_multi_line(multi_line: str):
    """
    输入多行文本，例如"\n837 9单1组\n 123 321 一组\n128 10单"
    返回各个数字的单数，组数，
    :param multi_line:
    :return:
    """
    total_sum_dan = {}
    total_sum_zu = {}
    for line in multi_line.splitlines():
        # 忽略空白行和空行
        if not line.isspace() and not len(line) == 0 and not line.startswith('#'):
            # TODO: 单独处理特殊量词
            line = line.replace('两', '二')
            sep_line_list = split_string(line)
            label = get_label(sep_line_list)
            label_count_dict = get_label_count(label)
            # 提取X单，Y组，X单Y组的
            sep_line_list.remove(label)
            print(f"{label_count_dict}:{sep_line_list}\t orig:{line}")
            orig_nums = []
            if total_sum_dan.get(label_count_dict.get('单')):
                # 已经有了，直接加在最后
                orig_nums = total_sum_dan.get(label_count_dict.get('单'))
            orig_nums.extend(sep_line_list)
            total_sum_dan[label_count_dict.get('单')] = orig_nums

            orig_nums = []
            if total_sum_zu.get(label_count_dict.get('组')):
                orig_nums = total_sum_zu.get(label_count_dict.get('组'))
            orig_nums.extend(sep_line_list)
            total_sum_zu[label_count_dict.get('组')] = orig_nums
    # 删除 0单&0组
    if total_sum_dan.get(0):
        total_sum_dan.pop(0)
    if total_sum_zu.get(0):
        total_sum_zu.pop(0)
    return total_sum_dan, total_sum_zu


def sort_digits_in_string(s: str) -> str:
    """
    将字符串分割成单独的数字字符，排序后并转换为整数
    :param s: 原始数字(字符串格式)
    :return: 排序后合并好的数字（字符串格式）
    """
    digits = [int(char) for char in s]
    # 对数字进行排序
    digits_sorted = sorted(digits)
    # 将排序后的数字转换回字符串，并连接在一起
    sorted_str = ''.join(map(str, digits_sorted))
    return sorted_str


def add_up_zu(zu_dict):
    """
    组:原始数字的顺序不重要，对数字组合拆分为单个数组后排序，合并为新的数字组合标记，然后用字典统计排序后的数字出现的总组数
    例如：123, 132, 213, 231, 312, 321 都记作`123`累计统计组数
    :param zu_dict:
    :return:
    """
    appear_count_dict = dict()
    for digit_count, dict_value_list in zu_dict.items():
        for list_value in dict_value_list:
            sorted_digits = sort_digits_in_string(list_value)
            if sorted_digits in appear_count_dict:
                appear_count_dict[sorted_digits] = appear_count_dict[sorted_digits] + digit_count
            else:
                appear_count_dict[sorted_digits] = digit_count
    return appear_count_dict


def add_up_dan(dan_dict):
    """
    单：原始数字的顺序是重要的，用字典统计数字组合出现的总单数
    例如：123, 132, 213, 231, 312, 321 都分别累计统计单数
    :param dan_dict:
    :return:
    """
    appear_count_dict = dict()
    for digit_count, dict_value_list in dan_dict.items():
        for orig_digit in dict_value_list:
            if orig_digit in appear_count_dict:
                appear_count_dict[orig_digit] = appear_count_dict[orig_digit] + digit_count
            else:
                appear_count_dict[orig_digit] = digit_count
    return appear_count_dict


def collect_v_count_dict_to_count_v_list_dict(count_dict):
    count_v_list_dict = dict()
    for value, count in count_dict.items():
        orig_nums = []
        if count in count_v_list_dict:
            orig_nums = count_v_list_dict[count]
        orig_nums.append(value)
        count_v_list_dict[count] = orig_nums
    return count_v_list_dict