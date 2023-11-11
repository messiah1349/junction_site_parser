export EFS_DIR=./gmk_data
wget -e robots=off --recursive --no-clobber --page-requisites \
  --html-extension --convert-links --restrict-file-names=windows \
  --domains steelnews.biz --no-parent --accept=html \
  -P $EFS_DIR https://steelnews.biz/steel-news/page/2/
