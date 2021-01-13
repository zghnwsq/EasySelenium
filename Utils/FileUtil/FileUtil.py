import os


def remove(file_path):
    if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            for file_name in files:
                if os.path.exists(os.path.join(root, file_name)):
                    os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                remove(os.path.join(root, dir_name))
                if os.path.isdir(os.path.join(root, dir_name)):
                    os.rmdir(os.path.join(root, dir_name))
        os.rmdir(file_path)
    if os.path.isfile(file_path) and os.path.exists(file_path):
        os.remove(file_path)


# f_path = r'D:\PythonProject\EasySelenium\Report\TestApi\xxxx'
# remove(f_path)




