# name-weaver
为你的孩子生成一个好听的名字


```sql
CREATE TABLE "word"
(
    id       INTEGER primary key autoincrement,
    word     varchar(2) unique,
    bi_hua   INTEGER,
    uri      text not null,
    ping_yin text not null
)

```
