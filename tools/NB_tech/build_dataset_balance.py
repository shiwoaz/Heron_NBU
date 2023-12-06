import os
import csv
import os.path
import pickle
import random


def is_abnormal(video_pth, pkl_save_pth='/home/ma-user/work/dataset/NB_tech/NBUabnormal_snippets/'):  # 绝对路径
    videoname = os.path.basename(video_pth).split('.')[0]  # 不带后缀的文件名
    [vtype, scence, index] = videoname.split('_')  # need check  , index:1,2,3...
    pkl_name = vtype + '_' + scence

    pkl_pth = os.path.join(pkl_save_pth, pkl_name + '.pickle')

    with open(pkl_pth, 'rb') as file:
        gt = pickle.load(file)[pkl_name]  # gt:list contain frame level label
        begin_frame = (int(index) - 1) * 64  # every video have 64 frames
        gt_snippets = gt[begin_frame:begin_frame + 64]

    if max(gt_snippets) > 0.5:
        return True
    else:
        return False

# 判断一个文件是否是视频文件
def is_video_file(file_path):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    ext = os.path.splitext(file_path)[1].lower()
    return ext in video_extensions


# 递归遍历目录，将视频文件的绝对路径与类别标号存储到CSV文件中
def traverse_directory(dir_path, csv_writer):
    global count
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory.")
        return

    for entry in os.scandir(dir_path):
        if entry.is_dir():
            traverse_directory(entry.path, csv_writer)  # 递归遍历子目录
        elif is_video_file(entry.path):
            if 'normal' in os.path.basename(entry.path):
                cls = 0
            else:
                cls = 1 if is_abnormal(entry.path) else 0
            csv_writer.writerow([entry.path, cls], )  # 存储视频文件的路径与类别标号
            path_cls_list.append([entry.path, cls])
            count += 1


count = 0
path_cls_list = []

# 测试
if __name__ == '__main__':
    dir_path = '/home/ma-user/work/dataset/NB_tech/NBUabnormal_snippets'
    csv_file_path = '/home/ma-user/work/dataset/NB_tech/all.csv'
    # dir_path = r'E:/tm/NB_tech_dataset/NBUabnormal_snippets'
    # csv_file_path = 'test.txt'

    # 打开CSV文件并写入表头
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ')
        # 遍历目录并将视频文件的路径与类别标号存储到CSV文件中
        traverse_directory(dir_path, csv_writer)
    print(f"CSV file saved to {csv_file_path}. count:{count}")

    # cls balance
    path_cls_list_abn = [e for e in path_cls_list if e[1] == 1]
    normal_num = len(path_cls_list) - len(path_cls_list_abn)
    abnormal_num = len(path_cls_list_abn)
    path_cls_list_balanced = path_cls_list + path_cls_list_abn * int(normal_num / abnormal_num)

    # save sorted list
    sorted_list_save_path = '/home/ma-user/work/dataset/NB_tech/all_sorted.csv'
    with open(sorted_list_save_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        # 遍历目录并将视频文件的路径与类别标号存储到CSV文件中
        path_cls_list.sort(key=lambda x: x[0])
        for item in path_cls_list:
            csv_writer.writerow(item)  # 存储视频文件的路径与类别标号
    print(f"CSV file saved to {sorted_list_save_path}. count:{len(path_cls_list)}")

    # save balanced list
    balanced_list_save_path = '/home/ma-user/work/dataset/NB_tech/all_balanced.csv'
    with open(balanced_list_save_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ')
        # 遍历目录并将视频文件的路径与类别标号存储到CSV文件中
        random.shuffle(path_cls_list_balanced)
        for item in path_cls_list_balanced:
            csv_writer.writerow(item)  # 存储视频文件的路径与类别标号
    print(f"CSV file saved to {balanced_list_save_path}. count:{len(path_cls_list_balanced)}")
