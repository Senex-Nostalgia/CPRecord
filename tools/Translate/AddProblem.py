import os
import sys
import html
def translate1(intputname, outputname):
	I = open(intputname, "r", encoding='utf-8')
	O = open(outputname, "w", encoding='utf-8')
	L = I.readlines()
	c = 0
	for t in L:
		if (c == 0 or c == len(L) - 1):
			pass
		else:
			O.write(html.escape(t))
		c += 1

def TranslateMarkdownToHtml(inputname, outputname, tmp, name):
	'''
	将Markdown转化为html
	将文件以二级标题分割为若干个部分, 对每个部分单独用pandoc处理
	这是因为我们要对代码块进行单独的处理
	处理后聚合为输出
	'''

	obj = open(inputname, "r", encoding='utf-8')
	blocksCount = 0
	type = []
	article = obj.readlines();
	fempty = True

	Cfile = open(os.path.join(tmp, str(blocksCount) + ".md"), "w")
	type.append(False)

	i = 0
	while i < len(article):
		# 如果遇到 ``` 就一直处理直到遇到下一个 ```，注意读写文件的刷新
		if (len(article[i]) >= 3 and article[i][0:3] == "```"):
			if (not fempty):
				blocksCount += 1
				type.append(True)
			else:
				type[len(type) - 1] = True # 如果是空的就要在上一个的基础上修改了
			
			j = i + 1
			while (j < len(article)):
				if (len(article[j]) < 3 or article[j][0:3] != "```"):
					j += 1
				else:
					break
			
			Cfile = open(os.path.join(tmp, str(blocksCount) + ".md"), "w", encoding='utf-8')
			for k in range(i, j + 1):
				Cfile.write(article[k])
			i = j

			blocksCount += 1
			Cfile = open(os.path.join(tmp, str(blocksCount) + ".md"), "w", encoding='utf-8')
			fempty = True
			type.append(False)
		else:
			fempty = False
			Cfile.write(article[i])
		
		i += 1
	# 不刷新会卡缓冲区，输出后必须要刷新。。。
	Cfile.flush()	
	'''
	for t in type:
		sys.stderr.write(str(t) + '\n')
	'''


	# 使用 pandoc 完成转换
	for z in range(blocksCount + 1):
		inName = os.path.join(tmp, str(z) + '.md')
		outName = os.path.join(tmp, str(z) + '.html')
		if type[z]:
			translate1(inName, outName)
		else:
			os.system("pandoc -f markdown+tex_math_dollars -t html " + inName + " -o " + outName + " --mathjax")
			sys.stderr.write("pandoc -f markdown+tex_math_dollars -t html " + inName + " -o " + outName + " --mathjax" + '\n')

	OUTPUT = open(outputname, "w", encoding='utf-8')
	OUTPUT.write('''<!DOCTYPE html>\n<html lang="zh-cn">\n\n<head>\n\t<meta charset="utf-8">\n\t<link type="text/css" rel="stylesheet" href="../additional_files/css/bootstrap.min.css">\n\t<link type="text/css" rel="stylesheet" href="../additional_files/css/sh_typical.min.css">\n\t<title>''')
	OUTPUT.write(name)
	OUTPUT.write('''</title>\n\t<script src="../additional_files/js/sh_main.min.js"></script>\n\t<script src="../additional_files/MathJax-master/MathJax.js?config=TeX-MML-AM_CHTML"></script>\n</head>\n<body>\n''')
	for g in range(blocksCount + 1):
		if type[g]:
			OUTPUT.write("""<div class="panel-body"><pre class="sh_sourceCode"><code class="sh_cpp">""")
		FFFFFile = open(os.path.join(tmp, str(g) + '.html'), "r", encoding='utf-8')
		OUTPUT.writelines(FFFFFile.readlines())
		if type[g]:
			OUTPUT.write("""\n</code><script>syntax_highlight()</script>\n</pre></div>\n""")
	
	OUTPUT.write("</body>\n</html>")
	return

cur = os.path.dirname(__file__)
inputPath = os.path.join(cur, 'input')
outputPath = os.path.join(cur, 'output')
tempPath = os.path.join(cur, 'tmp')
dirs = os.listdir(inputPath)

for file in dirs:
	# 将 inputPath 里的文件逐个提取出来
	basic = os.path.basename(os.path.join(inputPath, file)).split('.')[0]
	inFile = os.path.join(inputPath, basic + '.md')
	outFile = os.path.join(outputPath, basic + '.html')
	TranslateMarkdownToHtml(inFile, outFile, tempPath, basic)