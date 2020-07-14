from tkinter import *
import pymysql
import openpyxl
import my_reptile

db = pymysql.connect("localhost", "root", "root", "lwy", charset='utf8')
cursor = db.cursor()


class RpGui(object):
    def __init__(self, root):
        self.root = root
        self.init_window()

    def init_window(self):
        self.root.title('QQ音乐热评爬取')
        self.root.geometry("700x400+350+100")

        # 创建菜单按钮
        self.menubar = Menu(self.root)
        self.menubar.add_cascade(label='作者', command='')
        self.root.config(menu=self.menubar)

        # 创建标签
        self.image_file = PhotoImage(file='logo.png')
        self.logo = Label(self.root, image=self.image_file)
        self.logo.place(x=10, y=10)

        # 创建列表框
        self.sb = Scrollbar(self.root)
        self.sb.pack(side=RIGHT, fill=Y)
        self.lb = Listbox(self.root,  activestyle='none', width=90, height=15,
                          bd=5, listvariable=DISABLED, yscrollcommand=self.sb.set)
        self.lb.place(x=20, y=65)
        self.sb.config(command=self.lb.yview)

        # 创建交互控件
        self.music_name = StringVar()
        self.search_ipt = Entry(self.root, width=25, font=(
            'Arial', 14), textvariable=self.music_name)
        self.search_ipt.place(x=200, y=20)
        self.search_btn = Button(root, text='爬取热评',
                                 command=self.search_comments)
        self.search_btn.place(x=500, y=20)
        self.export_btn = Button(
            self.root, width=20, text='一键导出到Excel', command=self.export_excel)
        self.export_btn.place(x=150, y=350)
        self.add_btn = Button(self.root, width=20, text='添加收藏',
                              command=self.add_comments)
        self.add_btn.place(x=350, y=350)

    # 调用my_reptile模块获取热评
    def search_comments(self):
        music_name = self.music_name.get()
        results = my_reptile.get_comments(music_name)
        for i in results:
            self.lb.insert(0, i)

    # 添加喜欢的热评到数据库
    def add_comments(self):
        index = self.lb.curselection()
        # 判断是否有选中
        if index:
            value = self.lb.get(index)
            sql = "INSERT INTO comments VALUES (%s)"
            cursor.execute(sql, value)
            db.commit()
        else:
            return False

    # 将数据库的热评导入到表格
    def export_excel(self):
        sql = "SELECT * FROM comments"
        cursor.execute(sql)
        comments = cursor.fetchall()
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = '热门评论'
        for comment in comments:
            sheet.append(comment)
        wb.save('热评.xlsx')


if __name__ == '__main__':
    root = Tk()
    rpGui = RpGui(root)
    root.mainloop()
