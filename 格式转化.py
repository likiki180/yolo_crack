import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_file, txt_file, class_dict, skip_classes=None):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图像尺寸
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # 写入目标文件
    with open(txt_file, 'w') as f:
        for obj in root.iter('object'):
            # 获取类别名称
            class_name = obj.find('name').text

            # 如果类别在跳过列表中，则继续下一个对象
            if skip_classes and class_name in skip_classes:
                continue

            # 获取类别名称并转换为类别索引
            if class_name in class_dict:
                class_index = class_dict[class_name]
            else:
                # 如果类别不在字典中，跳过该对象
                continue

            # 获取边界框坐标
            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            ymin = int(xmlbox.find('ymin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymax = int(xmlbox.find('ymax').text)

            # 计算 YOLO 格式的坐标（归一化到 [0, 1] 区间）
            x_center = ((xmin + xmax) / 2) / width
            y_center = ((ymin + ymax) / 2) / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height

            # 写入文件
            f.write(f'{class_index} {x_center} {y_center} {w} {h}\n')

def convert_all_xmls_in_folder(folder_path, class_dict, skip_classes=None):
    # 遍历文件夹中的所有 XML 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            xml_file = os.path.join(folder_path, filename)
            txt_file = xml_file.replace('.xml', '.txt')
            convert_xml_to_txt(xml_file, txt_file, class_dict, skip_classes)

# 定义类别名称到索引的映射
class_dict = {'D00': 0, 'D10': 1, 'D20': 2, 'D40': 3}

# 定义需要跳过的类别
skip_classes = ['Repair']

# 文件夹路径，其中包含 XML 文件
folder_path = r'C:\Users\kiki\PycharmProjects\yolo5\rddc2020\yolov5\my_try_for_test\lab'

# 转换文件夹中的所有 XML 文件
convert_all_xmls_in_folder(folder_path, class_dict, skip_classes)