# chrome_custom
## 使用方法

- 首次部署安装后请用超级管理员身份用户登录windows，选择中右键执行 set_policies_reg_permission.ps1 脚本文件获得注册表编辑权限
- ie_forbidden_file_system.reg，禁止访问ie访问磁盘，双击运行
- 完全清除白名单注册表限制，选择中右键执行 delete_block_url.ps1 

系统设置 - 远程应用 - 应用发布机 - 更新 - 创建账号数量
- 0 : 使用administrator账号访问应用
- 非 0 : 使用 js_xxx 或 jms_ 其他普通账号访问应用

安装部署后，修改 Chrome_Path.txt 文件（文件只需要 5 行）注意使用英文符号

- 第一行：是否开启开发者工具，默认 safe 不开启，修改为 dev 则开启
- 第二行：chrome应用的路径如 C:\Program Files\Chrome\chrome92\chrome.exe
- 第三行：chrome启动的参数如 --kiosk --disable-print-preview --no-default-browser-check --proxy-server=127.0.0.1:8080 --proxy-bypass-list=172.31.21.32,172.16.10.87
- 第四行：地址白名单功能  enable / disable
- 第五行：chrome 的 administrator 用户目录，如: C:\Users\Administrator\AppData\Local\Google\Chrome\User Data，默认为空