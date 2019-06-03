import pycparser
import sys

def get_src(path):
    my_open = open(path, 'r')
    # 若文件不存在,报错，若存在，读取
    my_infor = my_open.readlines()
    # readlines()方法读取所有剩余行,将他们作为一个字符串列表返回
    my_open.close()
    # close()关闭文件,结束访问
    # print(my_infor)
    src = ""
    for text in my_infor:
        if '#include' in text:
            continue
        src += text
    # print(src)
    return src


def get_ast(src):
    parser = pycparser.c_parser.CParser()
    ast = parser.parse(src)
    ast.show()
    return ast

def parse_ast(ast):
    return 1


def main():
    # print(sys.path)
    path = 'C:\\Users\\temp\\Desktop\\test.c'
    get_ast(get_src(path))


if __name__ == '__main__':
    main()
