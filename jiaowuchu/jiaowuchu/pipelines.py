import json
import pymysql

class JiaowuchuPipeline:

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123', charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS crawl')
        self.conn.commit()
        self.conn.select_db('crawl')
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jiaowuchu (
                通知标题 VARCHAR(255),
                通知类型 VARCHAR(255),
                发布时间 VARCHAR(255),
                摘要 VARCHAR(255),
                详情 TEXT,
                url VARCHAR(255),
                附件信息 TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "INSERT INTO jiaowuchu (通知标题, 通知类型, 发布时间, 摘要, 详情, url, 附件信息) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    item.get("title", ""),
                    item.get("section", ""),
                    item.get("post_time", ""),
                    item.get("brief", ""),
                    item.get("content", ""),
                    item.get("url", ""),
                    json.dumps(item.get("attachment", [])),  # 假设附件是一个列表
                )
            )

            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error inserting item into database: {e}")
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
