"# guru_testing" 
# Bài tập nhóm môn Đảm bảo chất lượng và kiểm thử phần mềm

Kiểm thử các chức năng sau:
- Login*
- New Customer
- New Account
- Deposit
- Widthdraw
- Fund Transfer*
- Customized Statement Form*
- Log out*

*Chức năng có 2 vai trò (manager/customer)

Web kiểm thử: [Guru99Bank](http://www.demo.guru99.com/V4/)

## Thành viên:
- Đỗ Trịnh Huy Hoàng - 21IT612
- Nguyễn Thành Nhân - 21IT502
- Trần Thị Thu Dung - 21IT271

## Cài đặt và thực thi
- cài đặt thư viện: 
```bash
    pip install -r requirement.txt
```
- Chạy toàn bộ bài kiểm tra: 
```bash
    pytest tests/
```
- Chạy chức năng muốn kiểm tra:
```bash
    pytest tests/[tên file chức năng]
```
- Chạy và suất ra file html toàn bộ chức năng:
```bash
    pytest -v --html=[name].html tests/
```
- Chạy và suất ra file html 1 chức năng:
```bash
    pytest -v --html=[name].html tests/[tên file chức năng]
```



