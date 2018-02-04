# git日常使用

## 远程同步到本地 

场景：周末在家里的电脑上做了更新并提交到远程github上，周一到公司需要将远程github上的内容更新到公司电脑上

步骤总结：

1. 查看远程仓库`git remote -v`
2. 从远程获取最新版本到本地 `git fetch origin master`
3. 比较本地仓库和远程仓库的区别`git log -p master.. origin/master`
4. 把远程仓库合并到本地仓库`git merge origin/master`



```shell
wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$ git remote -v
origin  https://github.com/BoobooWei/UP210_shell.git (fetch)
origin  https://github.com/BoobooWei/UP210_shell.git (push)

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$ get fetch origin master
bash: get: command not found

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$ git fetch origin master
remote: Counting objects: 9, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 9 (delta 7), reused 9 (delta 7), pack-reused 0
Unpacking objects: 100% (9/9), done.
From https://github.com/BoobooWei/UP210_shell
 * branch            master     -> FETCH_HEAD
   0cedd8c..eac9163  master     -> origin/master

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$ git log -p master.. origin/master
commit eac9163ee88b2fc9625383b9d201769fc7ff2399
Author: 大宝 <rgweiyaping@hotmail.com>
Date:   Fri Dec 9 18:44:11 2016 +0800

    格式修改

    格式修改

diff --git a/00_shell_variables.md b/00_shell_variables.md
index d639f9a..65d4720 100644
--- a/00_shell_variables.md
+++ b/00_shell_variables.md
@@ -1,29 +1,7 @@
 # Shell Scripts

-- [Shell Scripts](#shell-scripts)
-       - [教学环境介绍](#教学环境介绍)
-       - [shell 简介](#shell-简介)
-               - [什么是 shell](#什么是-shell)
-               - [shell 历史](#shell-历史)
-               - [常见的 shell](#常见的-shell)
-               - [为什么 Shell](#为什么-shell)
-       - [shell的变量功能](#shell的变量功能)
-               - [什么是变量](#什么是变量)
-               - [变量的设置、查看和取消 echo unset](#变量的设置查看和取消-echo-unset)

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
$ git merge origin/master
Updating 0cedd8c..eac9163
Fast-forward
 00_shell_variables.md              |  69 ++++++-----------------
 01_shell_flow_control_statement.md |  20 ++-----
 02_shell_regular_expression.md     |  18 +++---
 03_shell_sed_awk.md                |  56 ++++++-------------
 04_shell_brackets.md               | 109 ++++++++++---------------------------
 pic/04.pdf                         | Bin 426153 -> 0 bytes
 pic/Thumbs.db                      | Bin 0 -> 36864 bytes
 7 files changed, 76 insertions(+), 196 deletions(-)
 delete mode 100644 pic/04.pdf
 create mode 100644 pic/Thumbs.db

wei@wei-PC MINGW64 /d/Git/UP210_shell (master)
```

## 本地同步到远程

场景1：周一到公司修改文件，并需要同步到远程github

步骤总结：

1. 添加修改文件`git add file`
2. 提交修改内容 `git commit -m "add toc"`
3. 同步到远程github`git push`

```shell
wei@wei-PC MINGW64 /d/Git/DB100_mysql (master)
$ git add *.md

wei@wei-PC MINGW64 /d/Git/DB100_mysql (master)
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   "00-MySQL\347\256\241\347\220\206\350\257\276\347\250\213\347\256\200\344\273\213.md"
        modified:   "01-MySQL\345\222\214MariaDB\346\225\260\346\215\256\345\272\223\344\273\213\347\273\215.md"
        modified:   "02-\347\273\223\346\236\204\345\214\226\346\237\245\350\257\242\350\257\255\350\250\200SQL\344\273\213\347\273\215\345\222\214\345\237\272\346\234\254\346\223\215\344\275\234.md"
        modified:   "03-MySQL\345\244\207\344\273\275\344\270\216\346\201\242\345\244\215.md"
        modified:   "04-MySQL\345\244\215\345\210\266replication.md"


wei@wei-PC MINGW64 /d/Git/DB100_mysql (master)

$ git commit -m "add toc"
[master fd0729d] add toc
 5 files changed, 7 insertions(+), 73 deletions(-)

wei@wei-PC MINGW64 /d/Git/DB100_mysql (master)
$ git push
Username for 'https://github.com': booboowei
Counting objects: 7, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (7/7), done.
Writing objects: 100% (7/7), 610 bytes | 0 bytes/s, done.
Total 7 (delta 6), reused 0 (delta 0)
remote: Resolving deltas: 100% (6/6), completed with 6 local objects.
To https://github.com/BoobooWei/DB100_mysql.git
   0520f53..fd0729d  master -> master

wei@wei-PC MINGW64 /d/Git/DB100_mysql (master)


场景2：在公司重命名了一个文件，并同步到远程github

步骤总结：

1. 添加修改文件`git add file`
2. 提交修改内容 `git commit -m "add toc"`
3. 同步到远程github`git push`
4. 添加删除文件`git rm renamefile`
5. 提交修改内容 `git commit -m "add toc"`
6. 同步到远程github`git push`

```shell
$ git add *.md

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$ git commit -m "add toc"
[master 6505ae6] add toc
 6 files changed, 1702 insertions(+), 153 deletions(-)
 create mode 100644 01-python.md

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$ git push
Username for 'https://github.com': booboowei
Counting objects: 8, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 18.80 KiB | 0 bytes/s, done.
Total 8 (delta 5), reused 0 (delta 0)
remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
To https://github.com/BoobooWei/PY100_python.git
   96d4672..6505ae6  master -> master

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$ git rm 01.python.md
rm '01.python.md'

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$ git commit -m "mv 01.python.md 01-python.md"
[master 869ce5e] mv 01.python.md 01-python.md
 1 file changed, 1759 deletions(-)
 delete mode 100644 01.python.md

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$ git push
Username for 'https://github.com': booboowei
Counting objects: 2, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 235 bytes | 0 bytes/s, done.
Total 2 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local objects.
To https://github.com/BoobooWei/PY100_python.git
   6505ae6..869ce5e  master -> master

wei@wei-PC MINGW64 /d/Git/PY100_python (master)
$
```

场景3：在公司新建了一个目录work_dayday仓库，需要同步到远程

步骤总结：

1. 初始化本地仓库`git init`
2. 将本地内容添加至git索引中 `git add .`
3. 将索引添加至本地仓库中`git commit -m "first commit"`
4. 添加远程仓库路径`git remote add origin https://github.com/booboowei/work_dayday.git`
5. 将本地内容push至远程仓库中 `git push -u origin master`

## git报错处理

### 场景1 git报错411

```shell
$ git push
Counting objects: 34, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (34/34), done.
error: RPC failed; HTTP 411 curl 22 The requested URL returned error: 411 Length                                                          Required
fatal: The remote end hung up unexpectedly
Writing objects: 100% (34/34), 1.89 MiB | 0 bytes/s, done.
Total 34 (delta 2), reused 0 (delta 0)
fatal: The remote end hung up unexpectedly
Everything up-to-date
```

使用Git提交比较大的文件的时候可能会出现这个错误

解决方法：`git config http.postBuffer  524288000`


```shell
booboowei@booboo MINGW64 ~/Desktop/dba (master)
$ git config http.postBuffer  524288000

booboowei@booboo MINGW64 ~/Desktop/dba (master)
$ git push
Counting objects: 34, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (34/34), done.
Writing objects: 100% (34/34), 1.89 MiB | 0 bytes/s, done.
Total 34 (delta 2), reused 0 (delta 0)
To http://git.jiagouyun.com/weiyaping/dba.git
   df4a2cd..f1c8a88  master -> master

```
