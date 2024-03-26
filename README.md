<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a><img src="https://github.com/ChiYuKe/ONI-Kanimal_GUI/blob/main/Assets/hqbase.png" width="200" height="200" alt="ONI"></a>
</p>
  
<!-- markdownlint-disable-next-line MD036 -->


  
  自己打包的话需要下载 [tkdnd](https://sourceforge.net/projects/tkdnd/files/Windows%20Binaries/TkDND%202.8/tkdnd2.8-win32-x86_64.tar.gz/download)，
  打开终端输入
   ```bash
   pyinstaller --onefile --noconsole --name your_exe_name --add-data "your_tkdnd_path" --icon=your_ico.ico your_python_file.py
   ```

这只是个简单的界面程序，它缺少一个主程序，你需要将kanimalGUI和[kanimal](https://github.com/skairunner/kanimal-SE/releases/tag/1.3.26)放在同一文件夹内，如果有疑问的话，你也可以查看[kanimal-SE](https://github.com/skairunner/kanimal-SE)他的运行思路

