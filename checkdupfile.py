# -*- coding: utf-8 -*-
from __future__ import print_function
import fnmatch
import os
import hashlib
import sys
import csv

CHUNM_SIZE = 8192

def is_file_match(f, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(f, pattern):
            return True
    return False

def find_specific_files(dir, pattern=["*"], exclude_dir=[]):
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if is_file_match(full_path, pattern):
                yield full_path
        for directory in exclude_dir:
            if directory in exclude_dir:
                exclude_dir.remove(directory)

def get_chunk(file):
    with open(file,'rb') as fb:
        while True:
            chunk = fb.read(CHUNM_SIZE)
            if not chunk:
                break
            else:
                yield chunk

def get_md5_sum(file):
    md5_obj = hashlib.md5()
    for chunk in get_chunk(file):
        md5_obj.update(chunk)
    return md5_obj.hexdigest()

def main():

    dir_for_search = sys.argv[1]
     
    # 1. 创建文件对象
    f = open('dup.csv','w',encoding='utf-8')
    
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    
    # 3. 构建列表头
    csv_writer.writerow(["文件地址1","文件地址2"])

    if not os.path.isdir(dir_for_search):
        raise SystemExit("{dir} is not a directories.".format(dir=dir_for_search))
    record = {}
    for file in find_specific_files(dir_for_search):
        md5_sum = get_md5_sum(file)
        if md5_sum in record and os.path.basename(record.get(md5_sum)) == os.path.basename(file):
            print("find duplicated file {0} vs {1}".format(record.get(md5_sum), file))
            csv_writer.writerow([record.get(md5_sum),file])
            #print(os.path.basename(record.get(md5_sum)) + "  "+os.path.basename(file))
        else:
            record[md5_sum] = file
    print(len(record))
    f.close()
    

if __name__ == '__main__':
    sys.argv.append(r'D:\ebook')
    main()
