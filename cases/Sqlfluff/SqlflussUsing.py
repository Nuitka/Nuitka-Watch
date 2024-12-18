import sqlfluff, pprint

chkstr = "select * from tbl where col1 = 'foo';"
ret = sqlfluff.lint(chkstr, dialect="postgres")
pprint.pprint(ret)