# Research Toolkit 科研工具箱
> 自己写的科研工具或者是好用的开源软件介绍。

由于自己写的工具只是在小范围的测试，会存在一些没有发觉的bug，因此会用【*】标出。如果你在使用过程中发现了bug，那就赶快给我提issue吧！每个工具都使用文件夹来归类，文件夹里面的README给出了可以快速上手的示例。

+ [rename_pdf_with_title](rename_pdf_with_title)：
![](rename_pdf_with_title/figures/example.png)
【*】在整理和搜索论文的时候，如果论文的文件名和论文的题目相同，我们不需要点开论文来看就可以回忆起论文的内容，这样会大大增加我们的效率。由于在arxiv等网站下载的论文是用数字或者其他方式命名的，如果我们只是想使用文件夹来归类的话，就需要自己手动点开文件，然后复制标题并重命名。这样的方法略显麻烦，rename_pdf_with_title可以用来完成论文重命名的工作。rename_pdf_with_title能够自动解析pdf文件，识别它的标题，根据识别结果对pdf文件进行重命名。