# 告诉编译器这是全局变量search_key_word
global search_key_word

def set_value(value):
    # 告诉编译器我在这个方法中使用的a是刚才定义的全局变量search_key_word,而不是方法内部的局部变量.
    global search_key_word
    search_key_word = value

def get_value():
    # 同样告诉编译器我在这个方法中使用的a是刚才定义的全局变量search_key_word,并返回全局变量,而不是方法内部的局部变量.
    global search_key_word
    return search_key_word